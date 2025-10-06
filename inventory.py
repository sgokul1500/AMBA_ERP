# ===============================
# inventory.py - Inventory Operations
# ===============================

import pandas as pd
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

# -------------------------------
# 1. Load Inventory Data
# -------------------------------
def load_inventory():
    return pd.DataFrame({
        "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
        "Stock Quantity": [120, 80, 50],
        "Unit Price": [1500, 2000, 500]
    })

# -------------------------------
# 2. Update Inventory After Order
# -------------------------------
def update_inventory(inventory_df, product_name, quantity):
    inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"] -= quantity
    return inventory_df

# -------------------------------
# 3. Predict Stockout Days
# -------------------------------
def predict_stockout_days(inventory_df):
    predictions = {}
    for idx, row in inventory_df.iterrows():
        # Simulate past 10 days usage
        np.random.seed(idx)
        past_usage = np.random.randint(1, 10, size=(10, 1))
        days = np.arange(1, 11).reshape(-1, 1)

        model = LinearRegression()
        model.fit(days, past_usage)
        # Predict days until stock hits 0
        if row["Stock Quantity"] > 0:
            stockout_day = max(int(-model.intercept_[0] / model.coef_[0][0]), 0)
        else:
            stockout_day = 0
        predictions[row["Product Name"]] = stockout_day
    return predictions

# -------------------------------
# 4. Detect Transaction Anomalies
# -------------------------------
def detect_anomalies(transactions_df):
    if transactions_df.empty:
        transactions_df["Anomaly"] = []
        return transactions_df

    model = IsolationForest(contamination=0.1, random_state=42)
    features = transactions_df[["Quantity", "Amount Collected"]]
    model.fit(features)
    preds = model.predict(features)
    transactions_df["Anomaly"] = ["No" if p == 1 else "Yes" for p in preds]
    return transactions_df
