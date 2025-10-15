import pandas as pd
import mysql.connector


csv_file = r"C:\Users\Hp\OneDrive\Desktop\exm1\Ethereum_historical_data_formatted.csv"
df = pd.read_csv(csv_file)
df.columns = [col.strip() for col in df.columns]


numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'marketCap']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')


datetime_cols = ['timeOpen', 'timeClose', 'timeHigh', 'timeLow', 'timestamp']
for col in datetime_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()


cursor.execute("CREATE DATABASE IF NOT EXISTS crypto_db")
cursor.execute("USE crypto_db")
cursor.execute("DROP TABLE IF EXISTS ethereum_prices")
cursor.execute("""
    CREATE TABLE ethereum_prices (
        timeOpen DATETIME,
        timeClose DATETIME,
        timeHigh DATETIME,
        timeLow DATETIME,
        open DECIMAL(18,2),
        high DECIMAL(18,2),
        low DECIMAL(18,2),
        close DECIMAL(18,2),
        volume BIGINT,
        marketCap DECIMAL(20,2),
        timestamp DATETIME PRIMARY KEY
    )
""")


for _, row in df.iterrows():
    cursor.execute("""
        REPLACE INTO ethereum_prices 
        (timeOpen, timeClose, timeHigh, timeLow, open, high, low, close, volume, marketCap, timestamp)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row['timeOpen'],
        row['timeClose'],
        row['timeHigh'],
        row['timeLow'],
        row['open'],
        row['high'],
        row['low'],
        row['close'],
        int(row['volume']) if not pd.isna(row['volume']) else None,
        row['marketCap'],
        row['timestamp']
    ))


conn.commit()
cursor.close()
conn.close()
print("Ethereum data uploaded successfully!")
