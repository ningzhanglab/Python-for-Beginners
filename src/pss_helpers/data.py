"""Local paths and reproducible synthetic data discovery."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def survey_csv() -> Path:
    """Locate the synthetic survey; explain how to create it if missing."""
    path = PROJECT_ROOT / "data" / "raw" / "messy_survey.csv"
    if not path.is_file():
        raise FileNotFoundError(
            "Synthetic data missing. From the repo root, run "
            "'uv run python data/scripts/make_messy_survey.py'."
        )
    return path
