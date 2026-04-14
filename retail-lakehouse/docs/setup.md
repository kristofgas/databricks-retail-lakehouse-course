# Setup and Local Development

## Prerequisites

- Python 3.10 or later
- Java 11 or 17 (required by PySpark — check with `java -version`)
- Git

## Clone and Install

```bash
git clone <repo-url>
cd retail-lakehouse

python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows

pip install -e ".[dev]"
```

The `.[dev]` install gives you:
- `pyspark` and `delta-spark` for running transformations
- `pyyaml` for config loading
- `pytest` and `chispa` for testing

## Verify Your Setup

```bash
pytest
```

This runs the test suite using a local SparkSession. You should see passing tests for the already-implemented functions (bronze ingestion, silver order cleaning, gold daily revenue, quality checks).

Some tests are intentionally skipped or commented out — these correspond to TODOs you'll implement during the course.

## Inspect the Sample Data

The quickest way to look at the data before writing any code:

```bash
# from the repo root
head -5 data/sample/orders.csv
head -5 data/sample/customers.csv
head -5 data/sample/products.csv
```

Or open a Python REPL:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("explore").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv("data/sample/orders.csv")
df.printSchema()
df.show(10, truncate=False)
```

## Run a Single Test File

```bash
pytest tests/test_bronze.py -v
pytest tests/test_silver.py -v
```

## Project Structure for Local Work

You can run and test all transformation logic locally. The local SparkSession reads CSVs and writes to a temporary Spark warehouse directory.

### What works locally

| Component | How |
|---|---|
| Reading CSVs | `spark.read.csv("data/sample/...")` |
| Transformation functions | Import from `retail_lakehouse.transformations` |
| Quality check functions | Import from `retail_lakehouse.quality` |
| Config loading | `load_config("dev")` reads `conf/dev.yml` |
| Unit tests | `pytest` with the fixture in `conftest.py` |

### What requires Databricks

| Component | Why |
|---|---|
| Writing to Unity Catalog tables | `saveAsTable()` with catalog.schema.table names needs a Databricks runtime |
| Running notebooks | Notebooks use `# MAGIC` syntax and `spark` global, which are Databricks-specific |
| SQL files | The queries reference Unity Catalog table names (e.g. `dev_retail.lakehouse.silver_orders`) |
| Jobs | Job entry points assume a Databricks cluster and catalog access |

### Bridging local and Databricks

A practical workflow:

1. **Develop locally** — write and test transformation functions in `src/` using pytest
2. **Move to Databricks** — import the repo, run notebooks against real Delta tables
3. **Iterate** — fix issues locally, push, pull into Databricks

## Config

Environment configs live in `conf/`. The default is `dev`:

```python
from retail_lakehouse.config import load_config
config = load_config("dev")   # reads conf/dev.yml
```

Each config file defines:
- `catalog` and `schema` — Unity Catalog namespace
- `*_path` — Volume paths for each medallion layer
- `tables` — Mapping of logical table keys to physical table names

When working locally, the catalog/schema/path values won't resolve to real locations. That's fine — you'll use them on Databricks. Locally, focus on the transformation functions and tests.

## Troubleshooting

**`java` not found:** PySpark needs Java. Install OpenJDK 17:
- macOS: `brew install openjdk@17`
- Ubuntu: `sudo apt install openjdk-17-jdk`

**Spark fails with address binding error:** The test fixture sets `spark.driver.bindAddress` to `127.0.0.1`. If you still get errors, check that nothing else is binding to Spark's default ports.

**Import errors for `retail_lakehouse`:** Make sure you installed in editable mode (`pip install -e ".[dev]"`). The `pyproject.toml` tells pip to look in `src/` for the package.
