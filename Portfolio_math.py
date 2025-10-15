# m2p1
# Portofolio_math.py

# Assign weights for the portfolio
# Check if weights are assigned based on the rule.(mentioned in 1st september slide)
# Calculate portfolio return
# Calculate portfolio risk 


import sqlite3
import pandas as pd
from datetime import datetime
import numpy as np

bitcoin_csv = r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Bitcoin_historical_data_formatted.csv"
ethereum_csv = r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Ethereum_historical_data_formatted.csv"
db_path = r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Portfolio_math.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS Bitcoin (
    timeOpen TEXT, timeClose TEXT, timeHigh TEXT, timeLow TEXT,
    open REAL, high REAL, low REAL, close REAL,
    volume REAL, marketCap REAL, timestamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Ethereum (
    timeOpen TEXT, timeClose TEXT, timeHigh TEXT, timeLow TEXT,
    open REAL, high REAL, low REAL, close REAL,
    volume REAL, marketCap REAL, timestamp TEXT
)
""")

df_btc = pd.read_csv(bitcoin_csv)
df_eth = pd.read_csv(ethereum_csv)

df_btc.to_sql("Bitcoin", conn, if_exists="replace", index=False)
df_eth.to_sql("Ethereum", conn, if_exists="replace", index=False)


cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    created_at TEXT,
    expected_return REAL,
    expected_risk REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER,
    asset_name TEXT,
    weight REAL,
    FOREIGN KEY(portfolio_id) REFERENCES portfolio(id)
)
""")


b_close = df_btc.sort_values("timestamp")["close"].values
e_close = df_eth.sort_values("timestamp")["close"].values

br = np.diff(b_close)/b_close[:-1]
er = np.diff(e_close)/e_close[:-1]
n = min(len(br), len(er))
returns = np.vstack((br[-n:], er[-n:])).T

weights = np.array([0.6, 0.4])
mr = np.mean(returns, 0)
pr = np.dot(weights, mr)
c = np.cov(returns.T)
pv = np.dot(weights.T, np.dot(c, weights))
risk = np.sqrt(pv)

portfolio_name = "Crypto Portfolio"
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute("""
INSERT INTO portfolio (name, created_at, expected_return, expected_risk)
VALUES (?, ?, ?, ?)
""", (portfolio_name, created_at, pr, risk))
portfolio_id = cursor.lastrowid

assets = [("Bitcoin", 0.5), ("Ethereum", 0.5)]
for asset_name, weight in assets:
    cursor.execute("""
    INSERT INTO portfolio_assets (portfolio_id, asset_name, weight)
    VALUES (?, ?, ?)
    """, (portfolio_id, asset_name, weight))

conn.commit()
conn.close()

print("Database created and populated successfully!")
