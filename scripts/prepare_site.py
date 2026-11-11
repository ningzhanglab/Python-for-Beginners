"""Stage downloadable copies from authoritative lesson notebooks before render."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / "downloads"
if target.exists():
    shutil.rmtree(target)
for source in sorted((ROOT / "lessons").rglob("*.ipynb")):
    destination = target / source.relative_to(ROOT / "lessons")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
print("Staged lesson notebook downloads.")
