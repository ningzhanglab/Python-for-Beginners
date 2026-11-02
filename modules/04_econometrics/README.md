# Module 4 — Applied econometrics

**Status: in progress.** The four foundational lessons and matching solutions below are on [draft PR #2](https://github.com/ningzhanglab/Python-for-Beginners/pull/2). The reproducible Python 3.12 `uv.lock` includes statsmodels 0.15.0. The latest cross-platform CI status is tracked in GitHub Actions; the remaining 12 lessons are **not yet authored**.

## Audience and prerequisites

Complete Module 2's pandas and Module 3's descriptive-statistics foundations, or bring equivalent experience in basic regression and Python. The module teaches empirical-research workflows while distinguishing fitted associations from causal identification.

## First lessons

| Lesson | Duration | Research technique |
| --- | --- | --- |
| [00 OLS by hand](00_ols_by_hand.ipynb) | 45 min | Centered slope, intercept, residuals and R² using NumPy |
| [01 OLS with statsmodels](01_ols_statsmodels.ipynb) | 45 min | Formula models, fit diagnostics, prediction and interpretation |
| [02 Standard errors and tests](02_standard_errors_and_tests.ipynb) | 50 min | Conventional, HC3 and cluster-robust inference; hypothesis tests |
| [03 Regression tables](03_regression_tables.ipynb) | 45 min | Coefficient and SE alignment, N and R², CSV/LaTeX export |

Each learner notebook has a complete companion in [solutions/04_econometrics](../../solutions/04_econometrics/), named `<lesson>_solutions.ipynb`. See the [executable regression cheat sheet](../../cheatsheets/regression_quickref.md) for a cross-language command reference.

## Planned, not yet released

- 04 Fixed effects with pyfixest (verify current package API, dependency locking and tests)
- 05 Panel models with linearmodels
- 06 Instrumental variables
- 07 Difference-in-differences
- 08 Event studies
- 09 Regression discontinuity
- 10 Binary outcomes
- 11 Count and nonlinear models
- 12 Matching and weighting
- 13 Weights and survey data
- 14 Simulation and bootstrap
- 15 Checkpoint

## Data and caveats

The introductory examples generate 150 entirely fictional people in 30 shared-shock groups using a fixed seed; they do not include real individuals or external downloads. Clustering illustrates dependence within groups, but is not a magic solution to bias or poor research design.

**Still required:** verification of the latest CI after notebook additions, a novice learner walkthrough, public Colab/Binder launches (the repository is private), website publication, and later econometric lessons.
