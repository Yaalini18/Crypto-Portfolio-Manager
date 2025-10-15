import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime, timezone
from pathlib import Path

DATA_PATHS = {
    "BTC": Path(r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Bitcoin_historical_data_formatted.csv"),
    "ETH": Path(r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Ethereum_historical_data_formatted.csv")
}

def load_data():
    df = pd.DataFrame()
    found = False
    for asset, path in DATA_PATHS.items():
        if path.exists():
            tmp = pd.read_csv(path)
            close_col = [col for col in tmp.columns if col.lower() == "close"]
            if close_col:
                prices = pd.to_numeric(tmp[close_col[0]], errors="coerce").ffill().fillna(0)
            else:
                numeric_cols = tmp.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    prices = pd.to_numeric(tmp[numeric_cols[0]], errors="coerce").ffill().fillna(0)
                else:
                    continue
            df[f"{asset}_pct_change"] = prices.pct_change().fillna(0)
            found = True

    if not found:
        rng = np.random.RandomState(42)
        n = 2000
        df = pd.DataFrame({
            "BTC_pct_change": rng.normal(0, 1, size=n).cumsum(),
            "ETH_pct_change": rng.normal(0, 1.2, size=n).cumsum()
        })
    df["Portfolio_pct_change"] = df.mean(axis=1)
    return df

def train_and_predict_series(series, label):
    y = np.asarray(series).astype(float)
    N = len(y)
    if N == 0:
        return None
    X_full = np.arange(N).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X_full, y)
    y_pred_full = model.predict(X_full)
    mse = mean_squared_error(y, y_pred_full)
    r2 = r2_score(y, y_pred_full)
    last_n = min(10, N)
    return {
        "label": label,
        "mse": mse,
        "r2": r2,
        "actual_last": y[-last_n:].tolist(),
        "pred_last": y_pred_full[-last_n:].tolist()
    }

def run_all_predictions(df):
    results = {}
    summary_rows = []
    for col in df.columns:
        if col.endswith("_pct_change"):
            res = train_and_predict_series(df[col].fillna(0), col)
            if res:
                results[col] = res
                summary_rows.append([col, res["mse"], res["r2"]])
    summary_df = pd.DataFrame(summary_rows, columns=["Asset", "MSE", "R²"])
    print("\nPrediction Summary\n")
    print(summary_df.to_string(index=False))
    print("\nDetailed Predictions\n")
    for asset, res in results.items():
        df_display = pd.DataFrame({
            "Actual": np.round(res["actual_last"], 6),
            "Predicted": np.round(res["pred_last"], 6)
        })
        print(f"{asset}")
        print(df_display)
        print()
    return results

def store_predictions(results, db_path="crypto.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, asset TEXT, mse REAL, r2 REAL, ts TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS prediction_rows
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, asset TEXT, actual REAL, predicted REAL, ts TIMESTAMP)""")
    for asset, vals in results.items():
        c.execute("INSERT INTO predictions(asset, mse, r2, ts) VALUES (?, ?, ?, ?)",
                  (asset, vals["mse"], vals["r2"], datetime.now(timezone.utc).isoformat()))
        for a, p in zip(vals["actual_last"], vals["pred_last"]):
            c.execute("INSERT INTO prediction_rows(asset, actual, predicted, ts) VALUES (?, ?, ?, ?)",
                      (asset, float(a), float(p), datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Loading data...")
    df = load_data()
    print("\nSample Daily Returns:")
    print(df.head())

    print("\nRunning predictions...")
    results = run_all_predictions(df)

    if results:
        print("Storing predictions to database...")
        store_predictions(results)

    print("Done.")
