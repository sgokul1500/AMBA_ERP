# ===============================
# app.py - AMBA_ERP Fun Prototype with Dynamic Inventory
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from inventory import load_inventory, update_stock, log_inventory_transaction

# -------------------------------
# Page Configuration
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
    return pd.read_excel("sample_inventory.xlsx")

customer_df = load_customers()
inventory_df = load_inventory()
inventory_log = []

# -------------------------------
# Sidebar / Navbar
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Customer Overview", "📝 Create New Order", "📦 Inventory Dashboard"])
st.sidebar.markdown("---")
st.sidebar.info("Select a page above to interact with the ERP system prototype!")

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
    st.markdown("💡 Tip: Shows all customer order values, collections, and outstanding balances.")

# -------------------------------
# Page: Create New Order
# -------------------------------
elif page == "📝 Create New Order":
    st.subheader("🛒 Create a New Sales Order")

    products = inventory_df["Product Name"].tolist()

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
                # Check stock and update
                success, inventory_df = update_stock(product_name, quantity, inventory_df)
                if not success:
                    st.error("⚠️ Insufficient stock for this product!")
                else:
                    with st.spinner("Processing your order... ⏳"):
                        for percent in range(0, 101, 10):
                            time.sleep(0.05)
                            st.progress(percent)

                    # SQL INSERT statement (prototype)
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

                    # Log inventory transaction
                    transaction = log_inventory_transaction(product_name, quantity)
                    inventory_log.append(transaction)

                    st.subheader("📦 Updated Inventory After Order")
                    st.dataframe(inventory_df)

                    st.subheader("📝 Inventory Log")
                    st.dataframe(pd.DataFrame(inventory_log))

                    st.balloons()

# -------------------------------
# Page: Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(inventory_df)
    st.markdown("💡 Stock levels shown as plain numbers for simplicity.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan </h4>", unsafe_allow_html=True)
