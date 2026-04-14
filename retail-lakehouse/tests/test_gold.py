"""Tests for gold aggregation logic."""

from pyspark.sql import Row
from pyspark.sql.types import (
    StructType, StructField, StringType, TimestampType, IntegerType, DoubleType,
)

from retail_lakehouse.transformations.gold import build_daily_revenue


SILVER_ORDERS_SCHEMA = StructType([
    StructField("order_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("product_id", StringType()),
    StructField("order_timestamp", TimestampType()),
    StructField("quantity", IntegerType()),
    StructField("unit_price", DoubleType()),
    StructField("total_amount", DoubleType()),
    StructField("currency", StringType()),
    StructField("country", StringType()),
    StructField("order_status", StringType()),
])


def _make_silver_orders(spark, rows):
    return spark.createDataFrame(rows, schema=SILVER_ORDERS_SCHEMA)


class TestBuildDailyRevenue:
    def test_filters_to_completed_only(self, spark):
        from datetime import datetime
        rows = [
            ("ORD-001", "C1", "P1", datetime(2024, 1, 15, 9, 0), 1, 100.0, 100.0, "EUR", "NL", "completed"),
            ("ORD-002", "C2", "P2", datetime(2024, 1, 15, 10, 0), 1, 50.0, 50.0, "EUR", "DE", "cancelled"),
        ]
        df = _make_silver_orders(spark, rows)
        result = build_daily_revenue(df)
        row = result.collect()[0]
        assert row["total_revenue"] == 100.0
        assert row["order_count"] == 1

    def test_groups_by_date(self, spark):
        from datetime import datetime
        rows = [
            ("ORD-001", "C1", "P1", datetime(2024, 1, 15, 9, 0), 1, 100.0, 100.0, "EUR", "NL", "completed"),
            ("ORD-002", "C2", "P2", datetime(2024, 1, 15, 14, 0), 1, 50.0, 50.0, "EUR", "DE", "completed"),
            ("ORD-003", "C3", "P3", datetime(2024, 1, 16, 9, 0), 1, 75.0, 75.0, "EUR", "FR", "completed"),
        ]
        df = _make_silver_orders(spark, rows)
        result = build_daily_revenue(df)
        assert result.count() == 2


# TODO: Add tests for build_revenue_by_category after implementing it
# class TestBuildRevenueByCategory:
#     def test_joins_with_products(self, spark):
#         # Create 2 orders for PROD-001 (category "Electronics") and 1 for PROD-002 ("Office")
#         # Assert result has 2 rows (one per category)
#         pass
#
#     def test_aggregates_revenue_correctly(self, spark):
#         # Create 2 completed orders with known total_amounts in the same category
#         # Assert total_revenue equals the sum
#         pass
#
#     def test_excludes_non_completed_orders(self, spark):
#         # Create one completed and one cancelled order for the same category
#         # Assert total_revenue only includes the completed order
#         pass

# TODO: Add tests for build_customer_lifetime_value after implementing it
# class TestBuildCustomerLifetimeValue:
#     def test_computes_lifetime_revenue(self, spark):
#         # Create 3 completed orders for the same customer with known amounts
#         # Assert lifetime_revenue equals the sum
#         pass
#
#     def test_counts_distinct_orders(self, spark):
#         # Create 2 completed orders for one customer
#         # Assert total_orders == 2
#         pass
#
#     def test_computes_date_range(self, spark):
#         # Create orders on Jan 1 and Jan 31
#         # Assert first_order_date and last_order_date match
#         pass
