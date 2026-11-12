"""Verify the portable handoff from an unrelated folder and protect generated starters."""
import contextlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import nbformat
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_course import check_sources


class PortableProject(unittest.TestCase):
    def test_fresh_process_with_spaces_and_unrelated_working_folder(self):
        with tempfile.TemporaryDirectory(prefix='course portable test ') as temporary:
            base = Path(temporary)
            project = base / 'analysis folder'
            project.mkdir()
            for name in ['analyze.py', 'fetch_data.py', 'README.md']:
                shutil.copyfile(ROOT / 'examples/income-life' / name, project / name)
            source = ROOT / 'data/raw/gapminder.tsv'
            raw = project / 'data/raw/gapminder.tsv'
            raw.parent.mkdir(parents=True)
            raw.write_bytes(source.read_bytes())
            unrelated = base / 'different working folder'
            unrelated.mkdir()
            env = os.environ.copy()
            env['MPLCONFIGDIR'] = str(base / 'matplotlib')
            subprocess.run([sys.executable, str(project / 'analyze.py')], cwd=unrelated,
                           env=env, check=True, capture_output=True, text=True, timeout=60)
            result = pd.read_csv(project / 'results/model-2007.csv')
            self.assertEqual(int(result.loc[0, 'n_countries']), 142)
            self.assertAlmostEqual(result.loc[0, 'estimate_years_per_log_unit'], 7.202801571, places=6)
            self.assertEqual(raw.read_bytes(), source.read_bytes())
            self.assertFalse((unrelated / 'results').exists())
            # Reject a damaged input instead of adopting it or claiming a new successful result.
            raw.write_bytes(raw.read_bytes() + b' ')
            failed = subprocess.run([sys.executable, str(project / 'analyze.py')], cwd=unrelated,
                                    env=env, capture_output=True, text=True, timeout=60)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn('checksum changed', failed.stderr)

    def test_hand_edited_starter_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(ROOT / '_quarto.yml', root / '_quarto.yml')
            folder = root / 'projects/example'
            folder.mkdir(parents=True)
            source = ROOT / 'projects/01-fertility-income'
            shutil.copyfile(source / '02-solution.ipynb', folder / '02-solution.ipynb')
            notebook = nbformat.read(source / '01-starter.ipynb', as_version=4)
            cell = next(cell for cell in notebook.cells if 'TODO' in cell.source)
            cell.source += '\n# hand edit outside the generator'
            nbformat.write(notebook, folder / '01-starter.ipynb')
            with self.assertRaisesRegex(AssertionError, 'Stale project starter'), contextlib.redirect_stdout(io.StringIO()):
                check_sources(root)


if __name__ == '__main__':
    unittest.main()
