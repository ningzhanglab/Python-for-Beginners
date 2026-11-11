"""Stage downloadable copies from authoritative lesson notebooks before render."""

from pathlib import Path
import shutil

import nbformat

from check_course import outcome_cell

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / "downloads"
if target.exists():
    shutil.rmtree(target)
for source in sorted((ROOT / "lessons").rglob("*.ipynb")):
    destination = target / source.relative_to(ROOT / "lessons")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    # The build runs in a disposable copy. Downloads remain exact copies of the
    # originals; only the temporary render inputs receive the outcome checks.
    notebook = nbformat.read(source, as_version=4)
    notebook.cells.append(outcome_cell(notebook))
    nbformat.write(notebook, source)
print("Staged lesson notebook downloads.")
