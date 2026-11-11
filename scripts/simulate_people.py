"""Generate deliberately messy, simulated survey data; no real people are used."""

import argparse
import csv
import inspect
import io
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]


def generate_people():
    """Return a deterministic UTF-8 CSV using only Python's standard library."""
    rng = random.Random(20261111)
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["person_id", "age", "education", "education_years", "employed", "hourly_wage"])
    labels = {12: "secondary", 14: "college", 16: "university", 18: "postgraduate"}
    for person_id in range(1, 121):
        age = rng.randint(22, 64)
        education_years = rng.choice([12, 14, 16, 18])
        employed = int(rng.random() >= 0.2)
        wage = round(8 + 0.9 * education_years + 0.08 * age + rng.uniform(-2, 2), 2)
        # Blank wages for non-workers; -99 means a worker did not report a wage.
        wage_text = str(wage) if employed else ""
        if employed and person_id % 7 == 0:
            wage_text = "-99"
        education = labels[education_years]
        if person_id % 9 == 0:
            education = " " + education.upper() + " "
        age_text = str(age) if person_id % 13 else "unknown"
        writer.writerow([person_id, age_text, education, education_years, employed, wage_text])
    return output.getvalue().encode("utf-8")


def people_setup_source():
    """Embed this exact generator in standalone notebooks, including in Colab."""
    return (
        "#| code-fold: true\n"
        '#| code-summary: "Prepared simulated-data setup (run this cell)"\n'
        "# Prepared setup: simulated people, generated locally; no real survey data.\n"
        "from pathlib import Path\nimport csv\nimport io\nimport random\n\n"
        + inspect.getsource(generate_people)
        + '\npeople_file = Path("data/simulated_people.csv")\n'
        + "people_file.parent.mkdir(parents=True, exist_ok=True)\n"
        + "if not people_file.exists():\n    people_file.write_bytes(generate_people())\n"
        + 'print("Simulated data ready: 120 fictional people; not evidence about real wages.")'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify CSV and shared notebook setup without writing.")
    parser.add_argument("--sync-notebooks", action="store_true", help="Update only tagged simulation setup cells.")
    args = parser.parse_args()
    destination = ROOT / "data/simulated_people.csv"
    generated = generate_people()
    if args.check:
        if destination.read_bytes() != generated:
            raise SystemExit("FAIL: simulated CSV differs from the fixed-seed generator.")
    else:
        destination.write_bytes(generated)
    for path in (ROOT / "lessons").rglob("*.ipynb"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for cell in notebook["cells"]:
            if "course-people-setup" not in cell.get("metadata", {}).get("tags", []):
                continue
            if args.sync_notebooks:
                cell["source"] = people_setup_source().splitlines(keepends=True)
                changed = True
            elif "".join(cell["source"]) != people_setup_source():
                raise SystemExit(f"FAIL: shared simulation setup is stale in {path.name}; use --sync-notebooks.")
        if changed:
            path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: fixed-seed simulated CSV and shared notebook setup agree." if args.check else "Generated simulated_people.csv and checked notebook setup.")


if __name__ == "__main__":
    main()
