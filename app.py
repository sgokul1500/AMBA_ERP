# ===============================
# app.py - AMBA_ERP Fun Prototype with Resettable State
# ===============================

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from inventory import load_inventory, load_orders, update_inventory, predict_stockout_days, detect_anomalies

# -------------------------------
# 1. Page Config
# -------------------------------
st.set_page_config(
    page_title="AMBA-ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# 2. Load Original Data
# -------------------------------
if "inventory" not in st.session_state:
    st.session_state["inventory"] = load_inventory()

if "orders" not in st.session_state:
    st.session_state["orders"] = load_orders()

# -------------------------------
# 3. Sidebar / Navbar
# -------------------------------
st.sidebar.title("🛠 Amba ERP Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Customer Overview", "📝 Create New Order",
                                   "📦 Inventory Dashboard", "📈 Stockout Prediction",
                                   "⚠️ Anomaly Detection"])

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset App"):
    st.session_state.clear()
    st.experimental_rerun()

# -------------------------------
# 4. Header
# -------------------------------
st.markdown("<h1 style='text-align: center; color: #4B0082;'>Amba ERP Prototype</h1>", unsafe_allow_html=True)

# -------------------------------
# 5. Customer Overview
# -------------------------------
if page == "🏠 Customer Overview":
    st.subheader("📊 Customer Overview")
    st.dataframe(st.session_state["orders"])
    st.markdown("💡 Shows all customer orders and payments.")

# -------------------------------
# 6. Create New Order
# -------------------------------
elif page == "📝 Create New Order":
    st.subheader("🛒 Create a New Sales Order")
    products = st.session_state["inventory"]["Product Name"].tolist()

    with st.form("new_order_form"):
        customer_name = st.text_input("Customer Name 🧑‍💼")
        product_name = st.selectbox("Select Product 🏭", products)
        quantity = st.number_input("Quantity 🔢", min_value=1, value=1)
        amount_collected = st.number_input("Amount Collected 💵", min_value=0.0, value=0.0, step=0.01)
        last_payment_date = st.date_input("Last Payment Date 📅 (Optional)", value=None)

        submitted = st.form_submit_button("🚀 Submit Order")

        if submitted:
            if not customer_name.strip():
                st.error("⚠️ Customer Name is required!")
            else:
                # Update Inventory
                st.session_state["inventory"] = update_inventory(
                    st.session_state["inventory"], product_name, quantity
                )

                # Record Order
                st.session_state["orders"] = st.session_state["orders"].append({
                    "customer_name": customer_name,
                    "product_name": product_name,
                    "quantity": quantity,
                    "amount_collected": amount_collected,
                    "last_payment_date": last_payment_date,
                    "order_date": datetime.today()
                }, ignore_index=True)

                # Display SQL
                sql_insert_order = f"""
INSERT INTO Orders (customer_name, product_name, quantity, amount_collected, last_payment_date, order_date)
VALUES ('{customer_name}', '{product_name}', {quantity}, {amount_collected}, {'NULL' if not last_payment_date else f"'{last_payment_date}'"}, '{datetime.today().strftime('%Y-%m-%d')}');
"""
                st.subheader("✅ Order Recorded (Prototype)")
                st.code(sql_insert_order, language="sql")

# -------------------------------
# 7. Inventory Dashboard
# -------------------------------
elif page == "📦 Inventory Dashboard":
    st.subheader("📦 Inventory Dashboard")
    st.dataframe(st.session_state["inventory"])
    st.markdown("💡 Updated in real-time as orders are placed.")

# -------------------------------
# 8. Stockout Prediction
# -------------------------------
elif page == "📈 Stockout Prediction":
    st.subheader("📈 Stockout Prediction (Days to Depletion)")
    predictions = predict_stockout_days(st.session_state["inventory"], st.session_state["orders"])
    pred_df = pd.DataFrame({
        "Product Name": list(predictions.keys()),
        "Days to Stockout": list(predictions.values())
    })
    st.line_chart(pred_df.set_index("Product Name"))

# -------------------------------
# 9. Anomaly Detection
# -------------------------------
elif page == "⚠️ Anomaly Detection":
    st.subheader("⚠️ Anomaly Detection in Orders")
    anomalies = detect_anomalies(st.session_state["orders"])
    st.dataframe(anomalies)

# -------------------------------
# 10. Footer
# -------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #FF1493;'>Developed by Gokul Srinivasan</h4>", unsafe_allow_html=True)
