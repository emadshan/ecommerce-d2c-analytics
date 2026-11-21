CREATE OR REPLACE VIEW mart.vw_monthly_business AS
SELECT date_trunc('month',order_date)::date month,
       COUNT(*) orders,
       COUNT(*) FILTER (WHERE order_status='delivered') delivered_orders,
       SUM(order_value_inr) gross_order_value_inr,
       AVG(order_value_inr) aov_inr,
       AVG((delivery_outcome='RTO')::int::numeric) rto_rate
FROM mart.fact_orders GROUP BY 1;
CREATE OR REPLACE VIEW mart.vw_channel_performance AS
SELECT channel,COUNT(*) orders,COUNT(DISTINCT customer_id) customers,
       SUM(order_value_inr) gross_order_value_inr,
       AVG((delivery_outcome='RTO')::int::numeric) rto_rate
FROM mart.fact_orders GROUP BY channel;
CREATE OR REPLACE VIEW mart.vw_payment_city_rto AS
SELECT city_tier,payment_method,COUNT(*) orders,
       AVG((delivery_outcome='RTO')::int::numeric) rto_rate
FROM mart.fact_orders GROUP BY 1,2;
CREATE OR REPLACE VIEW mart.vw_product_sales AS
SELECT p.product_id,p.product_name,p.category,SUM(i.quantity) units,
       SUM(i.line_revenue_inr) gross_revenue_inr,SUM(i.line_cogs_inr) cogs_inr
FROM mart.fact_order_items i JOIN raw.products p USING(product_id)
GROUP BY 1,2,3;
