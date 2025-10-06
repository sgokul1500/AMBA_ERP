# ===============================
# app.py - AMBA_ERP Fun Prototype with Interactive Sidebar/Navbar
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(
    page_title="AMBA-ERP",            # 👈 Changes tab title                  # 👈 Adds e
    layout="wide",                    # Optional: makes it wide
    initial_sidebar_state="expanded"  # Optional: sidebar open by default
)
# -------------------------------
# 1. Load Data
# -------------------------------
@st.cache_data
def load_customers():
    return pd.read_excel("sample_inventory.xlsx")

customer_df = load_customers()

# -------------------------------
# Sidebar / Navbar
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")

page = st.sidebar.radio("Go to:", ["🏠 Customer Overview", "📝 Create New Order", "📦 Inventory Dashboard"])

st.sidebar.markdown("---")
st.sidebar.info("Select a page above to interact with the ERP system prototype!")
#GitHub Badge (opens README.md)
# st.sidebar.markdown(
#     "[![GitHub](https://img.shields.io/badge/View%20on-GitHub-black?logo=github)](https://github.com/sgokul1500/AMBA_ERP/blob/main/README.md)"
# )
# -------------------------------
# Header
# -------------------------------
st.markdown("<h1 style='text-align: center; color: #4B0082;'> Amba ERP  Prototype </h1>", unsafe_allow_html=True)

# -------------------------------
# Page: Customer Overview
# -------------------------------
if page == "🏠 Customer Overview":
    st.subheader("📊 Customer Overview")
    st.dataframe(customer_df)
    st.markdown(
        "💡 Tip: This shows all customer order values, collections, and outstanding balances."
    )

# -------------------------------
# Page: Create New Order
# -------------------------------
elif page == "📝 Create New Order":
    st.subheader("🛒 Create a New Sales Order")

    products = ["Transformer Laminations", "Motor Stamping", "Custom Parts"]

    with st.form("new_order_form"):
        customer_name = st.text_input("Customer Name (Type new or existing) 🧑‍💼")
        product_name = st.selectbox("Select Product 🏭", products)
        quantity = st.number_input("Quantity 🔢", min_value=1, value=1)
        amount_collected = st.number_input("Amount Collected 💵", min_value=0.0, value=0.0, step=0.01)
        last_payment_date = st.date_input("Last Payment Date 📅 (Optional)", value=None)

        submitted = st.form_submit_button("🚀 Submit Order")

        if submitted:
            if not customer_name.strip():
                st.error("⚠️ Customer Name is required!")
            else:
                with st.spinner("Processing your order... ⏳"):
                    for percent in range(0, 101, 10):
                        time.sleep(0.05)
                        st.progress(percent)

                # SQL INSERT statement
                sql_insert_order = f"""
INSERT INTO Orders (customer_name, product_name, quantity, amount_collected, last_payment_date, order_date)
VALUES (
    '{customer_name}',
    '{product_name}',
    {quantity},
    {amount_collected},
    {'NULL' if not last_payment_date else f"'{last_payment_date}'"},
    '{datetime.today().strftime('%Y-%m-%d')}'
);
"""
                st.success("✅ Order validated successfully!")
                st.code(sql_insert_order, language="sql")

                st.balloons()
                

# -------------------------------
# Page: Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    inventory_df = pd.DataFrame({
        "Product Name": ["Transformer Laminations", "Motor Stamping", "Custom Parts"],
        "Stock Quantity": [120, 80, 50],
        "Unit Price ($)": [1500, 2000, 500]
    })

    st.dataframe(inventory_df)
    st.markdown("💡 Stock levels shown as plain numbers for simplicity.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown(
    "<h4 style='text-align: center; color: #FF1493;'>Developed by  Gokul Srinivasan </h4>",
    unsafe_allow_html=True
)
