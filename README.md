# Beyond Discount Rates: A Valuation Framework for Unpriced Systematic Risk

[![Zenodo](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.24243060-007ec6)](https://doi.org/10.5281/zenodo.24243060)
[![SSRN](https://img.shields.io/badge/SSRN-10.2139%2Fssrn.5180040-1f4e79)](https://doi.org/10.2139/ssrn.5180040)
[![replication](https://github.com/apapadogiannis/beyond-discount-rates/actions/workflows/replicate.yml/badge.svg)](https://github.com/apapadogiannis/beyond-discount-rates/actions/workflows/replicate.yml)

Replication package for the article by Agisilaos Papadogiannis, forthcoming in *The Journal of Investing* (2027).
Title and abstract: `paper/abstract.pdf`; also on SSRN: [doi:10.2139/ssrn.5180040](https://doi.org/10.2139/ssrn.5180040).
Archived on Zenodo: [doi:10.5281/zenodo.24243060](https://doi.org/10.5281/zenodo.24243060) (v1.0).
The article is copyright PMR and its text is not distributed here; this repository holds the code and the data behind its figures and empirical exhibits, so that every reported number can be reproduced.

## What this is

This paper introduces a dual-risk valuation framework that extends traditional discounted
cash flow (DCF) analysis by decomposing expected return into a market-based cost of capital
and a belief-driven gain of capital. By embedding expectation error directly into the DCF
identity, the framework captures return premiums that arise from the persistent
misestimation of future cash flows. We derive closed-form valuation expressions integrating
both return components and introduce an effective hurdle rate for unified discounting. For
empirical implementation, the model constructs two price-based proxies for the gain of
capital: a realized gain, which recovers the theoretical gain exactly, and an implied gain,
its valuation-space counterpart, which we prove to be exactly proportional to it. Applied
to U.S. equity indices (SPY, QQQ, IWM) from 2000 to 2023, the realized gain of capital is
large, persistent, and regime-dependent, exhibiting decade-scale sign regimes that no
constant discount rate can generate. This framework provides a principled method for
financial practitioners to dynamically adjust project hurdle rates, diagnose valuation
asymmetries, and systematically incorporate expectation risk into capital budgeting
decisions.

## Layout

```
scripts/    the code (see below)
data/       the input data, with source and terms in data/README.md
outputs/    results.json: every number behind Exhibits 10 and 11
            gain_of_capital.csv: the realized and implied gain for every fund, horizon and month
paper/      title and abstract of the article (PDF and LaTeX source); the full text is not included
```

## Reproducing

Requirements: Python 3.11+, `pip install -r requirements.txt` (pandas, numpy, matplotlib).
`requirements-lock.txt` lists the exact versions under which the files in `outputs/` were
generated.

```bash
git clone https://github.com/apapadogiannis/beyond-discount-rates
cd beyond-discount-rates
pip install -r requirements.txt
./run_all.sh    # a few seconds
```

The scripts are deterministic and use only the files in `data/`; nothing is downloaded.
Re-running them reproduces `outputs/results.json` and `outputs/gain_of_capital.csv` and
writes the four figures (`figures/`), which are generated locally and not tracked. A GitHub
Actions workflow re-runs the pipeline on every push and once a month and fails if either output file differs
from the committed one.

| Script | What it produces | Where it appears |
|---|---|---|
| `check_identities.py` | Numerical check of the closed-form results on 100,000 random parameter draws | Equations 8 to 16, 22 and 26; Propositions 2 to 6 |
| `make_exhibits.py` | Annual cost of capital of each fund: geometric mean return over the sample | Exhibit 10 |
| | Realized gain of capital at the 6-, 12-, 24- and 36-month horizons (figure and summary statistics) | Exhibit 11 |
| | Implied gain of capital and its exact proportionality to the realized gain | Equation 21, Proposition 6 |
| `fig_theory.py` | Gain of capital against cumulative misestimation | Exhibit 4 |
| | Feasible range of pessimistic misestimation | Exhibit 5 |
| | Fair value against the gain of capital, by discount rate | Exhibit 6 |
| `fetch_prices.py` | How the price file was retrieved (documentation; not run by `run_all.sh`) | |

Exhibits 1 to 3 and 7 to 9 of the article are tables and a flow diagram and have no code.

### Definitions

For a fund with month-end adjusted closing prices $P_t$, an annual cost of capital $c$ and a
horizon of $h$ months, with $C = (1+c)^{h/12}$:

$$g^{\text{realized}}_{t,T} = \frac{P_T}{P_t} - C, \qquad g^{\text{implied}}_{t,T} = \frac{P_T}{P_t\,C} - 1 = \frac{g^{\text{realized}}_{t,T}}{C}.$$

The sample runs from the end of January 2000 to the end of December 2023 (287 monthly
returns for SPY and QQQ; 283 for IWM, whose series begins in May 2000). The cost of capital
of each fund is $(P_{\text{last}}/P_{\text{first}})^{12/n} - 1$ over its own sample, with
$n$ the number of months: 7.18% for SPY, 7.25% for QQQ and 7.69% for IWM. Every start month
$t$ for which $T$ falls inside the sample is used.

The keys of `outputs/results.json` are named after the exhibits
(`exhibit10_cost_of_capital`, `exhibit11_realized_gain`, `proposition6_proportionality`).
For each fund and horizon, `exhibit11_realized_gain` gives the number of observations, the
mean, standard deviation, minimum and maximum of the realized gain, the share of months in
which it exceeds 20 percentage points in absolute value, the share of positive months
(overall, for start months in 2000 to 2002 and in 2010 to 2018), the first-order
autocorrelation, the number of sign changes, and the dispersion of QQQ and IWM relative
to SPY.

## How the check works

1. `outputs/results.json` and `outputs/gain_of_capital.csv` are stored in this repository exactly as they were when the
   article's numbers were taken from them.
2. `./run_all.sh` reruns every script on the files in `data/` and overwrites those files with
   freshly computed ones.
3. `git diff --exit-code -- outputs/results.json outputs/gain_of_capital.csv` then compares each fresh file with the
   stored version, character by character. If nothing is printed, they are identical; any
   difference is listed and counts as a failure.

The workflow behind the badge does exactly these three steps on a new machine with the pinned
package versions, on every push and once a month, so a green badge means the stored
files still follow from the data and code. The stored files are also frozen in the Zenodo
archive, which cannot be altered after release.

Two limits. The comparison is between regenerated and stored files, not with the article's
PDF: to connect the two, use the script table above, which says where each output appears in
the article. And the figures and LaTeX table bodies are written locally from the same values but are
not stored here, so they are not part of the comparison.

## Data and licensing

The single input file is `data/etf_adjclose_monthly.csv`: monthly adjusted closing prices
of SPY, QQQ and IWM from Yahoo Finance, retrieved on March 27, 2025. `data/README.md` gives
the details and the terms. The file is stored in the repository because Yahoo rescales
adjusted prices after every distribution, so a later download does not return the same
numbers.

Third-party data remain the property of their sources and are included for replication
only, with attribution; they are not covered by the license of this repository.
Code: MIT License. `outputs/results.json` and `outputs/gain_of_capital.csv`: CC BY 4.0, cite the article.

## Citation

> Papadogiannis, A. (2027). "Beyond discount rates: A valuation framework for unpriced
> systematic risk." *The Journal of Investing*, forthcoming.
> SSRN: https://doi.org/10.2139/ssrn.5180040

Code and data:

> Papadogiannis, A. (2026). "Beyond discount rates: A valuation framework for unpriced systematic risk. Replication package." Zenodo.
> https://doi.org/10.5281/zenodo.24243060

## Disclaimer

Independent research; no funding, no institutional position. Not investment advice.
