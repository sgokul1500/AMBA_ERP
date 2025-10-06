from datetime import datetime

def validate_order(customer_name, product_name, quantity, stock_quantity):
    if not customer_name.strip():
        return False, "Customer Name is required!"
    if quantity > stock_quantity:
        return False, "Insufficient stock!"
    return True, "Order valid"

def generate_order_sql(customer_name, product_name, quantity, amount_collected, last_payment_date):
    order_sql = f"""
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
    inventory_sql = f"""
INSERT INTO InventoryLog (product_name, transaction_type, quantity, transaction_date)
VALUES (
    '{product_name}',
    'OUT',
    {quantity},
    '{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}'
);
"""
    return order_sql, inventory_sql
