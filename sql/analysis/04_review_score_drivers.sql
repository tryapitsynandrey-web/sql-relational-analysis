-- FileName: 04_review_score_drivers.sql — Correlating review scores with delivery times and products.

-- 1. Distribution of Review Scores
SELECT 
    review_score,
    COUNT(review_id) as total_reviews,
    ROUND((COUNT(review_id)::DECIMAL / SUM(COUNT(review_id)) OVER ()) * 100, 2) as pct_of_total
FROM olist.order_reviews
GROUP BY review_score
ORDER BY review_score DESC;

-- 2. Average Review Score by Delivery Performance (Delayed vs On-Time)
SELECT 
    CASE WHEN d.is_delayed THEN 'Delayed' ELSE 'On-Time' END as delivery_status,
    COUNT(r.review_id) as total_reviews,
    AVG(r.review_score) as avg_review_score
FROM olist.order_reviews r
JOIN olist.vw_delivery_sla_metrics d ON r.order_id = d.order_id
WHERE d.order_status = 'delivered'
GROUP BY CASE WHEN d.is_delayed THEN 'Delayed' ELSE 'On-Time' END;

-- 3. Bottom 10 Product Categories by Review Score (Min 50 orders)
WITH order_avg_review AS (
    SELECT order_id, AVG(review_score) as avg_score
    FROM olist.order_reviews
    GROUP BY order_id
),
order_categories AS (
    SELECT DISTINCT order_id, category_english
    FROM olist.vw_item_fact
    WHERE category_english IS NOT NULL
)
SELECT 
    c.category_english,
    COUNT(c.order_id) as total_orders,
    AVG(r.avg_score) as avg_review_score
FROM order_categories c
JOIN order_avg_review r ON c.order_id = r.order_id
GROUP BY c.category_english
HAVING COUNT(c.order_id) >= 50
ORDER BY avg_review_score ASC
LIMIT 10;
