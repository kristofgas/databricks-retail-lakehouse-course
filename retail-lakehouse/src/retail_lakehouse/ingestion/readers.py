"""Functions for reading raw source files into Spark DataFrames."""

from pyspark.sql import DataFrame, SparkSession


def read_csv(spark: SparkSession, path: str, header: bool = True, infer_schema: bool = True) -> DataFrame:
    """Read a CSV file into a DataFrame.

    In production you would use Auto Loader (cloudFiles) for incremental
    ingestion. For this learning project we use spark.read.csv directly.
    """
    return (
        spark.read
        .option("header", header)
        .option("inferSchema", infer_schema)
        .csv(path)
    )


def read_csv_with_schema(spark: SparkSession, path: str, schema) -> DataFrame:
    """Read a CSV file with an explicit schema.

    Providing a schema avoids inference costs and prevents silent type
    mismatches when source data changes unexpectedly.
    """
    return (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(path)
    )
