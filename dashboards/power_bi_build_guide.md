# Power BI Build Guide

## Model
Import the CSVs in `data/exports/powerbi/` after running `python python/run_analytics.py` and `python python/export_powerbi.py`. For a fuller star schema, connect Power BI directly to PostgreSQL `mart` views. Create a Date table and relate it to order date; use single-direction dimension-to-fact relationships.

## Page 1 — Executive scorecard
Cards: Orders, Delivered Orders, Net Sales, Contribution, Contribution Margin %, AOV, RTO Rate. Line chart: monthly net sales and contribution. Bar: channel contribution. Slicers: date, platform, city tier.

## Page 2 — Product & customer
Funnel by device; cohort retention matrix; RFM segment table; category revenue and units. Slicers: device, category, cohort month.

## Page 3 — Marketing
Channel CAC, ROAS and spend; attribution model comparison; acquired customers by channel; repeat-customer contribution by channel. Add a note that attribution is descriptive, not incrementality.

## Page 4 — Operations & finance
RTO by city tier and payment method; monthly P&L; contribution by payment method; returns by reason. Add a COD-share what-if parameter and explain its assumptions.

## Page 5 — Experiments
Variant conversion, absolute lift, 95% CI, p-value and guardrail delta. Show decision labels and SRM status.

## Build steps
1. Get Data → Text/CSV → select exports.
2. Set INR numeric columns to Decimal Number and dates to Date.
3. Create Date table: `Date = CALENDAR(MIN(Orders[order_date]), MAX(Orders[order_date]))`.
4. Mark Date table and connect it to monthly/order date fields.
5. Add measures from `dax_measures.dax`.
6. Use consistent INR formatting and percentage formatting.
7. Add a methodology tooltip page with KPI definitions and limitations.
