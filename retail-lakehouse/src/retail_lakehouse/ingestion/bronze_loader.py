"""Load raw data into bronze Delta tables with ingestion metadata."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def add_ingestion_metadata(df: DataFrame, source_name: str) -> DataFrame:
    """Append standard ingestion metadata columns to a raw DataFrame."""
    return (
        df
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.lit(source_name))
    )


def write_bronze_table(df: DataFrame, table_fqn: str, mode: str = "append") -> None:
    """Write a DataFrame to a bronze Delta table.

    On Databricks this creates a managed Delta table in Unity Catalog.
    Locally (tests), it writes to the Spark warehouse directory.
    """
    (
        df.write
        .format("delta")
        .mode(mode)
        .saveAsTable(table_fqn)
    )


def ingest_to_bronze(df_raw: DataFrame, source_name: str, table_fqn: str, mode: str = "overwrite") -> DataFrame:
    """Full bronze ingestion: add metadata and write to Delta.

    Returns the enriched DataFrame for inspection.
    """
    df_bronze = add_ingestion_metadata(df_raw, source_name)
    write_bronze_table(df_bronze, table_fqn, mode=mode)
    return df_bronze
