"""Check course source contracts and the committed dataset, without network access."""

import re
from pathlib import Path

import nbformat
import pandas as pd
import yaml

from simulate_people import generate_people, people_setup_source
from notebook_packages import package_setup_source
from course_setups import check_generated_setups
from prepare_projects import prepare as prepare_projects, verified_bytes
from prepare_data import prepare as prepare_country_data
from project_starters import make_starter, serialized

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ("You will learn", "Why it matters", "Worked example", "Try it",
            "When it goes wrong", "Recap")


def notebook_sources(root=ROOT):
    return sorted([*(root / 'lessons').rglob('*.ipynb'), *(root / 'projects').rglob('*.ipynb')])


def notebook_download(source, root=ROOT):
    relative = source.relative_to(root)
    return Path('downloads') / (source.relative_to(root / 'lessons') if relative.parts[0] == 'lessons' else relative)


def check_sources(root=ROOT):
    config = yaml.safe_load((root / "_quarto.yml").read_text(encoding="utf-8"))
    assert '!downloads/' in config['project']['render'], 'Downloads must remain unexecuted source copies.'
    assert config["execute"] == {
        "enabled": True, "error": False, "cache": False, "freeze": False, "daemon": False
    }, "Fresh execution and failure on unexpected errors are required."
    notebooks = notebook_sources(root)
    assert notebooks, "No lesson notebooks found."
    for path in notebooks:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        text = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "markdown")
        positions = [text.index(f"## {section}") for section in SECTIONS]
        assert positions == sorted(positions), f"Lesson section order: {path}"
        goals = text.split("## You will learn", 1)[1].split("## Why it matters", 1)[0]
        assert 2 <= len(re.findall(r"^- ", goals, re.MULTILINE)) <= 4, f"Learning goal count: {path}"
        marker = '<summary>Hint' if nb.metadata.get('course', {}).get('kind') == 'project-starter' else '<summary>Solution'
        assert 3 <= text.count(marker) <= 5, f"Exercise count: {path}"
        assert text.count("<details>") == text.count("</details>"), f"Unclosed solution: {path}"
        assert "colab.research.google.com/github/" in text, f"Missing Colab link: {path}"
        expected_download = 'https://ningzhanglab.github.io/Python-for-Beginners/' + notebook_download(path, root).as_posix()
        assert expected_download in text, f"Missing portable notebook download: {path}"
        assert not re.search(r"```(?:python|\{python\})", text), f"Use executable cells for code: {path}"
        assert "made-up numbers" in text, f"Label fictional examples: {path}"
        assert not nb.metadata.get("quarto", {}), f"Keep execution policy in project config: {path}"
        checks = nb.metadata.get("course", {}).get("checks", [])
        check_generated_setups(nb, path)
        if nb.metadata.get('course', {}).get('kind') == 'project-starter':
            solution = nbformat.read(path.with_name('02-solution.ipynb'), as_version=4)
            assert path.read_text(encoding="utf-8") == serialized(make_starter(solution)), f'Stale project starter: {path}'
        assert checks and all(isinstance(check, str) for check in checks), f"Missing outcome checks: {path}"
        for check in checks:
            compile(check, f"{path.name}:outcome-check", "exec")
        packages = nb.metadata.get("course", {}).get("packages", [])
        package_cells = [cell for cell in nb.cells if "course-package-setup" in cell.metadata.get("tags", [])]
        if packages:
            assert len(package_cells) == 1, f"Expected one package setup: {path}"
            assert package_cells[0].source == package_setup_source(packages), f"Stale package setup: {path}"
            assert next(cell for cell in nb.cells if cell.cell_type == "code") is package_cells[0], f"Package setup must run first: {path}"
        else:
            assert not package_cells, f"Undeclared package setup: {path}"
        for exported in nb.metadata.get("course", {}).get("exports", []):
            assert exported.startswith("downloads/outputs/") and ".." not in Path(exported).parts, path
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
    config = yaml.safe_load((root / "_quarto.yml").read_text(encoding="utf-8"))
    navigation = str(config["website"]["sidebar"]["contents"])
    course_map = (root / "lessons/index.qmd").read_text(encoding="utf-8")
    positions = []
    for part, expected in {"00-start": 3, "01-basics": 6, "02-data": 8, "03-viz": 4, "04-regression": 6, "05-workflow": 4}.items():
        notebooks = sorted((root / "lessons" / part).glob("*.ipynb"))
        assert len(notebooks) == expected, f"Incomplete {part}: expected {expected} lessons."
        for notebook in notebooks:
            relative = notebook.relative_to(root).as_posix()
            assert relative in navigation, f"Missing from sidebar: {relative}"
            positions.append(navigation.index(relative))
            assert notebook.relative_to(root / "lessons").as_posix() in course_map, f"Missing from course map: {relative}"
    assert positions == sorted(positions), "Core lessons must appear in curriculum order in the sidebar."
    for source in (root / 'projects').glob('*/*.ipynb'):
        assert source.relative_to(root).as_posix() in navigation, f'Missing project navigation: {source}'
    for name in ['stata-python', 'r-python', 'pandas', 'glossary', 'errors']:
        reference = root / 'reference' / (name + '.qmd')
        assert reference.is_file() and len(reference.read_text(encoding="utf-8")) > 1500, f'Missing reference content: {name}'
        assert f'reference/{name}.qmd' in navigation, f'Missing reference navigation: {name}'
    print("PASS: 31 lessons, two project pairs and five reference pages are present in ordered navigation.")


def check_exports(root, notebooks=None):
    """Verify generated figure/table exports, without changing learner sources."""
    from PIL import Image
    lessons = notebooks if notebooks is not None else [nbformat.read(path, as_version=4) for path in notebook_sources(root)]
    count = 0
    for notebook in lessons:
        course = notebook.metadata.get("course", {})
        for exported in course.get("exports", []):
            path = root / exported
            assert path.is_file() and path.stat().st_size > 0, f"Missing export: {path}"
            if path.suffix == ".png":
                with Image.open(path) as picture:
                    assert picture.format == "PNG"
                    expected_size = course.get("export_sizes", {}).get(exported)
                    if expected_size:
                        assert list(picture.size) == expected_size, (exported, picture.size)
                    picture.verify()
            elif path.suffix == ".pdf":
                assert path.read_bytes().startswith(b"%PDF-"), path
            elif path.suffix == ".csv":
                assert not pd.read_csv(path).empty, path
            elif path.suffix == ".html":
                assert "<table" in path.read_text(encoding="utf-8"), path
            elif path.suffix == '.zip':
                import zipfile
                with zipfile.ZipFile(path) as archive:
                    assert archive.testzip() is None, path
                    assert all(not Path(name).is_absolute() and '..' not in Path(name).parts for name in archive.namelist()), path
                    expected_members = course.get('export_members', {}).get(exported)
                    if expected_members:
                        assert set(archive.namelist()) == set(expected_members), path
                    if 'income-life-project/requirements.txt' in archive.namelist():
                        assert archive.read('income-life-project/requirements.txt') == (ROOT / 'requirements.txt').read_bytes(), 'Stale bundled dependency file.'
            count += 1
    if count:
        print(f"PASS: {count} generated figure/table exports and declared image sizes.")


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
    assert prepare_country_data(verified_bytes('gapminder.tsv', root / 'data/raw')) == (root / 'data/gapminder.csv').read_bytes()
    for name, content in prepare_projects(root / 'data/raw').items():
        assert (root / 'data' / name).read_bytes() == content, f'Stale project data: {name}'
    print("PASS: country panel schema, coverage, unique country-years and complete positive measurements.")
    print("PASS: derived region lookup and deterministic simulated survey data.")
    print("PASS: pinned raw country source and exact World Bank project transformations.")


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
