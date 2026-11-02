# Choose your setup path

**Fastest:** [Google Colab](colab.md) runs notebooks in your browser. When the first lesson is released, use its own Colab badge and choose **File → Save a copy in Drive** before editing. This starter stage does not yet have executable lesson notebooks.

**Local:** use Python 3.12 and [uv](https://docs.astral.sh/uv/). From the repository root:

~~~sh
uv sync
uv run python setup/check_setup.py
uv run jupyter lab
~~~

The third command starts JupyterLab; lesson notebooks will appear under `modules/` as each is released. `uv.lock` has not yet been verified/committed, so installs are provisional.

**For Stata/R users:** the planned [placement guide](../book/placement_guide.qmd) will help you skip material you already know.

Windows, macOS, Linux, VS Code and troubleshooting-specific pages will be added and checked in the infrastructure milestone. Do not upload confidential project data to Colab.
