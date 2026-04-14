"""Tests for silver transformation logic."""

from datetime import datetime

from pyspark.sql import Row

from retail_lakehouse.transformations.silver import (
    deduplicate_orders,
    cast_order_types,
    add_order_total,
    clean_orders,
)


class TestDeduplicateOrders:
    def test_removes_exact_duplicates(self, spark):
        df = spark.createDataFrame([
            Row(order_id="ORD-001", customer_id="C1", product_id="P1"),
            Row(order_id="ORD-001", customer_id="C1", product_id="P1"),
            Row(order_id="ORD-002", customer_id="C2", product_id="P2"),
        ])
        result = deduplicate_orders(df)
        assert result.count() == 2

    def test_keeps_distinct_orders(self, spark):
        df = spark.createDataFrame([
            Row(order_id="ORD-001", customer_id="C1"),
            Row(order_id="ORD-002", customer_id="C2"),
        ])
        result = deduplicate_orders(df)
        assert result.count() == 2


class TestAddOrderTotal:
    def test_computes_total_correctly(self, spark):
        df = spark.createDataFrame([
            Row(quantity=3, unit_price=10.0),
        ])
        result = add_order_total(df)
        row = result.collect()[0]
        assert row["total_amount"] == 30.0

    def test_handles_fractional_prices(self, spark):
        df = spark.createDataFrame([
            Row(quantity=2, unit_price=29.99),
        ])
        result = add_order_total(df)
        row = result.collect()[0]
        assert row["total_amount"] == 59.98


class TestCleanOrders:
    def test_full_pipeline_drops_metadata(self, spark):
        df = spark.createDataFrame([
            Row(
                order_id="ORD-001",
                customer_id="C1",
                product_id="P1",
                order_timestamp="2024-01-15 09:00:00",
                quantity="2",
                unit_price="29.99",
                currency="EUR",
                country="NL",
                order_status="completed",
                _ingested_at=datetime.now(),
                _source_file="orders.csv",
            ),
        ])
        result = clean_orders(df)
        assert "_ingested_at" not in result.columns
        assert "_source_file" not in result.columns


# TODO: Add tests for clean_customers after implementing it
# class TestCleanCustomers:
#     def test_deduplicates_on_customer_id(self, spark):
#         # Create two rows with the same customer_id
#         # Assert result.count() drops to 1
#         pass
#
#     def test_lowercases_segment(self, spark):
#         # Create a row with customer_segment="Premium"
#         # Assert the result value is "premium"
#         pass
#
#     def test_casts_signup_date(self, spark):
#         # Create a row with signup_date as a string "2024-01-15"
#         # Assert the result column type is DateType
#         pass
#
#     def test_drops_ingestion_metadata(self, spark):
#         # Create a row with _ingested_at and _source_file columns
#         # Assert neither column exists in the result
#         pass
