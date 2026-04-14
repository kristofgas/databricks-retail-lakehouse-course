-- =============================================================
-- Validation Queries
-- Run these in a Databricks SQL editor to inspect pipeline output.
-- Adjust catalog/schema to match your environment.
-- =============================================================

-- Check: bronze_orders row count and sample
SELECT COUNT(*) AS row_count FROM dev_retail.lakehouse.bronze_orders;
SELECT * FROM dev_retail.lakehouse.bronze_orders LIMIT 10;

-- Check: duplicate order_ids in bronze (should find the intentional dupe)
SELECT order_id, COUNT(*) AS cnt
FROM dev_retail.lakehouse.bronze_orders
GROUP BY order_id
HAVING cnt > 1;

-- Check: silver_orders row count (should be less than bronze after dedup)
SELECT COUNT(*) AS row_count FROM dev_retail.lakehouse.silver_orders;

-- Check: silver_orders has no nulls in key columns
SELECT
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_ids,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_ids,
    SUM(CASE WHEN order_timestamp IS NULL THEN 1 ELSE 0 END) AS null_timestamps,
    SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END) AS null_totals
FROM dev_retail.lakehouse.silver_orders;

-- Check: silver_orders total_amount is computed correctly
SELECT order_id, quantity, unit_price, total_amount,
       (quantity * unit_price) AS expected_total,
       ABS(total_amount - (quantity * unit_price)) < 0.01 AS matches
FROM dev_retail.lakehouse.silver_orders
LIMIT 10;

-- Check: gold_daily_revenue has data
SELECT * FROM dev_retail.lakehouse.gold_daily_revenue ORDER BY order_date;

-- Check: gold revenue sums match silver
SELECT
    (SELECT ROUND(SUM(total_amount), 2) FROM dev_retail.lakehouse.silver_orders WHERE order_status = 'completed') AS silver_total,
    (SELECT ROUND(SUM(total_revenue), 2) FROM dev_retail.lakehouse.gold_daily_revenue) AS gold_total;
