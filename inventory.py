# ===============================
# inventory.py - Inventory & Analysis Functions
# ===============================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

# -------------------------------
# Sample Inventory Data
# -------------------------------
inventory_df = pd.DataFrame({
    "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
    "Stock Quantity": [120, 80, 50],
    "Unit Price": [1500, 2000, 500]
})

# -------------------------------
# Sample Orders Data
# -------------------------------
orders_df = pd.DataFrame(columns=[
    "customer_name", "product_name", "quantity", "amount_collected", "last_payment_date", "order_date"
])

# -------------------------------
# Update Inventory
# -------------------------------
def update_inventory(inv_df, product_name, quantity_ordered):
    inv_df.loc[inv_df["Product Name"] == product_name, "Stock Quantity"] -= quantity_ordered
    return inv_df

# -------------------------------
# Predict Stockout Days
# -------------------------------
def predict_stockout_days(inv_df, orders_df):
    result = []
    for _, row in inv_df.iterrows():
        product = row["Product Name"]
        stock = row["Stock Quantity"]
        # Filter orders for this product
        product_orders = orders_df[orders_df["product_name"] == product]
        if product_orders.empty:
            daily_rate = 0.5  # default usage
        else:
            # Use last 10 orders
            recent_orders = product_orders.tail(10)
            daily_rate = recent_orders["quantity"].mean()
        predicted_days = stock / daily_rate if daily_rate > 0 else np.nan
        result.append({"Product Name": product, "Predicted Stockout Days": predicted_days})
    return pd.DataFrame(result)

# -------------------------------
# Anomaly Detection
# -------------------------------
def detect_anomalies(orders_df):
    if orders_df.empty:
        return pd.DataFrame()
    clf = IsolationForest(contamination=0.1, random_state=42)
    X = orders_df[["quantity", "amount_collected"]].fillna(0)
    clf.fit(X)
    orders_df["anomaly"] = clf.predict(X)
    return orders_df[orders_df["anomaly"] == -1][
        ["customer_name", "product_name", "quantity", "amount_collected", "last_payment_date"]
    ]
