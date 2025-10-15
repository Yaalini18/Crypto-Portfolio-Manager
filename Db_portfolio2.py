import sqlite3
import pandas as pd
from datetime import datetime
import numpy as np

bitcoin_csv = r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Bitcoin_historical_data_formatted.csv"
ethereum_csv = r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Ethereum_historical_data_formatted.csv"
db_path = r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Db_portfolio2.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

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

df_btc = pd.read_csv(bitcoin_csv).sort_values("timestamp")
df_eth = pd.read_csv(ethereum_csv).sort_values("timestamp")

b_close = df_btc["close"].values
e_close = df_eth["close"].values

br = np.diff(b_close)/b_close[:-1]
er = np.diff(e_close)/e_close[:-1]
n = min(len(br), len(er))
returns = np.vstack((br[-n:], er[-n:])).T

weights_list = [
    [0.6, 0.4],
    [0.5, 0.5],
    [0.7, 0.3],
    [0.4, 0.6],
    [0.3, 0.7],
    [0.65, 0.35],
    [0.55, 0.45],
    [0.45, 0.55],
    [0.35, 0.65],
    [0.2, 0.8]
]

for i, w in enumerate(weights_list, 1):
    w = np.array(w)
    mr = np.mean(returns, 0)
    pr = np.dot(w, mr)
    c = np.cov(returns.T)
    pv = np.dot(w.T, np.dot(c, w))
    risk = np.sqrt(pv)
    
    portfolio_name = f"Crypto Portfolio {i}"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
    INSERT INTO portfolio (name, created_at, expected_return, expected_risk)
    VALUES (?, ?, ?, ?)
    """, (portfolio_name, created_at, pr, risk))
    
    portfolio_id = cursor.lastrowid
    assets = [("Bitcoin", w[0]), ("Ethereum", w[1])]
    
    for asset_name, weight in assets:
        cursor.execute("""
        INSERT INTO portfolio_assets (portfolio_id, asset_name, weight)
        VALUES (?, ?, ?)
        """, (portfolio_id, asset_name, weight))

conn.commit()
conn.close()

print("10 portfolios created and stored successfully in Db_portfolio2.db!")
