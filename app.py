# ===============================
# app.py - AMBA_ERP Prototype with AI/ML Features
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from inventory import load_inventory, update_inventory, predict_stockout_days, detect_anomalies

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AMBA-ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_customers():
    return pd.DataFrame({
        "Customer Name": ["Customer 1","Customer 2","Customer 3","Customer 4","Customer 5"],
        "Total Order Value ($)": [167500,105000,37500,75000,30000],
        "Total Collected ($)": [10000,0,0,50000,25000],
        "Outstanding Balance ($)": [157500,105000,37500,25000,5000],
        "Last Payment Date": ["2025-07-30","-","-","2025-07-25","2025-07-28"]
    })

customer_df = load_customers()
inventory_df = load_inventory()
transactions_df = pd.DataFrame(columns=["Customer Name","Product","Quantity","Amount Collected","Date"])

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Customer Overview", "📝 Create New Order", "📦 Inventory Dashboard", "🤖 AI/ML Insights"])
st.sidebar.markdown("---")
st.sidebar.info("Select a page to interact with the ERP prototype.")

# -------------------------------
# Header
# -------------------------------
st.markdown("<h1 style='text-align: center; color: #4B0082;'> Amba ERP Prototype </h1>", unsafe_allow_html=True)

# -------------------------------
# Page: Customer Overview
# -------------------------------
if page == "🏠 Customer Overview":
    st.subheader("📊 Customer Overview")
    st.dataframe(customer_df)
    st.markdown("💡 Tip: Shows all customer orders, collections, and outstanding balances.")

# -------------------------------
# Page: Create New Order
# -------------------------------
elif page == "📝 Create New Order":
    st.subheader("🛒 Create a New Sales Order")

    products = inventory_df["Product Name"].tolist()

    with st.form("new_order_form"):
        customer_name = st.text_input("Customer Name 🧑‍💼")
        product_name = st.selectbox("Select Product 🏭", products)
        quantity = st.number_input("Quantity 🔢", min_value=1, value=1)
        amount_collected = st.number_input("Amount Collected 💵", min_value=0.0, value=0.0, step=0.01)
        last_payment_date = st.date_input("Last Payment Date 📅 (Optional)", value=None)

        submitted = st.form_submit_button("Submit Order")

        if submitted:
            if not customer_name.strip():
                st.error("⚠️ Customer Name is required!")
            elif quantity > inventory_df.loc[inventory_df["Product Name"]==product_name,"Stock Quantity"].values[0]:
                st.error("⚠️ Insufficient stock!")
            else:
                # Update Inventory
                inventory_df = update_inventory(inventory_df, product_name, quantity)

                # Log transaction
                transactions_df.loc[len(transactions_df)] = [customer_name, product_name, quantity, amount_collected, datetime.today().strftime('%Y-%m-%d')]

                # SQL Statements
                sql_insert_order = f"""
INSERT INTO Orders (customer_name, product_name, quantity, amount_collected, last_payment_date, order_date)
VALUES (
    '{customer_name}', '{product_name}', {quantity}, {amount_collected},
    {'NULL' if not last_payment_date else f"'{last_payment_date}'"},
    '{datetime.today().strftime('%Y-%m-%d')}'
);
"""
                sql_insert_inventory = f"""
INSERT INTO InventoryLog (product_name, quantity, transaction_date, transaction_type)
VALUES (
    '{product_name}', {quantity}, '{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}', 'OUT'
);
"""
                st.subheader("✅ SQL Output")
                st.code(sql_insert_order, language="sql")
                st.code(sql_insert_inventory, language="sql")

# -------------------------------
# Page: Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(inventory_df)
    st.markdown("💡 Current stock levels with dynamic updates from new orders.")

# -------------------------------
# Page: AI/ML Insights
# -------------------------------
elif page == "🤖 AI/ML Insights":
    st.subheader("🤖 AI/ML Prototype Features")

    st.markdown("### 1️⃣ Inventory Stockout Prediction")
    stockout_pred = predict_stockout_days(inventory_df)
    st.dataframe(pd.DataFrame(list(stockout_pred.items()), columns=["Product","Predicted Days to Stockout"]))

    st.markdown("### 2️⃣ Transaction Anomaly Detection")
    transactions_anomaly = detect_anomalies(transactions_df)
    st.dataframe(transactions_anomaly)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan</h4>", unsafe_allow_html=True)
