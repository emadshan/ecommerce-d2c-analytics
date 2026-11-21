CREATE TABLE IF NOT EXISTS staging.orders AS
SELECT o.*, NULLIF(BTRIM(city),'') AS city_clean,
       CASE WHEN order_value_inr < 0 OR order_value_inr > 100000 THEN NULL ELSE order_value_inr END AS order_value_clean
FROM raw.orders o WHERE 1=0;
TRUNCATE staging.orders;
INSERT INTO staging.orders
SELECT o.*, INITCAP(BTRIM(city)) AS city_clean,
       CASE WHEN order_value_inr < 0 OR order_value_inr > 100000 THEN NULL ELSE order_value_inr END
FROM raw.orders o;
CREATE TABLE IF NOT EXISTS staging.events AS
SELECT * FROM raw.events WHERE 1=0;
TRUNCATE staging.events;
INSERT INTO staging.events
SELECT DISTINCT ON (session_id,event_name,event_timestamp) *
FROM raw.events
WHERE COALESCE(is_bot,FALSE)=FALSE
ORDER BY session_id,event_name,event_timestamp,ingested_at DESC;
CREATE INDEX IF NOT EXISTS ix_stg_orders_customer_date ON staging.orders(customer_id,order_date);
CREATE INDEX IF NOT EXISTS ix_stg_events_session_time ON staging.events(session_id,event_timestamp);
