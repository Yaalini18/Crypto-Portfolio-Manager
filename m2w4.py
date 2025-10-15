import pandas as pd
import matplotlib.pyplot as plt

data = {
    'timestamp': pd.date_range(start='2025-01-01', periods=5, freq='D'),
    'bitcoin_close': [50000, 51000, 50500, 51500, 52000],
    'ethereum_close': [3000, 3100, 3050, 3150, 3200]
}

df = pd.DataFrame(data)
df['bitcoin_return'] = df['bitcoin_close'].pct_change()
df['ethereum_return'] = df['ethereum_close'].pct_change()
df['portfolio_return'] = 0.5 * df['bitcoin_return'] + 0.5 * df['ethereum_return']
df['bitcoin_cum_return'] = (1 + df['bitcoin_return']).cumprod()
df['ethereum_cum_return'] = (1 + df['ethereum_return']).cumprod()
df['portfolio_cum_return'] = (1 + df['portfolio_return']).cumprod()

plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['bitcoin_cum_return'], label='Bitcoin Cumulative Return')
plt.plot(df['timestamp'], df['ethereum_cum_return'], label='Ethereum Cumulative Return')
plt.plot(df['timestamp'], df['portfolio_cum_return'], label='Portfolio Cumulative Return', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.title('Portfolio vs Single Asset Returns')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Insights:")
print("- Portfolio return smooths out fluctuations compared to individual assets.")
print("- Diversification reduces risk and improves stability.")

df.to_csv('m2w4.csv', index=False)
print("Data exported to portfolio_vs_assets_returns.csv")
