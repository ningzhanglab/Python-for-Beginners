# Module 2 — Data wrangling with pandas

**Status: all ten lesson notebooks and their solutions are authored and cross-platform CI-verified.** [GitHub Actions run #41400291708](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41400291708) passed 47 tests on Ubuntu, Windows and macOS, including the checkpoint generator-consistency regression test. A beginner walkthrough, real Colab/Binder launches and a published website remain unverified. The lessons are on a draft branch, not yet on `main`, and public Colab/Binder links are not live.

## Goals and prerequisites

Read, inspect, select, clean, merge, reshape, and validate research datasets. Complete [Module 1](../01_python_basics/README.md), or start here if you already know Python's basic data types and functions.

## Available on this branch

| Lesson | Time | Research task |
| --- | --- | --- |
| [01 DataFrames introduction](01_dataframes_intro.ipynb) | 40 min | Inspect data and round-trip CSV, Excel, Stata and Parquet |
| [02 Selecting and filtering](02_selecting_filtering.ipynb) | 40 min | Build a sample with `.loc`, Boolean filters, and sorted data |
| [03 Cleaning](03_cleaning.ipynb) | 45 min | Normalize labels, recode missing wages, flag duplicates/outliers |
| [04 Creating variables](04_creating_variables.ipynb) | 45 min | Indicators, bins, log wages and method chaining |
| [05 Merging](05_merging.ipynb) | 45 min | Many-to-one joins, validation, unmatched keys and appending |
| [06 Reshaping](06_reshaping.ipynb) | 45 min | Wide/long, unique identifiers, panel-ready rows |
| [07 Groupby and aggregate](07_groupby_aggregate.ipynb) | 40 min | Group means, demeaning, and weighted summaries |
| [08 Panels and time](08_panels_and_time.ipynb) | 45 min | Parsing dates, lags, MultiIndex, balance checks |
| [09 Larger data](09_larger_data.ipynb) | 40 min | Memory, CSV chunking, categorical types, Parquet |
| [10 Wrangling checkpoint](10_wrangling_project.ipynb) | 55 min | Reproduce a 90-row synthetic survey, clean/merge/reshape, and verify export |

Each notebook has a corresponding completed notebook in [solutions/02_data_wrangling](../../solutions/02_data_wrangling/), with `_solutions.ipynb` appended to the lesson stem.

## Remaining verification

- Conduct the required beginner walkthrough and check every public Colab/Binder launch after the repository is accessible.
- Revisit the direct usage of the 90-row generator across earlier lessons as more modules are built.

## Data and reproducibility

Lessons 01–09 include the **same small, six-row fictional survey extract** in their setup cells so no download, API key, or GitHub raw URL is required. It is a *teaching illustration*, not the 90-row deterministic survey produced by [the generator](../../data/scripts/make_messy_survey.py). The checkpoint uses the generator's deterministic algorithm and 90-row schema, with the same seeded, fully fictional data.

Use Python 3.12 and the repository's `uv.lock` for the reproducible local environment. The lessons teach direct `.loc` assignments compatible with pandas' Copy-on-Write behavior. All new cells must be run from a fresh kernel before release.

**Not yet verified:** real Colab/Binder launch, beginner walkthrough, and full website integration.
