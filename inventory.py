# ===============================
# inventory.py - Data & Logic
# ===============================

import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np

# -------------------------------
# 1. Load Original Inventory Data
# -------------------------------
def load_inventory():
    # Original stock data
    return pd.DataFrame({
        "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
        "Stock Quantity": [120, 80, 50],
        "Unit Price": [1500, 2000, 500]
    })

# -------------------------------
# 2. Load Orders Data
# -------------------------------
def load_orders():
    # Empty orders initially
    return pd.DataFrame(columns=[
        "customer_name", "product_name", "quantity",
        "amount_collected", "last_payment_date", "order_date"
    ])

# -------------------------------
# 3. Update Inventory After Order
# -------------------------------
def update_inventory(inventory_df, product_name, quantity):
    inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"] -= quantity
    return inventory_df

# -------------------------------
# 4. Predict Stockout Days
# -------------------------------
def predict_stockout_days(inventory_df, orders_df):
    predictions = {}
    for product in inventory_df["Product Name"]:
        product_orders = orders_df[orders_df["product_name"] == product]
        if len(product_orders) < 2:
            predictions[product] = None
            continue

        # Use order quantities and dates to predict depletion
        X = np.array([(datetime.today() - d).days for d in product_orders["order_date"]]).reshape(-1, 1)
        y = product_orders["quantity"].values
        model = LinearRegression()
        model.fit(X, y)

        # Estimate days to stockout
        current_stock = inventory_df.loc[inventory_df["Product Name"] == product, "Stock Quantity"].values[0]
        daily_rate = model.coef_[0] if model.coef_[0] > 0 else 1  # avoid zero or negative
        days_to_stockout = max(int(current_stock / daily_rate), 1)
        predictions[product] = days_to_stockout

    return predictions

# -------------------------------
# 5. Detect Anomalies in Orders
# -------------------------------
def detect_anomalies(orders_df):
    anomalies = []
    for _, row in orders_df.iterrows():
        if row["quantity"] > 1000:  # arbitrary threshold
            anomalies.append({
                "customer_name": row["customer_name"],
                "product_name": row["product_name"],
                "quantity": row["quantity"],
                "reason": "Quantity unusually high"
            })
    return anomalies
