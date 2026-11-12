"""Derive incomplete starter notebooks from the authoritative project solutions."""

import argparse
import copy
import json
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def make_starter(solution):
    notebook = copy.deepcopy(solution)
    course = notebook.metadata.course
    course.kind = 'project-starter'
    course.checks = list(course.starter_checks)
    course.exports = []
    course.pop('export_sizes', None)
    cells = []
    inside_solution = False
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            cell.source = cell.source.replace('02-solution.ipynb', '01-starter.ipynb').replace(' · Complete solution', ' · Starter')
            cell.source = cell.source.replace('Attempt the [starter notebook](01-starter.ipynb) before reading the worked analysis.', 'Use the incomplete tasks below to build your analysis, then compare with the separate complete solution.')
            cell.source = cell.source.replace('this complete solution', 'the separate complete solution').replace('attempt the separate starter first.', 'use the incomplete tasks to plan the analysis.')
            if '<details><summary>Solution' in cell.source:
                inside_solution = True
                cell.source = cell.source.replace('<details><summary>Solution', '<details><summary>Hint')
                cell.source = cell.source.replace('Run this solution after your own attempt.', 'Use the worked-step headings to plan your code. The separate complete solution is available after your attempt.')
            elif inside_solution and '</details>' in cell.source:
                inside_solution = False
                cell.source = 'Keep your sample, units and interpretation explicit. Compare with the separate solution after trying.\n\n</details>'
            if 'project-answer' in cell.metadata.get('tags', []):
                continue
        elif cell.cell_type == 'code':
            if inside_solution:
                cell.source = '# TODO: write your exercise code here after attempting the main project tasks.'
            elif 'starter_source' in cell.metadata:
                cell.source = cell.metadata['starter_source']
        cells.append(cell)
    notebook.cells = cells
    notebook.cells.insert(3, nbformat.v4.new_markdown_cell(
        '**This starter is deliberately incomplete.** Prepared setup and input checks run as supplied; '
        'cells marked TODO are your analysis tasks. Running the starter does not complete them. '
        'Try the tasks before opening the [complete solution](02-solution.ipynb).'))
    for index, cell in enumerate(notebook.cells):
        cell.id = f'cell-{index:03d}'
    return notebook


def serialized(notebook):
    return json.dumps(json.loads(nbformat.writes(notebook)), ensure_ascii=False, indent=1, sort_keys=True) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync', action='store_true', help='Regenerate starters after editing solutions.')
    args = parser.parse_args()
    count = 0
    for source in sorted((ROOT / 'projects').glob('*/02-solution.ipynb')):
        target = source.with_name('01-starter.ipynb')
        content = serialized(make_starter(nbformat.read(source, as_version=4)))
        if args.sync:
            target.write_text(content, encoding='utf-8')
        else:
            assert target.read_text(encoding='utf-8') == content, f'Stale project starter: {target}'
        count += 1
    assert count == 2, 'Expected two guided project pairs.'
    print(f'PASS: {count} project starters match their authoritative solutions.')


if __name__ == '__main__':
    main()
