-- FileName: 01_revenue_and_aov_behavior.sql — Analyzes overall revenue, AOV, and top performing categories.

-- 1. Total Revenue and Average Order Value (AOV) by Month
SELECT 
    DATE_TRUNC('month', order_purchase_timestamp) as revenue_month,
    COUNT(order_id) as total_orders,
    SUM(total_order_value) as total_revenue,
    SUM(total_order_value) / NULLIF(COUNT(order_id), 0) as average_order_value
FROM olist.vw_order_fact
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp)
ORDER BY revenue_month;

-- 2. Top 10 Product Categories by Total Revenue
SELECT 
    category_english,
    COUNT(DISTINCT order_id) as orders_sold,
    SUM(total_item_value) as total_revenue,
    SUM(total_item_value) / NULLIF(COUNT(DISTINCT order_id), 0) as average_item_value
FROM olist.vw_item_fact
WHERE order_status = 'delivered'
  AND category_english IS NOT NULL
GROUP BY category_english
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. Top 10 States by GMV (Gross Merchandise Value)
SELECT 
    customer_state,
    COUNT(DISTINCT customer_unique_id) as unique_customers,
    COUNT(order_id) as total_orders,
    SUM(total_order_value) as gmv
FROM olist.vw_order_fact
WHERE order_status = 'delivered'
GROUP BY customer_state
ORDER BY gmv DESC
LIMIT 10;
