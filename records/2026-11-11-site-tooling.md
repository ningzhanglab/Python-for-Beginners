# 2026-11-11 — Executable course website tooling

- **Date:** 2026-11-11
- **Type:** Decision
- **Status:** Implemented
- **Tags:** website, notebooks, reproducibility, teaching
- **Responsible:** To be confirmed by the owner.
- **AI assistance:** Codex, model not reported; evaluated tooling, authored the first slice and ran the checks below. A person still needs to review beginner accessibility, instructional depth, licensing and publication choices.
- **Related Issue / PR:** [Issue #3](https://github.com/ningzhanglab/Python-for-Beginners/issues/3); [PR #4](https://github.com/ningzhanglab/Python-for-Beginners/pull/4).

## Why this mattered

The course needs one lesson source that can become both a searchable static webpage and a runnable browser notebook. A broken example or exercise solution must fail the build. Phase 1 must demonstrate the complete path before the owner reviews bulk content development.

Acceptance criteria are recorded in Issue #3: two complete lessons (0.2 and 2.1), licensed running-example data, a prepared scatter plot, complete site navigation with unwritten work labelled coming soon, reproducible execution, PR checks and a Pages deployment workflow. The owner keeps course licensing undecided and plans to make the currently private repository public later, then enable Pages.

## Decision and alternatives

Use **Quarto 1.11.9**, the stable release returned by the official GitHub releases API on 2026-11-11, with its website project type and built-in Flatly/Darkly themes. Use Python 3.12 and `requirements.txt` for the complete pinned Python environment. The first available lessons need pandas, matplotlib, openpyxl and the notebook/build stack; regression packages wait until lessons need them.

Lesson `.ipynb` files are authoritative, with no saved outputs. Non-lesson pages use `.qmd`. Colab opens the tracked notebook; the website offers a staged copy of the same source. A private-repository fallback is downloading the notebook and uploading it in Colab. Colab data setup retrieves the exact checksum-verified public upstream extract if the local CSV is absent. Normal builds use committed data and need no data download.

Quarto executes `.ipynb` files in place. To preserve sources and keep downloads reproducible, `scripts/build.py` validates the originals, copies the site sources to a disposable folder, renders there with explicit `--execute`, then copies the website output back and checks it against the originals. Caching and freezing are disabled; errors are fatal. Teaching demonstrations catch their specific expected errors rather than enabling an allow-errors mode.

**Jupyter Book / MyST** is a strong alternative for notebook-based learning, with rich cross-references and executable documents. It could satisfy the course requirements but introduces a different authoring and deployment configuration without a concrete advantage for this small first slice. Quarto already covers the required navigation, search, themes and execution. No Jupyter Book build was run.

**MkDocs Material** offers strong documentation navigation and presentation. Executable lesson/notebook synchronization would need additional integration beyond a basic MkDocs build. That increases the maintenance surface for the central “all shown code executes” requirement. No MkDocs build was run.

Use GitHub Actions to build on PRs and main; upload review artifacts, then deploy checked main output with GitHub's Pages artifact actions. Deployment does not enable Pages or change visibility. The workflow uses the current official action releases verified on the decision date.

## Documentation consulted

- [Quarto website projects](https://quarto.org/docs/websites/), [navigation](https://quarto.org/docs/websites/website-navigation.html), [Python execution and caching](https://quarto.org/docs/computations/python.html), [project scripts](https://quarto.org/docs/projects/scripts.html), and [GitHub Pages publishing](https://quarto.org/docs/publishing/github-pages.html).
- [Quarto stable releases](https://github.com/quarto-dev/quarto-cli/releases/latest) and [setup action](https://github.com/quarto-dev/quarto-actions/tree/v2.2.0/setup).
- [GitHub custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html).
- [Upstream data licensing](https://github.com/jennybc/gapminder/blob/391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c/DESCRIPTION) and the exact source links in [data provenance](../data/README.md).

## Verification and evidence

- **Pass:** Quarto 1.11.9 runs locally; all seven pages render with both lesson notebooks and solutions executed. The build checks internal links and fragments, assets, notebook downloads, image alt text and a nonempty search index.
- **Pass:** source contracts and country-panel checks; two safeguard tests reject altered upstream bytes and a notebook marked to skip execution.
- **Pass:** the committed CSV exactly matches the checksum-verified upstream transformation using `scripts/prepare_data.py --check --source /tmp/python-course-gapminder.tsv`.
- **Pass:** `python scripts/check_fresh_runtime.py` executes all 30 lesson code cells and solutions, with file-format values checked separately, from separate empty working folders. Each download recreates the committed CSV byte for byte. This is a Python fresh-runtime check, not a Google Colab service test.
- **Pass:** a temporary copy with a deliberate unexpected `RuntimeError` fails the complete build and retains its unchanged input notebook.
- **Pass:** local browser checks of the start button, next-lesson navigation, grouped sidebar, search results, solution disclosures and keyboard theme control. At 390 × 844 and 1366 × 900, the landing page has no horizontal overflow and its start button is above the fold; the loading lesson also has no page overflow at phone width. Light/dark navigation and download-button contrast were inspected and corrected. This is not a full accessibility audit.
- CI and its downloadable artifact are recorded in the PR after they complete. Do not treat configured checks as demonstrated results.
- **Not run:** live Pages site, actual Google Colab service execution, Windows setup, full screen-reader/WCAG audit, or read-through of the unwritten Parts 0–2. Those are not implied by successful local execution.

## Limitations and next steps

The course remains a first review edition. The data end in 2007 and are not suitable as current country statistics. Course licensing is unresolved. After Phase 1 review, proceed through the handoff's remaining phases. Publication requires owner actions for visibility and Pages, followed by a live-site check. The optional local-install lesson must be tested on supported learner platforms before it is called complete.
