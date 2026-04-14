# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — Ingest Bronze
# MAGIC
# MAGIC **Goal:** Load raw CSV data into bronze Delta tables, adding ingestion metadata.
# MAGIC
# MAGIC Bronze tables are the raw landing zone. We preserve the original data exactly
# MAGIC as-is and only add metadata about when and from where it was ingested.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from retail_lakehouse.config import load_config, get_table_fqn
from retail_lakehouse.ingestion.readers import read_csv
from retail_lakehouse.ingestion.bronze_loader import ingest_to_bronze

config = load_config("dev")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest orders

# COMMAND ----------

DATA_DIR = "../data/sample"

df_raw_orders = read_csv(spark, f"{DATA_DIR}/orders.csv")
print(f"Raw orders: {df_raw_orders.count()} rows")
df_raw_orders.show(5)

# COMMAND ----------

orders_table = get_table_fqn(config, "bronze_orders")
print(f"Writing to: {orders_table}")

df_bronze_orders = ingest_to_bronze(
    df_raw_orders,
    source_name="orders.csv",
    table_fqn=orders_table,
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify the bronze table
# MAGIC
# MAGIC We use `display()` instead of `.show()` here. In Databricks, `display()`
# MAGIC renders DataFrames as interactive, sortable tables. Locally, `.show()` is fine.

# COMMAND ----------

df_bronze_orders.printSchema()
display(df_bronze_orders)

# COMMAND ----------

# MAGIC %md
# MAGIC Notice the `_ingested_at` and `_source_file` columns. These are standard
# MAGIC metadata fields that help with debugging and lineage tracking.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Explore Delta table history
# MAGIC
# MAGIC Delta Lake tracks every write as a versioned transaction. Use
# MAGIC `DESCRIBE HISTORY` to see what happened to a table over time.
# MAGIC This is one of the key advantages of Delta over plain Parquet.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- If you are using a different config (test/prod), adjust the catalog below.
# MAGIC DESCRIBE HISTORY dev_retail.lakehouse.bronze_orders

# COMMAND ----------

# MAGIC %md
# MAGIC Each row is a transaction. You can also query an older version with:
# MAGIC ```sql
# MAGIC SELECT * FROM dev_retail.lakehouse.bronze_orders VERSION AS OF 0
# MAGIC ```
# MAGIC This is called **time travel** — it's useful for debugging and auditing.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest customers and products

# COMMAND ----------

for filename, table_key in [("customers.csv", "bronze_customers"), ("products.csv", "bronze_products")]:
    df_raw = read_csv(spark, f"{DATA_DIR}/{filename}")
    table_fqn = get_table_fqn(config, table_key)
    print(f"Ingesting {filename} → {table_fqn} ({df_raw.count()} rows)")
    ingest_to_bronze(df_raw, source_name=filename, table_fqn=table_fqn)

print("All bronze tables loaded.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optional stretch
# MAGIC
# MAGIC We used `inferSchema=True` to let Spark guess column types. This is
# MAGIC convenient but unreliable — Spark might infer `quantity` as string in
# MAGIC some edge cases. Look at `read_csv_with_schema()` in
# MAGIC `src/retail_lakehouse/ingestion/readers.py` and try using it with an
# MAGIC explicit `StructType` schema for `orders.csv`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next
# MAGIC
# MAGIC Proceed to `03_build_silver.py` to clean and transform the bronze data.
