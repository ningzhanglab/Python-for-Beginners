"""Execute each source notebook in a fresh folder, exercising the Colab data path.

Requires internet access. This checks a fresh Python runtime, not Google's Colab UI.
"""

import os
from pathlib import Path
import tempfile

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    for source in sorted((ROOT / "lessons").rglob("*.ipynb")):
        with tempfile.TemporaryDirectory(prefix="course-fresh-runtime-") as temporary:
            workspace = Path(temporary)
            os.environ["MPLCONFIGDIR"] = str(workspace / "matplotlib")
            os.environ["JUPYTER_RUNTIME_DIR"] = str(workspace / "jupyter")
            notebook = nbformat.read(source, as_version=4)
            NotebookClient(notebook, timeout=120, kernel_name="python3",
                           resources={"metadata": {"path": str(workspace)}}).execute()
            assert (workspace / "data/gapminder.csv").read_bytes() == (ROOT / "data/gapminder.csv").read_bytes()
            cells = sum(cell.cell_type == "code" for cell in notebook.cells)
            print(f"PASS: {source.name}, {cells} cells and solutions; downloaded CSV matches committed data exactly.")


if __name__ == "__main__":
    main()
