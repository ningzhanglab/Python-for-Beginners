# A small analysis someone else can rerun

Question: do richer countries have longer life expectancy in this historical teaching extract? This is a descriptive association, not a causal design.

This folder's downloadable version contains the original `data/raw/gapminder.tsv`, its two Python scripts and a generated copy of the course's sole `requirements.txt`. The raw TSV is never edited. Outputs go to `results/`, beside the scripts, even when you launch the script from a different working folder.

From this extracted folder, use Python 3.12. If you have uv installed:

```sh
uv venv --python 3.12
uv pip sync requirements.txt
```

On macOS/Linux run:

```sh
.venv/bin/python analyze.py
```

On Windows PowerShell run:

```powershell
.venv\Scripts\python analyze.py
```

The script produces a 2007 scatter, a selected-coefficient CSV and notes with source, units, sample, uncertainty settings, alt text and environment versions. `--year 2002` writes separate filenames. Both example years contain 142 country observations; the 2007 log-income coefficient is about 7.202802 years per natural-log unit. Small numeric tolerances are appropriate across platforms; font rendering and image bytes need not match across operating systems.

`fetch_data.py` verifies the existing raw file's SHA-256 before use. If it is absent, it downloads the pinned public source. Run the file directly to download/verify it. `--from-file /path/to/gapminder.tsv` supplies an existing exact copy offline. It stops on changed bytes instead of adopting a newer dataset. Creating the Python environment needs internet; with packages and the included raw file present, analysis works offline.

## Source and rights

Gapminder historical teaching extract packaged by Jennifer Bryan, commit `391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c`, retrieved 2026-11-11. Original TSV: https://raw.githubusercontent.com/jennybc/gapminder/391b5a40d3574c3b89d889dd7d72f7f3fdb4a70c/inst/extdata/gapminder.tsv . SHA-256: `f74275b4a2f4a7c8e3a09a752f9d6e43d1759d78d5cbfdebaaa3e1a6efc68f78`.

Source data are CC0; see https://creativecommons.org/publicdomain/zero/1.0/ and the upstream package DESCRIPTION. All 1704 source observations are retained; analysis selects one year and renames columns in memory. The course's original code, text and figures have no selected license. No open license is implied for those materials.

Before sharing research, document your own question, source rights, sample decisions, versions, limitations and the exact command. A successful rerun verifies a computation; it does not establish that the question or model is appropriate.
