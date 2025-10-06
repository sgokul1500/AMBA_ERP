# ===============================
# app.py - AMBA_ERP Fun Prototype with ML Insights
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from inventory import inventory_df, orders_df, update_inventory, predict_stockout_days, detect_anomalies

st.set_page_config(
    page_title="AMBA-ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Sidebar / Navbar
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Customer Overview",
        "📝 Create New Order",
        "📦 Inventory Dashboard",
        "📈 Stockout Prediction",
        "⚠️ Anomaly Detection"
    ]
)
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
    st.dataframe(orders_df if not orders_df.empty else pd.DataFrame(columns=["Customer Name", "Product Name", "Quantity", "Amount Collected", "Last Payment Date", "Order Date"]))
    st.markdown("💡 Shows all customer order values, collections, and outstanding balances.")

# -------------------------------
# Create New Order
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
            elif quantity > inventory_df.loc[inventory_df["Product Name"] == product_name, "Stock Quantity"].values[0]:
                st.error("⚠️ Insufficient stock!")
            else:
                # Update inventory and orders
                update_inventory(product_name, quantity, customer_name, amount_collected, last_payment_date)
                
                # SQL statements (prototype)
                sql_insert_order = f"""
INSERT INTO Orders (customer_name, product_name, quantity, amount_collected, last_payment_date, order_date)
VALUES ('{customer_name}', '{product_name}', {quantity}, {amount_collected}, {'NULL' if not last_payment_date else f"'{last_payment_date}'"}, '{datetime.today().strftime('%Y-%m-%d')}');
"""
                sql_insert_inventory = f"""
INSERT INTO InventoryLog (product_name, transaction_type, quantity, transaction_date)
VALUES ('{product_name}', 'OUT', {quantity}, '{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}');
"""
                st.success("✅ Order processed successfully!")
                st.markdown("### Generated SQL Statements")
                st.code(sql_insert_order, language="sql")
                st.code(sql_insert_inventory, language="sql")

# -------------------------------
# Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(inventory_df)
    st.markdown("💡 Current stock levels for all products.")

# -------------------------------
# Stockout Prediction
# -------------------------------
# -------------------------------
# Stockout Prediction
# -------------------------------
elif page == "📈 Stockout Prediction":
    st.subheader("⏳ Inventory Stockout Prediction")
    product_selected = st.selectbox("Select Product to Predict Stockout 🏭", inventory_df["Product Name"].tolist())
    predicted_days = predict_stockout_days(product_selected)
    
    st.metric(label=f"Predicted days before {product_selected} stockout", value=predicted_days)
    
    # Correct bar chart
    stockout_chart_df = pd.DataFrame({
        "Product": [product_selected],
        "Days Remaining": [predicted_days]
    }).set_index("Product")  # Set product as index for x-axis
    
    st.bar_chart(stockout_chart_df)


# -------------------------------
# Anomaly Detection
# -------------------------------
elif page == "⚠️ Anomaly Detection":
    st.subheader("⚠️ Detect Anomalies in Orders")
    anomalies = detect_anomalies()
    if anomalies.empty:
        st.success("No anomalies detected.")
    else:
        st.warning(f"{len(anomalies)} anomalous orders detected!")
        st.dataframe(anomalies)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan</h4>", unsafe_allow_html=True)
