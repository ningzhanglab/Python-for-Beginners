# Course data

Only open, small teaching data belong here. The course's original licensing remains undecided; that does not change the third-party data terms below.

## `gapminder.csv`

- **Question:** Do people live longer in richer countries?
- **Source:** Gapminder historical teaching extract, packaged by Jennifer Bryan in the R `gapminder` package. [Package documentation](https://jennybc.github.io/gapminder/), [upstream dataset documentation](https://github.com/jennybc/gapminder/blob/391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c/man/gapminder.Rd).
- **Exact download:** [upstream TSV](https://raw.githubusercontent.com/jennybc/gapminder/391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c/inst/extdata/gapminder.tsv), commit `391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c`.
- **Retrieved:** 2026-11-11.
- **License:** CC0, explicitly declared in the [upstream package DESCRIPTION](https://github.com/jennybc/gapminder/blob/391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c/DESCRIPTION). [CC0 terms](https://creativecommons.org/publicdomain/zero/1.0/). Redistribution and adaptation are permitted. Credit: Gapminder and Jennifer Bryan; this is not an endorsement.
- **Preparation:** `python scripts/prepare_data.py`. Uses only Python's standard library, verifies the upstream SHA-256, renames columns, converts tabs to commas, and preserves all original values and row order. No rows are removed, no values are imputed, and no figures are rounded. To verify: `python scripts/prepare_data.py --check` (network required), or add `--source /path/to/gapminder.tsv` for an offline check.
- **Upstream SHA-256:** `f74275b4a2f4a7c8e3a09a752f9d6e43d1759d78d5cbfdebaaa3e1a6efc68f78`.
- **Size and coverage:** 1,704 rows, 6 columns; 142 countries × 12 five-year observations, 1952–2007. A row is a country-year. This filtered teaching extract contains no missing values in these six columns. It is not a representative sample of individuals, a complete country list, or current statistics. Continent labels and country boundaries follow the historical source.

| Course column | Upstream name | Meaning / units |
| --- | --- | --- |
| `country` | `country` | Country name in the historical extract |
| `region` | `continent` | Broad continent grouping: Africa, Americas, Asia, Europe, Oceania; no new classification added |
| `year` | `year` | Calendar year, every five years |
| `life_exp` | `lifeExp` | Life expectancy at birth, years |
| `population` | `pop` | Population, people |
| `gdp_pc` | `gdpPercap` | GDP per person, US dollars adjusted for inflation, as described by the upstream package; not current dollars or household income |

The upstream package does not identify a dollar base year in its variable documentation. Do not infer one or compare these numbers directly with a different vintage of GDP data. This extract is suitable for learning commands and discussing association; research requires checking the underlying measurement methodology and the appropriate current source.

The Excel and Stata files made in lesson 2.1 are temporary format conversions of this same CSV, generated under ignored `scratch/`. They introduce no additional observations or data source. The notebook's Colab preparation recreates the same CSV from the same checksum-verified upstream bytes when no local copy exists.

No simulated person-level dataset or time series has been added in Phase 1. Their generation scripts, fixed seeds and provenance will accompany the later lessons that need them.
