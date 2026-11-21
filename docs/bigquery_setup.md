# BigQuery Setup

1. Create a Google Cloud project and enable BigQuery.
2. Create dataset `vastraa` in the region you intend to use.
3. Upload `events.csv` to `vastraa.raw_events` (CSV autodetect; preserve timestamps and booleans).
4. Run `sql/bigquery/01_events_partitioned.sql`.
5. Partition on `DATE(event_timestamp)` and cluster on `channel`, `device`, `event_name`.
6. For large date-scoped queries, always filter `DATE(event_timestamp)` to enable partition pruning.
7. Validate row counts, bot exclusion and event deduplication against `data/exports/data_quality_profile.csv`.

Example:
```sql
SELECT DATE(event_timestamp) event_date, channel, COUNT(*) events
FROM `vastraa.analytics.events_clean`
WHERE DATE(event_timestamp) BETWEEN '2026-10-01' AND '2026-10-31'
GROUP BY 1,2;
```
