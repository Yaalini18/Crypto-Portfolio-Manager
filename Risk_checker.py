# -*- coding: utf-8 -*-
"""Risk_checker.ipynb
Automatically generated for BTC + ETH portfolio.
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""Global Configuration"""

DATABASE_FILE_PATH = 'crypto_data.db'
COINS_IN_PORTFOLIO = ['BTC', 'ETH']
MARKET_BENCHMARK = 'BTC'
BENCHMARK_PORTFOLIO_RULE = 'risk_level'

RISK_THRESHOLDS = {
    'Volatility': {'limit': 5.0, 'operator': '<='},
    'Sharpe Ratio': {'limit': 1.0, 'operator': '>='},
    'Max Drawdown': {'limit': -20.0, 'operator': '>='},
    'Sortino Ratio': {'limit': 1.0, 'operator': '>='},
    'Beta': {'limit': 1.2, 'operator': '<='},
    'Max Asset Weight': {'limit': 0.40, 'operator': '<='}
}

"""Email Alert Configuration"""
SENDER_EMAIL = "b1865741@gmail.com"               # ← Put your Gmail here
SENDER_PASSWORD = "yhey ndqt zyhx dszv"     # ← Put your Gmail App Password here
RECEIVER_EMAIL = "hariombalang@gmail.com"      # ← Receiver email

"""ANALYSIS & RISK CHECKING ENGINE"""

def assign_weights(market_caps):
    total = sum(market_caps.values())
    return {asset: cap / total for asset, cap in market_caps.items()}

def calculate_volatility(daily_returns):
    return daily_returns.std()

def calculate_sharpe_ratio(daily_returns):
    if daily_returns.std() == 0: return 0.0
    return (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)

def calculate_max_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def calculate_sortino_ratio(daily_returns):
    negative_returns = daily_returns[daily_returns < 0]
    downside_deviation = negative_returns.std()
    if np.isnan(downside_deviation) or downside_deviation == 0: return np.inf
    return (daily_returns.mean() / downside_deviation) * np.sqrt(252)

def calculate_beta(portfolio_returns, market_returns):
    covariance = np.cov(portfolio_returns, market_returns)[0, 1]
    market_variance = np.var(market_returns)
    return 0.0 if market_variance == 0 else covariance / market_variance

def check_max_asset_weight(weights):
    return max(weights.values())

def run_risk_checker():
    print("--- RUNNING ANALYSIS AND RISK CHECKS ---")
    btc = pd.read_csv("Bitcoin_historical_data_formatted.csv")
    eth = pd.read_csv("Ethereum_historical_data_formatted.csv")

    btc["timestamp"] = pd.to_datetime(btc["timestamp"])
    eth["timestamp"] = pd.to_datetime(eth["timestamp"])

    btc = btc[["timestamp","close","marketCap"]].rename(columns={"close":"BTC","marketCap":"btc_mcap"})
    eth = eth[["timestamp","close","marketCap"]].rename(columns={"close":"ETH","marketCap":"eth_mcap"})

    df = pd.merge(btc, eth, on="timestamp", how="inner").set_index("timestamp")
    returns_df = df[["BTC","ETH"]].pct_change().dropna()

    market_caps = {"BTC": df["btc_mcap"].iloc[-1], "ETH": df["eth_mcap"].iloc[-1]}
    weights = assign_weights(market_caps)

    portfolio_returns = (returns_df[list(weights.keys())] * pd.Series(weights)).sum(axis=1).dropna()
    market_returns = returns_df[MARKET_BENCHMARK].dropna()
    common_index = portfolio_returns.index.intersection(market_returns.index)

    metrics = {
        'Volatility': calculate_volatility(portfolio_returns),
        'Sharpe Ratio': calculate_sharpe_ratio(portfolio_returns),
        'Max Drawdown': calculate_max_drawdown(portfolio_returns),
        'Sortino Ratio': calculate_sortino_ratio(portfolio_returns),
        'Beta': calculate_beta(portfolio_returns[common_index], market_returns[common_index]),
        'Max Asset Weight': check_max_asset_weight(weights)
    }

    results, failed_rules = [], []
    for rule_name, value in metrics.items():
        threshold = RISK_THRESHOLDS[rule_name]['limit']
        operator = RISK_THRESHOLDS[rule_name]['operator']
        passed = eval(f"{value} {operator} {threshold}")
        status = "PASS" if passed else "FAIL"
        result_row = {
            'portfolio_name': BENCHMARK_PORTFOLIO_RULE,
            'rule_name': rule_name,
            'calculated_value': round(value, 4),
            'rule_check': f"{operator} {threshold}",
            'status': status,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        results.append(result_row)
        if not passed:
            failed_rules.append(result_row)

    print("\n--- Risk Assessment Summary ---")
    for res in results:
        print(f"Rule: {res['rule_name']:<18}, Status: {res['status']:<4}, Value: {res['calculated_value']:<8} (Rule: {res['rule_check']})")

    return results, failed_rules

def store_risk_results_in_db(results):
    if not results:
        print("No results to store in the database.")
        return
    print("\n--- Storing risk check results in the database... ---")
    conn = sqlite3.connect(DATABASE_FILE_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS risk_assessment (
                   portfolio_name TEXT,
                   rule_name TEXT,
                   calculated_value REAL,
                   rule_check TEXT,
                   status TEXT,
                   timestamp TEXT)""")
    cur.execute("DELETE FROM risk_assessment WHERE portfolio_name = ?", (results[0]['portfolio_name'],))
    data_to_insert = [tuple(res.values()) for res in results]
    cur.executemany("""INSERT INTO risk_assessment
                       (portfolio_name, rule_name, calculated_value, rule_check, status, timestamp)
                       VALUES (?, ?, ?, ?, ?, ?)""", data_to_insert)
    conn.commit()
    conn.close()
    print("Successfully stored risk assessment results.")

def send_email_alert(failed_rules):
    if not failed_rules:
        return

    subject = "ALERT: Portfolio Risk Rule Violation Detected"
    body = "The following risk rules have failed:\n\n"
    for failure in failed_rules:
        body += (f"  - Rule: {failure['rule_name']}\n"
                 f"    Condition: {failure['rule_check']}\n"
                 f"    Actual Value: {failure['calculated_value']}\n\n")

    msg = MIMEMultipart()
    msg['From'], msg['To'], msg['Subject'] = SENDER_EMAIL, RECEIVER_EMAIL, subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"  > ERROR: Failed to send email. Reason: {e}")

"""MAIN EXECUTION BLOCK"""

if __name__ == "__main__":
    all_results, failed_rules_list = run_risk_checker()
    store_risk_results_in_db(all_results)
    if failed_rules_list:
        send_email_alert(failed_rules_list)
    else:
        print("\nAll risk rules passed. No alert necessary.")
    print("\n--- RISK CHECKER COMPLETE ---")
