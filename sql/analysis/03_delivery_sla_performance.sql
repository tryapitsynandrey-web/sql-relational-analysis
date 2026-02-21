-- FileName: 03_delivery_sla_performance.sql — Evaluates delivery performance, delays, and estimates.

-- 1. Overall SLA Performance (On-time vs Delayed)
SELECT 
    COUNT(*) as total_deliveries,
    COUNT(*) FILTER (WHERE is_delayed) as total_delayed_orders,
    ROUND((COUNT(*) FILTER (WHERE is_delayed)::DECIMAL / 
        NULLIF(COUNT(*), 0)) * 100, 2) as delayed_rate_pct,
    AVG(actual_delivery_days) as avg_actual_delivery_days,
    AVG(estimated_delivery_days) as avg_estimated_delivery_days
FROM olist.vw_delivery_sla_metrics
WHERE order_status = 'delivered';

-- 2. Average Delay by State
SELECT 
    c.customer_state,
    COUNT(*) as total_deliveries,
    COUNT(*) FILTER (WHERE s.is_delayed) as delayed_orders,
    ROUND((COUNT(*) FILTER (WHERE s.is_delayed)::DECIMAL / 
        NULLIF(COUNT(*), 0)) * 100, 2) as delayed_rate_pct,
    AVG(s.delay_vs_estimate_days) FILTER (WHERE s.is_delayed) as avg_delay_days_when_delayed
FROM olist.vw_delivery_sla_metrics s
JOIN olist.customers c ON s.customer_id = c.customer_id
WHERE s.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY delayed_rate_pct DESC;
