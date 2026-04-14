# Databricks notebook source
# MAGIC %md
# MAGIC # 06 — Run Pipeline as a Job
# MAGIC
# MAGIC **Goal:** Understand how the full pipeline can be orchestrated as a Databricks job.
# MAGIC
# MAGIC In production, you wouldn't run notebooks manually. Instead, Databricks Jobs
# MAGIC would call the entry points in `src/retail_lakehouse/jobs/`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## How jobs work
# MAGIC
# MAGIC Each file in `src/retail_lakehouse/jobs/` has a `run(env)` function:
# MAGIC
# MAGIC | Job | What it does |
# MAGIC |---|---|
# MAGIC | `bronze_job.py` | Reads raw CSVs → writes bronze Delta tables |
# MAGIC | `silver_job.py` | Reads bronze → cleans → writes silver tables |
# MAGIC | `gold_job.py` | Reads silver → aggregates → writes gold tables |
# MAGIC | `full_pipeline_job.py` | Runs all three in sequence |
# MAGIC
# MAGIC A Databricks Workflow would call `full_pipeline_job.run("prod")` on a schedule.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run the full pipeline from this notebook
# MAGIC
# MAGIC This is equivalent to what a scheduled job would do:

# COMMAND ----------

from retail_lakehouse.jobs.full_pipeline_job import run

run(env="dev")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify the output

# COMMAND ----------

from retail_lakehouse.config import load_config, get_table_fqn

config = load_config("dev")

for table_key in ["bronze_orders", "silver_orders", "gold_daily_revenue"]:
    fqn = get_table_fqn(config, table_key)
    count = spark.read.table(fqn).count()
    print(f"{fqn}: {count} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## What's next?
# MAGIC
# MAGIC - Complete the TODO implementations in `silver_job.py` and `gold_job.py`
# MAGIC - Run the full pipeline again and verify all tables populate
# MAGIC - Explore the SQL files in `sql/` for analytics queries
# MAGIC - Run the quality checks notebook to validate everything
