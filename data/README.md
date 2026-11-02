# Course datasets and provenance

**Never commit third-party data without first verifying its redistribution terms.** A code package's license does not automatically cover the underlying datasets.

## Dataset A — Synthetic household survey (under construction)

- **Source:** deterministic data generator in [scripts/make_messy_survey.py](scripts/make_messy_survey.py).
- **Creator:** this project, using a fixed NumPy random seed; no real individuals, families, or confidential data.
- **License:** MIT for original generated synthetic files and the generator; see [../LICENSE](../LICENSE).
- **Recreate:** from the repository root, run `uv run python data/scripts/make_messy_survey.py`.
- **Outputs:** synthetic person-wave survey in CSV, Excel, and Stata formats, plus a household lookup CSV. Outputs are ignored by Git until format and reproducibility checks are complete.
- **Known intentional issues:** inconsistent text labels, -99 missing codes, numeric strings, duplicate IDs, implausible outlier, mixed date formats, survey weights and two waves stored in wide columns.
- **Codebook:** column descriptions are in the generator's docstring. This is synthetic practice data; it cannot support substantive claims about actual populations.

## Planned third-party sources (not yet bundled)

| Source | Intended use | Redistribution status |
| --- | --- | --- |
| Wooldridge wage data | OLS and descriptive stats | TODO(verify) dataset-specific terms and attribution |
| World Bank WDI | Country-year panel | TODO(verify) API terms, snapshot policy, citations |
| Causal-design datasets | DiD, IV, RD | TODO(verify) data provenance and terms for each study |
| FRED series | Macro/time-series | TODO(verify) series-level terms and key-free snapshots |

No real third-party datasets are distributed by this foundation commit.

## Module 2 checkpoint reproducibility

[Module 2's 90-row checkpoint](../modules/02_data_wrangling/10_wrangling_project.ipynb) reproduces this project's seeded synthetic survey and household lookup without fetching files from GitHub, so its examples can run in a self-contained notebook. [The regression test](../tests/test_checkpoint_data.py) executes the checkpoint's input-generation cells and compares the fictional raw survey and household lookup with the canonical generator's CSV outputs. This detects drift between the two teaching paths. Lessons 01–09 use a separate, six-row fictional teaching extract for shorter demonstrations; their numbers are not identical to the full 90-row survey.
