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
| Package manager | uv with pyproject.toml | `uv.lock` must be generated and committed once dependency resolution can be verified. |
| Website engine | Quarto, planned | Official GitHub Pages publishing documentation: https://quarto.org/docs/publishing/github-pages.html ; site is *not deployed yet*. |
| Notebooks | Do not commit unexecuted notebooks | Lesson notebooks and solution notebooks require top-to-bottom execution before they enter the course. |
| Output policy | Generated data in `data/processed/` is ignored | Source scripts and data provenance remain version-controlled. |
| Sample data | Deterministic synthetic survey | No human-subjects data, no fabricated empirical paper results. |
| Repository history | Preserve the existing AGENTS / CHANGELOG / records convention | Avoid a duplicate activity log. |

## TODO(verify) and open owner inputs

- **TODO(verify):** Resolve and commit `uv.lock`; mirror pinned versions in conda environment, then update README to promise reproducible installs.
- **TODO(verify):** Run setup and data-generation tests on all three operating systems through GitHub Actions; review actual run results.
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
