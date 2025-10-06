# ===============================
# inventory.py - Helper Functions
# ===============================

import pandas as pd
from datetime import datetime

def load_inventory():
    """Return initial inventory DataFrame"""
    return pd.DataFrame({
        "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
        "Stock Quantity": [120, 80, 50],
        "Unit Price": [1500, 2000, 500]
    })

def update_stock(product_name, quantity, inventory_df):
    """Deduct stock for a given product. Returns success flag and updated DataFrame"""
    idx = inventory_df.index[inventory_df["Product Name"] == product_name][0]
    if inventory_df.at[idx, "Stock Quantity"] >= quantity:
        inventory_df.at[idx, "Stock Quantity"] -= quantity
        return True, inventory_df
    else:
        return False, inventory_df

def log_inventory_transaction(product_name, quantity):
    """Return a dict representing a stock deduction event"""
    return {
        "product_name": product_name,
        "quantity_deducted": quantity,
        "transaction_date": datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    }
