# Setup troubleshooting (first checks)

## uv is not recognized

Confirm installation of [uv](https://docs.astral.sh/uv/getting-started/installation/) and restart your terminal so PATH changes take effect.

## Wrong Python version

The course targets Python 3.12. Run `python --version` and `uv python install 3.12`, then `uv sync` from the repository root.

## A notebook says ModuleNotFoundError

Confirm you ran `uv sync`. In local Jupyter, choose the kernel belonging to your project environment. Re-run `uv run python setup/check_setup.py`.

## Data files missing

Run the reproducible generator from the repository root:

~~~sh
uv run python data/scripts/make_messy_survey.py
~~~

This creates synthetic files only. Generated files under `data/raw/` are intentionally ignored by Git.

## Colab did not save changes

Open **File → Save a copy in Drive** and edit the new copy, not the GitHub preview.

This document is a foundation, not yet the spec's verified list of 15 common install errors; platform-specific guidance is pending.
