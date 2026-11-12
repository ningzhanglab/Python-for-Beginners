"""Run the descriptive income/life-expectancy analysis from a verified raw file."""
import argparse
from pathlib import Path
import platform

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.formula.api as smf

from fetch_data import ensure_data

ROOT = Path(__file__).resolve().parent


def analyze(year=2007):
    source = ensure_data()
    countries = pd.read_csv(source, sep='\t').rename(columns={
        'continent': 'region', 'lifeExp': 'life_exp', 'pop': 'population', 'gdpPercap': 'gdp_pc'})
    if countries.duplicated(['country', 'year']).any():
        raise ValueError('Duplicate country-year keys need review.')
    sample = countries.loc[countries['year'] == year, ['country', 'life_exp', 'gdp_pc']].dropna().copy()
    if len(sample) < 3 or not sample['gdp_pc'].gt(0).all():
        raise ValueError('Select an observed year with at least three complete, positive-income observations.')
    sample['log_gdp_pc'] = np.log(sample['gdp_pc'])
    model = smf.ols('life_exp ~ log_gdp_pc', sample, missing='raise').fit(cov_type='HC1', use_t=True)
    interval = model.conf_int().loc['log_gdp_pc']
    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    table = pd.DataFrame([{
        'year': year, 'n_countries': int(model.nobs), 'term': 'log_gdp_pc',
        'estimate_years_per_log_unit': model.params['log_gdp_pc'],
        'HC1_standard_error': model.bse['log_gdp_pc'], 'ci95_lower': interval.iloc[0],
        'ci95_upper': interval.iloc[1], 'covariance': 'HC1; t-based approximate intervals',
    }])
    table.to_csv(results / f'model-{year}.csv', index=False, float_format='%.10f')
    plt.rcParams.update({'font.size': 12})
    figure, axis = plt.subplots(figsize=(6, 4), layout='constrained', facecolor='white')
    axis.scatter(sample['gdp_pc'], sample['life_exp'], color='#21645a', alpha=0.8, edgecolor='white', linewidth=0.4)
    axis.set_xscale('log')
    axis.set(xlabel='GDP per person (inflation-adjusted US dollars; log axis)',
             ylabel='Life expectancy at birth (years)', title=f'Income and life expectancy · {year}')
    axis.grid(axis='y', alpha=0.25)
    figure.savefig(results / f'income-life-{year}.png', dpi=300, facecolor='white')
    plt.close(figure)
    notes = (f'Historical Gapminder teaching extract via Jennifer Bryan (CC0). Year: {year}. '
             f'N={len(sample)} complete country observations; equal country weights. '
             'Outcome: life expectancy at birth in years. Predictor: natural log of GDP per person '
             "in the extract's inflation-adjusted US dollars; base year unspecified. "
             'HC1 standard errors; t-based approximate 95% intervals. Association, not a causal estimate. '
             'Alt text: Scatter of country GDP per person on a log axis and life expectancy, '
             'with a broad positive association and substantial dispersion. '
             f'Environment: Python {platform.python_version()}, pandas {pd.__version__}, '
             f'statsmodels {statsmodels.__version__}.\n')
    (results / f'notes-{year}.txt').write_text(notes, encoding='utf-8')
    print(table.to_string(index=False))
    print('Results:', results)
    return table


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--year', type=int, default=2007, help='One of the observed five-year points, 1952–2007.')
    args = parser.parse_args()
    analyze(args.year)
