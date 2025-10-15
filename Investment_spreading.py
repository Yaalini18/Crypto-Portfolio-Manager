import pandas as pd
import numpy as np

btc = pd.read_csv(r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Bitcoin_historical_data_formatted.csv")
eth = pd.read_csv(r"C:\Users\Hp\OneDrive\Desktop\crypto_upload\Ethereum_historical_data_formatted.csv")

btc = btc[["timestamp", "close"]].rename(columns={"close": "BTC"})
eth = eth[["timestamp", "close"]].rename(columns={"close": "ETH"})

data = pd.merge(btc, eth, on="timestamp", how="inner").sort_values("timestamp")

returns = data[["BTC", "ETH"]].pct_change().dropna()
mean_returns = returns.mean()
volatility = returns.std()

equal_weights = pd.Series(1/len(mean_returns), index=mean_returns.index)







inv_vol = 1 / volatility
risk_parity_weights = inv_vol / inv_vol.sum()








sharpe_ratios = mean_returns / volatility
sharpe_weights = sharpe_ratios / sharpe_ratios.sum()

momentum_signal = returns.tail(5).mean()
momentum_weights = momentum_signal.clip(lower=0)
if momentum_weights.sum() > 0:
    momentum_weights = momentum_weights / momentum_weights.sum()
else:
    momentum_weights = pd.Series(1/len(momentum_signal), index=momentum_signal.index)

# print("Equal-Weight Rule:\n", equal_weights, "\n")
print("Risk-Parity Rule:\n", risk_parity_weights, "\n")
# print("Sharpe-Maximization Rule:\n", sharpe_weights, "\n")
# print("Momentum Rule:\n", momentum_weights, "\n")
