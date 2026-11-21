# Head of Product — Funnel & Customer Insights

## Finding
The synthetic event design includes a mobile-specific loss between shipping details and payment information. The key diagnostic is the step conversion `add_shipping_info → add_payment_info`, segmented by device, with bots and duplicate events removed.

In the cleaned event data, mobile sessions move from shipping information to payment information at 71.2%, compared with 100.4% on desktop. This step-level difference is the key diagnostic signal in the generated sample.

## Recommended product work
1. Instrument field-level validation errors, payment method failures and latency at checkout.
2. Simplify address and delivery promise entry on mobile.
3. Test saved addresses and one-tap UPI selection.
4. Monitor completed purchase, payment failure, refunds and support contacts as guardrails.

## Customer analytics
Use cohort retention to distinguish one-time discount buyers from repeat cohorts. Use RFM clusters as descriptive groups for CRM activation, not as permanent customer labels.
