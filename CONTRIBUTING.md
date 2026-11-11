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

Windows instructions are provided for contributors but have not yet been tested on Windows. The optional learner installation lesson remains coming soon. A university-managed computer may prevent installation; use Colab to take the lessons.

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
```

The first two commands need internet access; the simulation and package-source checks are offline. The fresh-runtime check executes each notebook and all solutions from an empty working folder, then verifies required data and declared exports. Optional notebook paths restrict it to selected lessons while iterating; run all lessons before completing a phase. It exercises the Colab-style data path in Python; it does **not** establish that the Google Colab service/UI was tested. The upstream check verifies the pinned checksum and complete CSV transformation. For an offline upstream check, add `--source /path/to/gapminder.tsv`.

## Preview and review

```sh
python -m http.server 8765 --directory _site --bind 127.0.0.1
```

Visit [the preview](http://127.0.0.1:8765/) and stop the server with Ctrl+C. Rebuild after editing. Review a desktop and a phone-width window, light/dark themes, sidebar, search, previous/next links, figure labels and exercise disclosures. An automatic alt-text check is not a full accessibility audit. External links and actual Colab execution need separate checks; disclose anything not performed.

## Write and update sources

Edit the `.ipynb` files in `lessons/` for lessons, and `.qmd` files for other pages. The source notebook is also the downloadable and Colab version; never maintain a separate hand-edited copy. Generated notebook downloads are staged automatically by the pre-render script. Keep exercises' solutions in executable code cells inside the disclosure markers, so the website can hide them while the build still tests them. Declare each notebook's required data files and outcome checks in its `course` metadata. The simulated-data setup cell is generated from `scripts/simulate_people.py`; change that source first, then run `python scripts/simulate_people.py --sync-notebooks` to update the CSV and tagged cell together.

Keep learning steps small. Define new terms, explain what each cell does and what its output means, and state when numbers are made up. Document every added dataset in [data/README.md](data/README.md) after checking its redistribution rights. Remove personal information from any bug report or example.

The regression notebooks declare `course.packages` and start with a tagged package setup cell generated by `scripts/notebook_packages.py`. Change `requirements.txt` first, then run `python scripts/notebook_packages.py --sync`. Do not hand-edit embedded versions. In a prepared contributor environment the cell installs nothing; in a fresh browser runtime it installs the requested analysis libraries under the shared constraints. If analysis libraries were already imported, the cell requires a session restart after installation. Verify changed installation paths in a clean environment as well as the normal build.

## History and review

Git commits and PRs record routine changes. Update [CHANGELOG.md](CHANGELOG.md) for significant learner-facing changes, under Unreleased with a PR link (or a tracking issue for an explicitly authorized direct-to-main phase). Use a [record](records/README.md) only when a substantial decision or investigation deserves preserving its reasoning. Do not create one for each lesson or work session.

Phase 1 was reviewed and merged; the owner authorized Phase 2 directly on main and requested continuation to Phase 3 under that workflow. Further changes normally use topic branches and focused PRs unless explicitly authorized otherwise. Parts 0–4 are the current completed scope; do not label later content available before it exists. Course licensing is still undecided; the repository's eventual public visibility and Pages activation are owner actions. Do not claim a live-site or release check before it happened.
