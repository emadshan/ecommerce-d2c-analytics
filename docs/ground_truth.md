# Synthetic Ground Truth (Validation Targets)

This file documents intentional data-generating mechanisms. Analysts should discover these through analysis rather than hard-code the conclusions.

1. **Paid social vs branded search:** paid social has higher acquisition cost, but customers acquired through it are designed to produce stronger repeat-purchase contribution over time. Branded search has low apparent CAC and high apparent ROAS because it captures existing demand. Observational attribution over-credits branded search as an acquisition source.
2. **Tier-3 COD RTO:** tier-3 COD RTO probability is 31%; tier-3 prepaid probability is 4.5%. Tier-1/2 COD risk is lower than tier-3 COD.
3. **Mobile checkout friction:** mobile sessions have a deliberate 29% probability of failing to reach `add_payment_info` after `add_shipping_info`; desktop does not receive this penalty.
4. **Festive margin dip:** October/November demand is weighted upward, while the average discount rate is higher (27% vs 13% non-festive before random noise), reducing contribution margin.
5. **Experimentation:** `EXP_POSITIVE` treatment has +15% relative conversion propensity; `EXP_INCONCLUSIVE` +1%; `EXP_GUARDRAIL` +2% conversion propensity but +18% relative refund/complaint propensity. Sampling noise means significance is not guaranteed for every generated seed.
6. **Data quality traps:** 3.5% bot-event probability; duplicate event records; 13% missing UTM tags; delayed ingestion up to 72 hours; null pincodes; inconsistent city spellings; high order-value outliers.

The generator is seeded with `20261121`. Experiment assignment and outcome fields are generated independently of orders so the experiment readout is a controlled synthetic demonstration, not an actual randomized test on order outcomes.
