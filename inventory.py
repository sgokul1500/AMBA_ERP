# ===============================
# inventory.py - ERP Inventory & Analytics Module
# ===============================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

# -------------------------------
# 1. Dummy Data Generation
# -------------------------------

def generate_dummy_data():
    # Products
    products = ["Transformer Laminations", "Motor Stamping", "Custom Parts", "Core Sheets", "Rotor Laminations"]
    stock_qty = [120, 80, 50, 200, 150]
    unit_price = [1500, 2000, 500, 300, 1000]

    inventory_df = pd.DataFrame({
        "Product Name": products,
        "Stock Quantity": stock_qty,
        "Unit Price": unit_price
    })

    # Customers
    customers = [f"Customer {i}" for i in range(1, 11)]

    # Historical Orders
    np.random.seed(42)
    orders = []
    for _ in range(100):
        cust = np.random.choice(customers)
        prod_idx = np.random.randint(0, len(products))
        prod = products[prod_idx]
        qty = np.random.randint(1, 10)
        amount_collected = qty * unit_price[prod_idx] * np.random.choice([0.5, 1.0])
        last_payment = datetime.today() - timedelta(days=np.random.randint(0, 60))
        orders.append([cust, prod, qty, amount_collected, last_payment.date(), datetime.today().date()])
    
    orders_df = pd.DataFrame(orders, columns=["Customer Name", "Product Name", "Quantity", "Amount Collected", "Last Payment Date", "Order Date"])
    
    return inventory_df, orders_df

inventory_df, orders_df = generate_dummy_data()


# -------------------------------
# 2. Update Inventory on New Order
# -------------------------------
def update_inventory(product_name, quantity):
    global inventory_df
    idx = inventory_df.index[inventory_df["Product Name"] == product_name][0]
    inventory_df.loc[idx, "Stock Quantity"] -= quantity
    inventory_df.loc[idx, "Stock Quantity"] = max(inventory_df.loc[idx, "Stock Quantity"], 0)
    return inventory_df


# -------------------------------
# 3. Stockout Prediction
# -------------------------------
def predict_stockout_days(product_name):
    df = orders_df[orders_df["Product Name"] == product_name].copy()
    if df.empty:
        return None

    # Convert Order Date to ordinal for regression
    df["Order Date Ord"] = pd.to_datetime(df["Order Date"]).map(datetime.toordinal)
    X = df["Order Date Ord"].values.reshape(-1, 1)
    y = df["Quantity"].cumsum().values  # cumulative orders

    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)

    # Predict when stock reaches 0
    current_stock = inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"].values[0]
    last_date_ord = X.max()
    predicted_date_ord = (current_stock + y.max() - model.intercept_) / model.coef_[0]
    predicted_date = datetime.fromordinal(int(predicted_date_ord))
    days_left = (predicted_date - datetime.today()).days
    return max(days_left, 0)


# -------------------------------
# 4. Anomaly Detection
# -------------------------------
def detect_anomalies():
    df = orders_df[["Quantity", "Amount Collected"]].copy()
    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(df)
    anomalies = orders_df[df["anomaly"] == -1]
    return anomalies
