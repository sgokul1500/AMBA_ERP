# ===============================
# app.py - AMBA_ERP Fun Prototype with Interactive Sidebar/Navbar
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from inventory import (
    inventory_df,
    orders_df,
    update_inventory,
    predict_stockout_days,
    detect_anomalies
)

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="AMBA-ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Initialize Session State
# -------------------------------
if "orders" not in st.session_state:
    st.session_state["orders"] = orders_df.copy()
if "inventory" not in st.session_state:
    st.session_state["inventory"] = inventory_df.copy()

# -------------------------------
# Sidebar / Navbar
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🏠 Customer Overview", "📝 Create New Order", "📦 Inventory Dashboard",
     "📈 Stockout Prediction", "🚨 Anomaly Detection"]
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
    st.dataframe(st.session_state["orders"])
    st.markdown(
        "💡 Tip: This shows all customer order values, collections, and outstanding balances."
    )

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
            elif quantity > st.session_state["inventory"].loc[
                st.session_state["inventory"]["Product Name"] == product_name, "Stock Quantity"
            ].values[0]:
                st.error("⚠️ Insufficient stock for the selected product!")
            else:
                with st.spinner("Processing your order... ⏳"):
                    time.sleep(0.5)

                # SQL INSERT statement (Prototype)
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
                # Update Inventory & Orders in Session
                # -------------------------------
                st.session_state["inventory"] = update_inventory(
                    st.session_state["inventory"], product_name, quantity
                )

                new_order = pd.DataFrame([{
                    "customer_name": customer_name,
                    "product_name": product_name,
                    "quantity": quantity,
                    "amount_collected": amount_collected,
                    "last_payment_date": last_payment_date,
                    "order_date": datetime.today()
                }])
                st.session_state["orders"] = pd.concat(
                    [st.session_state["orders"], new_order], ignore_index=True
                )

# -------------------------------
# Page: Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(st.session_state["inventory"])
    st.markdown("💡 Stock levels shown as plain numbers for simplicity.")

# -------------------------------
# Page: Stockout Prediction
# -------------------------------
elif page == "📈 Stockout Prediction":
    st.subheader("📈 Inventory Stockout Prediction")
    predicted_days = predict_stockout_days(st.session_state["inventory"], st.session_state["orders"])
    st.line_chart(predicted_days.set_index("Product Name")["Predicted Stockout Days"])
    st.markdown("💡 Predicted days until stockout based on order trends.")

# -------------------------------
# Page: Anomaly Detection
# -------------------------------
elif page == "🚨 Anomaly Detection":
    st.subheader("🚨 Anomaly Detection in Transactions")
    anomalies = detect_anomalies(st.session_state["orders"])
    if anomalies.empty:
        st.success("✅ No anomalies detected!")
    else:
        st.dataframe(anomalies)
        st.markdown("⚠️ Highlighted transactions have unusual quantities or collection amounts.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown(
    "<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan</h4>",
    unsafe_allow_html=True
)
