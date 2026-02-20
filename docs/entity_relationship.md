# Entity Relationship Model

This document outlines the core structural entities within the Olist PostgreSQL schema, detailing primary keys, foreign keys, and relational data grains.

## Overall Relational Model
The database is structured as a normalized relational schema centered around the `orders` table. It operates conceptually similar to a snowflake schema, where the central transaction (`orders`) bridges human customers (`customers`) to physical purchased goods (`order_items`), financial transactions (`order_payments`), and feedback loops (`order_reviews`).

## Core Tables (Normalized Raw Data)

### 1. `olist.orders`
*   **Grain:** 1 row per checkout transaction.
*   **Primary Key:** `order_id`
*   **Foreign Keys:** `customer_id` -> `olist.customers`
*   **Description:** The central hub of the database. Tracks the temporal lifecycle of an order from purchase timestamp to delivery and estimated SLA.

### 2. `olist.customers`
*   **Grain:** 1 row per order-specific customer profile.
*   **Primary Key:** `customer_id`
*   **Foreign Keys:** None.
*   **Description:** Stores geographic routing data (zip, city, state) for the buyer. Note that a single human being (`customer_unique_id`) generates a new, distinct `customer_id` for every unique order they place.

### 3. `olist.order_items`
*   **Grain:** 1 row per physical product unit shipped within an order.
*   **Primary Key:** `(order_id, order_item_id)`
*   **Foreign Keys:** 
    *   `order_id` -> `olist.orders`
    *   `product_id` -> `olist.products`
    *   `seller_id` -> `olist.sellers`
*   **Description:** The transactional line items. Contains the individual product `price` and the apportioned `freight_value` for that specific item.

### 4. `olist.order_payments`
*   **Grain:** 1 row per sequential payment method utilized on an order.
*   **Primary Key:** `(order_id, payment_sequential)`
*   **Foreign Keys:** `order_id` -> `olist.orders`
*   **Description:** Details the funding mechanics (e.g., credit card, boleto) and installment plans chosen to settle the total order value.

### 5. `olist.order_reviews`
*   **Grain:** 1 row per submitted customer review.
*   **Primary Key:** `(review_id, order_id)`
*   **Foreign Keys:** `order_id` -> `olist.orders`
*   **Description:** Customer satisfaction scores (1-5) and text commentary linked back to the parent transaction.

### 6. Dimension Tables (`products`, `sellers`, `category_name_translation`)
*   **Grain:** 1 row per unique entity ID.
*   **Primary Keys:** `product_id`, `seller_id`, `product_category_name` respectively.
*   **Description:** Static lookup tables providing descriptive attributes (dimensions, weight, English translation, seller location) to the transactional facts.

## Semantic Views (Abstracted Logic)
*   `vw_order_fact`: Consolidates `order_items` (Sum of price + freight) up to the `order_id` grain to prevent fan-out when joining to customer locations.
*   `vw_item_fact`: Enriches the raw `order_items` grain with English category translations and the parent order status.
*   `vw_customer_monthly_metrics`: Aggregates activity to the `customer_unique_id` grain per calendar month, establishing cohort baselines.
*   `vw_delivery_sla_metrics`: Remains at the `order_id` grain but pre-computes complex date physics (extracting epoch intervals) into standardized `_days` metrics.
