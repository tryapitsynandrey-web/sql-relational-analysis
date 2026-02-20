# Payment Type Behavior Report

## Executive Summary
- Credit cards dominate the volume of both orders and absolute payment value.
- Payment installment preferences suggest a price-sensitive consumer base.
- Vouchers/Boletos feature a unique and elevated correlation with order abandonment/cancellation.
- Credit infrastructure is currently the lifeblood of the scaling GMV.
- Alternate payments (debit) remain drastically underutilized.

## Key Metrics
| Metric | Status / Trend |
| --- | --- |
| Dominant Payment | Credit Card |
| Highest Cancellation | Voucher/Boleto |

## Findings
`05_payment_usage.png` indicates that the platform's survival is tied overwhelmingly to successful credit authorization. Conversely, `05_payment_cancellation.png` details exactly how high friction asynchronous payments (like Boleto) result in drastically higher unfulfilled endpoints. 

## Business Recommendations
1. Analyze the Boleto funnel to identify if the cancellation is driven by friction, fraud, or buyer remorse.
2. Incentivize direct debit or immediate payment gateways to reduce payment-pending limbo.
3. Guarantee robust redundancy for the platform's active credit card gateways to prevent catastrophic downtime.

## Assumptions & Limitations
- Cancellation logic is based solely on final state and doesn't unpack sequential payment drop-offs natively.
