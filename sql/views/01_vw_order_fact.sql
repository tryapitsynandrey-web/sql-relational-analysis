-- FileName: 01_vw_order_fact.sql — Order-level grain view integrating total value and customer status.

DROP VIEW IF EXISTS olist.vw_order_fact CASCADE;

CREATE VIEW olist.vw_order_fact AS
WITH order_value AS (
    SELECT 
        order_id,
        SUM(price + freight_value) as total_order_value
    FROM olist.order_items
    GROUP BY order_id
)
SELECT 
    o.order_id,
    c.customer_unique_id,
    o.order_status,
    o.order_purchase_timestamp,
    COALESCE(v.total_order_value, 0) as total_order_value,
    c.customer_state
FROM olist.orders o
LEFT JOIN olist.customers c ON o.customer_id = c.customer_id
LEFT JOIN order_value v ON o.order_id = v.order_id;
