import sqlite3
import pandas as pd

bitcoin_csv = r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Bitcoin_historical_data_formatted.csv"
ethereum_csv = r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Ethereum_historical_data_formatted.csv"

df_bitcoin = pd.read_csv(bitcoin_csv)
df_ethereum = pd.read_csv(ethereum_csv)

conn = sqlite3.connect(r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\crypto_data.db")
cursor = conn.cursor()

def create_table_from_df(df, table_name):
    df.columns = [col.replace(" ", "_") for col in df.columns]
    columns = ", ".join([f"{col} TEXT" for col in df.columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
    df.to_sql(table_name, conn, if_exists="replace", index=False)

create_table_from_df(df_bitcoin, "Bitcoin")
create_table_from_df(df_ethereum, "Ethereum")

conn.commit()
conn.close()
