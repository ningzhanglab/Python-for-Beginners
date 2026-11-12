# First-release review

The curriculum is available on the [course website](https://ningzhanglab.github.io/Python-for-Beginners/). Publication is separate from a versioned release. Phase 5 is tracked in [Issue #9](https://github.com/ningzhanglab/Python-for-Beginners/issues/9). Licensing remains undecided; this checklist grants no additional reuse rights.

## Technical review

The [Phase 5 review record](records/2026-11-11-phase-five-review.md) records the exact automated and browser coverage, findings and limitations. A passing automatic accessibility scan is not WCAG certification or a human beginner study. Windows runner checks cover commands and analysis, not installer/editor screens.

Before approving the final commit, verify:

- [x] Required tests, executing build and all 35 independent fresh-runtime checks passed; verify the final PR head also has green CI.
- [x] Agent browser review covered 45 pages × two widths × two themes, plus keyboard search, disclosures, table scrolling and figure enlargement. Zero detected axe violations; incomplete measurements and human follow-up are documented in the record.
- [x] Internal links, 35 exact notebook downloads, portable ZIP/exports and 107 public HTTP links passed. HTTP success is separate from actual Colab execution.
- [x] Recorded actual Colab runs of lessons 0.2, 2.1, 4.5 and the fertility complete solution, including the setup restart prompt. Other Colab UI paths remain untested individually.
- [ ] Review and merge the focused PR, then verify the main-branch deployment and live downloads for that commit.

## Human learner review — not yet run

Ask a person who has never programmed to follow the first-hour browser path without coaching. Record consent to use anonymized feedback, the notebook/commit, elapsed active time, where they hesitated, errors encountered and whether they could explain the result. Do not publish their account details or personal data.

- [ ] They can start lesson 0.2, run a cell, change a value, explain the changed output, save their own copy and recover from a name error.
- [ ] They can complete exercises before opening solutions and rerun from a restarted session.
- [ ] A later learner can describe the country-year sample, units, missingness and association/causation limit, then complete one project starter before reading its solution.
- [ ] Adjust wording or timing based on observed difficulty; have the learner retry affected steps.

## Accessibility and optional local setup — human follow-up

- [ ] Test with a screen reader (for example VoiceOver or NVDA), including navigation landmarks, table headers, code, figure descriptions and open/close focus in the enlarged-figure viewer.
- [ ] Confirm keyboard-only access and 200% browser zoom on the learner's browser/device; check the actual physical phone, not only a resized browser.
- [ ] On a Windows learner computer, install uv and VS Code through approved sources, select the `.venv` notebook kernel and rerun the interpreter check. Repeat installer/editor steps on macOS. Managed university computers may have different restrictions.
- [ ] If Stata/R equivalence is to be claimed, run and compare those programs separately; current bridges are reading aids only.

## Owner decisions — deliberately pending

- [ ] Decide whether and how to license original code, lesson text, figures and simulated data. Until then, keep the undecided notice and third-party licenses distinct.
- [ ] Approve instructional accuracy, pace, accessibility findings and remaining limitations for a named first release.
- [ ] Only after an explicit release request: choose a version/date, move the appropriate Unreleased changelog entries, create the tag/release and verify its citation/downloads.

No first-release tag or release has been created by the Phase 5 review.
