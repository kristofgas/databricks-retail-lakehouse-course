"""Data quality check functions for silver and gold tables.

Each function returns a dict with:
  - check_name: human-readable label
  - passed: bool
  - details: string with context on pass/fail
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from retail_lakehouse.constants import ORDER_STATUSES_VALID


def check_no_nulls(df: DataFrame, column: str) -> dict:
    """Assert that a column has zero null values."""
    null_count = df.filter(F.col(column).isNull()).count()
    passed = null_count == 0
    return {
        "check_name": f"no_nulls_{column}",
        "passed": passed,
        "details": f"{null_count} nulls found" if not passed else "OK",
    }


def check_unique(df: DataFrame, column: str) -> dict:
    """Assert that all values in a column are unique."""
    total = df.count()
    distinct = df.select(column).distinct().count()
    passed = total == distinct
    return {
        "check_name": f"unique_{column}",
        "passed": passed,
        "details": f"{total - distinct} duplicates found" if not passed else "OK",
    }


def check_accepted_values(df: DataFrame, column: str, accepted: list[str]) -> dict:
    """Assert that a column only contains values from an accepted list.

    TODO: Implement this check:
    1. Find distinct values in the column
    2. Check if any value is NOT in the accepted list
    3. Return the appropriate result dict with invalid values in details
    """
    raise NotImplementedError("TODO: Implement check_accepted_values")


def check_positive_values(df: DataFrame, column: str) -> dict:
    """Assert that all values in a numeric column are > 0.

    TODO: Implement this check:
    1. Count rows where the column value is <= 0 or null
    2. Return result dict with count of violations
    """
    raise NotImplementedError("TODO: Implement check_positive_values")


def run_silver_orders_checks(df: DataFrame) -> list[dict]:
    """Run all quality checks for silver_orders."""
    results = [
        check_no_nulls(df, "order_id"),
        check_unique(df, "order_id"),
        check_no_nulls(df, "customer_id"),
        check_no_nulls(df, "order_timestamp"),
        # TODO: Add check_accepted_values(df, "order_status", ORDER_STATUSES_VALID)
        # TODO: Add check_positive_values for "quantity" and "unit_price"
    ]
    return results


def run_gold_daily_revenue_checks(df: DataFrame) -> list[dict]:
    """Run quality checks for gold_daily_revenue.

    TODO: Implement checks:
    - order_date should have no nulls
    - total_revenue should be positive
    - order_count should be positive
    """
    raise NotImplementedError("TODO: Implement run_gold_daily_revenue_checks")
