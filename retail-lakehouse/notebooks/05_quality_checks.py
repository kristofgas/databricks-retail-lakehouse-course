# Databricks notebook source
# MAGIC %md
# MAGIC # 05 — Quality Checks
# MAGIC
# MAGIC **Goal:** Run data quality assertions on silver and gold tables.
# MAGIC
# MAGIC Good data pipelines don't just transform — they validate. This notebook
# MAGIC runs checks and reports pass/fail results.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from retail_lakehouse.config import load_config, get_table_fqn
from retail_lakehouse.quality.checks import (
    run_silver_orders_checks,
    run_gold_daily_revenue_checks,
)

config = load_config("dev")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver orders checks

# COMMAND ----------

df_silver_orders = spark.read.table(get_table_fqn(config, "silver_orders"))

results = run_silver_orders_checks(df_silver_orders)
for r in results:
    status = "PASS" if r["passed"] else "FAIL"
    print(f"[{status}] {r['check_name']}: {r['details']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold daily revenue checks
# MAGIC
# MAGIC **Your turn.** Implement `run_gold_daily_revenue_checks()` in
# MAGIC `src/retail_lakehouse/quality/checks.py`, then uncomment below.

# COMMAND ----------

# Uncomment after implementing:
#
# df_gold_daily = spark.read.table(get_table_fqn(config, "gold_daily_revenue"))
# gold_results = run_gold_daily_revenue_checks(df_gold_daily)
# for r in gold_results:
#     status = "PASS" if r["passed"] else "FAIL"
#     print(f"[{status}] {r['check_name']}: {r['details']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Quick SQL validation
# MAGIC
# MAGIC You can also validate directly with SQL. Mixing Python and SQL cells
# MAGIC is a common pattern in Databricks notebooks.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- If you are using a different config (test/prod), adjust the catalog below.
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_ids,
# MAGIC     SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END) AS null_totals
# MAGIC FROM dev_retail.lakehouse.silver_orders

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Adjust catalog if not using dev config.
# MAGIC SELECT order_status, COUNT(*) AS cnt
# MAGIC FROM dev_retail.lakehouse.silver_orders
# MAGIC GROUP BY order_status
# MAGIC ORDER BY cnt DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC Once all checks pass, you can be confident your pipeline produces
# MAGIC trustworthy data. In production, you would wire these checks into
# MAGIC alerting or pipeline gates.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next
# MAGIC
# MAGIC Proceed to `06_run_pipeline_as_job.py` to see how the full pipeline runs.
