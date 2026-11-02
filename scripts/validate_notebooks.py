"""Validate the published notebook lesson template and launch links."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import quote

import nbformat

REPOSITORY = "ningzhanglab/Python-for-Beginners"
REQUIRED_HEADINGS = (
    "## Learning goals",
    "## If you know Stata/R",
    "## Try it",
    "## Common errors",
    "## Recap",
    "## Next steps",
)


def validate(root: Path) -> list[str]:
    """Return one actionable error message for each discovered problem."""
    errors: list[str] = []
    lessons = sorted((root / "modules").glob("**/*.ipynb"))
    for path in lessons:
        relative = path.relative_to(root).as_posix()
        try:
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
        except (OSError, ValueError) as exc:
            errors.append(f"{relative}: invalid notebook: {exc}")
            continue
        if not nb.cells or nb.cells[0].cell_type != "markdown":
            errors.append(f"{relative}: first cell must be Markdown title + badges")
            continue
        first = nb.cells[0].source
        if not first.startswith("# "):
            errors.append(f"{relative}: first cell needs a level-one title")
        if "**Time:**" not in first or "**Prerequisites:**" not in first:
            errors.append(f"{relative}: missing time or prerequisites")
        expected_colab = (
            f"https://colab.research.google.com/github/{REPOSITORY}/blob/main/{relative}"
        )
        expected_binder = (
            f"https://mybinder.org/v2/gh/{REPOSITORY}/main?filepath="
            f"{quote(relative, safe='')}"
        )
        if expected_colab not in first:
            errors.append(f"{relative}: missing or incorrect Colab path")
        if expected_binder not in first:
            errors.append(f"{relative}: missing or incorrect Binder path")
        if "Save a copy in Drive" not in first:
            errors.append(f"{relative}: missing Colab save reminder")
        markdown = [cell.source for cell in nb.cells if cell.cell_type == "markdown"]
        whole = "\n".join(markdown)
        for heading in REQUIRED_HEADINGS:
            if heading not in whole:
                errors.append(f"{relative}: missing {heading!r}")
        goal_cells = [s for s in markdown if s.startswith("## Learning goals")]
        goals = [] if not goal_cells else [
            line for line in goal_cells[0].splitlines() if line.strip().startswith("- ")
        ]
        if len(goals) != 3:
            errors.append(f"{relative}: expected exactly 3 learning goals")
        exercise_count = sum(s.startswith("### ★") for s in markdown)
        if not 3 <= exercise_count <= 6:
            errors.append(f"{relative}: expected 3 to 6 graduated exercises")
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                if cell.execution_count is not None or cell.outputs:
                    errors.append(f"{relative}: cell {i + 1} contains committed outputs")
                if len(cell.source.splitlines()) > 15:
                    errors.append(f"{relative}: cell {i + 1} is over 15 lines")
        solution_path = root / "solutions" / relative.removeprefix("modules/")
        solution_path = solution_path.with_name(solution_path.stem + "_solutions.ipynb")
        if not solution_path.is_file():
            errors.append(f"{relative}: missing matching solutions notebook")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    failures = validate(args.root)
    for failure in failures:
        print(failure)
    count = len(list((args.root / "modules").glob("**/*.ipynb")))
    print(f"Validated {count} published lesson notebooks.")
    if not count:
        print("WARNING: no lessons have been published yet")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
