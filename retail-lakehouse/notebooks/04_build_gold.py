# Databricks notebook source
# MAGIC %md
# MAGIC # 04 — Build Gold
# MAGIC
# MAGIC **Goal:** Create business-ready aggregate tables from silver data.
# MAGIC
# MAGIC Gold tables are the final layer — optimized for analysts, dashboards, and
# MAGIC reporting. Each gold table answers a specific business question.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from retail_lakehouse.config import load_config, get_table_fqn
from retail_lakehouse.transformations.gold import (
    build_daily_revenue,
    build_revenue_by_category,
    build_customer_lifetime_value,
)

config = load_config("dev")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Daily Revenue
# MAGIC
# MAGIC This one is already implemented. Run it and inspect.

# COMMAND ----------

df_silver_orders = spark.read.table(get_table_fqn(config, "silver_orders"))

df_daily_revenue = build_daily_revenue(df_silver_orders)
df_daily_revenue.show(truncate=False)

# COMMAND ----------

gold_daily_fqn = get_table_fqn(config, "gold_daily_revenue")
df_daily_revenue.write.format("delta").mode("overwrite").saveAsTable(gold_daily_fqn)
print(f"Written to {gold_daily_fqn}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Revenue by Category
# MAGIC
# MAGIC **Your turn.** Implement `build_revenue_by_category()` in
# MAGIC `src/retail_lakehouse/transformations/gold.py`, then run below.

# COMMAND ----------

# Uncomment after implementing:
#
# df_products = spark.read.table(get_table_fqn(config, "bronze_products"))
# df_rev_category = build_revenue_by_category(df_silver_orders, df_products)
# df_rev_category.show(truncate=False)
#
# gold_cat_fqn = get_table_fqn(config, "gold_revenue_by_category")
# df_rev_category.write.format("delta").mode("overwrite").saveAsTable(gold_cat_fqn)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Customer Lifetime Value
# MAGIC
# MAGIC **Your turn.** Implement `build_customer_lifetime_value()`, then run below.

# COMMAND ----------

# Uncomment after implementing:
#
# df_clv = build_customer_lifetime_value(df_silver_orders)
# df_clv.show(truncate=False)
#
# gold_clv_fqn = get_table_fqn(config, "gold_customer_lifetime_value")
# df_clv.write.format("delta").mode("overwrite").saveAsTable(gold_clv_fqn)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next
# MAGIC
# MAGIC Proceed to `05_quality_checks.py` to validate your silver and gold tables.
