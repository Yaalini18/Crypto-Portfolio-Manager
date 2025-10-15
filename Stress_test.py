import pandas as pd
import sqlite3
import numpy as np

# ---------- RULE SETTER ----------
def risk_parity_rule(returns):
    vols = returns.std()
    inv_vols = 1 / vols
    return inv_vols / inv_vols.sum()

# ---------- EXTENDED STRESS TEST DATA ----------
scenarios = {
    "Bull Market": pd.DataFrame({
        "BTC": [0.05, 0.04, 0.03, 0.06, 0.07, 0.05, 0.04, 0.03, 0.06, 0.05],
        "ETH": [0.04, 0.03, 0.02, 0.05, 0.06, 0.04, 0.03, 0.02, 0.05, 0.04],
        "LTC": [0.03, 0.02, 0.01, 0.04, 0.05, 0.03, 0.02, 0.01, 0.04, 0.03]
    }),
    "Bear Market": pd.DataFrame({
        "BTC": [-0.05, -0.04, -0.03, -0.06, -0.07, -0.05, -0.04, -0.03, -0.06, -0.05],
        "ETH": [-0.04, -0.03, -0.02, -0.05, -0.06, -0.04, -0.03, -0.02, -0.05, -0.04],
        "LTC": [-0.03, -0.02, -0.01, -0.04, -0.05, -0.03, -0.02, -0.01, -0.04, -0.03]
    }),
    "Volatile Market": pd.DataFrame({
        "BTC": [0.10, -0.10, 0.12, -0.08, 0.09, -0.07, 0.11, -0.06, 0.10, -0.09],
        "ETH": [0.08, -0.07, 0.09, -0.06, 0.07, -0.05, 0.08, -0.04, 0.09, -0.06],
        "LTC": [0.07, -0.05, 0.06, -0.04, 0.05, -0.03, 0.06, -0.02, 0.07, -0.04]
    })
}

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("Stress_Test.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio_returns (
    scenario TEXT,
    weights TEXT,
    mean_return REAL
)
""")

# ---------- CALCULATE & STORE ----------
for name, df in scenarios.items():
    weights = risk_parity_rule(df)
    portfolio_returns = df.dot(weights)
    mean_ret = portfolio_returns.mean()
    
    cursor.execute(
        "INSERT INTO portfolio_returns (scenario, weights, mean_return) VALUES (?, ?, ?)",
        (name, weights.to_json(), float(mean_ret))
    )
    print(f"Scenario: {name}")
    print("Weights:\n", weights.round(3))
    print("Mean Portfolio Return:", round(mean_ret, 4), "\n")

conn.commit()
conn.close()
