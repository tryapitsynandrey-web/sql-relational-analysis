-- FileName: 04_vw_delivery_sla_metrics.sql — SLA view calculating delivery times, delays, and estimates.

DROP VIEW IF EXISTS olist.vw_delivery_sla_metrics CASCADE;

CREATE VIEW olist.vw_delivery_sla_metrics AS
SELECT 
    order_id,
    customer_id,
    order_status,
    -- Elapsed days from purchase to customer receipt; NULL for undelivered orders.
    EXTRACT(EPOCH FROM (order_delivered_customer_date - order_purchase_timestamp))/86400.0 as actual_delivery_days,
    -- Days from purchase to the promised delivery date; used as the SLA baseline.
    EXTRACT(EPOCH FROM (order_estimated_delivery_date - order_purchase_timestamp))/86400.0 as estimated_delivery_days,
    -- Positive values indicate SLA breach; negative values indicate early delivery.
    EXTRACT(EPOCH FROM (order_delivered_customer_date - order_estimated_delivery_date))/86400.0 as delay_vs_estimate_days,
    -- Boolean SLA flag; TRUE when customer received the order after the committed date.
    CASE 
        WHEN order_delivered_customer_date > order_estimated_delivery_date THEN true
        ELSE false
    END as is_delayed
FROM olist.orders
-- Only consider orders that are meant to be delivered or are in process
WHERE order_status NOT IN ('canceled', 'unavailable');
