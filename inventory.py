# ===============================
# inventory.py - Inventory Management & Predictions
# ===============================

import pandas as pd
import numpy as np
from datetime import datetime

# -------------------------------
# 1. Load initial inventory
# -------------------------------
def load_inventory():
    inventory_df = pd.DataFrame({
        "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
        "Stock Quantity": [120, 80, 50],
        "Unit Price": [1500, 2000, 500],
        "Daily Usage Rate": [5, 4, 2]  # dummy usage rate for prediction
    })
    return inventory_df

inventory_df = load_inventory()

# -------------------------------
# 2. Orders DataFrame
# -------------------------------
orders_df = pd.DataFrame(columns=[
    "Customer Name", "Product Name", "Quantity", "Amount Collected", "Last Payment Date", "Order Date"
])

# -------------------------------
# 3. Update Inventory Function
# -------------------------------
def update_inventory(product_name, quantity):
    global inventory_df
    inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"] -= quantity
    inventory_df["Stock Quantity"] = inventory_df["Stock Quantity"].clip(lower=0)

# -------------------------------
# 4. Predict Stockout Over Next N Days
# -------------------------------
def predict_stockout_days(days=30):
    pred_df = pd.DataFrame({"Day": np.arange(0, days+1)})
    for _, row in inventory_df.iterrows():
        stock = row["Stock Quantity"]
        rate = row["Daily Usage Rate"]
        pred = np.maximum(stock - rate * np.arange(0, days+1), 0)
        pred_df[row["Product Name"]] = pred
    return pred_df

# -------------------------------
# 5. Anomaly Detection in Orders
# -------------------------------
def detect_anomalies(order_quantity_threshold=50):
    if orders_df.empty:
        return pd.DataFrame(columns=["Product Name", "Quantity", "Flag"])
    anomalies = orders_df[orders_df["Quantity"] > order_quantity_threshold].copy()
    anomalies["Flag"] = "High Quantity Order"
    return anomalies
