# 01 — Local setup: Python for research

**Time:** 25–35 minutes · **Prerequisites:** None. **This is a Markdown setup lesson, not an executable notebook.**

## Choose a path

If you want zero installation, [use Colab](../../setup/colab.md) and save a copy of each lesson to Drive. A local Python environment is useful for restricted data that must stay on a permitted machine, long-running research projects, and offline work.

## Python 3.12 and uv

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) using its official platform-specific instructions. Do not execute installation commands copied from untrusted sources.
2. Clone this repository (with GitHub Desktop or Git):

~~~shell
git clone https://github.com/ningzhanglab/Python-for-Beginners.git
cd Python-for-Beginners
~~~

3. Install the locked Python environment, then test it:

~~~shell
uv python install 3.12
uv sync --locked
uv run python setup/check_setup.py
~~~

4. Start a notebook server using:

~~~shell
uv run jupyter lab
~~~

The project uses `pyproject.toml` and `uv.lock` for reproducible installs. **The first notebooks are on a draft branch until merged, and the repository is currently private.** If you work from PR #2, switch to its topic branch before opening lessons.

## Alternative paths

- **Conda:** [environment.yml](../../environment.yml) is provided as a provisional alternative; it is not yet exactly pinned or OS-verified. Do not claim conda reproduces the uv lock.
- **VS Code:** Install VS Code and its official Python and Jupyter extensions. Open the repository folder, select the `.venv` Python interpreter, and choose the corresponding notebook kernel.
- **Windows/macOS/Linux:** The uv commands above are cross-platform. Platform-specific installation and shell commands are in the [official uv installation docs](https://docs.astral.sh/uv/getting-started/installation/). When using PowerShell, use the appropriate shell syntax for activation only if you activate manually; `uv run` avoids activation.

## Check your setup

- `uv run python setup/check_setup.py` exits successfully and prints installed package versions.
- Open [the welcome lesson](00_welcome.ipynb) in JupyterLab and run every cell from the top.
- Reopen the notebook and confirm its input cells still make sense after a fresh kernel restart.

## Common setup errors

- **`uv` is not recognized:** verify installation and restart your terminal so PATH changes take effect.
- **Wrong Python version:** use `uv python install 3.12` and run `uv sync --locked` again.
- **Missing packages in Jupyter:** choose the kernel from this project's `.venv`; do not accidentally use a global Python interpreter.
- **Cannot clone a private repository:** authenticate to GitHub with an account that has access, or wait until the repo is public.

Continue to [Notebooks vs. scripts](02_notebooks_vs_scripts.ipynb). Never upload restricted or confidential data to cloud notebooks without permission.
