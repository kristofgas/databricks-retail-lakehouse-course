"""Silver transformation job — entry point for Databricks job scheduler.

TODO: Implement this job:
1. Read bronze_orders and bronze_customers from Delta tables
2. Apply clean_orders() and clean_customers()
3. Write results to silver_orders and silver_customers tables
4. Optionally: enrich_orders_with_customers and write to a separate table

Hint: Follow the same pattern as bronze_job.py.
"""

from pyspark.sql import SparkSession

from retail_lakehouse.config import load_config, get_table_fqn
from retail_lakehouse.transformations.silver import clean_orders


def run(env: str = "dev") -> None:
    spark = SparkSession.builder.getOrCreate()
    config = load_config(env)

    # --- Orders ---
    bronze_orders_fqn = get_table_fqn(config, "bronze_orders")
    silver_orders_fqn = get_table_fqn(config, "silver_orders")

    print(f"Reading {bronze_orders_fqn}")
    df_bronze_orders = spark.read.table(bronze_orders_fqn)

    df_silver_orders = clean_orders(df_bronze_orders)

    print(f"Writing {silver_orders_fqn}")
    df_silver_orders.write.format("delta").mode("overwrite").saveAsTable(silver_orders_fqn)

    # --- Customers ---
    # TODO: Read bronze_customers, apply clean_customers(), write to silver_customers
    print("TODO: Silver customers not yet implemented.")

    print("Silver transformation complete.")


if __name__ == "__main__":
    run()
