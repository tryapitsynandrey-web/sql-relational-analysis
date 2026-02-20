# Cohorts & Retention Report

## Executive Summary
- New user acquisition drives absolute revenue growth, not recurring purchasers.
- MoM retention rates crash immediately off the first month of activity.
- Long-term cohort degradation reveals limited loyalty.
- Lifetime Value (LTV) maxes out early in the customer lifecycle.
- E-commerce nature of platform may naturally lean against recurring FMCG sales.

## Key Metrics
| Metric | Status / Trend |
| --- | --- |
| Month 1 Retention | Very Low |
| Long-term LTV Growth | Marginal |

## Findings
`02_retention_trend.png` visually confirms the severe drop-off in active buyers following their initial joining purchase. `02_ltv_growth.png` demonstrates that a customer's total value effectively ceases compounding shortly after acquisition, proving Olist acts primarily as a single-utility marketplace for users rather than a recurring destination.

## Business Recommendations
1. Establish aggressive retargeting campaigns for Month 1 purchasers to break the cycle.
2. Institute loyalty mechanics (points/discounts) specifically for second purchases.
3. Optimize acquisition CAC heavily, as poor LTV means single purchases must inherently be profitable.

## Assumptions & Limitations
- User consolidation depends fully on `customer_unique_id`.
- Does not account for guest checkout blurring if unsupported by the architecture.
