-- FileName: 01_bulk_insert_data.sql — Inserts CSV data using psql \copy command

\copy olist.customers(customer_id,customer_unique_id,customer_zip_code_prefix,customer_city,customer_state) FROM '/project/data/raw/olist/olist_customers_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

\copy olist.products(product_id,product_category_name,product_name_lenght,product_description_lenght,product_photos_qty,product_weight_g,product_length_cm,product_height_cm,product_width_cm) FROM '/project/data/raw/olist/olist_products_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

\copy olist.sellers(seller_id,seller_zip_code_prefix,seller_city,seller_state) FROM '/project/data/raw/olist/olist_sellers_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

\copy olist.category_name_translation(product_category_name,product_category_name_english) FROM '/project/data/raw/olist/product_category_name_translation.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

\copy olist.orders(order_id,customer_id,order_status,order_purchase_timestamp,order_approved_at,order_delivered_carrier_date,order_delivered_customer_date,order_estimated_delivery_date) FROM '/project/data/raw/olist/olist_orders_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

\copy olist.order_items(order_id,order_item_id,product_id,seller_id,shipping_limit_date,price,freight_value) FROM '/project/data/raw/olist/olist_order_items_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

\copy olist.order_payments(order_id,payment_sequential,payment_type,payment_installments,payment_value) FROM '/project/data/raw/olist/olist_order_payments_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

\copy olist.order_reviews(review_id,order_id,review_score,review_comment_title,review_comment_message,review_creation_date,review_answer_timestamp) FROM '/project/data/raw/olist/olist_order_reviews_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');