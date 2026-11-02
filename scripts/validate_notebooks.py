"""Check minimal lesson metadata; expand as lesson content is added."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for notebook_path in sorted(root.glob("modules/**/*.ipynb")):
        notebook = nbformat.read(notebook_path, as_version=4)
        markdown = [cell.source for cell in notebook.cells if cell.cell_type == "markdown"]
        if not markdown or not markdown[0].lstrip().startswith("# "):
            errors.append(f"{notebook_path}: missing Markdown title cell")
        if markdown and "colab.research.google.com" not in markdown[0]:
            errors.append(f"{notebook_path}: first cell missing Colab badge")
        if not any("Learning goals" in cell for cell in markdown):
            errors.append(f"{notebook_path}: missing learning goals")
        if not any("Common errors" in cell for cell in markdown):
            errors.append(f"{notebook_path}: missing common-errors section")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    for error in errors:
        print(error)
    if errors:
        return 1
    count = len(list(args.root.glob("modules/**/*.ipynb")))
    print(f"Validated {count} lesson notebooks; no errors found.")
    if count == 0:
        print("No lesson notebooks yet; this does NOT verify the course.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
