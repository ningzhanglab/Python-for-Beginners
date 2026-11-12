# Changelog

A concise, user-facing summary of **significant** changes. Follow the spirit of [Keep a Changelog](https://keepachangelog.com/); group related changes rather than recording every commit.

Exact file diffs live in Git history. Use [records/](records/README.md) only when substantial decisions, investigations, experiments, or verification evidence need separate documentation.

New entries belong under Unreleased until the owner requests a release. Link the PR, or the tracking issue for an explicitly authorized direct-to-main phase.

## Unreleased

### Fixed

- Notebook downloads and result links work from Colab as well as the course website; builds explicitly stage generated exports and version revised styles. Accessibility polish improves contents/breadcrumb contrast and target sizes, pandas table headers, keyboard scrolling of reference tables, dark TODO comments, and enlarged figures' captions, descriptions and focus. Added a separate browser audit profile, public-link checker, Windows learner-environment checks and a first-release checklist; human learner/assistive-technology review and licensing/release decisions remain pending ([PR #10](https://github.com/ningzhanglab/Python-for-Beginners/pull/10); [review evidence](records/2026-11-11-phase-five-review.md)).

### Added

- Full curriculum draft: four workflow lessons, a portable raw-data-to-results project, two guided World Bank projects with incomplete starters and complete solutions, and five executed reference pages. Pinned public snapshots retain missingness and provider rights; expanded checks verify all 35 notebooks, generated inputs/downloads and 17 exports. Phone review improved project entry points and reference-table scrolling. Beginner/accessibility polish and release sign-off remain separate ([PR #8](https://github.com/ningzhanglab/Python-for-Beginners/pull/8)).
- Analysis path: ten lessons in Parts 3–4 cover readable charts, PNG/PDF exports, descriptive tables, formula OLS, categories and interactions, robust and clustered standard errors, country/time fixed effects, and downloadable regression tables. Figures fit phone screens and open larger when selected. Standalone package setup uses the shared dependency pins; builds check model outcomes and generated exports ([Issue #6](https://github.com/ningzhanglab/Python-for-Beginners/issues/6)).
- Complete core path: 17 lessons across Parts 0–2, with independent browser notebooks, exercises and solutions, a reproducible simulated survey, validated merges, panel reshaping and date/time-series practice. Builds also check lesson-specific outcomes and exact dataset regeneration. This phase was explicitly requested directly on main ([Issue #5](https://github.com/ningzhanglab/Python-for-Beginners/issues/5)).
- First review edition of the economics and social-science Python course: an executable Quarto website, complete browser-notebook and data-loading lessons, a documented CC0 country panel, notebook downloads and automated build/Pages workflows ([#4](https://github.com/ningzhanglab/Python-for-Beginners/pull/4)). See the [site-tooling decision](records/2026-11-11-site-tooling.md). Later lessons are marked coming soon; course licensing and publication remain owner decisions.
