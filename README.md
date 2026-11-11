# Python for Beginners: Economics & Social Sciences

A free, self-paced course for students and researchers who have never programmed. Start in your browser, then learn to load, clean, summarize and visualize data, interpret regressions, and organize analysis another person can rerun.

**Status: Phase 3 analysis path available.** All 27 lessons in Parts 0–4 are complete: browser notebooks, Python basics, pandas data handling, charts, OLS and fixed effects. Parts 5–6 and the reference pages remain coming soon. Phase 1 was reviewed and merged in [PR #4](https://github.com/ningzhanglab/Python-for-Beginners/pull/4); subsequent phases were authorized directly on `main` ([Phase 2](https://github.com/ningzhanglab/Python-for-Beginners/issues/5), [Phase 3](https://github.com/ningzhanglab/Python-for-Beginners/issues/6)).

## Start learning

- [0.2 Your first notebook, in the browser](lessons/00-start/02-first-notebook.ipynb) — calculations, variables, functions, errors and a prepared chart.
- [Part 1: Python basics](lessons/01-basics/01-values-variables.ipynb) — values, collections, decisions, functions, errors and libraries.
- [2.1 Loading data and looking at it](lessons/02-data/01-loading-data.ipynb) — inspect the same country panel in CSV, Excel and Stata formats.
- [Part 3: Visualization](lessons/03-viz/01-first-plots.ipynb) — labelled charts, group comparisons and PNG/PDF exports.
- [Part 4: Statistics and regression](lessons/04-regression/01-descriptive-statistics.ipynb) — descriptive tables, OLS, robust/clustered uncertainty, fixed effects and table exports.
- [Course map](lessons/index.qmd) — the planned sequence, Parts 0–6 and reference pages.

Each lesson has an **Open in Colab** link and a notebook download on its generated webpage. Colab requires a Google account to run and save work; local installation and paid software are not required. Before the repository is public, download a lesson notebook and upload it in Colab via **File → Upload notebook** if its GitHub link cannot open.

**Website:** not yet published. The intended address is [ningzhanglab.github.io/Python-for-Beginners](https://ningzhanglab.github.io/Python-for-Beginners/). The owner plans to make the repository public later and enable Pages. No live-site verification is claimed.

## What holds the course together

The running question is **“Do people live longer in richer countries?”** A small historical country panel appears throughout the planned course. Short introductions use made-up numbers for fictional countries; real data and simulated data are clearly distinguished. We teach errors as part of learning and distinguish association from causation.

The planned path covers Python basics; pandas data cleaning, grouping, merging and reshaping; charts; OLS and fixed effects; reproducible workflows; and guided projects. The first-hour path stays in the browser. See the course map for availability.

## Build and preview locally

For contributors, install **Python 3.12** and **[Quarto 1.11.9](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.11.9)**. With this repository as your working folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build.py
python -m http.server 8765 --directory _site --bind 127.0.0.1
```

Open [the local preview](http://127.0.0.1:8765/). Stop the server with Ctrl+C. Windows setup notes and details of the checks are in [CONTRIBUTING.md](CONTRIBUTING.md). This is contributor setup; learners can start with Colab.

`requirements.txt` pins the Python environment for CI and local builds. The build checks the sources and dataset, executes all lesson code and solutions, renders the website, and checks internal links, fragment targets, assets, downloads and image alt text. Execution is isolated so notebook sources stay unchanged. It uses committed data without downloading anything; installation needs internet access. Lesson-specific outcome checks verify samples, transformations, model results and generated figure/table exports without adding validation cells to learner notebooks. The standalone regression notebooks include prepared package setup generated from this same dependency file; contributors synchronize it with `python scripts/notebook_packages.py --sync` after changing pins.

## Sources and generated files

| Location | Purpose |
| --- | --- |
| `lessons/**/*.ipynb` | Authoritative, output-free lesson sources; also runnable in Colab |
| `index.qmd`, `about.qmd`, `lessons/index.qmd`, `projects/`, `reference/` | Website pages and planned curriculum |
| `_quarto.yml`, `styles.css` | Built-in light/dark themes, navigation, search and small style adjustments |
| `data/` | Country panel, derived region lookup, simulated survey and data dictionaries |
| `scripts/`, `tests/` | Data preparation, isolated build and meaningful safeguard checks |
| `.github/workflows/course.yml` | PR checks and main-branch Pages deployment |
| `_site/`, `downloads/`, `scratch/`, `.quarto/` | Generated or temporary output; ignored by Git |

## Reproducibility and rights

The 1,704-row Gapminder teaching extract is pinned to an upstream commit and checksum. It covers 142 countries at five-year intervals from 1952 to 2007; it is not current statistics. See [data/README.md](data/README.md) for its CC0 license, source, units, limitations and exact regeneration command. The Excel and Stata practice files are generated conversions of that same dataset. The country-region lookup is also derived from it. A separate fixed-seed simulation creates 120 fictional person records for missing-value and recoding practice. The dates lesson derives its time series from Canada's panel observations; it does not invent annual measurements. Regenerate the simulated CSV with `python scripts/simulate_people.py`; verify it and the shared notebook setup with `python scripts/simulate_people.py --check`.

**The course's original code, text, figures and simulated data do not yet have a selected license.** The owner explicitly left licensing undecided. No `LICENSE` has been added; the dataset retains its separate CC0 terms. See [LICENSE_GUIDANCE.md](LICENSE_GUIDANCE.md).

## Review and publication

When ready to publish, the owner should make the repository public, select **Settings → Pages → Build and deployment → Source: GitHub Actions**, then rerun **Course build and Pages** on `main`. Review the available lessons for instructional accuracy, pace and clarity before a first release. Deployment does not enable Pages or change visibility itself. Before enablement, the main build can succeed while its deploy job fails.

Every successful build uploads a `course-site` Actions artifact for inspection. Download and unzip it, then serve the extracted folder using a local HTTP server. The workflow deploys only checked main-branch output, never PR code.

See [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md), [CHANGELOG.md](CHANGELOG.md), and the [site-tooling decision](records/2026-11-11-site-tooling.md) for maintenance and review details.
