
# m2p4
# Compare portfolio return vs. single asset return with some sample data
# Plot the graphs, Draw some insights.
# Export to csv


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
dates = pd.date_range(start='2025-01-01', periods=100, freq='D')
bitcoin_prices = 50000 + np.cumsum(np.random.randn(100) * 500)
ethereum_prices = 3000 + np.cumsum(np.random.randn(100) * 50)

df = pd.DataFrame({
    'timestamp': dates,
    'bitcoin_close': bitcoin_prices,
    'ethereum_close': ethereum_prices
})

df['bitcoin_return'] = df['bitcoin_close'].pct_change()
df['ethereum_return'] = df['ethereum_close'].pct_change()
df['portfolio_return'] = 0.5 * df['bitcoin_return'] + 0.5 * df['ethereum_return']
df['bitcoin_cum_return'] = (1 + df['bitcoin_return']).cumprod()
df['ethereum_cum_return'] = (1 + df['ethereum_return']).cumprod()
df['portfolio_cum_return'] = (1 + df['portfolio_return']).cumprod()

plt.figure(figsize=(12, 6))
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
print("- Most Volatile: Ethereum .  cumulative return of 1.15 means your investment is now worth 115% of its original value, which is a 15% profit. ")
print("- Moderately Volatile: Bitcoin.A cumulative return of 0.90 means your investment is now worth only 90% of its original value, which is a 10/% loss")
print("- Least Volatile: The diversified Portfolio.")

output_file = 'portfolio_vs_assets_returns.csv'
df.to_csv(output_file, index=False)
print(f"Data exported to {output_file}")
