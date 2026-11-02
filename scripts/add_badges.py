"""Validate or refresh launch badges in published lesson notebooks."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import quote

import nbformat

REPOSITORY = "ningzhanglab/Python-for-Beginners"
BADGE_LINE = re.compile(r"(?m)^\[!\[Open in Colab\]\([^\n]*$")


def make_badges(relative_path: str) -> str:
    """Return a Colab and Binder badge line using a repository-relative path."""
    encoded = quote(relative_path, safe="")
    colab = (
        "[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
        f"(https://colab.research.google.com/github/{REPOSITORY}/blob/main/"
        f"{relative_path})"
    )
    binder = (
        "[![Launch Binder](https://mybinder.org/badge_logo.svg)]"
        f"(https://mybinder.org/v2/gh/{REPOSITORY}/main?filepath={encoded})"
    )
    return f"{colab} · {binder}"


def expected_first_cell(first_cell: str, badge_line: str) -> str:
    """Replace an existing launch-badge line or insert one after the title."""
    if BADGE_LINE.search(first_cell):
        return BADGE_LINE.sub(lambda _match: badge_line, first_cell)
    title, separator, remainder = first_cell.partition("\n")
    if not title.startswith("# "):
        raise ValueError("First Markdown cell must have a level-one title")
    return title + "\n\n" + badge_line + (separator + remainder if separator else "")


def sync_notebook(root: Path, path: Path, *, write: bool = False) -> bool:
    """Return True if badges match; optionally refresh the first cell."""
    nb = nbformat.read(path, as_version=4)
    if not nb.cells or nb.cells[0].cell_type != "markdown":
        raise ValueError(f"{path}: first cell must be Markdown")
    relative = path.relative_to(root).as_posix()
    original = nb.cells[0].source
    updated = expected_first_cell(original, make_badges(relative))
    if original == updated:
        return True
    if write:
        nb.cells[0].source = updated
        nbformat.write(nb, path)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="Validate only (default)")
    modes.add_argument("--write", action="store_true", help="Update incorrect paths")
    args = parser.parse_args()
    paths = sorted((args.root / "modules").glob("**/*.ipynb"))
    wrong = 0
    for path in paths:
        if not sync_notebook(args.root, path, write=args.write):
            wrong += 1
            print(f"{'Updated' if args.write else 'Needs update'}: {path.relative_to(args.root)}")
    print(f"Checked badges in {len(paths)} lesson notebooks.")
    return int(wrong > 0 and not args.write)


if __name__ == "__main__":
    raise SystemExit(main())
