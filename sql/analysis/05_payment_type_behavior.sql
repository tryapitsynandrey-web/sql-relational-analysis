-- FileName: 05_payment_type_behavior.sql — Analyzing payment preferences and cancellation correlations.

-- 1. Payment Method Popularity and Average Value
SELECT 
    payment_type,
    COUNT(DISTINCT order_id) as total_orders_used,
    SUM(payment_value) as total_payment_value,
    AVG(payment_value) as avg_transaction_value,
    AVG(payment_installments) as avg_installments
FROM olist.order_payments
GROUP BY payment_type
ORDER BY total_orders_used DESC;

-- 2. Cancellation Rate by Payment Type
WITH order_payment_types AS (
    SELECT DISTINCT order_id, payment_type
    FROM olist.order_payments
)
SELECT 
    p.payment_type,
    COUNT(*) as total_orders,
    COUNT(*) FILTER (WHERE o.order_status = 'canceled') as canceled_orders,
    ROUND((COUNT(*) FILTER (WHERE o.order_status = 'canceled')::DECIMAL / 
        NULLIF(COUNT(*), 0)) * 100, 2) as cancellation_rate_pct
FROM order_payment_types p
JOIN olist.orders o ON p.order_id = o.order_id
GROUP BY p.payment_type
HAVING COUNT(*) > 100
ORDER BY cancellation_rate_pct DESC;
