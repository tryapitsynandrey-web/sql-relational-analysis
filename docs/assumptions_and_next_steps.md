# Assumptions, Limitations, and Next Steps

## Key Assumptions
*   **Geographic Focus:** The business operates strictly within Brazilian states, meaning postal codes and geographic delivery routing complexities are constrained to domestic infrastructure capabilities.
*   **Platform Role:** Olist operates as an integrated marketplace connecting independent sellers with buyers, meaning logistical delays are heavily influenced by 3rd-party sellers and carriers, not necessarily unified warehouse dispatches.
*   **Valid Review Window:** Reviews mapped to a delivered order accurately reflect that specific transaction experience.

## Known Limitations
*   **Profitability Blindspot:** The dataset includes `price` and `freight_value` but excludes Cost of Goods Sold (COGS), marketing spend, and operational overhead. We can measure top-line GMV but cannot deduce true margin or net profitability.
*   **Attribution Void:** No web origin, traffic source, or marketing campaign attribution exists. Customer Acquisition Cost (CAC) and channel ROI cannot be evaluated.
*   **Returns and Refunds:** The `order_status` tracks `canceled` and `unavailable` but lacks explicit lifecycle tracking for post-delivery returns, refunds, or chargebacks. True net revenue is likely overstated.

## Risks
*   **Brittle Ingestion:** Relying purely on structural `COPY` means any upstream schema shift in the raw CSVs will decisively break the entire pipeline.
*   **Review Bias:** Satisfied customers commonly do not leave reviews, whilst disgruntled customers facing delayed SLAs are highly motivated to leave 1-star reviews. The average review score is likely pulled downward by negativity bias.

## Recommended Next Analyses
*   **Market Basket Analysis:** Investigate product affinities (which items are bought together) to drive cross-sell logic and bundle discounts.
*   **Seller Quality Tiering:** Shift focus from customers to sellers. Identify high-cancellation or consistently delayed sellers and establish penalty or reward SLAs based on metric behavior.
*   **Predictive Churn:** Utilize the cohort retention drop-off profile to trigger pre-emptive re-engagement discounts at the exact monthly threshold where customers historically stop buying.

## Data Gaps to Address
*   **Integrate Customer Acquisition Cost (CAC):** Merge ad-spend and traffic data to generate precise LTV:CAC ratios per cohort.
*   **Logistics Carrier Identification:** Add distinct carrier IDs to pinpoint which exact shipping companies are driving the SLA delays across the top 10 worst-performing states.
*   **Refund Ledger:** Incorporate the finance reconciliation ledger to adjust Gross Revenue to Net Revenue accurately.

## Potential Product / Business Actions
*   **Boleto Restructuring:** The high cancellation rate of 'boleto' (voucher) payments requires product friction adjustments. Implement shorter expiry windows or mandate partial upfront card holds for high-value items.
*   **Geo-SLA Adjustments:** SLA algorithms for northern states consistently fail. The estimated delivery date formula must dynamically pad extra transit days for notoriously delayed zip codes to artificially stabilize customer expectations and protect review scores.
