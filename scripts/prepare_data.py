"""Rebuild the course CSV from a pinned, CC0 upstream teaching extract."""

import argparse
import csv
import hashlib
import io
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_COMMIT = "391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c"
SOURCE = f"https://raw.githubusercontent.com/jennybc/gapminder/{UPSTREAM_COMMIT}/inst/extdata/gapminder.tsv"
SHA256 = "f74275b4a2f4a7c8e3a09a752f9d6e43d1759d78d5cbfdebaaa3e1a6efc68f78"
RENAMES = {"country": "country", "continent": "region", "year": "year",
           "lifeExp": "life_exp", "pop": "population", "gdpPercap": "gdp_pc"}


def prepare(raw):
    if hashlib.sha256(raw).hexdigest() != SHA256:
        raise ValueError("Upstream checksum changed; review the source before using it.")
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8")), delimiter="\t"))
    if len(rows) != 1704 or set(rows[0]) != set(RENAMES):
        raise ValueError("Unexpected dataset size or columns.")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(RENAMES.values()), lineterminator="\n")
    writer.writeheader()
    writer.writerows({RENAMES[key]: value for key, value in row.items()} for row in rows)
    return buffer.getvalue().encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Use an already downloaded upstream TSV.")
    parser.add_argument("--check", action="store_true", help="Compare without modifying the CSV.")
    args = parser.parse_args()
    if args.source:
        raw = args.source.read_bytes()
    else:
        with urlopen(SOURCE, timeout=30) as response:
            raw = response.read()
    prepared = prepare(raw)
    destination = ROOT / "data/gapminder.csv"
    if args.check:
        if destination.read_bytes() != prepared:
            raise SystemExit("FAIL: committed CSV differs from the pinned source transformation.")
        print("PASS: CSV exactly matches the pinned source transformation.")
    else:
        destination.parent.mkdir(exist_ok=True)
        destination.write_bytes(prepared)
        print("Prepared data/gapminder.csv (1,704 rows).")


if __name__ == "__main__":
    main()
