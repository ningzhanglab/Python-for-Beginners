"""Run the documented, project-owned regression cheatsheet example."""

import re
from pathlib import Path

import numpy as np

CHEATSHEET = Path(__file__).resolve().parents[1] / "cheatsheets" / "regression_quickref.md"


def test_regression_quickref_is_executable():
    markdown = CHEATSHEET.read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)\n```", markdown, flags=re.DOTALL)
    assert len(blocks) == 1, "Keep exactly one runnable end-to-end example"
    environment: dict[str, object] = {}
    exec(compile(blocks[0], str(CHEATSHEET), "exec"), environment)
    table = environment["table"]
    model_ols = environment["fit_ols"]
    model_hc3 = environment["fit_hc3"]
    model_cluster = environment["fit_cluster"]
    assert model_hc3.cov_type == "HC3"
    assert model_cluster.cov_type == "cluster"
    assert model_cluster.use_t
    assert int(model_cluster.nobs) == 150
    assert environment["data"]["cluster"].nunique() == 30
    assert np.allclose(model_ols.params, model_hc3.params)
    assert np.allclose(model_ols.params, model_cluster.params)
    assert (table[["conventional_se", "hc3_se", "cluster_se"]] > 0).all().all()
