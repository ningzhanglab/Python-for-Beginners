"""Check snapshot integrity and the exclusion/missingness decisions in project inputs."""

import csv
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from prepare_projects import prepare, verified_bytes


class ProjectData(unittest.TestCase):
    def test_changed_raw_snapshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            shutil.copyfile(ROOT / 'data/raw/manifest.json', target / 'manifest.json')
            (target / 'wb-gdp-2019.json').write_text('[]')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                verified_bytes('wb-gdp-2019.json', target)

    def test_aggregates_are_excluded_but_missing_economies_retained(self):
        metadata = json.loads(verified_bytes('wb-economies.json'))[1]
        aggregates = {row['id'] for row in metadata if row['region']['id'] == 'NA'}
        raw = json.loads(verified_bytes('wb-gdp-2019.json'))[1]
        missing = {row['countryiso3code'] for row in raw if row['value'] is None and row['countryiso3code'] and row['countryiso3code'] not in aggregates}
        rows = list(csv.DictReader(io.StringIO(prepare()['fertility_income_2019.csv'].decode())))
        codes = {row['economy_code'] for row in rows}
        self.assertFalse(codes & aggregates)
        self.assertTrue(missing)
        self.assertTrue(missing <= codes)
        self.assertTrue(all(row['gdp_pc_usd'] == '' for row in rows if row['economy_code'] in missing))
        self.assertEqual(len(rows), len(codes))


if __name__ == '__main__':
    unittest.main()
