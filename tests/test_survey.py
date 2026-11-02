"""Regression tests for the synthetic survey and its intentional pitfalls."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pandas as pd

GENERATOR = Path(__file__).resolve().parents[1] / "data/scripts/make_messy_survey.py"


def load_generator():
    spec = spec_from_file_location("make_messy_survey", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_survey_formats_and_known_messes(tmp_path):
    paths = load_generator().generate(tmp_path)
    assert all(path.is_file() for path in paths.values())
    survey = pd.read_csv(paths["csv"])
    households = pd.read_csv(paths["households"])
    assert len(survey) == 90
    assert len(households) == 30
    assert survey.person_id.duplicated().any()
    assert "-99" in survey.wage_2023.astype(str).tolist()
    assert "not reported" in survey.wage_2024.tolist()
    assert " north " in survey.region.tolist()
    assert set(survey.household_id).issubset(set(households.household_id))
    assert households.household_id.is_unique
    stata = pd.read_stata(paths["stata"])
    assert isinstance(stata.employment.dtype, pd.CategoricalDtype)
    excel = pd.read_excel(paths["excel"])
    assert len(excel) == len(survey)


def test_csv_is_deterministic(tmp_path):
    generator = load_generator()
    a = generator.generate(tmp_path / "one")["csv"].read_bytes()
    b = generator.generate(tmp_path / "two")["csv"].read_bytes()
    assert a == b
