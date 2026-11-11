"""Independent algebra checks for the covariance and fixed-effects teaching examples."""

from pathlib import Path
import unittest

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]


class AnalysisMethods(unittest.TestCase):
    def test_hc1_matches_sandwich_and_preserves_ols_point_estimates(self):
        data = pd.read_csv(ROOT / "data/gapminder.csv").query("year == 2007").copy()
        data["log_gdp_pc"] = np.log(data["gdp_pc"])
        ordinary = smf.ols("life_exp ~ log_gdp_pc", data=data, missing="raise").fit()
        robust = smf.ols("life_exp ~ log_gdp_pc", data=data, missing="raise").fit(cov_type="HC1", use_t=True)
        x = np.column_stack([np.ones(len(data)), data["log_gdp_pc"]])
        y = data["life_exp"].to_numpy()
        beta = np.linalg.lstsq(x, y, rcond=None)[0]
        residual = y - x @ beta
        bread = np.linalg.inv(x.T @ x)
        scores = x * residual[:, None]
        covariance = len(data) / (len(data) - x.shape[1]) * bread @ (scores.T @ scores) @ bread
        np.testing.assert_allclose(robust.params, beta, rtol=1e-10, atol=1e-10)
        np.testing.assert_allclose(ordinary.params, robust.params)
        np.testing.assert_allclose(robust.cov_params(), covariance, rtol=1e-10, atol=1e-10)

    def test_two_way_fixed_effects_matches_double_demeaning(self):
        # Balanced fictional panel; the independent calculation removes both sets of means.
        toy = pd.DataFrame({
            "country": np.repeat(["Northland", "Eastria", "Southport"], 4),
            "year": np.tile([2000, 2005, 2010, 2015], 3),
            "income": [8, 11, 12, 16, 20, 21, 25, 28, 3, 5, 8, 9],
            "life": [60, 64, 65, 67, 70, 71, 75, 76, 50, 54, 56, 59],
        })
        demeaned = {}
        for name in ["income", "life"]:
            demeaned[name] = (toy[name] - toy.groupby("country")[name].transform("mean")
                              - toy.groupby("year")[name].transform("mean") + toy[name].mean())
        x, y = demeaned["income"].to_numpy(), demeaned["life"].to_numpy()
        expected = (x @ y) / (x @ x)
        result = PanelOLS.from_formula("life ~ 1 + income + EntityEffects + TimeEffects",
                                       data=toy.set_index(["country", "year"])).fit()
        np.testing.assert_allclose(result.params["income"], expected, rtol=1e-10)
        self.assertEqual(result.nobs, 12)
        self.assertTrue(result.model.entity_effects and result.model.time_effects)


if __name__ == "__main__":
    unittest.main()
