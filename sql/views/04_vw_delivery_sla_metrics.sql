-- FileName: 04_vw_delivery_sla_metrics.sql — SLA view calculating delivery times, delays, and estimates.

DROP VIEW IF EXISTS olist.vw_delivery_sla_metrics CASCADE;

CREATE VIEW olist.vw_delivery_sla_metrics AS
SELECT 
    order_id,
    customer_id,
    order_status,
    -- Calculate Actual Delivery Time (Days)
    EXTRACT(EPOCH FROM (order_delivered_customer_date - order_purchase_timestamp))/86400.0 as actual_delivery_days,
    -- Calculate Estimated Delivery Time (Days)
    EXTRACT(EPOCH FROM (order_estimated_delivery_date - order_purchase_timestamp))/86400.0 as estimated_delivery_days,
    -- Calculate Delay (Positive means delayed, Negative means early)
    EXTRACT(EPOCH FROM (order_delivered_customer_date - order_estimated_delivery_date))/86400.0 as delay_vs_estimate_days,
    -- Boolean flags for SLA grouping
    CASE 
        WHEN order_delivered_customer_date > order_estimated_delivery_date THEN true
        ELSE false
    END as is_delayed
FROM olist.orders
-- Only consider orders that are meant to be delivered or are in process
WHERE order_status NOT IN ('canceled', 'unavailable');
