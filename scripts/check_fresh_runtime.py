"""Execute each source notebook in a fresh folder, exercising the Colab data path.

Requires internet access. This checks a fresh Python runtime, not Google's Colab UI.
"""

import argparse
import os
from pathlib import Path
import tempfile

import nbformat
from nbclient import NotebookClient

from check_course import check_practice_formats, outcome_cell, check_exports, notebook_sources

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="*", type=Path, help="Optional source notebook paths; default: all lessons.")
    args = parser.parse_args()
    sources = sorted({path.resolve() for path in args.notebooks}) if args.notebooks else notebook_sources(ROOT)
    for source in sources:
        if not any(source.is_relative_to(ROOT / folder) for folder in ['lessons', 'projects']) or source.suffix != ".ipynb" or not source.is_file():
            parser.error(f"Not a source lesson notebook: {source}")
        with tempfile.TemporaryDirectory(prefix="course-fresh-runtime-") as temporary:
            workspace = Path(temporary)
            os.environ["MPLCONFIGDIR"] = str(workspace / "matplotlib")
            os.environ["JUPYTER_RUNTIME_DIR"] = str(workspace / "jupyter")
            notebook = nbformat.read(source, as_version=4)
            cells = sum(cell.cell_type == "code" for cell in notebook.cells)
            notebook.cells.append(outcome_cell(notebook))
            NotebookClient(notebook, timeout=120, kernel_name="python3",
                           resources={"metadata": {"path": str(workspace)}}).execute()
            for filename in notebook.metadata.get("course", {}).get("required_data", []):
                assert (workspace / "data" / filename).read_bytes() == (ROOT / "data" / filename).read_bytes(), filename
            if (workspace / "scratch/countries.xlsx").exists():
                check_practice_formats(workspace)
            check_exports(workspace, [notebook])
            print(f"PASS: {source.name}, {cells} lesson cells and solutions; outcome checks and required data match.")


if __name__ == "__main__":
    main()
