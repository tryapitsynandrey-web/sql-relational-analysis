-- FileName: 03_add_constraints.sql — Applies primary keys, foreign keys, and indexes.

-- Add Primary Keys
ALTER TABLE olist.customers ADD CONSTRAINT pk_customers PRIMARY KEY (customer_id);
ALTER TABLE olist.products ADD CONSTRAINT pk_products PRIMARY KEY (product_id);
ALTER TABLE olist.sellers ADD CONSTRAINT pk_sellers PRIMARY KEY (seller_id);
ALTER TABLE olist.category_name_translation ADD CONSTRAINT pk_category_translation PRIMARY KEY (product_category_name);
ALTER TABLE olist.orders ADD CONSTRAINT pk_orders PRIMARY KEY (order_id);
ALTER TABLE olist.order_items ADD CONSTRAINT pk_order_items PRIMARY KEY (order_id, order_item_id);
-- Payments can have multiple sequential payments per order, combining for uniqueness
ALTER TABLE olist.order_payments ADD CONSTRAINT pk_order_payments PRIMARY KEY (order_id, payment_sequential);
-- Reviews could potentially be duplicated per order in edge cases, but combining review_id and order_id ensures strict uniqueness
ALTER TABLE olist.order_reviews ADD CONSTRAINT pk_order_reviews PRIMARY KEY (review_id, order_id);

-- Add Foreign Keys
ALTER TABLE olist.orders 
    ADD CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id) 
    REFERENCES olist.customers(customer_id);

ALTER TABLE olist.order_items 
    ADD CONSTRAINT fk_items_orders FOREIGN KEY (order_id) 
    REFERENCES olist.orders(order_id);

ALTER TABLE olist.order_items 
    ADD CONSTRAINT fk_items_products FOREIGN KEY (product_id) 
    REFERENCES olist.products(product_id);

ALTER TABLE olist.order_items 
    ADD CONSTRAINT fk_items_sellers FOREIGN KEY (seller_id) 
    REFERENCES olist.sellers(seller_id);

ALTER TABLE olist.order_payments 
    ADD CONSTRAINT fk_payments_orders FOREIGN KEY (order_id) 
    REFERENCES olist.orders(order_id);

ALTER TABLE olist.order_reviews 
    ADD CONSTRAINT fk_reviews_orders FOREIGN KEY (order_id) 
    REFERENCES olist.orders(order_id);

-- Indexes for performance on Analytical Queries
CREATE INDEX idx_orders_customer_id ON olist.orders(customer_id);
CREATE INDEX idx_orders_status_date ON olist.orders(order_status, order_purchase_timestamp);
CREATE INDEX idx_items_product_id ON olist.order_items(product_id);
CREATE INDEX idx_reviews_order_id ON olist.order_reviews(order_id);
