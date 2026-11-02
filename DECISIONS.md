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
