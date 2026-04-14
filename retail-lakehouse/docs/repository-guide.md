# Repository Guide

## What goes where?

### `notebooks/`
Databricks-compatible Python notebooks. Numbered for learning progression. Each notebook has a single purpose: explore, ingest, transform, validate, or run.

Notebooks **import** from the `retail_lakehouse` package. They do not contain large blocks of reusable logic — that belongs in `src/`.

### `src/retail_lakehouse/`
The installable Python package. Contains all reusable PySpark functions for ingestion, transformation, quality checks, and job entry points.

Functions are plain PySpark — no magic wrappers, no hidden abstractions. You should always be able to read a function and understand the Spark operations it performs.

### `conf/`
YAML files with environment-specific config (catalog, schema, paths). Loaded by `retail_lakehouse.config`.

### `sql/`
Standalone SQL files for validation and ad-hoc analytics. Run these in a Databricks SQL editor or notebook to inspect outputs.

### `tests/`
pytest-based tests that validate transformations locally using a SparkSession. Some tests are incomplete — look for TODOs.

### `data/sample/`
Small CSV files representing source data. Used for local development and notebook walkthroughs. In production, this data would come from cloud storage or upstream systems.

## Naming Conventions

- Table names: `{layer}_{entity}` (e.g. `bronze_orders`, `silver_customers`, `gold_daily_revenue`)
- Python functions: `snake_case`, verb-first (e.g. `clean_orders`, `build_daily_revenue`)
- Configs: lowercase YAML keys
