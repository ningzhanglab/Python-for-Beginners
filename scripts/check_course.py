"""Check course source contracts and the committed dataset, without network access."""

import re
from pathlib import Path

import nbformat
import pandas as pd
import yaml

from simulate_people import generate_people, people_setup_source

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ("You will learn", "Why it matters", "Worked example", "Try it",
            "When it goes wrong", "Recap")


def check_sources(root=ROOT):
    config = yaml.safe_load((root / "_quarto.yml").read_text())
    assert config["execute"] == {
        "enabled": True, "error": False, "cache": False, "freeze": False, "daemon": False
    }, "Fresh execution and failure on unexpected errors are required."
    notebooks = sorted((root / "lessons").rglob("*.ipynb"))
    assert notebooks, "No lesson notebooks found."
    for path in notebooks:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        text = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "markdown")
        positions = [text.index(f"## {section}") for section in SECTIONS]
        assert positions == sorted(positions), f"Lesson section order: {path}"
        goals = text.split("## You will learn", 1)[1].split("## Why it matters", 1)[0]
        assert 2 <= len(re.findall(r"^- ", goals, re.MULTILINE)) <= 4, f"Learning goal count: {path}"
        assert 3 <= text.count("<summary>Solution") <= 5, f"Exercise count: {path}"
        assert text.count("<details>") == text.count("</details>"), f"Unclosed solution: {path}"
        assert "colab.research.google.com/github/" in text, f"Missing Colab link: {path}"
        assert "../../downloads/" in text, f"Missing notebook download: {path}"
        assert not re.search(r"```(?:python|\{python\})", text), f"Use executable cells for code: {path}"
        assert "made-up numbers" in text, f"Label fictional examples: {path}"
        assert not nb.metadata.get("quarto", {}), f"Keep execution policy in project config: {path}"
        checks = nb.metadata.get("course", {}).get("checks", [])
        assert checks and all(isinstance(check, str) for check in checks), f"Missing outcome checks: {path}"
        for check in checks:
            compile(check, f"{path.name}:outcome-check", "exec")
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            assert not cell.outputs and cell.execution_count is None, f"Strip saved output: {path}"
            assert not re.search(r"#\|\s*(eval:\s*false|error:\s*true)", cell.source), path
            assert not set(cell.metadata.get("tags", [])) & {"raises-exception", "skip-execution"}, path
            if "course-people-setup" in cell.metadata.get("tags", []):
                assert cell.source == people_setup_source(), f"Stale generated simulation setup: {path}"
            if "plt.show()" in cell.source:
                assert "#| fig-alt:" in cell.source, f"Figure needs alt text: {path}"
    print(f"PASS: {len(notebooks)} source notebooks, template, downloads and execution policy.")


def outcome_cell(notebook):
    """A temporary, non-displayed check cell; never saved in learner sources."""
    checks = notebook.metadata.get("course", {}).get("checks", [])
    return nbformat.v4.new_code_cell("#| include: false\n" + "\n".join(checks), id="course-outcome-checks")


def check_curriculum(root=ROOT):
    config = yaml.safe_load((root / "_quarto.yml").read_text())
    navigation = str(config["website"]["sidebar"]["contents"])
    course_map = (root / "lessons/index.qmd").read_text()
    positions = []
    for part, expected in {"00-start": 3, "01-basics": 6, "02-data": 8}.items():
        notebooks = sorted((root / "lessons" / part).glob("*.ipynb"))
        assert len(notebooks) == expected, f"Incomplete {part}: expected {expected} lessons."
        for notebook in notebooks:
            relative = notebook.relative_to(root).as_posix()
            assert relative in navigation, f"Missing from sidebar: {relative}"
            positions.append(navigation.index(relative))
            assert notebook.relative_to(root / "lessons").as_posix() in course_map, f"Missing from course map: {relative}"
    assert positions == sorted(positions), "Core lessons must appear in curriculum order in the sidebar."
    print("PASS: all 17 core lessons are present in the course map and ordered sidebar.")


def check_data(root=ROOT):
    table = pd.read_csv(root / "data/gapminder.csv")
    assert list(table) == ["country", "region", "year", "life_exp", "population", "gdp_pc"]
    assert table.shape == (1704, 6)
    assert table["country"].nunique() == 142
    assert sorted(table["year"].unique()) == list(range(1952, 2008, 5))
    assert not table.duplicated(["country", "year"]).any()
    assert table.notna().all().all()
    assert (table[["life_exp", "population", "gdp_pc"]] > 0).all().all()
    regions = pd.read_csv(root / "data/country_regions.csv")
    expected_regions = table[["country", "region"]].drop_duplicates().sort_values("country").reset_index(drop=True)
    pd.testing.assert_frame_equal(regions, expected_regions)
    assert not regions["country"].duplicated().any()
    assert (root / "data/simulated_people.csv").read_bytes() == generate_people()
    print("PASS: country panel schema, coverage, unique country-years and complete positive measurements.")
    print("PASS: derived region lookup and deterministic simulated survey data.")


def check_practice_formats(root):
    """Check generated format conversions outside the learner-facing notebooks."""
    original = pd.read_csv(root / "data/gapminder.csv")
    excel = pd.read_excel(root / "scratch/countries.xlsx", sheet_name="countries", engine="openpyxl")
    stata = pd.read_stata(root / "scratch/countries.dta", convert_categoricals=False)
    for imported in [excel, stata]:
        pd.testing.assert_frame_equal(original, imported, check_dtype=False, rtol=1e-10, atol=1e-10)
    print("PASS: generated Excel and Stata values match the course CSV.")


if __name__ == "__main__":
    check_sources()
    check_curriculum()
    check_data()
