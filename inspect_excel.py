# ===============================
# inspect_excel.py - AMBA_ERP
# ===============================

import pandas as pd

# -------------------------------
# 1. Load Excel Files
# -------------------------------
customers_file = "sample_inventory.xlsx"  # assuming customer info is in this file
inventory_file = "sample_inventory.xlsx"  # inventory info

# For simplicity, assuming sheet names or columns
# Customers Sheet: Customer Name, Total Order Value ($), Total Collected ($), Outstanding Balance ($), Last Payment Date
customers_df = pd.read_excel(customers_file, sheet_name=None).get('Customers')
# Inventory Sheet: Product Name, Unit Price, Stock Quantity
inventory_df = pd.read_excel(inventory_file, sheet_name=None).get('Inventory')

# -------------------------------
# 2. Generate SQL for Customers
# -------------------------------
print("-- SQL INSERT Statements for Customers --")
for idx, row in customers_df.iterrows():
    last_payment_date = 'NULL' if pd.isna(row['Last Payment Date']) else f"'{row['Last Payment Date'].strftime('%Y-%m-%d')}'"
    sql = f"""
INSERT INTO Customers (customer_name, total_order_value, total_collected, outstanding_balance, last_payment_date)
VALUES ('{row['Customer Name']}', {row['Total Order Value ($)']}, {row['Total Collected ($)']}, {row['Outstanding Balance ($)']}, {last_payment_date});
"""
    print(sql)

# -------------------------------
# 3. Generate SQL for Products
# -------------------------------
print("-- SQL INSERT Statements for Products --")
for idx, row in inventory_df.iterrows():
    sql = f"""
INSERT INTO Products (product_name, unit_price, stock_quantity)
VALUES ('{row['Product Name']}', {row['Unit Price']}, {row['Stock Quantity']});
"""
    print(sql)

print("\n-- Done generating SQL statements --")
