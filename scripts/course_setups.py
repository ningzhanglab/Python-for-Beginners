"""Generate prepared notebook setup from pinned inputs and the portable example sources."""
import hashlib
import base64
from pathlib import Path
import zlib

ROOT = Path(__file__).resolve().parents[1]
def project_data_setup_source(files):
    specifications = {name: hashlib.sha256((ROOT / 'data' / name).read_bytes()).hexdigest() for name in files}
    snapshots = {name: base64.b64encode(zlib.compress((ROOT / 'data' / name).read_bytes(), level=9)).decode('ascii') for name in files}
    return ("#| code-fold: true\n#| code-summary: \"Prepared project-data setup\"\n"
            "from pathlib import Path\nimport hashlib\nimport base64\nimport zlib\n\n"
            "# Frozen public-data snapshots, generated from the rights-documented course inputs.\n"
            f"expected_files = {specifications!r}\nsaved_snapshots = {snapshots!r}\ndata_paths = {{}}\n"
            "for name, expected in expected_files.items():\n"
            "    destination = Path('data') / name\n"
            "    if destination.exists():\n        raw = destination.read_bytes()\n"
            "    else:\n"
            "        raw = zlib.decompress(base64.b64decode(saved_snapshots[name]))\n"
            "    if hashlib.sha256(raw).hexdigest() != expected:\n"
            "        raise ValueError(f'Changed project input: {name}. Review its source before continuing.')\n"
            "    destination.parent.mkdir(parents=True, exist_ok=True)\n"
            "    destination.write_bytes(raw)\n    data_paths[name] = destination\n"
            "print('Verified project data:', ', '.join(data_paths))")


def workflow_setup_source():
    sources = {name: (ROOT / 'examples/income-life' / name).read_text(encoding="utf-8") for name in ['analyze.py', 'fetch_data.py', 'README.md']}
    sources['requirements.txt'] = (ROOT / 'requirements.txt').read_text(encoding="utf-8")
    return ("#| code-fold: true\n#| code-summary: \"Prepared portable-project files\"\n"
            "from pathlib import Path\nimport subprocess\nimport sys\n\n"
            "project_dir = Path('scratch/income-life-project').resolve()\n"
            "project_dir.mkdir(parents=True, exist_ok=True)\n"
            f"project_sources = {sources!r}\n"
            "for name, source in project_sources.items():\n"
            "    (project_dir / name).write_text(source, encoding='utf-8')\n"
            "command = [sys.executable, str(project_dir / 'fetch_data.py')]\n"
            "local_raw = Path('data/raw/gapminder.tsv')\n"
            "if local_raw.exists():\n    command += ['--from-file', str(local_raw.resolve())]\n"
            "subprocess.run(command, check=True)\n"
            "print('Project files ready:', project_dir)")


def check_generated_setups(notebook, path):
    for cell in notebook.cells:
        tags = cell.metadata.get('tags', [])
        if 'course-project-data-setup' in tags:
            expected = project_data_setup_source(notebook.metadata.course.required_data)
            assert cell.source == expected, f'Stale project-data setup: {path}'
        if 'course-workflow-setup' in tags:
            assert cell.source == workflow_setup_source(), f'Stale portable-project setup: {path}'


if __name__ == '__main__':
    import argparse
    import json
    import nbformat
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync', action='store_true', help='Refresh generated setup cells from their sources.')
    args = parser.parse_args()
    count = 0
    for path in sorted([*(ROOT / 'lessons').rglob('*.ipynb'), *(ROOT / 'projects').rglob('*.ipynb')]):
        notebook = nbformat.read(path, as_version=4)
        changed = False
        for cell in notebook.cells:
            tags = cell.metadata.get('tags', [])
            if 'course-project-data-setup' in tags:
                expected = project_data_setup_source(notebook.metadata.course.required_data)
            elif 'course-workflow-setup' in tags:
                expected = workflow_setup_source()
            else:
                continue
            count += 1
            if args.sync:
                cell.source = expected
                changed = True
            else:
                assert cell.source == expected, f'Stale generated setup: {path}'
        if changed:
            path.write_text(json.dumps(json.loads(nbformat.writes(notebook)), ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    print(f'PASS: {count} generated project-data/workflow setups match their sources.')
