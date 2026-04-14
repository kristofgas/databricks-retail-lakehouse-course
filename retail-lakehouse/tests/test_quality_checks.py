"""Tests for data quality check functions."""

from pyspark.sql import Row

from retail_lakehouse.quality.checks import check_no_nulls, check_unique


class TestCheckNoNulls:
    def test_passes_when_no_nulls(self, spark):
        df = spark.createDataFrame([
            Row(order_id="ORD-001"),
            Row(order_id="ORD-002"),
        ])
        result = check_no_nulls(df, "order_id")
        assert result["passed"] is True

    def test_fails_when_nulls_exist(self, spark):
        df = spark.createDataFrame([
            Row(order_id="ORD-001"),
            Row(order_id=None),
        ])
        result = check_no_nulls(df, "order_id")
        assert result["passed"] is False
        assert "1 nulls found" in result["details"]


class TestCheckUnique:
    def test_passes_when_all_unique(self, spark):
        df = spark.createDataFrame([
            Row(order_id="ORD-001"),
            Row(order_id="ORD-002"),
        ])
        result = check_unique(df, "order_id")
        assert result["passed"] is True

    def test_fails_when_duplicates_exist(self, spark):
        df = spark.createDataFrame([
            Row(order_id="ORD-001"),
            Row(order_id="ORD-001"),
            Row(order_id="ORD-002"),
        ])
        result = check_unique(df, "order_id")
        assert result["passed"] is False


# TODO: Add tests for check_accepted_values after implementing it
# class TestCheckAcceptedValues:
#     def test_passes_with_valid_values(self, spark):
#         # Create rows with order_status in ["completed", "pending"]
#         # Call check_accepted_values(df, "order_status", ["completed", "pending"])
#         # Assert result["passed"] is True
#         pass
#
#     def test_fails_with_invalid_values(self, spark):
#         # Create rows including order_status="unknown"
#         # Assert result["passed"] is False
#         # Assert "unknown" appears in result["details"]
#         pass

# TODO: Add tests for check_positive_values after implementing it
# class TestCheckPositiveValues:
#     def test_passes_with_positive_values(self, spark):
#         # Create rows with quantity=1, quantity=5
#         # Assert result["passed"] is True
#         pass
#
#     def test_fails_with_zero(self, spark):
#         # Create rows including quantity=0
#         # Assert result["passed"] is False
#         pass
#
#     def test_fails_with_negative(self, spark):
#         # Create rows including quantity=-1
#         # Assert result["passed"] is False
#         pass
