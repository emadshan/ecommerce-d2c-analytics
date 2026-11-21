-- BigQuery Standard SQL. Load CSV to `vastraa.raw_events` first.
CREATE OR REPLACE TABLE `vastraa.analytics.events_clean`
PARTITION BY DATE(event_timestamp)
CLUSTER BY channel, device, event_name AS
SELECT * EXCEPT(row_num)
FROM (
  SELECT *, ROW_NUMBER() OVER(
    PARTITION BY session_id,event_name,event_timestamp
    ORDER BY ingested_at DESC
  ) row_num
  FROM `vastraa.raw_events`
  WHERE COALESCE(is_bot,FALSE)=FALSE
)
WHERE row_num=1;
