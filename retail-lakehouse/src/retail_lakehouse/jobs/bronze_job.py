"""Bronze ingestion job — entry point for Databricks job scheduler."""

from pyspark.sql import SparkSession

from retail_lakehouse.config import load_config, get_table_fqn
from retail_lakehouse.ingestion.readers import read_csv
from retail_lakehouse.ingestion.bronze_loader import ingest_to_bronze
from retail_lakehouse.utils.paths import raw_file_path


def run(env: str = "dev") -> None:
    spark = SparkSession.builder.getOrCreate()
    config = load_config(env)

    sources = [
        ("orders.csv", "bronze_orders"),
        ("customers.csv", "bronze_customers"),
        ("products.csv", "bronze_products"),
    ]

    for filename, table_key in sources:
        path = raw_file_path(config, filename)
        table_fqn = get_table_fqn(config, table_key)

        print(f"Ingesting {filename} → {table_fqn}")
        df_raw = read_csv(spark, path)
        ingest_to_bronze(df_raw, source_name=filename, table_fqn=table_fqn)

    print("Bronze ingestion complete.")


if __name__ == "__main__":
    run()
