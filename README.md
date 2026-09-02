#  Crypto Portfolio Management System

A Python-based application that analyzes cryptocurrency portfolios using historical Bitcoin and Ethereum data. The system calculates portfolio return, evaluates multiple risk metrics, predicts future returns using Linear Regression, performs stress testing, and stores results in SQLite for future analysis.

##  Features

- Calculate portfolio expected return
- Compute six risk metrics:
  - Volatility
  - Sharpe Ratio
  - Sortino Ratio
  - Maximum Drawdown
  - Beta
  - Maximum Asset Concentration
- Predict future returns using Linear Regression
- Perform Bull, Bear, and Volatile market stress tests
- Store portfolio history in SQLite
- Send automated email alerts when risk thresholds are exceeded

##  Tech Stack

**Python • Pandas • NumPy • SQLite • scikit-learn **

## Project Workflow

```
Historical Data
      ↓
Data Processing
      ↓
Risk & Return Calculation
      ↓
SQLite Storage
      ↓
Prediction & Stress Testing
      ↓
Email Alerts
```

## Future Enhancements

- PostgreSQL support
- Live market data integration
- Interactive dashboard
- Portfolio optimization
