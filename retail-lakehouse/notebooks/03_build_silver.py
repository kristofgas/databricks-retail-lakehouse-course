# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Build Silver
# MAGIC
# MAGIC **Goal:** Clean, deduplicate, and type-cast bronze data into silver tables.
# MAGIC
# MAGIC Silver is where data becomes trustworthy. We fix types, remove duplicates,
# MAGIC standardize values, and enrich with joins.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from retail_lakehouse.config import load_config, get_table_fqn
from retail_lakehouse.transformations.silver import (
    clean_orders,
    clean_customers,
    enrich_orders_with_customers,
)

config = load_config("dev")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver orders
# MAGIC
# MAGIC `clean_orders` is already implemented. Let's run it and inspect the results.

# COMMAND ----------

df_bronze_orders = spark.read.table(get_table_fqn(config, "bronze_orders"))
print(f"Bronze orders: {df_bronze_orders.count()} rows")

df_silver_orders = clean_orders(df_bronze_orders)
print(f"Silver orders: {df_silver_orders.count()} rows (after dedup)")
df_silver_orders.printSchema()
display(df_silver_orders)

# COMMAND ----------

# MAGIC %md
# MAGIC Notice:
# MAGIC - Duplicates removed (compare row counts)
# MAGIC - `total_amount` column added
# MAGIC - Ingestion metadata dropped

# COMMAND ----------

silver_orders_fqn = get_table_fqn(config, "silver_orders")
df_silver_orders.write.format("delta").mode("overwrite").saveAsTable(silver_orders_fqn)
print(f"Written to {silver_orders_fqn}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver customers
# MAGIC
# MAGIC **Your turn.** The `clean_customers()` function in
# MAGIC `src/retail_lakehouse/transformations/silver.py` is not yet implemented.
# MAGIC
# MAGIC Go implement it, then come back and run the cell below.

# COMMAND ----------

# Uncomment after implementing clean_customers:
#
# df_bronze_customers = spark.read.table(get_table_fqn(config, "bronze_customers"))
# df_silver_customers = clean_customers(df_bronze_customers)
# df_silver_customers.show()
#
# silver_customers_fqn = get_table_fqn(config, "silver_customers")
# df_silver_customers.write.format("delta").mode("overwrite").saveAsTable(silver_customers_fqn)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Enriched orders (optional stretch)
# MAGIC
# MAGIC After both silver tables exist, implement `enrich_orders_with_customers()`
# MAGIC and test the join here.

# COMMAND ----------

# Uncomment after implementing enrich_orders_with_customers:
#
# df_enriched = enrich_orders_with_customers(df_silver_orders, df_silver_customers)
# df_enriched.show(10, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next
# MAGIC
# MAGIC Proceed to `04_build_gold.py` to create business-ready aggregates.
