import sqlite3
from datetime import datetime

conn = sqlite3.connect("portfolio.db")
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
conn.commit()

portfolio_name = "Crypto Portfolio"
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
expected_return = 0.12
expected_risk = 0.08

cursor.execute("""
INSERT INTO portfolio (name, created_at, expected_return, expected_risk)
VALUES (?, ?, ?, ?)
""", (portfolio_name, created_at, expected_return, expected_risk))

portfolio_id = cursor.lastrowid

assets = [
    ("Bitcoin", 0.5),
    ("Ethereum", 0.3),
    ("USDT", 0.2)
]

for asset_name, weight in assets:
    cursor.execute("""
    INSERT INTO portfolio_assets (portfolio_id, asset_name, weight)
    VALUES (?, ?, ?)
    """, (portfolio_id, asset_name, weight))
conn.commit()

cursor.execute("""
SELECT p.name, p.created_at, p.expected_return, p.expected_risk,
       a.asset_name, a.weight
FROM portfolio p
JOIN portfolio_assets a ON p.id = a.portfolio_id
""")

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
