"""Test badge synchronization without modifying other notebook content."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import nbformat

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "add_badges.py"
SPEC = spec_from_file_location("badge_script", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
BADGES = module_from_spec(SPEC)
SPEC.loader.exec_module(BADGES)


def test_badge_line_matches_relative_paths():
    line = BADGES.make_badges("modules/01_python_basics/01_values_and_variables.ipynb")
    assert "github/ningzhanglab/Python-for-Beginners/blob/main/modules/01_" in line
    assert "filepath=modules%2F01_python_basics%2F01_values_and_variables.ipynb" in line


def test_repair_mismatched_badge(tmp_path: Path):
    root = tmp_path
    path = root / "modules" / "01_python_basics" / "01_sample.ipynb"
    path.parent.mkdir(parents=True)
    nb = nbformat.v4.new_notebook(
        cells=[nbformat.v4.new_markdown_cell("# Sample\n\nIntro")]
    )
    nbformat.write(nb, path)
    assert not BADGES.sync_notebook(root, path)
    assert not BADGES.sync_notebook(root, path, write=True)
    assert BADGES.sync_notebook(root, path)
    assert "Intro" in nbformat.read(path, as_version=4).cells[0].source
