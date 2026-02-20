# Metric Definitions

This document curates the central business intelligence metrics utilized throughout the repository, tying their business definitions directly back to their explicit SQL computation logic.

## Financial Metrics

### Total Revenue (GMV)
*   **Business Definition:** The total gross value of goods sold, inclusive of shipping costs (freight) passed on to the customer.
*   **SQL Logic:** `SUM(price + freight_value) AS total_order_value` (`sql/views/01_vw_order_fact.sql`)
*   **Caveats:** Does not subtract COGS, seller fees, refunds, or chargebacks. Pure top-line demand reflection.

### Average Order Value (AOV)
*   **Business Definition:** Mean revenue generated per completed transaction.
*   **SQL Logic:** `SUM(total_order_value) / NULLIF(COUNT(order_id), 0)` (`sql/analysis/01_revenue_and_aov_behavior.sql`)
*   **Caveats:** Canceled or unavailable orders are strictly omitted from the denominator via `WHERE order_status = 'delivered'`.

### Cumulative Lifetime Value (LTV)
*   **Business Definition:** The rolling sum of all payments effectively received from a unique human customer since their first purchase.
*   **SQL Logic:** `SUM(spend_this_month) OVER (PARTITION BY customer_unique_id ORDER BY activity_month ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` (`sql/views/03_vw_customer_monthly_metrics.sql`)
*   **Caveats:** Tied safely to `payment_value` instead of listed `price` to ensure voucher/discount impacts are accurately captured in the customer's real wallet spend.

## Customer Behavior Metrics

### Retention Rate (%)
*   **Business Definition:** The percentage of a monthly customer cohort that successfully placed another order in a subsequent month.
*   **SQL Logic:** `ROUND((COUNT(customer_unique_id)::DECIMAL / NULLIF(FIRST_VALUE(COUNT(customer_unique_id)) OVER (...), 0)) * 100, 2)` (`sql/analysis/02_cohorts_and_retention.sql`)
*   **Caveats:** Months are strictly defined chronologically (`EXTRACT(year/month FROM age)`). If a customer purchases twice within the very same calendar month, they do not trigger a "Month 1" retention blip.

### Cancellation Rate (%)
*   **Business Definition:** The proportion of initialized transaction intents that ultimately failed or were purposefully voided before fulfillment.
*   **SQL Logic:** `ROUND((COUNT(*) FILTER (WHERE o.order_status = 'canceled')::DECIMAL / NULLIF(COUNT(*), 0)) * 100, 2)` (`sql/analysis/05_payment_type_behavior.sql`)
*   **Caveats:** Evaluators must note that `unavailable` status is distinct from `canceled`. This metric strictly targets willful cancellations or payment failures, not seller inventory stock-outs.

## Logistics & Satisfaction Metrics

### Delayed Rate (%)
*   **Business Definition:** The percentage of delivered orders that arrived at the customer's physical location *after* the estimated delivery date communicated at checkout.
*   **SQL Logic:** `COUNT(*) FILTER (WHERE is_delayed)::DECIMAL / NULLIF(COUNT(*), 0)` where `is_delayed` is `order_delivered_customer_date > order_estimated_delivery_date`. (`sql/analysis/03_delivery_sla_performance.sql` via `vw_delivery_sla_metrics`)
*   **Caveats:** Excludes orders that are still currently in transit or were canceled. It only grades fully completed lifecycle transactions.

### Actual Delivery Days
*   **Business Definition:** Operational transit time elapsed from checkout click to physical package drop-off.
*   **SQL Logic:** `EXTRACT(EPOCH FROM (order_delivered_customer_date - order_purchase_timestamp))/86400.0` (`sql/views/04_vw_delivery_sla_metrics.sql`)
*   **Caveats:** Ignores the `order_approved_at` delay, holding the business accountable for the entire clock starting precisely when the customer initiated the purchase.

### Average Review Score
*   **Business Definition:** The mean satisfaction score (1-5) submitted by customers regarding an order experience.
*   **SQL Logic:** `AVG(r.review_score)` (`sql/analysis/04_review_score_drivers.sql`)
*   **Caveats:** Reviews are highly susceptible to negative bias, where satisfied customers forget to review. Reviews are assigned at the `order_id` grain, meaning poor seller performance on one item drags down the review score of unrelated items bought in the same basket.
