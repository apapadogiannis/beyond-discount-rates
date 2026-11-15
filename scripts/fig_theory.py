"""Draws the three analytical figures of the paper (Exhibits 4, 5 and 6) from the model's equations.

Usage: python3 fig_theory.py
Writes figures/Fig-2_gain_vs_delta.png (Exhibit 4), figures/Fig-3_pessimistic_misestimation.png
(Exhibit 5) and figures/Fig-1_pv_fair_vs_gain.png (Exhibit 6). No data are used; the figure
files are not tracked in the repository.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "figures")
os.makedirs(FIG, exist_ok=True)

plt.rcdefaults()
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})

PV_BIAS = 1000                       # biased present value
N = 10                               # horizon T - t, in years
C_VALUES = [0.05, 0.10, 0.15, 0.20]  # cost of capital

# ---------- Exhibit 4 (Fig-2): gain of capital against cumulative misestimation ----------
# g = -(1 + c)^(T - t) * Delta / PV_bias                                   Equation (15)
delta = np.linspace(-90, 90, 200)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
for c in C_VALUES:
    ax.plot(delta, -(1 + c) ** N * delta / PV_BIAS, lw=1.6, label=rf"$c_{{t,T}}$ = {c}")
ax.set_xlabel(r"Cash Flow Misestimation $\Delta_{t}$")
ax.set_ylabel(r"Gain of Capital $g_{t,T}$")
ax.set_title(rf"Fig-2: Sensitivity of $g_{{t,T}}$ to $\Delta_{{t}}$ ($PV_{{bias}}$={PV_BIAS}, T-t={N})", fontsize=9)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.4)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Fig-2_gain_vs_delta.png"), dpi=150)
plt.close(fig)

# ---------- Exhibit 5 (Fig-3): feasible range of pessimistic misestimation ----------
# PV_fair = PV_bias - Delta                                                Equation (14)
c = 0.05
delta = np.linspace(-1500, 500, 400)
fig, axs = plt.subplots(2, 1, figsize=(6.4, 6.2), sharex=False)
axs[0].plot(delta, PV_BIAS - delta, color="blue", lw=1.6)
axs[0].set_ylabel(r"$PV_{fair}$")
axs[0].set_title("Fig-3: Value Preservation Under Pessimistic Cash Flow Misestimation", fontsize=9)
axs[1].plot(delta, -(1 + c) ** N * delta / PV_BIAS, color="green", lw=1.6)
axs[1].set_xlabel(r"Cumulative Misestimation $\Delta_{t}$")
axs[1].set_ylabel(r"Gain of Capital $g_{t,T}$")
axs[1].set_ylim(-1, 3)
for ax in axs:
    ax.axvspan(-PV_BIAS, 0, color="gray", alpha=0.25)
    ax.axvline(-PV_BIAS, color="red", ls="--", lw=1.6)
    ax.axvline(0, color="red", ls="--", lw=1.6)
    ax.grid(True, alpha=0.4)
axs[0].legend(handles=[
    Line2D([0], [0], color="blue", lw=1.6, label=r"$PV_{fair} = PV_{bias} - \Delta_{t}$"),
    Patch(facecolor="gray", edgecolor="gray", alpha=0.25, label="Moderately Pessimistic Region"),
    Line2D([0], [0], color="red", lw=1.6, ls="--", label=r"$\Delta_{t} = -PV_{bias}$ or 0"),
], loc="lower center", fontsize=7)
fig.suptitle(rf"Parameters: $PV_{{bias}}$={PV_BIAS}, $c_{{t,T}}$={c}, $T-t$={N}", fontsize=8)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(FIG, "Fig-3_pessimistic_misestimation.png"), dpi=150)
plt.close(fig)

# ---------- Exhibit 6 (Fig-1): fair value against the gain of capital ----------
# PV_fair = PV_bias * (1 + g / (1 + c)^(T - t))                            Equation (10)
gain = np.linspace(-100, 150, 200)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
for c in C_VALUES:
    ax.plot(gain, PV_BIAS * (1 + gain / (1 + c) ** N), lw=1.6, label=rf"$c_{{t,T}}$ = {c}")
ax.set_xlabel(r"Gain of Capital $g_{t,T}$")
ax.set_ylabel(r"Fair Valuation $PV_{fair}$")
ax.set_title(rf"Fig-1: Sensitivity of $PV_{{fair}}$ to $g_{{t,T}}$ ($PV_{{bias}}$={PV_BIAS}, Horizon={N})", fontsize=9)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.4)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "Fig-1_pv_fair_vs_gain.png"), dpi=150)
plt.close(fig)
print("Exhibits 4, 5 and 6 written to figures/")
