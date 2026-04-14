"""Shared pytest fixtures for the retail_lakehouse test suite."""

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """Create a local SparkSession for testing.

    Uses a single session for the entire test run (scope="session")
    to avoid the overhead of spinning up Spark repeatedly.
    """
    session = (
        SparkSession.builder
        .master("local[*]")
        .appName("retail-lakehouse-tests")
        .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse-tests")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )
    yield session
    session.stop()
