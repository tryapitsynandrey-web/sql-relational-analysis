# Payment Method Behavior & Cancellation Risk Analysis — Conclusions

---

## Key Findings
- Credit card transactions dominate the platform, constituting the overwhelming majority of both order volume and total GMV.
- Average transaction values are noticeably higher for credit card payments compared to alternative methods.
- The boleto (voucher) payment method suffers from an order cancellation rate drastically higher than the baseline average.
- Installment payments using credit cards are standard behavior across all mid-to-high ticket purchases.
- Debit card and alternative vouchers capture negligible shares of total transaction volume.

## Business Implications
- Extreme reliance on the credit card network creates a single-point-of-failure risk at the revenue collection layer.
- Boleto cancellations systematically inflate top-of-funnel conversion metrics with intent-to-buy actions that ultimately generate zero revenue.
- Revenue growth in high-AOV categories is structurally dependent on the continued availability of flexible installment financing.

## Actionable Recommendations
- Implement secondary, automated redundant routing for the primary credit card payment gateway to mitigate outage risks.
- Monitor the boleto cancellation rate explicitly as pseudo-abandoned cart volume rather than deliberate buyer-regret cancellations.
- Adjust checkout UX to aggressively incentivize immediate, digital payment methods over asynchronous voucher options.
