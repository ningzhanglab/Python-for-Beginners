# Contributing to Python for Beginners

We welcome corrections, small runnable examples, accessible explanations, and well-tested lessons for empirical economics and social science.

## Report an issue

Use [the issue tracker](https://github.com/ningzhanglab/Python-for-Beginners/issues) for an inaccurate explanation, confusing setup step, missing Stata/R translation, broken example, or lesson request. Supply the lesson path, your operating system, relevant versions, reproduction steps, and the expected result, without uploading private data.

## Propose a contribution

1. Read [README.md](README.md), [AGENTS.md](AGENTS.md), and [DECISIONS.md](DECISIONS.md).
2. For a significant new lesson or feature, open an Issue first; for typos, a small focused PR is enough.
3. Use a topic branch. Keep unrelated changes out of your PR.
4. For code, run `uv sync`, `uv run python setup/check_setup.py`, and `uv run pytest` using the committed lockfile. Run `uv run ruff check .` and `uv run ruff format --check .` if the tool is installed. Clearly disclose checks not run.
5. Never commit an unexecuted lesson notebook. A new lesson needs three learning objectives, runnable imports, worked examples, Stata/R comparisons, guided practice with friendly checks, common errors, recap, and matching completed solutions.
6. In the PR, explain *what*, *why*, *how verified*, and any remaining limitations. A maintainer reviews and merges; agents must not merge their own PRs.

## Teaching and data standards

- Write for readers with no programming background; define jargon and use descriptive variable names.
- Favor reproducible research tasks over isolated syntax examples.
- Add descriptive captions or alt text for figures; use readable, colorblind-safe charts.
- Never publish restricted data, student information, credentials, or API keys.
- Before adding datasets, verify permissions and document provenance and license in [data/README.md](data/README.md).
- Cite sources and distinguish executed numerical results from examples or estimates.

The original code and text are [MIT-licensed](LICENSE), per the owner's current decision. Third-party datasets and assets may require other permissions. See [records/README.md](records/README.md) for the selective record-keeping policy.
