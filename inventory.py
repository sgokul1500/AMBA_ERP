import pandas as pd

def get_inventory():
    # Sample inventory
    return pd.DataFrame({
        "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
        "Stock Quantity": [120, 80, 50],
        "Unit Price": [1500, 2000, 500]
    })

def check_stock(product_name, quantity, inventory_df):
    stock_qty = inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"].values[0]
    return stock_qty >= quantity, stock_qty
