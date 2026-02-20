-- FileName: 02_create_tables.sql — Creates tables with native PostgreSQL types.

-- Customers
DROP TABLE IF EXISTS olist.customers CASCADE;
CREATE TABLE olist.customers (
    customer_id VARCHAR(50) NOT NULL,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(100),
    customer_state VARCHAR(5)
);

-- Products
DROP TABLE IF EXISTS olist.products CASCADE;
CREATE TABLE olist.products (
    product_id VARCHAR(50) NOT NULL,
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);

-- Sellers
DROP TABLE IF EXISTS olist.sellers CASCADE;
CREATE TABLE olist.sellers (
    seller_id VARCHAR(50) NOT NULL,
    seller_zip_code_prefix VARCHAR(10),
    seller_city VARCHAR(100),
    seller_state VARCHAR(5)
);

-- Category Name Translation
DROP TABLE IF EXISTS olist.category_name_translation CASCADE;
CREATE TABLE olist.category_name_translation (
    product_category_name VARCHAR(100) NOT NULL,
    product_category_name_english VARCHAR(100)
);

-- Orders
DROP TABLE IF EXISTS olist.orders CASCADE;
CREATE TABLE olist.orders (
    order_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

-- Order Items
DROP TABLE IF EXISTS olist.order_items CASCADE;
CREATE TABLE olist.order_items (
    order_id VARCHAR(50) NOT NULL,
    order_item_id INT NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    seller_id VARCHAR(50) NOT NULL,
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10, 2),
    freight_value NUMERIC(10, 2)
);

-- Order Payments
DROP TABLE IF EXISTS olist.order_payments CASCADE;
CREATE TABLE olist.order_payments (
    order_id VARCHAR(50) NOT NULL,
    payment_sequential INT NOT NULL,
    payment_type VARCHAR(20),
    payment_installments INT,
    payment_value NUMERIC(10, 2)
);

-- Order Reviews
DROP TABLE IF EXISTS olist.order_reviews CASCADE;
CREATE TABLE olist.order_reviews (
    review_id VARCHAR(50) NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    review_score INT NOT NULL,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);
