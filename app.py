# ===============================
# app.py - AMBA_ERP Fun Prototype with Stock Prediction & Anomaly Detection
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import plotly.express as px

from inventory import load_inventory, load_orders, update_inventory, predict_stockout_days, detect_anomalies

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="AMBA-ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Load Data
# -------------------------------
if "inventory" not in st.session_state:
    st.session_state["inventory"] = load_inventory()
if "orders" not in st.session_state:
    st.session_state["orders"] = load_orders()

# -------------------------------
# Sidebar / Navbar
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Customer Overview",
    "📝 Create New Order",
    "📦 Inventory Dashboard",
    "📈 Stockout Prediction",
    "🚨 Anomaly Detection"
])
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
    st.dataframe(st.session_state["orders"])
    st.markdown("💡 Tip: Shows all orders submitted by customers.")

# -------------------------------
# Page: Create New Order
# -------------------------------
elif page == "📝 Create New Order":
    st.subheader("🛒 Create a New Sales Order")
    products = st.session_state["inventory"]["Product Name"].tolist()

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
                # Update inventory dynamically
                st.session_state["inventory"] = update_inventory(st.session_state["inventory"], product_name, quantity)

                # Append order
                new_order = pd.DataFrame([{
                    "customer_name": customer_name,
                    "product_name": product_name,
                    "quantity": quantity,
                    "amount_collected": amount_collected,
                    "last_payment_date": last_payment_date,
                    "order_date": datetime.today().strftime("%Y-%m-%d")
                }])
                st.session_state["orders"] = pd.concat([st.session_state["orders"], new_order], ignore_index=True)

                # Display SQL (prototype)
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

# -------------------------------
# Page: Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(st.session_state["inventory"])
    st.markdown("💡 Current stock quantities.")

# -------------------------------
# Page: Stockout Prediction
# -------------------------------
elif page == "📈 Stockout Prediction":
    st.subheader("📈 Inventory Stockout Prediction")
    stock_sim = predict_stockout_days(st.session_state["inventory"], st.session_state["orders"], days_ahead=30)
    fig = px.line(stock_sim, x="Day", y="Stock", color="Product",
                  labels={"Stock":"Remaining Stock", "Day":"Days Ahead"},
                  title="Projected Stock Levels Over Time")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 Lines show projected stock depletion per product based on recent orders.")

# -------------------------------
# Page: Anomaly Detection
# -------------------------------
elif page == "🚨 Anomaly Detection":
    st.subheader("🚨 Transaction Anomalies")
    anomalies_df = detect_anomalies(st.session_state["orders"])
    st.dataframe(anomalies_df)
    st.markdown("💡 Orders flagged as 'Anomaly = True' are unusually large compared to median quantities.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan</h4>", unsafe_allow_html=True)
