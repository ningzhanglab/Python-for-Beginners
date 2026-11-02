"""Generate a deterministic *synthetic* household survey for teaching data cleaning.

All people and households are fictional. A fixed seed makes the generated
numbers repeatable. The intentionally messy columns include:

- person_id: mostly unique, with one deliberately duplicated identifier
- household_id: key to join household.csv (many people per household)
- region: inconsistent capitalization and whitespace
- employment: human-readable employment category; Stata value labels
- interview_date: mixed ISO and US date strings
- wage_2023 and wage_2024: numbers stored as text, including -99 for missing,
  an invalid string, and an implausibly large outlier
- survey_weight: positive illustrative analysis weight, not a real survey design

The two wage columns are wide-format waves for reshape practice.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261101
N_PEOPLE = 90


def generate(output_dir: Path, seed: int = SEED) -> dict[str, Path]:
    """Write survey CSV/Excel/Stata and household lookup CSV to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows: list[dict[str, object]] = []
    labels = ["employed", "unemployed", "not in labor force"]
    regions = ["North", "SOUTH", "east", "West"]

    for i in range(N_PEOPLE):
        wage_base = int(rng.integers(12000, 88000))
        rows.append(
            {
                "person_id": 1001 + i,
                "household_id": f"H{i // 3 + 1:03d}",
                "region": regions[i % len(regions)],
                "employment": labels[i % len(labels)],
                "interview_date": (
                    f"2024-03-{i % 27 + 1:02d}"
                    if i % 2 == 0
                    else f"03/{i % 27 + 1:02d}/2024"
                ),
                "wage_2023": str(wage_base),
                "wage_2024": str(round(wage_base * float(rng.uniform(0.9, 1.2)))),
                "survey_weight": round(float(rng.uniform(0.6, 2.4)), 3),
            }
        )

    rows[0]["wage_2023"] = "-99"
    rows[1]["wage_2024"] = "not reported"
    rows[2]["region"] = " north "
    rows[3]["wage_2024"] = "9999999"
    rows[5]["person_id"] = rows[4]["person_id"]

    survey = pd.DataFrame(rows)
    household_ids = sorted(survey["household_id"].unique())
    households = pd.DataFrame(
        {
            "household_id": household_ids,
            "housing_type": ["rent" if i % 2 else "own" for i in range(len(household_ids))],
            "urban": [int(i % 3 != 0) for i in range(len(household_ids))],
        }
    )

    paths = {
        "csv": output_dir / "messy_survey.csv",
        "excel": output_dir / "messy_survey.xlsx",
        "stata": output_dir / "messy_survey.dta",
        "households": output_dir / "households.csv",
    }
    survey.to_csv(paths["csv"], index=False)
    survey.to_excel(paths["excel"], index=False)
    stata_survey = survey.copy()
    stata_survey["employment"] = pd.Categorical(
        stata_survey["employment"], categories=labels
    )
    stata_survey.to_stata(paths["stata"], write_index=False, version=118)
    households.to_csv(paths["households"], index=False)
    return paths


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "data" / "raw")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    for kind, path in generate(args.output, seed=args.seed).items():
        print(f"{kind}: {path}")


if __name__ == "__main__":
    main()
