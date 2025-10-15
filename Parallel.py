
# m2p3
# Parallel Execution 
# Extend logic: run multiple rule tests in parallel (ThreadPool).
# Example: run equal-weight, risk-based, performance-based at same time.
# Save outputs into DB .


import sqlite3
from concurrent.futures import ThreadPoolExecutor

coins = ["BTC", "ETH", "Stablecoin", "DeFi", "Meme"]

def risk_based_weights():
    weights = {
        "BTC": 40,
        "ETH": 20,
        "Stablecoin": 20,
        "DeFi": 10,
        "Meme": 10
    }
    return weights

def goal_based_weights():
    weights = {
        "BTC": 30,
        "ETH": 25,
        "Stablecoin": 10,
        "DeFi": 20,
        "Meme": 15
    }
    return weights

def save_to_db(rule_name, weights):
    conn = sqlite3.connect("parallel.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio_weights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule TEXT,
        coin TEXT,
        weight REAL
    )
    """)
    
    for coin, weight in weights.items():
        cursor.execute("INSERT INTO portfolio_weights (rule, coin, weight) VALUES (?, ?, ?)",
                       (rule_name, coin, weight))
    
    conn.commit()
    conn.close()
    print(f"Saved {rule_name} weights to database.")

def run_rule(rule_name, rule_func):
    weights = rule_func()
    save_to_db(rule_name, weights)
    return weights

if __name__ == "__main__":
    rules = {
        "Risk-Based": risk_based_weights,
        "Goal-Based": goal_based_weights
    }

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(run_rule, name, func) for name, func in rules.items()]
        
        for future in futures:
            result = future.result()
            print("Result:", result)
