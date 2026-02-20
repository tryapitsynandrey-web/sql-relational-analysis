-- FileName: 02_vw_item_fact.sql — Item-level grain view for detailed product analysis.

DROP VIEW IF EXISTS olist.vw_item_fact CASCADE;

CREATE VIEW olist.vw_item_fact AS
SELECT 
    i.order_id,
    (i.price + i.freight_value) as total_item_value,
    o.order_status,
    COALESCE(t.product_category_name_english, p.product_category_name) as category_english
FROM olist.order_items i
INNER JOIN olist.orders o ON i.order_id = o.order_id
LEFT JOIN olist.products p ON i.product_id = p.product_id
LEFT JOIN olist.category_name_translation t ON p.product_category_name = t.product_category_name;
