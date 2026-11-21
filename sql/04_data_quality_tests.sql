-- Each query should return zero for a clean mart unless noted.
SELECT 'duplicate_order_ids' test, COUNT(*) failures FROM (SELECT order_id FROM mart.fact_orders GROUP BY 1 HAVING COUNT(*)>1) q;
SELECT 'orphan_customers' test, COUNT(*) failures FROM mart.fact_orders o LEFT JOIN raw.customers c USING(customer_id) WHERE c.customer_id IS NULL;
SELECT 'invalid_order_value' test, COUNT(*) failures FROM mart.fact_orders WHERE order_value_inr IS NULL OR order_value_inr<0;
SELECT 'invalid_quantity' test, COUNT(*) failures FROM mart.fact_order_items WHERE quantity<=0;
SELECT 'bot_events_in_mart' test, COUNT(*) failures FROM mart.fact_events WHERE is_bot IS TRUE;
SELECT 'invalid_payment_method' test, COUNT(*) failures FROM mart.fact_orders WHERE payment_method NOT IN ('COD','UPI','prepaid_card','netbanking');
SELECT 'rto_not_cancelled' test, COUNT(*) failures FROM mart.fact_orders WHERE delivery_outcome='RTO' AND order_status<>'cancelled';
