import pandas as pd

def load_customers(file_path="sample_inventory.xlsx"):
    return pd.read_excel(file_path)

def get_customer_list(customer_df):
    return customer_df["Customer Name"].tolist()
