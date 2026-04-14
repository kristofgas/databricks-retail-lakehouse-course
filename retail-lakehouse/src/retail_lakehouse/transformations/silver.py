"""Silver layer transformations — cleaning, deduplication, enrichment."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import TimestampType, IntegerType, DoubleType

from retail_lakehouse.constants import INGESTION_METADATA_COLS


def deduplicate_orders(df: DataFrame) -> DataFrame:
    """Remove exact duplicate rows from the orders DataFrame."""
    return df.dropDuplicates(["order_id"])


def cast_order_types(df: DataFrame) -> DataFrame:
    """Cast columns to their proper types.

    Bronze tables often store everything as strings (especially with
    schema inference from CSV). Silver is where we enforce correct types.
    """
    return (
        df
        .withColumn("order_timestamp", F.col("order_timestamp").cast(TimestampType()))
        .withColumn("quantity", F.col("quantity").cast(IntegerType()))
        .withColumn("unit_price", F.col("unit_price").cast(DoubleType()))
    )


def add_order_total(df: DataFrame) -> DataFrame:
    """Compute total_amount = quantity * unit_price."""
    return df.withColumn("total_amount", F.round(F.col("quantity") * F.col("unit_price"), 2))


def clean_orders(df: DataFrame) -> DataFrame:
    """Full silver cleaning pipeline for orders.

    Chains: dedup → cast → add total → drop ingestion metadata.
    """
    return (
        df
        .transform(deduplicate_orders)
        .transform(cast_order_types)
        .transform(add_order_total)
        .drop(*INGESTION_METADATA_COLS)
    )


def clean_customers(df: DataFrame) -> DataFrame:
    """Silver cleaning for customers.

    TODO: Implement the following steps:
    1. Deduplicate on customer_id
    2. Trim whitespace from customer_name
    3. Lowercase the customer_segment column for consistency
    4. Cast signup_date to DateType
    5. Drop ingestion metadata columns (use INGESTION_METADATA_COLS)

    Look at clean_orders() above for the pattern.
    """
    raise NotImplementedError("TODO: Implement clean_customers")


def enrich_orders_with_customers(orders: DataFrame, customers: DataFrame) -> DataFrame:
    """Join silver orders with silver customers to add segment and name.

    TODO: Implement a left join on customer_id.
    Select: all order columns + customer_name, customer_segment from customers.
    Be careful not to duplicate the customer_id column.
    """
    raise NotImplementedError("TODO: Implement enrich_orders_with_customers")
