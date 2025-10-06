# ===============================
# inventory.py - Inventory Management Functions
# ===============================

import pandas as pd
from datetime import datetime

# Load initial inventory
def load_inventory():
    return pd.DataFrame({
        "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
        "Stock Quantity": [120, 80, 50],
        "Unit Price ($)": [1500, 2000, 500]
    })

# Update stock after a new order
def update_stock(product_name, quantity, inventory_df):
    if product_name in inventory_df["Product Name"].values:
        current_stock = inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"].values[0]
        if quantity > current_stock:
            return False, inventory_df  # Not enough stock
        inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"] -= quantity
        return True, inventory_df
    return False, inventory_df

# Pseudo InventoryLog
def log_inventory_transaction(product_name, quantity, transaction_type="OUT"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "product_name": product_name,
        "transaction_type": transaction_type,
        "quantity": quantity,
        "transaction_date": timestamp
    }
