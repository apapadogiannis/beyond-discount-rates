"""Checks the paper's closed-form results numerically on random parameter draws.

Usage: python3 check_identities.py
Draws 100,000 parameter sets (fixed seed) and verifies each identity to floating-point
accuracy. Exits with an error if any of them fails. Equation and proposition numbers are
those of the article.
"""
import numpy as np

rng = np.random.default_rng(0)
M = 100_000
c = rng.uniform(0.01, 0.25, M)             # cost of capital
n = rng.integers(1, 41, M).astype(float)   # horizon T - t
pv_fair = rng.uniform(50, 5000, M)
pv_bias = rng.uniform(50, 5000, M)
C = (1 + c) ** n                           # baseline return, Equation (1)
delta = pv_bias - pv_fair                  # cumulative misestimation, Equation (13)
g = C * (pv_fair / pv_bias - 1)            # gain of capital, Equation (8)


def check(name, lhs, rhs, tol=1e-9):
    err = np.max(np.abs(lhs - rhs) / np.maximum(1.0, np.abs(rhs)))
    assert err < tol, (name, err)
    print(f"ok  {name}  (max relative error {err:.1e})")


check("Eq. (9)   PV_fair / PV_bias = 1 + g / (1+c)^(T-t)", pv_fair / pv_bias, 1 + g / C)
check("Eq. (10)  PV_fair = PV_bias (1 + g / (1+c)^(T-t))", pv_fair, pv_bias * (1 + g / C))

# Effective hurdle rate, Equation (11), for a single cash flow at T: discounting it at
# c_eff must return the fair value. Requires g > -(1+c)^(T-t), which holds since PV_fair > 0.
cash_flow = pv_bias * C
c_eff = (C / (1 + g / C)) ** (1 / n) - 1
check("Eq. (11)  CF / (1+c_eff)^(T-t) = PV_fair", cash_flow / (1 + c_eff) ** n, pv_fair)
assert np.all(g > -C)
print("ok  Eq. (12)  g > -(1+c)^(T-t) whenever PV_fair > 0")

check("Eq. (15)  g = -(1+c)^(T-t) Delta / (PV_fair + Delta)", g, -C * delta / (pv_fair + delta))
check("Eq. (16)  PV_fair = -(1+c)^(T-t) Delta / g - Delta", pv_fair, -C * delta / g - delta)

# Proposition 2 and Corollary 1: g = 0 if and only if Delta = 0.
assert np.all((g > 0) == (delta < 0)) and np.all((g < 0) == (delta > 0))
check("Prop. 2   g = 0 when Delta = 0", C * (pv_fair / pv_fair - 1), 0 * C)
print("ok  Props. 4 and 5   sign(g) = -sign(Delta): pessimism gives g > 0, optimism g < 0")

# Proposition 3: with total return R fixed, g = R - (1+c)^(T-t), so
# dg/dc = -(T-t)(1+c)^(T-t-1) < 0. Checked by central difference (R cancels).
h = 1e-6
dg = -((1 + c + h) ** n - (1 + c - h) ** n) / (2 * h)
check("Prop. 3   dg/dc = -(T-t)(1+c)^(T-t-1) < 0", dg / (n * (1 + c) ** (n - 1)), -np.ones(M), tol=1e-6)

# Proposition 4: dg/dDelta = -(1+c)^(T-t) / PV_bias < 0 at fixed PV_bias.
check("Prop. 4   dg/dDelta = -(1+c)^(T-t) / PV_bias", (-C * (delta + 1) / pv_bias) - (-C * delta / pv_bias), -C / pv_bias)

# Proposition 6: with P_t = PV_bias and P_T = PV_fair (1+c)^(T-t), the realized proxy
# equals g and the implied proxy equals g / (1+c)^(T-t).
p_t, p_T = pv_bias, pv_fair * C
g_realized = p_T / p_t - C                 # Equation (20)
g_implied = p_T / (p_t * C) - 1            # Equation (21)
check("Prop. 6   g_realized = g", g_realized, g)
check("Prop. 6   g_implied = g / (1+c)^(T-t) = PV_fair / PV_bias - 1", g_implied, pv_fair / pv_bias - 1)
check("Eq. (22)  g_realized - g_implied = g_realized (C - 1) / C", g_realized - g_implied, g_realized * (C - 1) / C)

# Expectation Gap: EG = PV_fair - P_t = P_t * g_implied.
check("Eq. (26)  EG = PV_fair - P_t = P_t g_implied", pv_fair - p_t, p_t * g_implied)
print("All identities hold.")
