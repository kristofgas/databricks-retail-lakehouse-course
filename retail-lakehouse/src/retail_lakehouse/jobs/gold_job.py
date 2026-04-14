"""Gold aggregation job — entry point for Databricks job scheduler.

TODO: Implement this job:
1. Read silver_orders (and products if needed) from Delta tables
2. Build gold aggregates using functions from transformations/gold.py
3. Write each aggregate to its corresponding gold table

Tables to build:
- gold_daily_revenue (build_daily_revenue is already implemented)
- gold_revenue_by_category (TODO in gold.py)
- gold_customer_lifetime_value (TODO in gold.py)
"""

from pyspark.sql import SparkSession

from retail_lakehouse.config import load_config, get_table_fqn
from retail_lakehouse.transformations.gold import build_daily_revenue


def run(env: str = "dev") -> None:
    spark = SparkSession.builder.getOrCreate()
    config = load_config(env)

    silver_orders_fqn = get_table_fqn(config, "silver_orders")
    gold_daily_revenue_fqn = get_table_fqn(config, "gold_daily_revenue")

    print(f"Reading {silver_orders_fqn}")
    df_silver_orders = spark.read.table(silver_orders_fqn)

    # --- Daily Revenue (implemented) ---
    print(f"Building {gold_daily_revenue_fqn}")
    df_daily = build_daily_revenue(df_silver_orders)
    df_daily.write.format("delta").mode("overwrite").saveAsTable(gold_daily_revenue_fqn)

    # --- Revenue by Category ---
    # TODO: Read products, call build_revenue_by_category, write to table

    # --- Customer Lifetime Value ---
    # TODO: Call build_customer_lifetime_value, write to table

    print("Gold aggregation complete.")


if __name__ == "__main__":
    run()
