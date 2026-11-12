"""Regression checks for data integrity and execution-policy failures."""

import contextlib
import csv
import io
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import nbformat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_course import check_sources
from prepare_data import prepare
from simulate_people import generate_people


class BuildSafeguards(unittest.TestCase):
    def test_simulated_missing_codes_follow_the_codebook(self):
        rows = list(csv.DictReader(io.StringIO(generate_people().decode("utf-8"))))
        self.assertEqual(len(rows), 120)
        self.assertEqual(len({row["person_id"] for row in rows}), 120)
        self.assertEqual(sum(row["age"] == "unknown" for row in rows), 9)
        self.assertTrue(any(row["hourly_wage"] == "-99" for row in rows))
        for row in rows:
            if row["employed"] == "0":
                self.assertEqual(row["hourly_wage"], "")
            else:
                self.assertTrue(row["hourly_wage"] == "-99" or float(row["hourly_wage"]) > 0)

    def test_rejects_changed_upstream_data(self):
        with self.assertRaisesRegex(ValueError, "checksum"):
            prepare(b"unreviewed replacement data")

    def test_rejects_notebook_that_skips_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(ROOT / "_quarto.yml", root / "_quarto.yml")
            source = next((ROOT / "lessons").rglob("*.ipynb"))
            nb = nbformat.read(source, as_version=4)
            cell = next(cell for cell in nb.cells if cell.cell_type == "code")
            cell.metadata["tags"] = ["skip-execution"]
            destination = root / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True)
            nbformat.write(nb, destination)
            with self.assertRaises(AssertionError), contextlib.redirect_stdout(io.StringIO()):
                check_sources(root)

    def test_rejects_stale_simulation_setup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(ROOT / "_quarto.yml", root / "_quarto.yml")
            nb = nbformat.read(ROOT / "lessons/02-data/04-missing-types.ipynb", as_version=4)
            setup = next(cell for cell in nb.cells if "course-people-setup" in cell.metadata.get("tags", []))
            setup.source = setup.source.replace("20261111", "12345")
            destination = root / "lessons/02-data/04-missing-types.ipynb"
            destination.parent.mkdir(parents=True)
            nbformat.write(nb, destination)
            with self.assertRaisesRegex(AssertionError, "Stale generated simulation"):
                check_sources(root)

    def test_rejects_stale_analysis_package_setup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(ROOT / "_quarto.yml", root / "_quarto.yml")
            nb = nbformat.read(ROOT / "lessons/04-regression/02-correlation-ols.ipynb", as_version=4)
            setup = next(cell for cell in nb.cells if "course-package-setup" in cell.metadata.get("tags", []))
            setup.source += "\n# stale generated copy"
            destination = root / "lessons/04-regression/02-correlation-ols.ipynb"
            destination.parent.mkdir(parents=True)
            nbformat.write(nb, destination)
            with self.assertRaisesRegex(AssertionError, "Stale package setup"):
                check_sources(root)


if __name__ == "__main__":
    unittest.main()
