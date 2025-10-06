import streamlit as st
from datetime import datetime
import time
import pandas as pd

# Import backend modules
from order import validate_order, generate_order_sql
from inventory import get_inventory, check_stock
from customers import load_customers, get_customer_list

st.set_page_config(page_title="AMBA-ERP", layout="wide", initial_sidebar_state="expanded")

# -------------------------------
# Load Data
# -------------------------------
customer_df = load_customers()
inventory_df = get_inventory()
product_list = inventory_df["Product Name"].tolist()

# -------------------------------
# Sidebar
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
# Customer Overview
# -------------------------------
if page == "🏠 Customer Overview":
    st.subheader("📊 Customer Overview")
    st.dataframe(customer_df)
    st.markdown("💡 Shows all customer order values, collections, and outstanding balances.")

# -------------------------------
# Create New Order
# -------------------------------
elif page == "📝 Create New Order":
    st.subheader("🛒 Create a New Sales Order")

    with st.form("new_order_form"):
        customer_name = st.text_input("Customer Name 🧑‍💼")
        product_name = st.selectbox("Select Product 🏭", product_list)
        quantity = st.number_input("Quantity 🔢", min_value=1, value=1)
        amount_collected = st.number_input("Amount Collected 💵", min_value=0.0, value=0.0, step=0.01)
        last_payment_date = st.date_input("Last Payment Date 📅 (Optional)", value=None)

        submitted = st.form_submit_button("🚀 Submit Order")

        if submitted:
            # Check stock availability
            stock_ok, stock_qty = check_stock(product_name, quantity, inventory_df)
            
            # Validate order
            valid, msg = validate_order(customer_name, product_name, quantity, stock_qty)
            if not valid:
                st.error(f"⚠️ {msg}")
            else:
                with st.spinner("Processing your order... ⏳"):
                    for percent in range(0, 101, 10):
                        time.sleep(0.05)
                        st.progress(percent)

                # Generate SQL
                order_sql, inventory_sql = generate_order_sql(customer_name, product_name, quantity, amount_collected, last_payment_date)

                st.success("✅ Order validated successfully!")
                st.code(order_sql, language="sql")
                st.code(inventory_sql, language="sql")
                st.balloons()

# -------------------------------
# Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(inventory_df)
    st.markdown("💡 Stock levels shown as plain numbers for simplicity.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan</h4>", unsafe_allow_html=True)
