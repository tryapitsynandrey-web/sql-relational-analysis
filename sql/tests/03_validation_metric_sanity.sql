-- FileName: 03_validation_metric_sanity.sql — Asserts sanity checks for core metrics

-- 1. Check for Negative Prices or Freight in Order Items (Should return 0)
SELECT COUNT(*) as negative_price_items
FROM olist.order_items
WHERE price < 0 OR freight_value < 0;

-- 2. Check for Negative Payment Values (Should return 0)
SELECT COUNT(*) as negative_payments
FROM olist.order_payments
WHERE payment_value < 0;

-- 3. Time Travel Check: Delivery before Purchase (Should return 0)
SELECT order_id, order_purchase_timestamp, order_delivered_customer_date
FROM olist.orders
WHERE order_delivered_customer_date < order_purchase_timestamp;

-- 4. Invalid Review Scores (must be 1-5) (Should return 0)
SELECT review_id, review_score
FROM olist.order_reviews
WHERE review_score NOT IN (1, 2, 3, 4, 5);
