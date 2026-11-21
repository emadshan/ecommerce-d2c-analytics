CREATE TABLE IF NOT EXISTS mart.fact_orders AS
SELECT order_id,customer_id,order_date::date order_date,channel,device,payment_method,order_status,delivery_outcome,
       city_clean city,city_tier,discount_rate,shipping_fee_inr,order_value_clean order_value_inr,
       estimated_cogs_inr,sales_platform
FROM staging.orders WHERE 1=0;
TRUNCATE mart.fact_orders;
INSERT INTO mart.fact_orders
SELECT order_id,customer_id,order_date::date,channel,device,payment_method,order_status,delivery_outcome,
       city_clean,city_tier,discount_rate,shipping_fee_inr,order_value_clean,estimated_cogs_inr,sales_platform
FROM staging.orders;
CREATE TABLE IF NOT EXISTS mart.fact_order_items AS SELECT * FROM raw.order_items WHERE 1=0;
TRUNCATE mart.fact_order_items;
INSERT INTO mart.fact_order_items SELECT * FROM raw.order_items;
CREATE TABLE IF NOT EXISTS mart.fact_returns AS SELECT * FROM raw.returns WHERE 1=0;
TRUNCATE mart.fact_returns;
INSERT INTO mart.fact_returns SELECT * FROM raw.returns;
CREATE TABLE IF NOT EXISTS mart.fact_events AS SELECT * FROM staging.events WHERE 1=0;
TRUNCATE mart.fact_events;
INSERT INTO mart.fact_events SELECT * FROM staging.events;
CREATE INDEX IF NOT EXISTS ix_fact_orders_date ON mart.fact_orders(order_date);
CREATE INDEX IF NOT EXISTS ix_fact_orders_channel ON mart.fact_orders(channel);
