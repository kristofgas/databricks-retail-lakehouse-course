"""Tests for bronze ingestion logic."""

from pyspark.sql import Row

from retail_lakehouse.ingestion.bronze_loader import add_ingestion_metadata


class TestAddIngestionMetadata:
    def test_adds_ingested_at_column(self, spark):
        df = spark.createDataFrame([Row(order_id="ORD-001", quantity=2)])
        result = add_ingestion_metadata(df, "orders.csv")
        assert "_ingested_at" in result.columns

    def test_adds_source_file_column(self, spark):
        df = spark.createDataFrame([Row(order_id="ORD-001", quantity=2)])
        result = add_ingestion_metadata(df, "orders.csv")
        row = result.collect()[0]
        assert row["_source_file"] == "orders.csv"

    def test_preserves_original_columns(self, spark):
        df = spark.createDataFrame([Row(order_id="ORD-001", quantity=2)])
        result = add_ingestion_metadata(df, "orders.csv")
        assert "order_id" in result.columns
        assert "quantity" in result.columns

    def test_row_count_unchanged(self, spark):
        df = spark.createDataFrame([
            Row(order_id="ORD-001"),
            Row(order_id="ORD-002"),
            Row(order_id="ORD-003"),
        ])
        result = add_ingestion_metadata(df, "test.csv")
        assert result.count() == 3
