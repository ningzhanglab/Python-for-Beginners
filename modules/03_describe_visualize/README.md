# Module 3 — Describing and visualizing

**Status: all six planned lesson notebooks and their matching solutions are authored on draft PR #2.** [Cross-platform CI run #41405225377](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41405225377) passed on Ubuntu, Windows, and macOS with 59 tests, including clean-kernel notebook execution and inline figure generation. A beginner walkthrough, real Colab/Binder launches and a published website remain unverified.

## Prerequisites and learning goals

Complete [Module 2: Data wrangling](../02_data_wrangling/README.md), or enter with equivalent pandas skills. Learn to create reproducible descriptive tables, explore group differences, label figures accessibly, export high-resolution plots, and explain the limits of synthetic evidence.

## Lessons

| Lesson | Time | Focus |
| --- | --- | --- |
| [01 Summary statistics](01_summary_statistics.ipynb) | 45 min | Table 1, crosstabs, counts, weighted mean |
| [02 matplotlib basics](02_matplotlib_basics.ipynb) | 45 min | Histogram, scatter, trend lines, export |
| [03 Seaborn for data](03_seaborn_for_data.ipynb) | 45 min | Group distributions and fitted associations |
| [04 Publication figures](04_publication_figures.ipynb) | 45 min | Accessible style, illustrative intervals, vector output |
| [05 Time-series and panel plots](05_time_series_and_panel_plots.ipynb) | 45 min | Country trends and transparent binned scatter |
| [06 Checkpoint](06_checkpoint.ipynb) | 60 min | Recreate the 90-person synthetic survey, Table 1 and three figures |

Each learner notebook has a corresponding completed notebook in [solutions/03_describe_visualize](../../solutions/03_describe_visualize/), following the `_solutions.ipynb` naming convention.

## Data and methods

The early lessons use **fictional six-person wages, invented coefficients or synthetic country series**, solely to illustrate plotting methods. The checkpoint recreates the deterministic 90-row household survey used in Module 2. No empirical outcome, treatment effect or population inference is asserted.

All examples are intended to run offline using Python 3.12 with the repository's `uv.lock`. Original notebook outputs are stripped; plots are generated during execution. In the descriptive statistics lesson, weights illustrate a weighted mean but do not implement complex survey-design inference.

## Checkpoint self-assessment

- I can clean missing or implausible values consistently.
- I can generate a Table 1 with valid observation counts.
- I can produce a labeled histogram, a regional bar figure, and a time-wave line figure.
- I can reproduce these outputs after restarting the kernel.

**Still required:** a manual visual accessibility and formatting review, a beginner walkthrough, and real public Colab/Binder launch checks after merge and appropriate repository visibility.

**Next:** [Module 4 — Econometrics](../04_econometrics/README.md).
