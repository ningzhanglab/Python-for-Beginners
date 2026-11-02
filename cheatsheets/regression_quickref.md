# Regression quick reference (Python for Beginners)

This one-page guide accompanies [Module 4](../modules/04_econometrics/README.md). The example uses **fictional values**, not actual research subjects or a causal study. The complete code block is executed in [a pytest check](../tests/test_regression_quickref.py).

## Common tasks

| Task | Python / statsmodels | Stata | R |
| --- | --- | --- | --- |
| Basic OLS | `smf.ols("y ~ x", data=d).fit()` | `reg y x` | `lm(y ~ x, data=d)` |
| Conventional OLS covariance | `.fit()` | `reg y x` | `lm()` default |
| HC3 covariance | `.fit(cov_type="HC3")` | `vce(hc3)` (version-dependent) | `sandwich::vcovHC(m, type="HC3")` |
| Clustered covariance | `.fit(cov_type="cluster", cov_kwds={"groups": d["cluster"]}, use_t=True)` | `vce(cluster cluster)` | `sandwich::vcovCL(m, cluster=~cluster)` |
| Coefficients | `result.params` | `matrix list e(b)` | `coef(m)` |
| Standard errors | `result.bse` | `estat vce` | `sqrt(diag(vcov(m)))` |
| Confidence intervals | `result.conf_int()` | `reg` output | `confint(m)` |
| Fitted values | `result.predict(d)` | `predict yhat` | `predict(m, newdata=d)` |

Third-party R packages `sandwich` and `statsmodels` use their own licenses; this guide does not redistribute or relicense them.

## Copy-and-run synthetic example

This example simulates **30 groups × 5 workers** and explicitly compares covariance estimators. All three fits have the same OLS point estimates because only the estimated uncertainty changes. The standard errors are not expected to obey a universal ordering.

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(512)
clusters = np.repeat(np.arange(30), 5)
schooling = rng.integers(10, 19, size=len(clusters))
experience = rng.integers(0, 25, size=len(clusters))
shocks = rng.normal(0, 2, size=30)[clusters]
wage = 5 + 1.6 * schooling + 0.5 * experience + shocks
wage += rng.normal(0, 3, size=len(clusters))
data = pd.DataFrame({"wage": wage, "schooling": schooling,
                     "experience": experience, "cluster": clusters})
formula = "wage ~ schooling + experience"
fit_ols = smf.ols(formula, data=data).fit()
fit_hc3 = smf.ols(formula, data=data).fit(cov_type="HC3")
fit_cluster = smf.ols(formula, data=data).fit(
    cov_type="cluster", cov_kwds={"groups": data["cluster"]},
    use_t=True
)
table = pd.DataFrame({
    "coefficient": fit_cluster.params,
    "conventional_se": fit_ols.bse,
    "hc3_se": fit_hc3.bse,
    "cluster_se": fit_cluster.bse,
})
print(table.round(3))
print("N:", int(fit_cluster.nobs), "clusters:", data["cluster"].nunique())
```

## Interpret with care

**Model fit is not identification.** OLS coefficients are adjusted associations unless a credible research design justifies causal inference. HC3 helps with heteroskedasticity; cluster-robust inference allows within-cluster dependence when assumptions are appropriate. With few clusters, conventional inference can be unreliable. Always report the outcome units, covariates, estimation sample, covariance estimator, number of clusters, and degrees-of-freedom convention.

## Official references

- [statsmodels OLS](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html)
- [OLS.fit: `cov_type` and `cov_kwds`](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.fit.html)
- [Robust covariance inference](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.get_robustcov_results.html)
