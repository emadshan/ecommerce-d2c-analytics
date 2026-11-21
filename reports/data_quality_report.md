# Data Quality Report

## Expected raw issues
- Bots: approximately 3.5% of event rows.
- Duplicate semantic events: approximately 1.2% chance per emitted event.
- Missing UTM campaign: approximately 13%.
- Late ingestion: 0–72 hours after event timestamp.
- Customer and order pincodes: sparse nulls.
- City spelling/case inconsistencies: approximately 1%.
- Order-value outliers: approximately 0.1%.

## Controls
| Risk | Control |
|---|---|
| Duplicate events | Deduplicate by session, event name and timestamp; keep latest ingestion |
| Bots | Exclude `is_bot = true` from behavioural metrics |
| Missing UTM | Preserve as `(not set)`; do not infer channel from absent tags |
| Late arrivals | Use `ingested_at` for freshness monitoring |
| City spelling | Trim and standardize casing; maintain a production city mapping table |
| Outliers | Flag and investigate; do not silently delete |
| Referential integrity | Test order/customer and order/product joins |

Run `python python/data_quality.py` for observed counts and `python python/run_analytics.py` for exportable quality profiling.
