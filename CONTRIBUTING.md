# Contributing

Help us make Python approachable for a social-science student who has never programmed. Report unclear explanations and broken examples through GitHub Issues. For a substantial change, explain the intended learner outcome and acceptance criteria before writing it. Small corrections need no separate issue.

Work on a focused topic branch and open a pull request. Include what changed, why, the checks you actually ran, and any limits. Review AI-assisted material yourself. AI agents must also follow [AGENTS.md](AGENTS.md).

## Set up the contributor environment

Use Python 3.12 and Quarto 1.11.9. Get Quarto from its [official release](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.11.9) and make sure `quarto --version` reports `1.11.9`. Python dependencies come from `requirements.txt` only. We add libraries when an available lesson or a build check needs them.

On macOS or Linux, from the repository folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, the equivalent PowerShell commands are:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python scripts/build.py
```

Windows instructions are provided for contributors but have not yet been tested on Windows. The optional [learner installation lesson](lessons/05-workflow/01-local-installation.ipynb) uses uv and VS Code; its macOS environment commands have been checked, while Windows and the editor installation screens remain untested. A university-managed computer may prevent installation; the full curriculum can be taken in Colab.

## Required checks

With the environment active:

```sh
python -m unittest discover -s tests -v
python scripts/build.py
```

The safeguard tests reject changed data, skipped execution and stale generated setup cells. Independent numerical tests check HC1 covariance against its sandwich calculation and two-way fixed effects against double demeaning. The build validates the dataset and lesson structure, renders all pages with fresh notebook execution, and checks internal links and fragments, assets, image alt text, notebook downloads and the search index. Exercise solutions execute too. The converted Excel and Stata values are compared against the CSV after lesson execution. Additional checks in each notebook's `course.checks` metadata verify samples, transformations and model results. Declare generated figure/table exports in `course.exports` and expected PNG dimensions in `course.export_sizes`; the build validates them too. Validation cells are added only to disposable execution copies; source notebooks and downloads contain learner code only.

**Use `scripts/build.py` for the authoritative build.** Quarto executes notebook inputs in place; this wrapper renders disposable copies and publishes their generated output to `_site/`, preserving the clean source notebooks even on failure. Do not commit generated output, notebook execution counts or saved outputs. Deliberate error demonstrations catch and explain specific exceptions; unexpected errors must fail the build.

For notebook setup or data changes, also run:

```sh
python scripts/check_fresh_runtime.py
python scripts/prepare_data.py --check
python scripts/simulate_people.py --check
python scripts/notebook_packages.py
python scripts/prepare_projects.py --check
python scripts/course_setups.py
python scripts/project_starters.py
```

The first two commands need internet access; the simulation, project-data and generated-source checks are offline. The fresh-runtime check executes all 31 lessons and four project notebooks from empty working folders, then verifies required inputs and declared exports. Optional notebook paths restrict it to selected sources while iterating; run all notebooks before completing a phase. This exercises browser-style input preparation, including reconstruction of bundled World Bank snapshots; it does **not** establish that Google's Colab service/UI was tested. The upstream check verifies the pinned checksum and complete transformation; add `--source data/raw/gapminder.tsv` for the committed offline source.

## Preview and review

```sh
python -m http.server 8765 --directory _site --bind 127.0.0.1
```

Visit [the preview](http://127.0.0.1:8765/) and stop the server with Ctrl+C. Rebuild after editing. Review a desktop and a phone-width window, light/dark themes, sidebar, search, previous/next links, figure labels and exercise disclosures. An automatic alt-text check is not a full accessibility audit. External links and actual Colab execution need separate checks; disclose anything not performed.

## Write and update sources

Edit the `.ipynb` files in `lessons/` for lessons, and `.qmd` files for other pages. The source notebook is also the downloadable and Colab version; never maintain a separate hand-edited copy. Generated notebook downloads are staged automatically by the pre-render script. Keep exercises' solutions in executable code cells inside the disclosure markers, so the website can hide them while the build still tests them. Declare each notebook's required data files and outcome checks in its `course` metadata. The simulated-data setup cell is generated from `scripts/simulate_people.py`; change that source first, then run `python scripts/simulate_people.py --sync-notebooks` to update the CSV and tagged cell together.

Keep learning steps small. Define new terms, explain what each cell does and what its output means, and state when numbers are made up. Document every added dataset in [data/README.md](data/README.md) after checking its redistribution rights. Remove personal information from any bug report or example.

The regression notebooks declare `course.packages` and start with a tagged package setup cell generated by `scripts/notebook_packages.py`. Change `requirements.txt` first, then run `python scripts/notebook_packages.py --sync`. Do not hand-edit embedded versions. In a prepared contributor environment the cell installs nothing; in a fresh browser runtime it installs the requested analysis libraries under the shared constraints. If analysis libraries were already imported, the cell requires a session restart after installation. Verify changed installation paths in a clean environment as well as the normal build.

Project solutions in `projects/*/02-solution.ipynb` are authoritative. Each task cell has a `starter_source` hint that replaces its solution code in the derived starter; selected interpretation cells carry `project-answer` tags and are omitted there. Run `python scripts/project_starters.py --sync` after editing a solution. Starters execute their supplied setup and input checks, with TODO comments for the learner's unfinished analysis; full solution checks verify the completed model and exports. Do not claim that executing a starter solved the project.

Edit portable scripts and their README in `examples/income-life/`. Run `python scripts/course_setups.py --sync` after changing those files or the bundled, rights-documented project inputs. It embeds exact prepared input snapshots so no private-repository credentials are required in a fresh notebook. After synchronizing package/setup cells, synchronize project starters last. The build rejects stale generated cells or starters. The generated ZIP and dependency download use the exact authoritative `requirements.txt`; do not maintain another package list in the example folder.

Reference `.qmd` pages contain executable Python blocks, including outcome assertions where useful; Quarto runs them in the same fresh build. Stata/R expressions are reading bridges and have not been executed in those languages. The portable-script test also runs from an unrelated folder with spaces, verifies results and rejects corrupted raw input. Declare ZIP members in `course.export_members`; generated archives are checked for integrity, expected members and the exact shared dependency file.

## History and review

Git commits and PRs record routine changes. Update [CHANGELOG.md](CHANGELOG.md) for significant learner-facing changes, under Unreleased with a PR link (or a tracking issue for an explicitly authorized direct-to-main phase). Use a [record](records/README.md) only when a substantial decision or investigation deserves preserving its reasoning. Do not create one for each lesson or work session.

Phase 1 was reviewed and merged; the owner authorized Phases 2–3 directly on main. Phase 4 follows the topic-branch/PR workflow and supplies the full curriculum draft: 31 lessons, two guided projects and five reference pages. Full beginner read-through, accessibility polish and first-release sign-off remain Phase 5 work. Course licensing is still undecided; repository visibility and Pages configuration are owner actions. Do not claim a live-site or release check before it happened.
