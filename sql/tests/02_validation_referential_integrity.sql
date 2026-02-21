-- FileName: 02_validation_referential_integrity.sql — Asserts referential integrity constraints

-- 1. Orphan Keys: Orders without a valid Customer (Should return 0)
SELECT o.order_id, o.customer_id
FROM olist.orders o
LEFT JOIN olist.customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- 2. Orphan Keys: Order Items without a valid Order (Should return 0)
SELECT oi.order_id, oi.order_item_id
FROM olist.order_items oi
LEFT JOIN olist.orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;

-- 3. Orphan Keys: Order Items without a valid Product (Should return 0)
SELECT oi.product_id, oi.order_id
FROM olist.order_items oi
LEFT JOIN olist.products p ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

-- 4. Orphan Keys: Payments without a valid Order (Should return 0)
SELECT op.order_id, op.payment_sequential
FROM olist.order_payments op
LEFT JOIN olist.orders o ON op.order_id = o.order_id
WHERE o.order_id IS NULL;
