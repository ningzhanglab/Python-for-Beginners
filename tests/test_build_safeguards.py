"""Regression checks for data integrity and execution-policy failures."""

import contextlib
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


class BuildSafeguards(unittest.TestCase):
    def test_rejects_changed_upstream_data(self):
        with self.assertRaisesRegex(ValueError, "checksum"):
            prepare(b"unreviewed replacement data")

    def test_rejects_notebook_that_skips_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(ROOT / "_quarto.yml", root / "_quarto.yml")
            (root / "lessons").mkdir()
            source = next((ROOT / "lessons").rglob("*.ipynb"))
            nb = nbformat.read(source, as_version=4)
            cell = next(cell for cell in nb.cells if cell.cell_type == "code")
            cell.metadata["tags"] = ["skip-execution"]
            nbformat.write(nb, root / "lessons/broken.ipynb")
            with self.assertRaises(AssertionError), contextlib.redirect_stdout(io.StringIO()):
                check_sources(root)


if __name__ == "__main__":
    unittest.main()
