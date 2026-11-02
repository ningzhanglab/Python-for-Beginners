"""Execute every published notebook from a fresh kernel, including solutions."""

from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "modules").glob("**/*.ipynb")) + sorted(
    (ROOT / "solutions").glob("**/*.ipynb")
)


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda path: path.relative_to(ROOT).as_posix())
def test_notebook_executes(path):
    notebook = nbformat.read(path, as_version=4)
    executed = NotebookClient(
        notebook, timeout=120, kernel_name="python3", allow_errors=False
    ).execute()
    stdout = "\n".join(
        str(output.get("text", ""))
        for cell in executed.cells
        if cell.cell_type == "code"
        for output in cell.get("outputs", [])
        if output.get("output_type") == "stream"
    )
    if "solutions" in path.parts:
        assert "Hint:" not in stdout, f"Solution check failed: {path}"
        assert "✓" in stdout, f"No passing exercise checks in: {path}"
    else:
        assert "Hint:" in stdout, f"Learner exercises should offer hints: {path}"
