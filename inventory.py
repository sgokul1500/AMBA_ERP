# ===============================
# inventory.py - Inventory and Order Logic
# ===============================

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from datetime import datetime

# -------------------------------
# Inventory Data
# -------------------------------
inventory_df = pd.DataFrame({
    "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
    "Stock Quantity": [120, 80, 50],
    "Unit Price ($)": [1500, 2000, 500]
})

# Orders Data
orders_df = pd.DataFrame(columns=[
    "Customer Name", "Product Name", "Quantity",
    "Amount Collected", "Last Payment Date", "Order Date"
])

# -------------------------------
# Update Inventory
# -------------------------------
def update_inventory(product_name, quantity_ordered, customer_name, amount_collected, last_payment_date):
    global inventory_df, orders_df
    # Update stock
    inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"] -= quantity_ordered
    
    # Add order to orders_df
    new_order = {
        "Customer Name": customer_name,
        "Product Name": product_name,
        "Quantity": quantity_ordered,
        "Amount Collected": amount_collected,
        "Last Payment Date": last_payment_date,
        "Order Date": datetime.today().strftime("%Y-%m-%d")
    }
    orders_df = pd.concat([orders_df, pd.DataFrame([new_order])], ignore_index=True)

# -------------------------------
# Predict Stockout Days (Dummy ML)
# -------------------------------
def predict_stockout_days(product_name):
    # Dummy model: linear regression on stock vs time
    stock = inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"].values[0]
    daily_sale_rate = 10  # assume 10 units/day
    return max(stock // daily_sale_rate, 0)

# -------------------------------
# Anomaly Detection in Orders (Dummy ML)
# -------------------------------
def detect_anomalies():
    if orders_df.empty:
        return pd.DataFrame(columns=orders_df.columns)
    
    # Using IsolationForest for demo
    clf = IsolationForest(contamination=0.1, random_state=42)
    try:
        clf.fit(orders_df[["Quantity", "Amount Collected"]])
        preds = clf.predict(orders_df[["Quantity", "Amount Collected"]])
        anomalies = orders_df[preds == -1]
        return anomalies
    except:
        # If dataset too small, return empty
        return pd.DataFrame(columns=orders_df.columns)
