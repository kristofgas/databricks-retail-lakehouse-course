-- =============================================================
-- Analytics Queries
-- Business-friendly queries to explore gold layer outputs.
-- =============================================================

-- Top 5 revenue days
SELECT order_date, total_revenue, order_count
FROM dev_retail.lakehouse.gold_daily_revenue
ORDER BY total_revenue DESC
LIMIT 5;

-- Revenue trend (all days)
SELECT order_date, total_revenue,
       SUM(total_revenue) OVER (ORDER BY order_date) AS cumulative_revenue
FROM dev_retail.lakehouse.gold_daily_revenue
ORDER BY order_date;

-- TODO: Revenue by category (requires gold_revenue_by_category table)
-- SELECT category, total_revenue, total_quantity
-- FROM dev_retail.lakehouse.gold_revenue_by_category
-- ORDER BY total_revenue DESC;

-- TODO: Top customers by lifetime value (requires gold_customer_lifetime_value table)
-- SELECT customer_id, lifetime_revenue, total_orders, first_order_date, last_order_date
-- FROM dev_retail.lakehouse.gold_customer_lifetime_value
-- ORDER BY lifetime_revenue DESC
-- LIMIT 10;

-- Order status breakdown
SELECT order_status, COUNT(*) AS order_count, ROUND(SUM(total_amount), 2) AS total_value
FROM dev_retail.lakehouse.silver_orders
GROUP BY order_status
ORDER BY total_value DESC;

-- Revenue by country
SELECT country, ROUND(SUM(total_amount), 2) AS total_revenue, COUNT(*) AS order_count
FROM dev_retail.lakehouse.silver_orders
WHERE order_status = 'completed'
GROUP BY country
ORDER BY total_revenue DESC;
