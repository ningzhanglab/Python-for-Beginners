# Python for Beginners

**Python for Economics & Social Science — learn Python through empirical research, from messy data to reproducible evidence.**

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Project status](https://img.shields.io/badge/status-under%20construction-yellow.svg)](https://github.com/ningzhanglab/Python-for-Beginners/issues/1)

This educational project is designed for economics, public policy, political science, sociology, and related social-science learners. **The GitHub repository remains named Python-for-Beginners.**

> **Current status:** Modules 0–1 are authored and their notebooks have passed automated execution in a Python 3.12 environment. They remain on [draft PR #2](https://github.com/ningzhanglab/Python-for-Beginners/pull/2), not on `main`. The first three lessons of Module 2 are also underway. Modules 3–7 and the companion website remain under construction.

## Start here

Read [setup instructions](setup/README.md), then begin with [Module 0](modules/00_setup/README.md) and [Module 1](modules/01_python_basics/README.md). These include tested notebook lessons, completed solutions and a fundamentals checkpoint. [Module 2](modules/02_data_wrangling/README.md) now contains its first three lessons on file formats, filtering, and cleaning. You must check out the draft PR branch to use them locally for now. **Colab/Binder badges target `main` and public launches are not yet available while the repository is private.** Track remaining work in [issue #1](https://github.com/ningzhanglab/Python-for-Beginners/issues/1).

## Who this guide is for

- First-year economics or social-science graduate students.
- Research assistants and advanced undergraduates preparing empirical projects.
- Researchers comfortable with Stata or R who want a Python workflow.

Zero programming experience is required. A basic understanding of statistics and regression will help in the econometrics module. The emphasis is applied microeconomics, transparent data cleaning, and repeatable research.

## Course map

| Module | Theme | What you will learn |
| --- | --- | --- |
| [0](modules/00_setup/README.md) | Getting started | Colab, notebooks, local setup |
| [1](modules/01_python_basics/README.md) | Just-enough Python | Variables, loops, functions, NumPy, debugging |
| [2](modules/02_data_wrangling/README.md) | Data wrangling | pandas, merges, reshaping, panel data |
| [3](modules/03_describe_visualize/README.md) | Describing & plotting | Summary tables and publication-ready figures |
| [4](modules/04_econometrics/README.md) | Econometrics | OLS, standard errors, fixed effects, IV, DiD, RD |
| [5](modules/05_data_sources/README.md) | Getting data | APIs, FRED, World Bank, web data |
| [6](modules/06_reproducibility/README.md) | Reproducible research | Environments, Git, pipelines, replication |
| [7](modules/07_electives/README.md) | Electives | Text, causal ML, maps, AI use, time series |

Modules 0–1 and the first three Module 2 lessons have notebook paths on the draft branch; their durations are listed in the module READMEs. The remaining modules are planned, not yet runnable.

## Local setup (foundation stage)

Install [uv](https://docs.astral.sh/uv/) and Python 3.12, then:

~~~sh
git clone https://github.com/ningzhanglab/Python-for-Beginners.git
cd Python-for-Beginners
uv sync --locked
uv run python setup/check_setup.py
~~~

Use `uv run jupyter lab` to open the first lessons after checking out the draft PR branch. The repository includes a resolved [uv.lock](uv.lock) for Python 3.12, generated and verified in GitHub Actions. Use `uv sync --locked` to keep the pinned environment. The conda environment remains provisional; see [DECISIONS.md](DECISIONS.md).

## Learning data

The course will use a deterministic **synthetic household survey** with deliberately messy values, plus carefully licensed public datasets. Read [data/README.md](data/README.md). Third-party data retain their own terms and are not automatically MIT-licensed.

## How this differs from other resources

This guide is intended to be beginner-accessible and focused on the empirical-research workflow, with Stata/R comparisons and self-checking exercises. It complements [QuantEcon](https://quantecon.org/) and [Coding for Economists](https://aeturrell.github.io/coding-for-economists/). Neither resource is affiliated with this repository.

## Contributing, license, and project history

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before making contributions. Original project code and educational content are licensed under [MIT](LICENSE) **for now**, as chosen by the repository owner. Dataset permissions are documented separately.

For the spec-to-implementation decisions see [DECISIONS.md](DECISIONS.md), for noteworthy milestones see [CHANGELOG.md](CHANGELOG.md), and for detailed records when necessary see [records/README.md](records/README.md).

**Author affiliation, preferred contact, and public citation metadata:** TODO(owner); never infer these from a GitHub profile.
