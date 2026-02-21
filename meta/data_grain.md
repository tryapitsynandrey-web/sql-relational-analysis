# Data Grain Definition

## Core Table Grain
*   `olist.orders`: **1 row per discrete transaction** (identified by `order_id`).
*   `olist.order_items`: **1 row per physical product shipped** within an order (identified by `order_id` + `order_item_id`).
*   `olist.order_payments`: **1 row per payment method** applied to an order (identified by `order_id` + `payment_sequential`).
*   `olist.order_reviews`: **1 row per customer review** (identified by `review_id` + `order_id`).
*   `olist.customers`: **1 row per order-specific customer profile** (identified by `customer_id`). Distinct from `customer_unique_id` which tracks humans across multiple orders.

## View Grain
*   `vw_order_fact`: **1 row per order**. Resolves fan-out risks by pre-aggregating total purchase and freight values before joining to customer details.
*   `vw_item_fact`: **1 row per order item**. Enriches the raw item line with human-readable categories and parent order status.
*   `vw_customer_monthly_metrics`: **1 row per customer (`customer_unique_id`) per active calendar month**.
*   `vw_delivery_sla_metrics`: **1 row per order**. Evaluates day-level deltas between estimated and actual delivery timestamps.

## Analysis Query Grain
*   `01_revenue_and_aov.sql`: **1 row per reporting dimension** (e.g., 1 row per Month, 1 row per Category, 1 row per State).
*   `02_cohorts_and_retention.sql`: **1 row per cohort-month + months-since-first-purchase tuple**.
*   `03_delivery_sla_performance.sql`: **1 row for global aggregates**, or **1 row per customer state** for geo-specific SLA tracking.
*   `04_review_score_drivers.sql`: **1 row per categorical bucket** (e.g., Score 1-5, Delayed/On-Time, Category Name).
*   `05_payment_type_behavior.sql`: **1 row per physical payment type** (e.g., credit_card, boleto).

## Rationale
Explicitly defining grain prevents the most common SQL analytics error: Cartesian fan-out (double counting). For example, joining `order_items` directly to `order_payments` would multiply total revenue by the number of items and payment methods. The view layer abstracts these risks, ensuring downstream analytical queries operate on pre-resolved, safe grains.
