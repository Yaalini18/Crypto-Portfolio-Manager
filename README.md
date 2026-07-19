# Crypto Portfolio Management Projects Report


##  **Project m2p1 – Portfolio Metrics Calculation (Portfolio_math.py)** 

###  **Objective**
The purpose of this project is to build a structured approach to calculating portfolio metrics such as expected return and risk using historical cryptocurrency data. The project focuses on:
- Assigning fixed weights to assets like Bitcoin and Ethereum.
- Calculating daily returns and cumulative metrics.
- Storing the results into a SQLite database for future retrieval and analysis.

The project aims to demonstrate the integration of data manipulation, mathematical calculations, and database management using Python.

---

###  **Steps Performed**

1. **Database Setup**
   - Created a SQLite database (`Portfolio_math.db`) using Python’s `sqlite3` module.
   - Defined two tables, `Bitcoin` and `Ethereum`, to store historical price data.

2. **Data Loading**
   - Loaded Bitcoin and Ethereum historical data from CSV files using `pandas`.
   - Inserted the data into their respective database tables using the `to_sql` function.

3. **Portfolio Tables**
   - Created two additional tables:
     - `portfolio` to store portfolio metadata like name, creation date, expected return, and risk.
     - `portfolio_assets` to store asset allocation and weights.

4. **Calculating Portfolio Metrics**
   - Sorted closing prices by timestamp.
   - Calculated daily returns using percentage change formula.
   - Computed expected returns by applying assigned weights.
   - Calculated portfolio risk using the covariance matrix and standard deviation formula.

5. **Inserting Data into Database**
   - Inserted portfolio metrics and individual asset allocations into the database.
   - Used transactions (`commit`) to ensure data consistency.

---

###  **Results**

- The database was successfully created and populated with structured tables.
- Portfolio metrics such as expected return and portfolio risk were calculated accurately using historical data.
- Data integrity was maintained through the use of relational tables and foreign keys.
- This setup provides a foundation for further analysis and extensions like real-time tracking or automated rebalancing.

---

##  **Project m2p2 – Database Storage and Retrieval (Db_portfolio.py)**

###  **Objective**
The goal of this project is to enhance portfolio data storage by implementing robust database management for cryptocurrencies. It focuses on:
- Creating database tables to store asset prices and portfolio allocations.
- Loading data from CSV files.
- Performing mathematical computations to derive portfolio return and risk.
- Storing the results in a relational structure.

This project builds on the fundamentals of data handling and persistence.

---

###  **Steps Performed**

1. **Database Initialization**
   - Created a SQLite database named `Db_portfolio1.db`.
   - Defined tables for `Bitcoin`, `Ethereum`, `portfolio`, and `portfolio_assets`.

2. **Data Integration**
   - Imported historical price data from CSV files using `pandas`.
   - Inserted data into database tables.

3. **Portfolio Computation**
   - Calculated daily returns from historical price data.
   - Computed expected portfolio return using weighted averages.
   - Estimated portfolio risk using covariance and variance formulas.

4. **Storing Portfolio Information**
   - Inserted portfolio metrics such as name, return, and risk into the `portfolio` table.
   - Inserted asset names and weights into the `portfolio_assets` table.

5. **Data Management**
   - Used SQLite transactions to ensure consistency.
   - Enabled data retrieval for future queries or analysis.

---

###  **Results**

- Portfolio and asset information was stored in a well-structured relational database.
- The mathematical computations provided accurate estimations of portfolio performance metrics.
- The system is prepared to handle multiple portfolios with various asset combinations.
- The project lays groundwork for more advanced portfolio tracking and optimization algorithms.

---

##  **Project m2p3 – Parallel Execution (Parallel Execution of Portfolio Rules)**

###  **Objective**
The aim of this project is to extend portfolio analysis by executing multiple allocation strategies in parallel, improving efficiency and scalability. The focus is on:
- Defining multiple portfolio allocation rules such as risk-based and goal-based strategies.
- Running computations concurrently using threads.
- Storing results in a database for later retrieval and analysis.

This demonstrates how concurrent programming can enhance computational workflows.

---

###  **Steps Performed**

1. **Defining Allocation Rules**
   - Created functions for `risk_based_weights` and `goal_based_weights`.
   - Defined asset allocation percentages for each rule.

2. **Database Setup**
   - Created a SQLite database `parallel.db`.
   - Defined the `portfolio_weights` table to store results.

3. **Parallel Processing**
   - Used Python’s `ThreadPoolExecutor` to execute multiple rules in parallel.
   - Submitted tasks to the thread pool, where each allocation was computed and stored.

4. **Data Storage**
   - Inserted the computed weights into the database with rule identifiers.
   - Committed transactions after every operation to maintain integrity.

5. **Result Retrieval**
   - Fetched results and printed confirmations after each task completed.

---

###  **Results**

- Multiple portfolio allocation rules were executed without blocking each other.
- Computations were completed faster due to parallel execution.
- The database stored rule-based allocations in a structured way for future use.
- The system demonstrated robustness and efficiency in handling multiple investment strategies simultaneously.

---

##  **Project m2p4 – Portfolio vs. Single Asset Return Comparison**

###  **Objective**
The objective of this project is to simulate and compare the cumulative returns of a portfolio and individual assets over time. The project focuses on:
- Generating sample data for Bitcoin and Ethereum.
- Calculating daily and cumulative returns.
- Visualizing the portfolio’s behavior versus single assets.
- Exporting the results for further analysis.

The project aims to demonstrate the importance of diversification in reducing volatility.

---

###  **Steps Performed**

1. **Data Simulation**
   - Used random walk techniques to simulate daily closing prices for Bitcoin and Ethereum.
   - Ensured reproducibility by setting a random seed.

2. **Return Calculation**
   - Calculated daily returns as percentage changes.
   - Computed portfolio return using equal weighting.

3. **Cumulative Return**
   - Applied cumulative product to derive growth curves for each asset and the portfolio.

4. **Visualization**
   - Plotted cumulative returns over time using `matplotlib`.
   - Distinguished portfolio returns with a dashed line for clarity.

5. **Insights**
   - Analyzed how diversification smooths portfolio performance.
   - Highlighted the trade-off between stability and peak performance.

6. **Data Export**
   - Saved the computed data into a CSV file for further exploration or reporting.

---

###  **Results**

- Realistic price data was generated to model cryptocurrency performance.
- The portfolio’s cumulative return curve demonstrated reduced volatility compared to individual assets.
- Insights into diversification were validated through visual analysis.
- Data was exported successfully, enabling further research or integration into reports.

---

##  **Final Remarks**

These projects collectively cover the lifecycle of portfolio management—from data acquisition and storage to advanced computations and visualization. The integration of Python, SQLite, and statistical modeling techniques showcases how technology can empower data-driven investment strategies. The projects also lay the foundation for more complex portfolio optimizations and real-time performance monitoring tools.

---

Let me know if you want this report converted into PDF format, or enriched with charts, tables, and diagrams for presentation purposes.


# Crypto Portfolio Management Projects Report

## **Project m3p1 – Risk Checker (Risk_checker.py)**

### **Objective**
To implement a risk management engine for a crypto portfolio (BTC + ETH) by applying 6 rules, storing results in a database, and sending alerts for violations.

---

### **Steps Performed**
1. **Database Setup**
   - Created `crypto_data.db` with `risk_assessment` table.
   - Stored portfolio name, rule, value, condition, status, and timestamp.

2. **Data Preparation**
   - Loaded BTC & ETH CSV files.
   - Calculated daily returns, merged datasets, and assigned weights using market caps.

3. **Risk Rule Implementation**
   - Implemented functions for:
     - Volatility
     - Sharpe Ratio
     - Max Drawdown
     - Sortino Ratio
     - Beta
     - Max Asset Weight
   - Compared values against predefined thresholds.

4. **Storing Results**
   - Inserted evaluation results into SQLite.
   - Replaced old entries with new calculations.

5. **Email Alerts**
   - Configured Gmail SMTP with App Password.
   - Sent alerts if any rule failed, listing violated conditions.

---

### **Results**
- Built complete **risk checker pipeline**.
- Evaluated 6 rules and stored results in SQLite.
- Alerts sent automatically on failure.
- Enables proactive crypto portfolio monitoring.

---

## **Project m3p2 – Portfolio Predictor (predictor.py)**

### **Objective**
To predict portfolio and asset returns using **Linear Regression**, evaluate accuracy, and store results in a database.

---

### **Steps Performed**
1. **Data Loading**
   - Loaded BTC & ETH CSV files.
   - Calculated percentage change returns for assets and portfolio.

2. **Model Training**
   - Trained Linear Regression on returns.
   - Evaluated using **MSE** and **R²**.

3. **Database Storage**
   - Created `predictions` and `prediction_rows` tables.
   - Stored summary metrics and actual vs predicted values.

---

### **Results**
- Predictions generated for BTC, ETH, and portfolio.
- Accuracy measured with MSE and R².
- Results stored in SQLite for tracking.
- Forms base for advanced ML (XGBoost/Random Forest).



# Crypto Portfolio Management Projects Report

## **Project m4p1 – Rule Setter & Stress Testing**

### **Objective**
To implement portfolio allocation rules (from Sept 30 slide), calculate returns under different market conditions, and apply stress tests to analyze portfolio performance.

---

### **Steps Performed**

1. **Rule Setter Implementation**
   - Developed multiple investment spreading rules:
     - **Equal-Weight Rule** – All assets get the same weight.
     - **Risk-Parity Rule** – Assets with lower volatility receive higher weight.
     - **Sharpe-Maximization Rule** – Assets with higher Sharpe ratios receive more weight.
     - **Momentum Rule** – Recent winners are assigned more weight.

2. **Data Preparation**
   - Loaded historical BTC & ETH data from CSV files.
   - Merged datasets on timestamp and calculated daily returns.
   - Computed mean returns and volatility for both assets.

3. **Portfolio Weights Calculation**
   - Derived weights for each rule:
     - Equal-Weight: 50%-50%.
     - Risk-Parity: Based on inverse volatility.
     - Sharpe-Maximization: Based on return-to-risk ratio.
     - Momentum: Based on last 5-day performance.

4. **Stress Testing Scenarios**
   - Created synthetic scenarios for **Bull**, **Bear**, and **Volatile** markets.
   - Applied **Risk-Parity Rule** in all scenarios.
   - Calculated mean portfolio returns for each scenario.

5. **Database Setup**
   - Created `Stress_Test.db` with table `portfolio_returns`.
   - Stored scenario name, rule weights, and mean return.

6. **Execution & Output**
   - Printed weights and mean returns for each stress test scenario.
   - Inserted results into SQLite database for future retrieval.

---

### **Results**
- Implemented **4 allocation rules**: Equal-Weight, Risk-Parity, Sharpe, Momentum.
- Stress-tested the portfolio under **Bull, Bear, and Volatile** markets.
- Stored portfolio returns and weight allocations in `Stress_Test.db`.
- Insights:
  - Risk-Parity stabilizes portfolio in volatile conditions.
  - Sharpe rule prioritizes assets with higher efficiency.
  - Momentum captures short-term market trends.
  - Equal-weight provides a baseline for comparison.

---

### **Conclusion**
Milestone 4 successfully integrates **rule-based allocation** with **stress testing** to evaluate portfolio resilience under different scenarios. This forms the foundation for adaptive crypto portfolio strategies.



# **Final Project Summary: Crypto Portfolio Management System**

## **Project Goal**
The objective was to build a data-driven system capable of calculating, analyzing, and reporting cryptocurrency portfolio performance and risk — forming the base for an adaptive investment tool.

---

## **Phase 1: Foundational Metrics & Data Persistence (M2P1, M2P2)**
Established the data and computation backbone for portfolio analytics.

**Key Achievements:**
- **Database Design:** Created structured SQLite databases (`Portfolio_math.db`, `Db_portfolio1.db`) to store historical prices, metadata, and allocations.  
- **Metrics Calculation:** Implemented expected return and risk (volatility) computations using market data and weight-based formulas.  
- **Data Integrity:** Automated data import from CSVs and ensured persistence via transaction commits.

---

## **Phase 2: Performance & Scalability Enhancements (M2P3, M2P4)**
Enhanced speed, scalability, and introduced diversification analysis.

**Key Achievements:**
- **Parallel Execution (M2P3):** Used `ThreadPoolExecutor` for concurrent portfolio strategy execution (Risk-Based, Goal-Based).  
- **Diversification Analysis (M2P4):** Simulated random walk price data to evaluate cumulative returns and demonstrate lower volatility in diversified portfolios.

---

## **Phase 3: Advanced Analytics & Automated Alerting (M3P1, M3P2)**
Transitioned from static analytics to proactive, intelligent portfolio management.

**Key Achievements:**
- **Risk Checker (M3P1):** Validated six key metrics (Volatility, Sharpe, Sortino, Drawdown, Beta, Max Weight) against thresholds.  
- **Email Alerts:** Integrated Gmail SMTP to instantly notify failures in risk checks.  
- **Audit Trail:** Stored all results in the `risk_assessment` table for compliance tracking.  
- **Predictive Modeling (M3P2):** Used Linear Regression to forecast percentage returns for assets and portfolios, evaluating models with MSE and R² metrics.

---

## **Phase 4: Strategy & Resilience Testing (M4P1)**
Implemented rule-based allocation and simulated stress scenarios.

**Key Achievements:**
- **Rule-Based Allocation:** Designed 4 strategies — Equal-Weight, Risk-Parity, Sharpe-Maximization, and Momentum Rule.  
- **Stress Testing:** Evaluated performance under Bull, Bear, and Volatile market simulations.  
- **Resilience Insight:** Identified that Risk-Parity stabilizes outcomes under volatile conditions; results stored in `Stress_Test.db`.

---

## **Final Conclusion**
The project delivered a **complete crypto portfolio management system** combining:
- Automated data handling  
- Parallel computation  
- Real-time risk compliance  
- Predictive modeling  
- Strategic allocation and stress testing  

It demonstrates a strong foundation in **Python programming, financial modeling, and data-driven investment analysis**, offering a scalable path toward an adaptive AI-based investment platform.
#   C r y p t o - P o r t f o l i o - M a n a g e r 
 
 #   C r y p t o - P o r t f o l i o - M a n a g e r 
 
 
