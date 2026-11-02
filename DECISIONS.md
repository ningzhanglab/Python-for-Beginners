# Build decisions and verification log

This file documents deviations and choices under the owner-provided **Python for Economics & Social Science** build specification. It is not a per-commit activity log; see Git history and [issue #1](https://github.com/ningzhanglab/Python-for-Beginners/issues/1) for the implementation checklist.

## Confirmed owner choices

| Question | Decision | Why |
| --- | --- | --- |
| Repository name | Keep `ningzhanglab/Python-for-Beginners` | The owner explicitly requested no rename; spec's working title describes the curriculum, not the GitHub repo. |
| License | MIT for original code **and original educational content** for now | Owner explicitly chose MIT for this repo. Do not add the spec's suggested CC BY license unless the owner later requests it. Third-party data/assets remain subject to their own licenses. |
| Workflow | Small milestones on topic branches via pull requests | Existing `AGENTS.md` forbids writing directly to `main` without authorization. |

## Design choices

| Topic | Current choice | Notes |
| --- | --- | --- |
| Python | Target Python 3.12 | Ecosystem compatibility must be checked in CI on Linux, Windows, and macOS. |
| Package manager | uv with pyproject.toml and committed uv.lock | The Python 3.12 lock was generated in CI and locked installs passed on three OS runners. |
| Website engine | Quarto, planned | Official GitHub Pages publishing documentation: https://quarto.org/docs/publishing/github-pages.html ; site is *not deployed yet*. |
| Notebooks | Do not commit unexecuted notebooks | Lesson notebooks and solution notebooks require top-to-bottom execution before they enter the course. |
| Output policy | Generated data in `data/processed/` is ignored | Source scripts and data provenance remain version-controlled. |
| Sample data | Deterministic synthetic survey | No human-subjects data, no fabricated empirical paper results. |
| Repository history | Preserve the existing AGENTS / CHANGELOG / records convention | Avoid a duplicate activity log. |

## TODO(verify) and open owner inputs

- **Completed:** Commit a CI-resolved `uv.lock` for the pinned Python 3.12 uv environment. **TODO(verify):** mirror compatible exact pins in the conda environment, with actual conda OS tests.
- **Completed for current tests:** GitHub Actions setup, synthetic data tests, and notebook execution have passed on Ubuntu, Windows, and macOS. Future modules and workflows require their own verification.
- **TODO(verify):** Verify package and dataset contents, public redistribution licenses, attribution, snapshots, and third-party API fallbacks before adding teaching datasets.
- **TODO(verify):** Verify the current Quarto build and GitHub Pages publishing workflow before declaring the site live; configure Pages settings if necessary.
- **TODO(verify):** Execute every notebook before adding it, then validate Colab/Binder paths and exercise checks.
- **TODO(owner):** Preferred author attribution, affiliation, contact email, and any custom domain (optional). The copyright notice uses the verified name associated with the initial GitHub commit; owner should review.
- **TODO(owner):** Approve future release only after all acceptance criteria are checked; do not tag v1.0.0 prematurely.

## Milestones

1. Foundation (this PR): honest README, license, setup policy, directory outlines, initial helper/data tooling.
2. Infrastructure: lockfile, full CI verification, data snapshots, notebook validators and badges.
3. Quarto site and modules 0–2.
4. Tested cheat sheets, modules 3–4, data access and research pipelines.
5. Capstone, electives, instructor materials, accessibility pass, beginner walkthrough, release.

The spec's full acceptance checklist is not yet complete. Progress must not be presented as published curriculum.

## Foundation validation, 2026-11-01

- Local test evidence: four synthetic-survey/helper tests passed in a recreated sandbox with Python 3.13.5. This was **not** the complete Python 3.12 uv environment.
- GitHub Actions [foundation checks](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41394368763) were **successful** on Ubuntu, Windows, and macOS. Those checks install the project, run its setup smoke test and pytest tests, validate currently released notebooks (zero so far), and run Ruff lint. CI currently resolves dependencies without a committed uv.lock; a reproducible lock remains open.
- Work is reviewed in [draft PR #2](https://github.com/ningzhanglab/Python-for-Beginners/pull/2). No merge or GitHub Pages deployment has occurred.

## First notebooks and validation (2026-11-01)

- **Pass (local):** Two learner notebooks and two completed solutions executed end-to-end using Python 3.13.5 and `nbclient`; 4/4 passes. Each learner version gives hints for blank exercises, and all solution checks pass.
- **Pass (GitHub CI):** Fresh-kernel notebook tests, the template validator, and Ruff passed on Ubuntu, Windows, and macOS after a blank-line import style fix; CI uses Python 3.12. These runs covered eight pytest tests including the existing survey tests.
- **TODO(verify):** Colab/Binder badges point to `main` after merge; public access is blocked while the repository is private. Their paths are validated, but a live browser launch is not yet claimed.
- **Dependency locking:** CI temporarily prints the fully resolved `uv.lock` so it can be imported in the next commit; this should be removed immediately once the lockfile is reviewed and committed.

## Verified uv lockfile

- **Pass:** `uv.lock` was generated by `uv sync` on Ubuntu GitHub Actions using Python 3.12, then captured verbatim from [successful run #41395705452](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41395705452). The lock contains 111 package records; package hashes and platform resolution markers are preserved.
- CI was updated to `uv sync --locked --group dev` and the temporary lock-printing step was removed immediately after capturing it. CI status for this new locked configuration requires a new run.
- **TODO(verify):** conda environment is still provisional and has not been resolved against this lockfile. Avoid treating conda instructions as fully pinned until verified.

## Modules 0–1 — authoring and CI

- All planned Module 0 sections (two notebooks and two Markdown lessons) and all eight Module 1 notebook lessons plus corresponding solution notebooks are now in the draft PR.
- **Pass:** The new Module 0 and Module 1 notebook execution tests, validator and Ruff ran successfully in Python 3.12 GitHub Actions [run #41396837908](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41396837908), with Ubuntu, Windows and macOS jobs successful after a checkpoint-import style correction. Earlier additions were verified in [run #41396452536](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41396452536).
- A badge sync utility is being added. Its checks run separately from live browser launch verification; its CI result should be checked before claiming it passes in all environments.
- **Open:** the source specification requires a live beginner walkthrough, Colab/Binder access, and a website. The repo is private and PR unmerged, so public badge launching remains unverified. In particular, do not claim course publication based on notebook unit tests alone.

## Module 2 first lessons — 2026-11-01

- Scope: publish three pandas lessons (DataFrame and CSV/Excel/Parquet/Stata file I/O, selecting/filtering, cleaning) and three corresponding completed solutions. Other Module 2 topics are not yet complete.
- Source data: self-contained **six-row fictional teaching extract** in each notebook, deliberately distinct from the 90-row synthetic survey generator; no confidential or external data.
- Local precommit check: all six notebook **code-cell sequences** were executed via `nbclient` in fresh kernels using Python 3.13.5 and pandas 2.2.3. Learner versions printed nonfatal hints; completed solutions passed their checks. The optional Parquet branch was not exercised locally because `pyarrow` is absent from the local sandbox; the CI environment includes `pyarrow`.
- **TODO(verify):** GitHub Actions run with Python 3.12, the locked pandas release, Stata/Excel/Parquet I/O, Ruff, and the existing notebook validator. Do not claim success until the resulting CI checks complete.
- pandas 3 uses Copy-on-Write and disallows chained assignment; teaching examples use direct `.loc` assignment. Official references: https://pandas.pydata.org/docs/user_guide/copy_on_write.html and https://pandas.pydata.org/docs/user_guide/io.html .
- Public Colab/Binder links still point to the not-yet-updated `main` branch of this private repository. Live launch unverified.

## Module 2 variables, merging, reshaping (2026-11-01)

- New lessons 04–06 and their three completed solutions use the same self-contained six-row fictional survey, with an additional fictional household lookup for merges.
- **Pass (local, precommit):** all six code-cell sequences executed in separate clean `nbclient` kernels using Python 3.13.5 and pandas 2.2.3. Learner exercises printed hints without exceptions, while solutions passed all checks. Imports were normalized for Ruff before saving.
- **Pass (CI for prior batch):** Module 2 lessons 01–03 passed Ubuntu, Windows, macOS in [run #41398314510](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41398314510).
- **TODO(verify):** the newly added 04–06 notebooks must pass the locked Python 3.12 CI before being labeled cross-platform tested. Full module checkpoint, real Colab access, and site publication remain pending.

## Module 2 aggregation, panels, larger files (2026-11-01)

- Added lessons 07–09 with their solution notebooks. Lesson 08 explicitly distinguishes a unique *record* key from a verified longitudinal person identifier, avoiding spurious panel claims.
- **Pass (local, precommit):** all six code-cell sequences executed in fresh `nbclient` kernels using Python 3.13.5 / pandas 2.2.3. Learners' incomplete exercises printed hints; solutions' checks passed.
- The optional Parquet-writing code in lesson 09 is guarded when `pyarrow` is absent locally; GitHub CI uses the locked `pyarrow` installation.
- **Pass (CI for previous batch):** lessons 04–06 verified with GitHub Actions [run #41398857559](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41398857559) across Ubuntu, Windows, macOS.
- **TODO(verify):** cross-platform CI for the newly added 07–09 notebooks, before describing their CI status as passed.

## Module 2 checkpoint — 2026-11-01

- **Pass (local, precommit):** the 90-row synthetic checkpoint notebook and completed solution were reconstructed with their exact code-cell sequence and executed in clean `nbclient` kernels under Python 3.13.5 / pandas 2.2.3. Learner checks printed hints without stopping; solution checks passed. The Parquet branch cannot be fully tested locally without `pyarrow`, but the locked CI environment includes it.
- Input generation mirrors the committed `data/scripts/make_messy_survey.py` seed, row construction and intentional defects: 90 fictional people/wave records, 30 fictional household keys, one duplicated person identifier, sentinel -99, invalid text, and a wage outlier.
- The completed checkpoint solution builds a cleaned wage/region dataset, validates the many-to-one household join, and reshapes two cleaned annual wages to a 180-row analysis-ready table before export.
- **Lint fix:** removed an unused NumPy import from lesson 08 (learner and solution) after GitHub Actions flagged F401; other tests in [run #41399407132](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41399407132) had reached the lint stage.
- **TODO(verify):** full 10-lesson Module 2 CI (including actual Parquet writing in Python 3.12), walkthrough, private-repository badge access, and full-course release. Do not treat authored lessons alone as a published public course.

## Checkpoint source consistency test

- Added a regression test to compare the raw 90-row notebook-generated survey and household lookup directly against the project-owned `make_messy_survey.py` outputs. This guards against accidental drift while keeping the checkpoint runnable without external network access.
- The test runs in Python CI, not against real participant or private research data.

## Module 2 verified cross-platform (GitHub Actions, 2026-11-01)

- **Pass:** [run #41400291708](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41400291708) completed successfully on Ubuntu, Windows and macOS using Python 3.12 and `uv sync --locked`.
- Ubuntu logged **47 passing tests** (40 notebook executions across Modules 0–2 plus helper, dataset, badge and consistency tests), **20 learner notebooks validated**, all 20 badge paths checked, and Ruff passing.
- The new `tests/test_checkpoint_data.py` successfully compared the checkpoint's generated 90-row survey/households to the canonical generator outputs. The fully locked environment includes `pyarrow` and executes the checkpoint's analysis-ready Parquet round trip.
- Remaining blockers for public readiness: repository is private, lesson badges refer to `main`, live Colab/Binder launches and the beginner walkthrough are not yet verified; site deployment and later modules also remain incomplete.

## Module 3 initial lessons — 2026-11-01

- Two learner notebooks and matching solutions were added for Table 1 statistics and matplotlib plots. Both use **fictional, self-contained data**, so the first lessons do not require external downloads or research credentials.
- The summary-statistics notebook distinguishes observed wage counts from row counts and demonstrates a weighted mean while explicitly warning that the synthetic weights are *not* a survey-variance design.
- matplotlib examples use a noninteractive backend for portable execution on GitHub Actions, and create a high-resolution in-memory PNG. A fuller figure accessibility and site-rendered-output review remains to be completed.
- Initial CI executed the notebooks, but lint flagged an import spacing issue, corrected in a follow-up commit. **Pass:** final Module 3 notebook suite passed under the locked Python 3.12 GitHub CI environment; see run #41405225377.

- A third introductory Module 3 lesson adds Seaborn histogram, boxplot and descriptive regression-line examples, distinguishing association from causation. Results remain based on fictional data. **Pass:** notebook/solution execution and lint passed on Ubuntu, Windows and macOS in run #41405225377.

## Module 3 completion and visualization

- Authored all six Module 3 lessons with one matching completed solution notebook each. The checkpoint regenerates the seeded 90-row survey and requires a Table 1 and three labeled figures. The first five lessons draw on self-contained fictional examples.
- Earlier Module 3 lesson CI runs passed on Ubuntu, Windows and macOS, including [Seaborn run #41404568857](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41404568857) and [publication/panel run #41404876942](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41404876942).
- The plotting notebooks now display worked figures inline before closing the matplotlib figures. Source notebooks remain output-stripped to keep Git diffs readable. **Pass:** [GitHub Actions run #41405225377](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41405225377) completed successfully on Ubuntu, Windows, and macOS: 59 pytest tests passed, 26 learner notebooks validated, badge paths checked and Ruff passed. Notebook execution covers inline figure generation and the checkpoint solution. **TODO(verify):** inspect the rendered figures visually and complete the accessibility review.
- **Unfinished:** manual visual/alt-text and accessibility review, live Colab/Binder access, full website deployment, and learner walkthrough.

## Module 4 econometrics dependencies (2026-11-01)

- Added `statsmodels>=0.15,<0.16` as a core regression dependency, according to the existing owner spec. The project still uses MIT for its own content; statsmodels is separately distributed under BSD-3-Clause.
- `uv.lock` was resolved in [successful GitHub Actions run #41405968974](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/41405968974), with statsmodels **0.15.0** and 118 package records, using Python 3.12. Package hashes and platform markers were preserved verbatim from the CI-produced lockfile.
- CI returned to `uv sync --locked --group dev` after capturing the resolved lock. **TODO(verify):** check the new locked CI run across all three platforms and the new statsmodels notebooks before declaring them verified.
- Module 4 examples initially use deterministic fictional wage data, not third-party human-subjects records, and explicitly distinguish regression association from causation.
