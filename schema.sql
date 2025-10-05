-- ===============================
-- SCHEMA FOR AMBA_ERP SYSTEM
-- ===============================

-- ===============================
-- 1. Customers Table (Master Data)
-- ===============================
CREATE TABLE Customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional index for faster lookup by name
CREATE INDEX idx_customer_name ON Customers(customer_name);

-- ===============================
-- 2. Products Table (Master Data / Inventory)
-- ===============================
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE,
    unit_price NUMERIC(12,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster searches by product name
CREATE INDEX idx_product_name ON Products(product_name);

-- ===============================
-- 3. Orders Table (Transactional Data)
-- ===============================
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    order_value NUMERIC(12,2) NOT NULL,
    amount_collected NUMERIC(12,2) DEFAULT 0,
    balance_amount NUMERIC(12,2) AS (order_value - amount_collected) STORED,
    last_payment_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Index for faster queries by customer
CREATE INDEX idx_orders_customer_id ON Orders(customer_id);

-- ===============================
-- 4. InventoryLog Table (Stock Ledger)
-- ===============================
CREATE TABLE InventoryLog (
    log_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    transaction_type VARCHAR(50) NOT NULL, -- 'IN' for stock received, 'OUT' for stock sold
    quantity INT NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reference_order_id INT, -- link to Orders table if applicable
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (reference_order_id) REFERENCES Orders(order_id)
);

-- Index for faster product transaction history queries
CREATE INDEX idx_inventorylog_product_id ON InventoryLog(product_id);

-- ===============================
-- 5. Optional Payment History Table
-- (if you want to track multiple payments per order)
-- ===============================
CREATE TABLE Payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    payment_amount NUMERIC(12,2) NOT NULL,
    payment_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Index for faster queries by order
CREATE INDEX idx_payments_order_id ON Payments(order_id);

