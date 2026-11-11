"""Synchronize standalone notebook package setup from the one dependency file."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def package_setup_source(names):
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    pins = {}
    for line in requirements.splitlines():
        if line and not line.startswith("#") and "==" in line:
            name, version = line.split(";", 1)[0].strip().split("==", 1)
            pins[name.lower().replace("_", "-")] = version
    requested = [f"{name}=={pins[name]}" for name in names]
    return (
        '#| code-fold: true\n#| code-summary: "Prepared analysis-library setup (run first)"\n'
        "# Generated from requirements.txt; installs only in this Python runtime.\n"
        "import importlib.metadata\nfrom pathlib import Path\nimport subprocess\nimport sys\n\n"
        + f"requested = {requested!r}\n"
        + "needs_install = False\n"
        + "for requirement in requested:\n"
        + '    name, version = requirement.split("==")\n'
        + "    try:\n"
        + "        needs_install = needs_install or importlib.metadata.version(name) != version\n"
        + "    except importlib.metadata.PackageNotFoundError:\n"
        + "        needs_install = True\n"
        + "if needs_install:\n"
        + '    loaded = any(name in sys.modules for name in ["numpy", "pandas", "scipy", "statsmodels", "linearmodels"])\n'
        + '    constraints = Path("scratch/course-analysis-constraints.txt")\n'
        + "    constraints.parent.mkdir(parents=True, exist_ok=True)\n"
        + f"    constraints.write_text({requirements!r}, encoding='utf-8')\n"
        + '    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--constraint", str(constraints), *requested], check=True)\n'
        + "    if loaded:\n"
        + '        raise RuntimeError("Packages installed. Restart the notebook session, then run all cells from the top so updated libraries are used together.")\n'
        + 'print("Analysis libraries ready:", ", ".join(requested))'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sync", action="store_true", help="Update tagged setup cells after dependency changes.")
    args = parser.parse_args()
    count = 0
    for path in (ROOT / "lessons").rglob("*.ipynb"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        names = notebook.get("metadata", {}).get("course", {}).get("packages", [])
        if not names:
            continue
        tagged = [cell for cell in notebook["cells"] if "course-package-setup" in cell.get("metadata", {}).get("tags", [])]
        if len(tagged) != 1:
            raise SystemExit(f"FAIL: expected one package setup cell in {path.name}.")
        expected = package_setup_source(names)
        if args.sync:
            tagged[0]["source"] = expected.splitlines(keepends=True)
            path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        elif "".join(tagged[0]["source"]) != expected:
            raise SystemExit(f"FAIL: stale package setup in {path.name}; run with --sync.")
        count += 1
    print(f"PASS: {count} notebook package setups match requirements.txt.")


if __name__ == "__main__":
    main()
