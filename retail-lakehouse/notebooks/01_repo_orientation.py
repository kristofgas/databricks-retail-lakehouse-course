# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Repository Orientation
# MAGIC
# MAGIC **Goal:** Understand the project layout, config system, and sample data before writing any transformations.
# MAGIC
# MAGIC This notebook is read-only exploration. You don't need to change anything here.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Load the config

# COMMAND ----------

from retail_lakehouse.config import load_config

config = load_config("dev")
print(config)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Inspect the sample data files
# MAGIC
# MAGIC We'll read the CSVs to understand what our source data looks like.
# MAGIC
# MAGIC **Note:** Paths are relative to the notebook's location. In Databricks Repos,
# MAGIC this notebook lives in `notebooks/`, so we use `../data/sample/` to reach
# MAGIC the project root. On Databricks, you would typically upload these files to a
# MAGIC Volume and read from there instead (see `docs/databricks-guide.md`).

# COMMAND ----------

DATA_DIR = "../data/sample"

df_orders = spark.read.option("header", True).option("inferSchema", True).csv(
    f"{DATA_DIR}/orders.csv"
)
df_orders.printSchema()
display(df_orders)

# COMMAND ----------

df_customers = spark.read.option("header", True).option("inferSchema", True).csv(
    f"{DATA_DIR}/customers.csv"
)
df_customers.printSchema()
display(df_customers)

# COMMAND ----------

df_products = spark.read.option("header", True).option("inferSchema", True).csv(
    f"{DATA_DIR}/products.csv"
)
df_products.printSchema()
display(df_products)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Key observations
# MAGIC
# MAGIC Before moving on, answer these for yourself:
# MAGIC
# MAGIC 1. How many rows are in orders? Are there any duplicates?
# MAGIC 2. What data types did Spark infer? Are they all correct?
# MAGIC 3. Which columns would you want to clean or transform?
# MAGIC 4. How would you join these three datasets?

# COMMAND ----------

print(f"Orders row count: {df_orders.count()}")
print(f"Distinct order_ids: {df_orders.select('order_id').distinct().count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Explore the config helper
# MAGIC
# MAGIC See how table names are resolved from config:

# COMMAND ----------

from retail_lakehouse.config import get_table_fqn

print(get_table_fqn(config, "bronze_orders"))
print(get_table_fqn(config, "silver_orders"))
print(get_table_fqn(config, "gold_daily_revenue"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next
# MAGIC
# MAGIC Proceed to `02_ingest_bronze.py` to load this data into bronze Delta tables.
