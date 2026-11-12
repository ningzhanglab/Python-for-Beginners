# Phase 5 course review

**Status:** Technical/browser review complete; human review and first-release approval pending.
**Date:** 2026-11-11 (America/Los_Angeles)
**Tracking:** [Issue #9](https://github.com/ningzhanglab/Python-for-Beginners/issues/9), [PR #10](https://github.com/ningzhanglab/Python-for-Beginners/pull/10)
**Responsible:** To be assigned by the course owner.
**AI assistance:** Codex, model not reported; read the course, implemented fixes and ran computational/browser checks. A person must verify novice usability, assistive-technology behaviour, installer/editor steps, instructional suitability and release decisions.

## Scope and findings

Reviewed the 31 lessons, two project starter/solution pairs, five references and entry pages for defined terms, sample/units, navigation and setup. This was an agent read-through, not observation of a human beginner. Curriculum order, analysis code, outcome checks, data and dependency pins were preserved. Clarified the R bridge's one-row-per-country description and updated stale publication/setup notes.

Actual Colab use exposed broken generated-download links and visible Quarto-only button/callout markup. Notebook links now use the public website address; ordinary HTML links and Markdown quotations render in both environments. Local validation also checks those absolute course URLs. Generated exports are staged after execution rather than depending on Quarto's earlier resource discovery.

The browser review found pale active contents links, small breadcrumb targets, unnamed pandas index headers, dark TODO and breadcrumb contrast, reference tables unreachable by keyboard, overlapping captions on tall phone figures, and loss of focus after closing an enlarged figure. Fixes retain the built-in themes and figure viewer with small source CSS/HTML adjustments. The figure viewer is named, receives focus, preserves the original image description and returns to the opening link. A Lua filter consolidates pandas index/column-axis labels without changing table data. An independent comparison found all 929 body/index values in 56 pandas tables unchanged.

Custom CSS receives a content-derived filename in the disposable build so revised styling does not remain hidden behind an older browser cache. `_quarto-review.yml` enables the bundled axe-core 4.10.3 audit in a separate `_site-review/` folder. Production builds include no audit overlay or axe scripts. The review uses [Quarto's accessibility support](https://quarto.org/docs/output-formats/html-accessibility.html), WCAG 2.2 AA rules plus axe best practices, and manual browser checks. Passing rules do not establish complete WCAG conformance.

## Demonstrated checks

- Python 3.12 / Quarto 1.11.9: 11 safeguard/numerical/portable-project tests passed; all 35 notebooks independently executed from empty working folders with exact input and outcome checks.
- Executing site builds passed: 45 course pages (46 HTML documents including the exported regression table), 35 byte-identical notebook downloads, 17 declared exports, internal links/fragments, alt text, search and Excel/Stata conversion values.
- Exact upstream country transformation, fixed-seed simulation, World Bank transformations, 11 package setups, six generated data/workflow setups and both generated project starters passed.
- A real Windows runner created the documented uv/Python 3.12 environment, synchronized the sole dependency file, checked package compatibility and ran course validation plus all tests, including analysis from an unrelated folder with spaces. [Initial Windows run](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/43145230864). Explicit UTF-8 reads and preserved LF/raw snapshot bytes avoid platform-dependent source/checksum drift. The deployment now depends on both Linux build and Windows checks.
- Actual Google Colab runs completed lesson 0.2 (public download and chart), 2.1 (CSV/Excel/Stata), 4.5 (fixed effects, coefficient 1.4499 and clustered SE 0.7074), and the fertility complete solution (211 observations, simple slope −0.6571668229, region-adjusted slope −0.4138785106 and exports). The library setup's restart instruction was encountered in the panel lesson; execution completed after restarting/reopening. The fertility notebook at `8ec0ca8af195fa086a64fc6ed1998590dacb7606` also confirmed the revised portable links/formatting in Colab. The other Colab service/UI paths were not individually executed; the independent local check covered all notebooks.
- The PR #8 main deployment succeeded and the live homepage, representative pages/downloads and portable ZIP were verified before this review. Phase 5 changes are review content until merged and deployed.

Final browser coverage: all 45 course pages at 1280×900 and 390×844 in both light and dark themes (180 page states), with **zero detected axe violations and zero horizontal page overflow**. All use the final source styles and figure-viewer hook. Axe still marked some checks incomplete: contrast in 156 states and target size in 86 (168 states had at least one incomplete item). Representative reasons were partially obscured text in scrollable content and clipped sidebar items. These are unresolved automatic measurements, **not passed checks**; they remain part of human accessibility follow-up. The exported regression-table HTML is included in build/link/export checks, not in the 45-page axe sweep.

Keyboard checks verified mobile sidebar toggling; sideways table scrolling (scroll position changed from 0 to 37.5 pixels); search for “fixed effects” and keyboard selection of lesson 4.5; solution open/close with Enter; and enlarged-figure Escape exit with focus restored to the original figure link. The tall phone figure's image ended at y=552.30 and its caption began there, with no overlap. The viewer's Close button received focus and the original descriptive alt text survived enlargement. This is browser evidence, not a screen-reader study or a physical-phone test.

The public HTTP checker reached **107/107 URLs**, with no 404/410 or unverified service responses. It does not establish the content or execution of every external page. Linux build and Windows tests passed on the implementation branch in [this CI run](https://github.com/ningzhanglab/Python-for-Beginners/actions/runs/43155172441); final PR checks must also pass on the reviewed head. No PR deployment ran.

## Remaining human work

Use [RELEASE_CHECKLIST.md](../RELEASE_CHECKLIST.md). No human beginner participation, screen-reader study, physical-phone review, 200% browser-zoom test, Windows/macOS installer/editor walkthrough or Stata/R execution is claimed. Browser geometry tests are resized-browser checks. Automated contrast scans can leave clipped/overlapped content for manual review. No original-content license, version tag or first release was selected or created. Repository visibility and Pages configuration were not changed.
