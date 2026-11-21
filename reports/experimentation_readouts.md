# Experimentation Readouts

## Pre-registration
Primary metric: customer conversion within the experiment observation window. Guardrail: refund-or-complaint incidence. Randomization unit: customer. Allocation: 50/50. Two-sided alpha: 5%. Report absolute and relative effects with 95% confidence intervals. Check sample ratio mismatch (SRM) before interpreting outcomes.

## Test 1 — EXP_POSITIVE: simplified checkout
Hypothesis: reducing checkout friction increases conversion without worsening refunds.
Decision: **SHIP** if the observed lift is positive, statistically credible and guardrails are stable. The planted effect is +15% relative conversion propensity.

## Test 2 — EXP_INCONCLUSIVE: product recommendation widget
Hypothesis: recommendations increase conversion.
Decision: **ITERATE** when confidence interval includes zero or the test is underpowered. Planted effect is +1% relative conversion propensity.

## Test 3 — EXP_GUARDRAIL: aggressive promotion
Hypothesis: promotion increases conversion.
Decision: **KILL** if the guardrail deteriorates beyond the pre-registered tolerance. Planted effect: +2% conversion propensity and +18% relative refund/complaint propensity.

Exact p-values and intervals are generated in `data/exports/experiment_readouts.csv`. The readout script computes two-proportion z-tests and a sample allocation diagnostic. In a production experiment, SRM must compare observed allocation to the intended allocation and investigate assignment/logging defects.
