# Module 1 — Just-enough Python

**Status: all planned notebooks and matching solutions are authored and passing Python 3.12 CI.** Live Colab/Binder launches and a beginner usability walkthrough remain unverified.

## Learning goals and prerequisites

Turn economic questions into Python calculations; organize and validate small survey samples; understand errors, packages, NumPy, and reproducibility. Begin after [Module 0](../00_setup/README.md), or skip its introductory material if you already know notebooks.

## Lessons

| Lesson | Time | Focus |
| --- | --- | --- |
| [01 Values and variables](01_values_and_variables.ipynb) | 40 min | Types, f-strings, price and wage changes |
| [02 Lists and dictionaries](02_lists_and_dicts.ipynb) | 40 min | Containers, slicing, country indicators |
| [03 Conditionals and loops](03_conditionals_and_loops.ipynb) | 45 min | Recoding and iteration |
| [04 Functions](04_functions.ipynb) | 45 min | Deflation and annualized growth |
| [05 Modules and packages](05_modules_and_packages.ipynb) | 35 min | Imports and documentation |
| [06 Errors and debugging](06_errors_and_debugging.ipynb) | 40 min | Reading tracebacks and safe checks |
| [07 NumPy basics](07_numpy_basics.ipynb) | 45 min | Vectorization, RNG and matrix operations |
| [08 Checkpoint](08_checkpoint.ipynb) | 50 min | Small synthetic wage study |

Each lesson's completed solution is in [solutions/01_python_basics](../../solutions/01_python_basics/) with the same filename plus `_solutions` before `.ipynb`. Try the exercises before checking.

**Data:** fictional wages and country indicators embedded in cells, not real datasets. **Dependencies:** Python 3.12; NumPy (from the committed `uv.lock`) for Lessons 05, 07 and 08. All notebooks run offline once dependencies are installed.

**Self-assessment:** I can calculate real wages and growth rates, use lists/dictionaries/functions, understand simple exceptions, and reproduce an array-based result after restarting the kernel.

**Next:** [Module 2 — pandas](../02_data_wrangling/README.md) (planned, not yet authored).
