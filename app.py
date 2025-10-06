# ===============================
# app.py - AMBA_ERP Final Fun Prototype
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
from inventory import load_inventory, update_stock, log_inventory_transaction

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AMBA-ERP",            # Tab title
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Initialize Session State
# -------------------------------
if "inventory_df" not in st.session_state:
    st.session_state.inventory_df = load_inventory()

if "inventory_log" not in st.session_state:
    st.session_state.inventory_log = []

# -------------------------------
# Sidebar / Navbar
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Customer Overview", "📝 Create New Order", "📦 Inventory Dashboard"])
st.sidebar.markdown("---")
st.sidebar.info("Select a page above to interact with the ERP system prototype!")

# GitHub README badge
st.sidebar.markdown("""
[![GitHub](https://img.shields.io/badge/View%20on-GitHub-black?logo=github)](https://github.com/sgokul1500/AMBA_ERP/blob/main/README.md)
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Amba ERP Prototype</h1>", unsafe_allow_html=True)

# -------------------------------
# Page: Customer Overview
# -------------------------------
if page == "🏠 Customer Overview":
    st.subheader("📊 Customer Overview")
    st.dataframe(load_inventory())  # Can add separate customer info if available
    st.markdown("💡 Tip: Shows customer order values, collections, and outstanding balances.")

# -------------------------------
# Page: Create New Order
# -------------------------------
elif page == "📝 Create New Order":
    st.subheader("🛒 Create a New Sales Order")

    products = st.session_state.inventory_df["Product Name"].tolist()

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
                success, st.session_state.inventory_df = update_stock(product_name, quantity, st.session_state.inventory_df)
                if not success:
                    st.error("⚠️ Insufficient stock for this product!")
                else:
                    # Generate SQL (prototype only)
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

                    # Display SQL statement
                    st.subheader("📝 Generated SQL for Orders Table")
                    st.code(sql_insert_order, language="sql")

                    # Log inventory transaction
                    transaction = log_inventory_transaction(product_name, quantity)
                    st.session_state.inventory_log.append(transaction)

# -------------------------------
# Page: Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard (Dynamic)")

    # Show updated inventory
    st.dataframe(st.session_state.inventory_df)
    st.markdown("💡 Stock levels update automatically after new orders.")

    # Show inventory log if any
    if st.session_state.inventory_log:
        st.subheader("📝 Inventory Log")
        st.dataframe(pd.DataFrame(st.session_state.inventory_log))

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan</h4>", unsafe_allow_html=True)
