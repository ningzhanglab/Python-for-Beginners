# Module 2 — Data wrangling with pandas

**Status: in progress.** Three of ten planned lessons and their completed solutions are written and verified locally. The lessons are on a draft branch, not yet on `main`, and public Colab/Binder links are not live.

## Goals and prerequisites

Read, inspect, select, clean, merge, reshape, and validate research datasets. Complete [Module 1](../01_python_basics/README.md), or start here if you already know Python's basic data types and functions.

## Available on this branch

| Lesson | Time | Research task |
| --- | --- | --- |
| [01 DataFrames introduction](01_dataframes_intro.ipynb) | 40 min | Inspect data and round-trip CSV, Excel, Stata and Parquet |
| [02 Selecting and filtering](02_selecting_filtering.ipynb) | 40 min | Build a sample with `.loc`, Boolean filters, and sorted data |
| [03 Cleaning](03_cleaning.ipynb) | 45 min | Normalize labels, recode missing wages, flag duplicates/outliers |

Each notebook has a corresponding completed notebook in [solutions/02_data_wrangling](../../solutions/02_data_wrangling/), with `_solutions.ipynb` appended to the lesson stem.

## Remaining planned lessons

- 04 Creating variables
- 05 Merging
- 06 Reshaping
- 07 Groupby and aggregation
- 08 Panels and time
- 09 Larger data
- 10 Wrangling project / checkpoint

## Data and reproducibility

The first three notebooks include the **same small, six-row fictional survey extract** in their setup cells so no download, API key, or GitHub raw URL is required. It is a *teaching illustration*, not the 90-row deterministic survey produced by [the generator](../../data/scripts/make_messy_survey.py). Later lessons will introduce the larger generated file and document the difference.

Use Python 3.12 and the repository's `uv.lock` for the reproducible local environment. The lessons teach direct `.loc` assignments compatible with pandas' Copy-on-Write behavior. All new cells must be run from a fresh kernel before release.

**Not yet verified:** real Colab/Binder launch, beginner walkthrough, and the complete 10-lesson module.
