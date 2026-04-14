"""Gold layer transformations — business-ready aggregates."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_daily_revenue(df_silver_orders: DataFrame) -> DataFrame:
    """Aggregate daily revenue from completed orders.

    Output columns: order_date, total_revenue, order_count
    """
    return (
        df_silver_orders
        .filter(F.col("order_status") == "completed")
        .withColumn("order_date", F.to_date("order_timestamp"))
        .groupBy("order_date")
        .agg(
            F.round(F.sum("total_amount"), 2).alias("total_revenue"),
            F.count("order_id").alias("order_count"),
        )
        .orderBy("order_date")
    )


def build_revenue_by_category(df_silver_orders: DataFrame, df_products: DataFrame) -> DataFrame:
    """Revenue breakdown by product category.

    TODO: Join completed orders with products to compute per-category totals.

    Expected output columns: category, total_revenue, total_quantity.

    You'll need to decide: which join type? Which DataFrame contributes
    which columns? What happens if a product_id doesn't match?
    """
    raise NotImplementedError("TODO: Implement build_revenue_by_category")


def build_customer_lifetime_value(df_silver_orders: DataFrame) -> DataFrame:
    """Compute lifetime value per customer from completed orders.

    TODO: Think about what metrics define a customer's "lifetime value"
    and build a single aggregate table grouped by customer_id.

    Expected output columns: customer_id, lifetime_revenue, total_orders,
    first_order_date, last_order_date.

    Hint: Look at how build_daily_revenue handles filtering and aggregation.
    """
    raise NotImplementedError("TODO: Implement build_customer_lifetime_value")
