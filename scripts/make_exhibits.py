"""Builds the empirical exhibits of the paper (Exhibits 10 and 11) from data/etf_adjclose_monthly.csv.

Usage: python3 make_exhibits.py
Writes outputs/results.json (every number behind Exhibits 10 and 11 and the statements made
about them in the text), outputs/gain_of_capital.csv (the realized and implied gain of
capital for every fund, horizon and start month) and figures/Fig-11_realized_gain_horizons.png
(Exhibit 11; not tracked in the repository).
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data", "etf_adjclose_monthly.csv")
OUT = os.path.join(BASE, "outputs")
FIG = os.path.join(BASE, "figures")
os.makedirs(OUT, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

TICKERS = ["SPY", "QQQ", "IWM"]
NAMES = {"SPY": "S&P 500", "QQQ": "NASDAQ-100", "IWM": "Russell 2000"}
HORIZONS = [6, 12, 24, 36]              # months
SAMPLE = ("2000-01", "2023-12")         # first and last month-end price used
COLORS = {"SPY": "tab:blue", "QQQ": "tab:green", "IWM": "tab:red"}
plt.rcdefaults()
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})

prices = pd.read_csv(DATA, index_col=0, parse_dates=True).loc[SAMPLE[0]:SAMPLE[1], TICKERS]
res = {"sample": {"first_month": SAMPLE[0], "last_month": SAMPLE[1], "horizons_months": HORIZONS}}

# ---------- Exhibit 10: cost of capital = geometric mean annual return over the sample ----------
cost, e10 = {}, {}
for tk in TICKERS:
    p = prices[tk].dropna()
    n = len(p) - 1                                        # months between first and last price
    cost[tk] = (p.iloc[-1] / p.iloc[0]) ** (12 / n) - 1
    e10[tk] = {
        "index": NAMES[tk],
        "first_month": p.index[0].strftime("%Y-%m"),
        "last_month": p.index[-1].strftime("%Y-%m"),
        "months": n,
        "cost_of_capital_pct": round(cost[tk] * 100, 2),
    }
res["exhibit10_cost_of_capital"] = e10

# ---------- Gain of capital: Equations (20) and (21) ----------
# realized:  g = P_T / P_t - (1 + c)^(T - t)
# implied:   g = P_T / (P_t (1 + c)^(T - t)) - 1
rows = []
for tk in TICKERS:
    p = prices[tk].dropna()
    for h in HORIZONS:
        C = (1 + cost[tk]) ** (h / 12)
        R = (p.shift(-h) / p).dropna()                    # P_T / P_t, indexed by the start month t
        rows.append(pd.DataFrame({"date": R.index, "ticker": tk, "horizon_months": h,
                                  "g_realized": R.values - C, "g_implied": R.values / C - 1}))
g = pd.concat(rows, ignore_index=True)
out = g.copy()
out["date"] = out["date"].dt.strftime("%Y-%m")
out.to_csv(os.path.join(OUT, "gain_of_capital.csv"), index=False, float_format="%.6f", lineterminator="\n")

# ---------- Exhibit 11: summary of the realized gain, by horizon and fund ----------
e11 = {}
for h in HORIZONS:
    e11[f"{h}m"] = {}
    for tk in TICKERS:
        x = g[(g.ticker == tk) & (g.horizon_months == h)].set_index("date")["g_realized"]
        s = np.sign(x)
        e11[f"{h}m"][tk] = {
            "observations": int(len(x)),
            "first_start_month": x.index[0].strftime("%Y-%m"),
            "last_start_month": x.index[-1].strftime("%Y-%m"),
            "mean": round(float(x.mean()), 4),
            "std": round(float(x.std()), 4),
            "min": round(float(x.min()), 4),
            "min_start_month": x.idxmin().strftime("%Y-%m"),
            "max": round(float(x.max()), 4),
            "max_start_month": x.idxmax().strftime("%Y-%m"),
            "share_abs_above_20pp": round(float((x.abs() > 0.20).mean()), 4),
            "share_positive": round(float((x > 0).mean()), 4),
            "share_positive_starts_2000_2002": round(float((x.loc["2000":"2002"] > 0).mean()), 4),
            "share_positive_starts_2010_2018": round(float((x.loc["2010":"2018"] > 0).mean()), 4),
            "autocorrelation_lag1": round(float(x.autocorr(1)), 4),
            "sign_changes": int((s != s.shift()).iloc[1:].sum()),
        }
    sd = {tk: e11[f"{h}m"][tk]["std"] for tk in TICKERS}
    e11[f"{h}m"]["dispersion"] = {"QQQ_over_SPY": round(sd["QQQ"] / sd["SPY"], 4),
                                  "IWM_over_SPY": round(sd["IWM"] / sd["SPY"], 4)}
res["exhibit11_realized_gain"] = e11

# ---------- Proposition 6: implied = realized / (1 + c)^(T - t), identically ----------
C = g.apply(lambda r: (1 + cost[r.ticker]) ** (r.horizon_months / 12), axis=1)
gap = float((g.g_implied - g.g_realized / C).abs().max())
assert gap < 1e-12, gap
res["proposition6_proportionality"] = {
    "observations": int(len(g)),
    "max_abs_deviation_below_1e-12": True,
    "implied_over_realized": {tk: {f"{h}m": round((1 + cost[tk]) ** (-h / 12), 4) for h in HORIZONS} for tk in TICKERS},
}

with open(os.path.join(OUT, "results.json"), "w") as f:
    json.dump(res, f, indent=1)
    f.write("\n")

# ---------- Exhibit 11: figure ----------
fig, axes = plt.subplots(4, 1, figsize=(7.6, 8.8), sharex=True)
for ax, h in zip(axes, HORIZONS):
    for tk in TICKERS:
        x = g[(g.ticker == tk) & (g.horizon_months == h)]
        ax.plot(x.date, x.g_realized, color=COLORS[tk], lw=0.9, label=tk)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_title(f"{h}-Month Horizon", fontsize=8)
    ax.set_ylabel(r"$g^{\mathrm{realized}}_{t,T}$")
    ax.grid(True, alpha=0.4)
axes[0].legend(loc="upper right", ncol=3, fontsize=7)
axes[-1].set_xlabel("Date $t$")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Fig-11_realized_gain_horizons.png"), dpi=200)
plt.close(fig)

print("Exhibit 10:", {tk: f"{v['cost_of_capital_pct']:.2f}%" for tk, v in e10.items()})
print("Exhibit 11: std of realized gain", {h: {tk: e11[h][tk]["std"] for tk in TICKERS} for h in e11})
