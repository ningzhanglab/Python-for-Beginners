"""Keep the Module 2 checkpoint synchronized with the canonical survey generator."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import nbformat
import pandas as pd
from pandas.testing import assert_frame_equal

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "scripts" / "make_messy_survey.py"
CHECKPOINT = ROOT / "modules" / "02_data_wrangling" / "10_wrangling_project.ipynb"


def test_checkpoint_matches_canonical_generator(tmp_path):
    """Every fictional raw row and household attribute must agree."""
    spec = spec_from_file_location("synthetic_survey_generator", SOURCE)
    assert spec is not None and spec.loader is not None
    generator = module_from_spec(spec)
    spec.loader.exec_module(generator)
    paths = generator.generate(tmp_path)

    original_survey = pd.read_csv(
        paths["csv"], dtype={"wage_2023": "string", "wage_2024": "string"}
    )
    original_households = pd.read_csv(paths["households"])
    notebook = nbformat.read(CHECKPOINT, as_version=4)

    namespace = {}
    for cell in notebook.cells:
        if cell.cell_type == "code":
            exec(compile(cell.source, str(CHECKPOINT), "exec"), namespace)
            if "households" in namespace:
                break
    assert "survey" in namespace and "households" in namespace
    assert_frame_equal(original_survey, namespace["survey"], check_dtype=False)
    assert_frame_equal(original_households, namespace["households"], check_dtype=False)
    assert len(namespace["survey"]) == 90
    assert namespace["households"]["household_id"].is_unique
