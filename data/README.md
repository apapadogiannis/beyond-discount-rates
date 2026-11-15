# Data

The file used by the scripts, with its source, retrieval date and the terms stated by the
source. Third-party data remain the property of their sources and are redistributed here
for replication only, with attribution.

| File | Content | Source | Retrieved | Terms |
|---|---|---|---|---|
| `etf_adjclose_monthly.csv` | Monthly adjusted closing prices (US dollars) of three exchange-traded funds: SPDR S&P 500 ETF Trust (SPY), Invesco QQQ Trust (QQQ) and iShares Russell 2000 ETF (IWM), January 1998 to December 2024, as downloaded | Yahoo Finance, https://finance.yahoo.com, through the `yfinance` Python package (`scripts/fetch_prices.py`) | March 27, 2025 | Yahoo terms of service apply; no open license. The figures are fund prices adjusted for splits and distributions, reproduced here with attribution |

## Notes

- Each row is one month. The date is the first day of the month; the value is the adjusted
  close on the last trading day of that month. The row `2000-01-01` is therefore the price
  at the end of January 2000.
- Adjusted closing prices include reinvested distributions, so price ratios are total
  returns.
- The article uses the rows from `2000-01-01` to `2023-12-01`. The file is kept as
  downloaded; the earlier and later rows are not used.
- QQQ begins in March 1999 and IWM in May 2000 (the fund was launched on May 22, 2000), so
  their earlier cells are empty. The IWM sample is correspondingly shorter.
- Yahoo rescales the whole adjusted series after every distribution. A new download gives
  different price levels and, through rounding, slightly different returns. The numbers in
  the article are those of this file.
