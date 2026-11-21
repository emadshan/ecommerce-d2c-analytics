# PostgreSQL CSV Loading

After creating schema/tables with `sql/01_postgres_schema.sql`, run from `psql` on Windows (adjust absolute path):
```sql
\copy raw.customers FROM 'D:/ecommerce-d2c-analytics/data/raw/customers.csv' CSV HEADER;
\copy raw.products FROM 'D:/ecommerce-d2c-analytics/data/raw/products.csv' CSV HEADER;
\copy raw.orders FROM 'D:/ecommerce-d2c-analytics/data/raw/orders.csv' CSV HEADER;
\copy raw.order_items FROM 'D:/ecommerce-d2c-analytics/data/raw/order_items.csv' CSV HEADER;
\copy raw.returns FROM 'D:/ecommerce-d2c-analytics/data/raw/returns.csv' CSV HEADER;
\copy raw.events FROM 'D:/ecommerce-d2c-analytics/data/raw/events.csv' CSV HEADER;
\copy raw.campaigns FROM 'D:/ecommerce-d2c-analytics/data/raw/campaigns.csv' CSV HEADER;
\copy raw.daily_ad_spend FROM 'D:/ecommerce-d2c-analytics/data/raw/daily_ad_spend.csv' CSV HEADER;
\copy raw.experiment_assignments FROM 'D:/ecommerce-d2c-analytics/data/raw/experiment_assignments.csv' CSV HEADER;
```
Then execute SQL files 02–05 in order. For a clean rerun, truncate raw tables before reloading.
