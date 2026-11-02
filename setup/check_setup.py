"""Check that the course's core Python environment is usable."""

from __future__ import annotations

import importlib.metadata as metadata
import sys

EXPECTED = (3, 12)
PACKAGES = ("numpy", "pandas", "matplotlib", "jupyterlab", "ipykernel")


def main() -> int:
    print("Python:", sys.version.split()[0])
    if sys.version_info[:2] != EXPECTED:
        print("NOTICE: course target is Python 3.12; current interpreter differs.")
    missing = []
    for package in PACKAGES:
        try:
            print(f"{package}: {metadata.version(package)}")
        except metadata.PackageNotFoundError:
            print(f"{package}: NOT INSTALLED")
            missing.append(package)
    if missing:
        print("Install core dependencies using 'uv sync'.")
        return 1

    import pandas as pd

    sample = pd.DataFrame({"wage": [10, 12, 15]})
    assert sample["wage"].mean() > 0
    print("Core imports and DataFrame smoke test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
