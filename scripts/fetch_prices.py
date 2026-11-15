"""Downloads the price file from Yahoo Finance. Documentation only: run_all.sh does not call it.

Usage: pip install yfinance; python3 fetch_prices.py [output.csv]
This is how data/etf_adjclose_monthly.csv was retrieved on March 27, 2025. Yahoo rescales
adjusted closing prices after every distribution, so a new download returns different price
levels (and, through rounding, slightly different returns) from the stored file. The paper's
numbers are those of the stored file; this script writes to a separate file by default.
"""
import sys

import yfinance as yf

out = sys.argv[1] if len(sys.argv) > 1 else "etf_adjclose_monthly_new.csv"
data = yf.download(["SPY", "QQQ", "IWM"], start="1998-01-01", end="2024-12-31",
                   interval="1mo", auto_adjust=False, group_by="ticker")
adj = data.xs("Adj Close", level=1, axis=1).dropna(how="all")[["IWM", "QQQ", "SPY"]]
adj.to_csv(out)
print(f"Saved {len(adj)} monthly rows to {out}")
