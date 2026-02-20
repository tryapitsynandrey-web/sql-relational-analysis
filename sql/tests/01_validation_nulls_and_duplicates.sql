-- FileName: 01_validation_nulls_and_duplicates.sql — Asserts data quality dynamically via SQL queries.

-- 1. Check for Duplicate Orders (Should return 0)
SELECT 
    order_id, 
    COUNT(*) as duplicate_count
FROM olist.orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 2. Check for Duplicate Order Items (Should return 0)
SELECT 
    order_id, 
    order_item_id, 
    COUNT(*) as duplicate_count
FROM olist.order_items
GROUP BY order_id, order_item_id
HAVING COUNT(*) > 1;

-- 3. Check for NULL Values in Critical Fields (Customers) (Should return 0)
SELECT COUNT(*) as missing_customer_ids
FROM olist.customers
WHERE customer_id IS NULL;

-- 4. Check for NULL Values in Critical Fields (Orders) (Should return 0)
SELECT COUNT(*) as missing_purchases
FROM olist.orders
WHERE order_purchase_timestamp IS NULL
OR customer_id IS NULL;
