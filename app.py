# ===============================
# app.py - AMBA_ERP Fun Prototype with Sidebar, Stockout & Anomaly Dashboards
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import plotly.express as px
from inventory import inventory_df, orders_df, update_inventory, predict_stockout_days, detect_anomalies

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="AMBA-ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Customer Overview", "📝 Create New Order", "📦 Inventory Dashboard", "📈 Stockout Prediction", "⚠️ Anomaly Detection"])
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
    st.dataframe(orders_df if not orders_df.empty else pd.DataFrame({
        "Customer Name": ["Customer 1", "Customer 2", "Customer 3", "Customer 4", "Customer 5"],
        "Total Order Value": [167500, 105000, 37500, 75000, 30000],
        "Total Collected": [10000, 0, 0, 50000, 25000],
        "Outstanding Balance": [157500, 105000, 37500, 25000, 5000],
        "Last Payment Date": ["2025-07-30","-","-","2025-07-25","2025-07-28"]
    }))
    st.markdown("💡 Tip: Shows all customer orders, collections, and outstanding balances.")

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
            elif quantity > inventory_df.loc[inventory_df["Product Name"]==product_name, "Stock Quantity"].values[0]:
                st.error("⚠️ Insufficient stock!")
            else:
                # Update inventory and orders
                update_inventory(product_name, quantity)
                orders_df.loc[len(orders_df)] = [customer_name, product_name, quantity, amount_collected, last_payment_date, datetime.today().strftime("%Y-%m-%d")]

                # Display SQL-like output
                sql_insert_order = f"""
INSERT INTO Orders (customer_name, product_name, quantity, amount_collected, last_payment_date, order_date)
VALUES ('{customer_name}', '{product_name}', {quantity}, {amount_collected}, {'NULL' if not last_payment_date else f"'{last_payment_date}'"}, '{datetime.today().strftime('%Y-%m-%d')}');
"""
                sql_insert_inventory = f"""
INSERT INTO InventoryLog (product_name, quantity, transaction_type, transaction_date)
VALUES ('{product_name}', {quantity}, 'OUT', '{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}');
"""
                st.subheader("✅ Order Processed - SQL Statements")
                st.code(sql_insert_order, language="sql")
                st.code(sql_insert_inventory, language="sql")

# -------------------------------
# Page: Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(inventory_df[["Product Name", "Stock Quantity", "Unit Price"]])
    st.markdown("💡 Stock levels shown above are dynamically updated after each order.")

# -------------------------------
# Page: Stockout Prediction
# -------------------------------
elif page == "📈 Stockout Prediction":
    st.subheader("📈 Stockout Prediction (Next 30 Days)")
    pred_df = predict_stockout_days(days=30)
    fig = px.line(pred_df, x="Day", y=pred_df.columns[1:], labels={"value":"Stock Quantity","variable":"Product"})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 Lines show predicted stock depletion; steeper lines → faster stockout.")

# -------------------------------
# Page: Anomaly Detection
# -------------------------------
elif page == "⚠️ Anomaly Detection":
    st.subheader("⚠️ High Quantity Order Anomalies")
    anomalies = detect_anomalies(order_quantity_threshold=50)
    if anomalies.empty:
        st.success("No anomalies detected!")
    else:
        st.dataframe(anomalies)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan</h4>", unsafe_allow_html=True)
