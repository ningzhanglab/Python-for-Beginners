"""Prepare small project CSVs from checksum-pinned, committed World Bank snapshots."""

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'


def verified_bytes(name, root=RAW):
    manifest = json.loads((root / 'manifest.json').read_text())
    raw = (root / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest[name]['sha256']:
        raise ValueError(f'Snapshot checksum changed: {name}; review provenance before updating it.')
    return raw


def series(name, indicator, root=RAW):
    header, records = json.loads(verified_bytes(name, root))
    if header['pages'] != 1 or int(header['total']) != len(records):
        raise ValueError('Incomplete API snapshot; inspect pagination.')
    values = {}
    metadata = json.loads(verified_bytes('wb-economies.json', root))[1]
    aggregate_ids = {row['iso2Code'] for row in metadata if row['region']['id'] == 'NA'}
    for row in records:
        code = row['countryiso3code']
        if not code and row['country']['id'] in aggregate_ids:
            continue
        if not code:
            raise ValueError('An unidentified economy needs manual review.')
        if row['date'] != '2019' or row['indicator']['id'] != indicator or code in values:
            raise ValueError('Unexpected year/indicator or duplicate economy key.')
        value = row['value']
        if value is not None and (not isinstance(value, (float, int)) or not math.isfinite(value)):
            raise ValueError('Unexpected non-numeric indicator value.')
        values[code] = value
    return values


def prepare(root=RAW):
    header, metadata = json.loads(verified_bytes('wb-economies.json', root))
    if header['pages'] != 1 or int(header['total']) != len(metadata):
        raise ValueError('Incomplete economy metadata snapshot.')
    economies = {row['id']: row for row in metadata if row['region']['id'] != 'NA'}
    definitions = {
        'fertility_income_2019.csv': [('gdp', 'NY.GDP.PCAP.CD', 'gdp_pc_usd'), ('fertility', 'SP.DYN.TFRT.IN', 'fertility')],
        'internet_urban_2019.csv': [('internet', 'IT.NET.USER.ZS', 'internet_pct'), ('urban', 'SP.URB.TOTL.IN.ZS', 'urban_pct')],
    }
    outputs = {}
    for filename, indicators in definitions.items():
        values = [series('wb-' + source + '-2019.json', code, root) for source, code, _ in indicators]
        if set(values[0]) != set(values[1]):
            raise ValueError('Indicator snapshots have different economy coverage.')
        codes = sorted(set(values[0]) & set(economies))
        buffer = io.StringIO(newline='')
        writer = csv.writer(buffer, lineterminator='\n')
        writer.writerow(['economy_code', 'economy', 'region', 'year', *[column for _, _, column in indicators]])
        for code in codes:
            row = economies[code]
            writer.writerow([code, row['name'], row['region']['value'].strip(), 2019,
                             *[value[code] if value[code] is not None else '' for value in values]])
        outputs[filename] = buffer.getvalue().encode('utf-8')
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare prepared bytes without changing files.')
    args = parser.parse_args()
    for name, content in prepare().items():
        destination = ROOT / 'data' / name
        if args.check:
            if destination.read_bytes() != content:
                raise SystemExit(f'FAIL: {name} differs from its pinned snapshots.')
        else:
            destination.write_bytes(content)
    print('PASS: project CSVs exactly match their pinned source transformations.' if args.check else 'Prepared two World Bank project CSVs.')


if __name__ == '__main__':
    main()
