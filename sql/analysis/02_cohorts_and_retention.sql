-- FileName: 02_cohorts_and_retention.sql — Cohort analysis for user retention and lifetime value.

-- 1. Monthly Cohort Matrix (Retention Rate)
SELECT 
    cohort_month,
    months_since_first_purchase,
    COUNT(customer_unique_id) as returned_customers,
    FIRST_VALUE(COUNT(customer_unique_id)) OVER (
        PARTITION BY cohort_month 
        ORDER BY months_since_first_purchase ASC
    ) as cohort_size,
    ROUND((COUNT(customer_unique_id)::DECIMAL / 
        NULLIF(FIRST_VALUE(COUNT(customer_unique_id)) OVER (
            PARTITION BY cohort_month 
            ORDER BY months_since_first_purchase ASC
        ), 0)) * 100, 2) as retention_rate_pct
FROM olist.vw_customer_monthly_metrics
GROUP BY cohort_month, months_since_first_purchase
ORDER BY cohort_month, months_since_first_purchase;

-- 2. Cumulative Lifetime Value by Cohort
SELECT 
    cohort_month,
    months_since_first_purchase,
    AVG(cumulative_lifetime_spend) as avg_cumulative_ltv,
    MAX(cumulative_lifetime_spend) as max_cumulative_ltv
FROM olist.vw_customer_monthly_metrics
GROUP BY cohort_month, months_since_first_purchase
ORDER BY cohort_month, months_since_first_purchase;
