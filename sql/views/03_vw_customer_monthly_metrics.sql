-- FileName: 03_vw_customer_monthly_metrics.sql — Monthly summarized activity per customer.

DROP VIEW IF EXISTS olist.vw_customer_monthly_metrics CASCADE;

CREATE VIEW olist.vw_customer_monthly_metrics AS
WITH monthly_activity AS (
    SELECT 
        c.customer_unique_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) as activity_month,
        SUM(p.payment_value) as spend_this_month
    FROM olist.orders o
    JOIN olist.customers c ON o.customer_id = c.customer_id
    LEFT JOIN olist.order_payments p ON o.order_id = p.order_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY c.customer_unique_id, DATE_TRUNC('month', o.order_purchase_timestamp)
),
cohort_base AS (
    SELECT 
        customer_unique_id,
        activity_month,
        spend_this_month,
        MIN(activity_month) OVER (PARTITION BY customer_unique_id) as cohort_month
    FROM monthly_activity
)
SELECT 
    customer_unique_id,
    -- Running total lifetime spend
    SUM(spend_this_month) OVER (
        PARTITION BY customer_unique_id 
        ORDER BY activity_month ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as cumulative_lifetime_spend,
    -- First purchase month for cohort grouping
    cohort_month,
    -- Months since first purchase
    EXTRACT(year FROM age(activity_month, cohort_month)) * 12 +
    EXTRACT(month FROM age(activity_month, cohort_month)) as months_since_first_purchase
FROM cohort_base;
