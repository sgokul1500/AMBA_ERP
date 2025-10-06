# ===============================
# inventory.py - Inventory & Analytics Module
# ===============================

import pandas as pd
from datetime import datetime
import numpy as np

# -------------------------------
# Initial Inventory
# -------------------------------
def load_inventory():
    inventory_df = pd.DataFrame({
        "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
        "Stock Quantity": [120, 80, 50],
        "Unit Price": [1500, 2000, 500]
    })
    return inventory_df

# -------------------------------
# Orders storage
# -------------------------------
def load_orders():
    orders_df = pd.DataFrame(columns=["customer_name", "product_name", "quantity", "amount_collected", "last_payment_date", "order_date"])
    return orders_df

# -------------------------------
# Update Inventory
# -------------------------------
def update_inventory(inventory_df, product_name, quantity):
    idx = inventory_df.index[inventory_df["Product Name"] == product_name][0]
    inventory_df.at[idx, "Stock Quantity"] -= quantity
    return inventory_df

# -------------------------------
# Predict Stock Depletion Over Time
# -------------------------------
def predict_stockout_days(inv_df, orders_df, days_ahead=30):
    """
    Simulates future stock levels for each product over the next `days_ahead` days.
    Returns a DataFrame suitable for plotting line chart.
    """
    stock_sim = pd.DataFrame()
    for _, row in inv_df.iterrows():
        product = row["Product Name"]
        stock = row["Stock Quantity"]

        # Estimate daily consumption from last 10 orders
        product_orders = orders_df[orders_df["product_name"] == product]
        if product_orders.empty:
            daily_rate = 1  # default consumption
        else:
            daily_rate = product_orders["quantity"].tail(10).mean()

        # Simulate stock for each day
        days = list(range(days_ahead))
        stock_levels = [max(stock - daily_rate * d, 0) for d in days]
        df = pd.DataFrame({
            "Day": days,
            "Stock": stock_levels,
            "Product": product
        })
        stock_sim = pd.concat([stock_sim, df], ignore_index=True)

    return stock_sim

# -------------------------------
# Detect Anomalies in Transactions
# -------------------------------
def detect_anomalies(orders_df):
    """
    Simple anomaly detection: flag orders with unusually high quantity compared to median.
    """
    if orders_df.empty:
        return pd.DataFrame(columns=orders_df.columns.tolist() + ["Anomaly"])

    anomalies_df = orders_df.copy()
    anomalies_df["Anomaly"] = False
    for product in orders_df["product_name"].unique():
        median_qty = orders_df[orders_df["product_name"] == product]["quantity"].median()
        anomalies_df.loc[(orders_df["product_name"] == product) & (orders_df["quantity"] > 2 * median_qty), "Anomaly"] = True
    return anomalies_df
