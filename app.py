# ===============================
# app.py - AMBA_ERP Fun Prototype with Analytics Dashboards
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
from inventory import inventory_df, orders_df, update_inventory, predict_stockout_days, detect_anomalies

st.set_page_config(
    page_title="AMBA-ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Initialize Session State
# -------------------------------
if "inventory_df" not in st.session_state:
    st.session_state.inventory_df = inventory_df.copy()

if "orders_df" not in st.session_state:
    st.session_state.orders_df = orders_df.copy()

# -------------------------------
# Sidebar / Navbar
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🏠 Customer Overview", "📝 Create New Order", "📦 Inventory Dashboard", "📈 Stockout Prediction", "🚨 Anomaly Detection"]
)
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
    st.dataframe(st.session_state.orders_df)
    st.markdown("💡 Shows all customer orders and payments.")

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
        last_payment_date = st.date_input("Last Payment Date 📅 (Optional)")

        submitted = st.form_submit_button("🚀 Submit Order")

        if submitted:
            if not customer_name.strip():
                st.error("⚠️ Customer Name is required!")
            else:
                # Update inventory
                st.session_state.inventory_df = update_inventory(product_name, quantity)

                # Add new order
                new_order = pd.DataFrame([{
                    "Customer Name": customer_name,
                    "Product Name": product_name,
                    "Quantity": quantity,
                    "Amount Collected": amount_collected,
                    "Last Payment Date": last_payment_date if last_payment_date else "",
                    "Order Date": datetime.today().date()
                }])
                st.session_state.orders_df = pd.concat([st.session_state.orders_df, new_order], ignore_index=True)

                # Generate SQL
                sql_insert_order = f"""
INSERT INTO Orders (customer_name, product_name, quantity, amount_collected, last_payment_date, order_date)
VALUES ('{customer_name}', '{product_name}', {quantity}, {amount_collected}, {'NULL' if not last_payment_date else f"'{last_payment_date}'"}, '{datetime.today().strftime('%Y-%m-%d')}');
"""
                st.success("✅ Order validated successfully!")
                st.code(sql_insert_order, language="sql")

# -------------------------------
# Page: Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(st.session_state.inventory_df)
    st.markdown("💡 Stock levels dynamically update as orders are placed.")

# -------------------------------
# Page: Stockout Prediction
# -------------------------------
elif page == "📈 Stockout Prediction":
    st.subheader("⏳ Inventory Stockout Prediction")
    product = st.selectbox("Select Product for Prediction", st.session_state.inventory_df["Product Name"].tolist())
    days_left = predict_stockout_days(product)
    st.metric(label=f"Days until stockout for {product}", value=f"{days_left} days")
    # Stock trend chart
    st.line_chart(st.session_state.inventory_df.set_index("Product Name")["Stock Quantity"])

# -------------------------------
# Page: Anomaly Detection
# -------------------------------
elif page == "🚨 Anomaly Detection":
    st.subheader("⚠️ Detecting Anomalies in Transactions")
    anomalies = detect_anomalies()
    if anomalies.empty:
        st.success("No anomalies detected in current transactions.")
    else:
        st.dataframe(anomalies)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan </h4>", unsafe_allow_html=True)
