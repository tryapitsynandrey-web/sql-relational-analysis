# Assumptions

## Data Assumptions
*   **Timezones:** All timestamps (`order_purchase_timestamp`, `order_delivered_customer_date`, etc.) are assumed to be in a consistent timezone (e.g., UTC or local Brazilian time) and do not require conversion for relative delta calculations.
*   **Completeness:** The provided CSV datasets represent a complete snapshot of the Olist ecosystem for the evaluated time period. Missing `customer_id` or `product_id` references imply data corruption rather than expected systematic gaps.
*   **Categorical Translations:** The `category_name_translation` table accurately maps Portuguese categories to English. Missing translations gracefully fallback to the original Portuguese string without breaking aggregates.

## Business Assumptions
*   **Revenue Definition:** Total order value (Revenue/GMV) is defined as the sum of product `price` plus `freight_value`. Freight is treated as pass-through revenue.
*   **Cancellation Finality:** Orders with `order_status = 'canceled'` represent zero final revenue, despite having corresponding rows in `order_payments`.
*   **Delivery SLAs:** The `order_estimated_delivery_date` was communicated to the customer at checkout and represents the binding SLA target for on-time delivery calculations.

## Analytical Assumptions
*   **Cohort Assignment:** A customer's cohort is strictly defined by the month of their *first* `order_purchase_timestamp`, regardless of when the order was approved or delivered.
*   **LTV Calculation:** Cumulative Lifetime Value (LTV) relies on `payment_value` across all non-canceled orders tied to a `customer_unique_id`.
*   **Review Attribution:** A review score assigned to an `order_id` applies equally to all `order_item_id`s within that basket for category-level aggregations.
