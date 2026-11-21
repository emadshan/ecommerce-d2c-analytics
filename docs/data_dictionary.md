# Data Dictionary

| Table | Grain | Important columns |
|---|---|---|
| customers | One row/customer | customer_id, city, state, pincode, city_tier, created_at, acquisition_channel |
| products | One row/SKU | product_id, category, MRP, unit_cost, GST rate |
| orders | One row/order | order_id, customer_id, order_date, channel, device, payment_method, status, delivery_outcome, order_value |
| order_items | One row/order line | order_item_id, order_id, product_id, quantity, line revenue, line COGS |
| returns | One row/return | return_id, order_id, return_date, reason, refund amount |
| events | One row/event | event_id, session_id, event_timestamp, event_name, device, channel, UTM, bot flag |
| campaigns | One row/campaign | campaign_id, channel, campaign type |
| daily_ad_spend | One row/campaign/day | spend_date, campaign_id, spend, impressions |
| experiment_assignments | One row/customer/experiment | experiment_id, variant, assignment date, conversion, guardrail outcome |

All money columns are INR. `order_value_inr` is GST-inclusive. Event timestamps are local-naive synthetic timestamps for this exercise.
