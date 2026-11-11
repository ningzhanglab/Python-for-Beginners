"""Check course source contracts and the committed dataset, without network access."""

import re
from pathlib import Path

import nbformat
import pandas as pd
import yaml

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
        assert 3 <= text.count("<summary>Solution") <= 5, f"Exercise count: {path}"
        assert text.count("<details>") == text.count("</details>"), f"Unclosed solution: {path}"
        assert "colab.research.google.com/github/" in text, f"Missing Colab link: {path}"
        assert "../../downloads/" in text, f"Missing notebook download: {path}"
        assert not re.search(r"```(?:python|\{python\})", text), f"Use executable cells for code: {path}"
        assert "made-up numbers" in text, f"Label fictional examples: {path}"
        assert not nb.metadata.get("quarto", {}), f"Keep execution policy in project config: {path}"
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            assert not cell.outputs and cell.execution_count is None, f"Strip saved output: {path}"
            assert not re.search(r"#\|\s*(eval:\s*false|error:\s*true)", cell.source), path
            assert not set(cell.metadata.get("tags", [])) & {"raises-exception", "skip-execution"}, path
            if "plt.show()" in cell.source:
                assert "#| fig-alt:" in cell.source, f"Figure needs alt text: {path}"
    print(f"PASS: {len(notebooks)} source notebooks, template, downloads and execution policy.")


def check_data(root=ROOT):
    table = pd.read_csv(root / "data/gapminder.csv")
    assert list(table) == ["country", "region", "year", "life_exp", "population", "gdp_pc"]
    assert table.shape == (1704, 6)
    assert table["country"].nunique() == 142
    assert sorted(table["year"].unique()) == list(range(1952, 2008, 5))
    assert not table.duplicated(["country", "year"]).any()
    assert table.notna().all().all()
    assert (table[["life_exp", "population", "gdp_pc"]] > 0).all().all()
    print("PASS: country panel schema, coverage, unique country-years and complete positive measurements.")


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
    check_data()
