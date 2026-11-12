"""Fetch or verify the exact public, CC0 teaching source; no credentials needed."""
import argparse
import hashlib
from pathlib import Path
from urllib.request import urlopen

SOURCE = 'https://raw.githubusercontent.com/jennybc/gapminder/391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c/inst/extdata/gapminder.tsv'
SHA256 = 'f74275b4a2f4a7c8e3a09a752f9d6e43d1759d78d5cbfdebaaa3e1a6efc68f78'
DATA = Path(__file__).resolve().parent / 'data/raw/gapminder.tsv'


def ensure_data(destination=DATA, source=None):
    destination = Path(destination)
    if source is not None:
        raw = Path(source).read_bytes()
    elif destination.exists():
        raw = destination.read_bytes()
    else:
        with urlopen(SOURCE, timeout=30) as response:
            raw = response.read()
    if hashlib.sha256(raw).hexdigest() != SHA256:
        raise ValueError('Data checksum changed. Review the source; do not silently accept a replacement.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists() or source is not None:
        temporary = destination.with_suffix('.tmp')
        temporary.write_bytes(raw)
        temporary.replace(destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-file', type=Path, help='Use an existing exact source for an offline run.')
    args = parser.parse_args()
    print('Verified data:', ensure_data(source=args.from_file))
