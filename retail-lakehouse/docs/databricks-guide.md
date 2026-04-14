# Databricks Guide

How to use this project inside a Databricks workspace.

## Getting the Code into Databricks

### Option A: Git integration (recommended)

1. In your Databricks workspace, go to **Repos**
2. Click **Add Repo** and paste the Git URL
3. Databricks clones the repo and keeps it synced with your remote

This is the cleanest workflow. You edit locally, push, and pull in Databricks.

### Option B: Import manually

1. Download or clone the repo to your machine
2. In Databricks, navigate to your workspace folder
3. Upload the `notebooks/` files as Databricks notebooks
4. Upload the `src/`, `conf/`, and `data/` directories to a Databricks Repo or Volume

Git integration is strongly preferred — manual imports get out of sync quickly.

## Install the Package on Your Cluster

The notebooks import from `retail_lakehouse`, so the package must be available on the cluster.

### With Repos

Databricks Repos puts the repo root on the Python path, but the package lives under `src/`, which is one level deeper. Add this to the first cell of a notebook so imports resolve:

```python
import sys
sys.path.insert(0, "../src")
```

### With a wheel

For job runs or if you prefer explicit installs:

```bash
# locally, build the wheel
pip install build
python -m build

# upload dist/retail_lakehouse-0.1.0-py3-none-any.whl to a Volume
# then install on the cluster via notebook:
# %pip install /Volumes/.../retail_lakehouse-0.1.0-py3-none-any.whl
```

## Before Running Notebooks

### 1. Create your catalog and schema

The config files in `conf/` reference Unity Catalog namespaces. For dev work:

```sql
CREATE CATALOG IF NOT EXISTS dev_retail;
CREATE SCHEMA IF NOT EXISTS dev_retail.lakehouse;
```

Run this in a Databricks SQL editor or in a notebook cell with `%sql`.

### 2. Upload sample data to a Volume

The notebooks expect source data at the paths in `conf/dev.yml`. Create a Volume and upload:

```sql
CREATE VOLUME IF NOT EXISTS dev_retail.lakehouse.raw;
```

Then upload the CSV files:

```python
# From a notebook
dbutils.fs.cp("file:/Workspace/Repos/<you>/retail-lakehouse/data/sample/orders.csv",
              "/Volumes/dev_retail/lakehouse/raw/orders.csv")
dbutils.fs.cp("file:/Workspace/Repos/<you>/retail-lakehouse/data/sample/customers.csv",
              "/Volumes/dev_retail/lakehouse/raw/customers.csv")
dbutils.fs.cp("file:/Workspace/Repos/<you>/retail-lakehouse/data/sample/products.csv",
              "/Volumes/dev_retail/lakehouse/raw/products.csv")
```

Or upload through the Volumes UI in the Databricks catalog explorer.

### 3. Verify config matches your workspace

Open `conf/dev.yml` and confirm the catalog, schema, and paths match what you created. If your workspace uses different naming, update the YAML.

## How Notebooks Relate to `src/`

The notebooks are **orchestration and learning surfaces**. They import functions from `src/retail_lakehouse/` and call them with the right config and data.

```
notebooks/02_ingest_bronze.py
    ↓ imports
src/retail_lakehouse/ingestion/bronze_loader.py
    ↓ uses config from
conf/dev.yml
```

This separation matters because:
- Notebooks are for exploration and running pipelines interactively
- `src/` functions are testable, reusable, and version-controlled
- Jobs call `src/` directly — they don't run notebooks

When you implement a TODO, you edit the function in `src/`, then run the notebook to see the result.

## Catalogs, Schemas, and Tables

This project uses Unity Catalog's three-level namespace:

```
catalog.schema.table
  │       │      │
  │       │      └── bronze_orders, silver_orders, gold_daily_revenue, ...
  │       └── lakehouse
  └── dev_retail (or test_retail, prod_retail)
```

### Why three environments?

The `conf/` directory has `dev.yml`, `test.yml`, and `prod.yml`. Each points to a different catalog. This is how real teams isolate development from production data.

For the course, you only need `dev`. The other configs exist so you can see how environment separation works.

### Table naming convention

Tables follow the pattern `{layer}_{entity}`:
- `bronze_orders` — raw ingested orders
- `silver_orders` — cleaned and typed orders
- `gold_daily_revenue` — aggregated daily revenue

All table names are defined in the config, not hardcoded in the transformation code.

## Running the Notebooks

Attach a cluster with Databricks Runtime 14.0+ (or any runtime that includes PySpark 3.5+).

Run the notebooks in order:

1. `01_repo_orientation.py` — read-only exploration
2. `02_ingest_bronze.py` — creates bronze tables
3. `03_build_silver.py` — creates silver tables (requires your TODO implementations)
4. `04_build_gold.py` — creates gold tables (requires your TODO implementations)
5. `05_quality_checks.py` — validates outputs
6. `06_run_pipeline_as_job.py` — runs the full pipeline end-to-end

## Running SQL Files

Open `sql/validation_queries.sql` or `sql/analytics_queries.sql` in a Databricks SQL editor. These query the tables you built and help you verify correctness.

## Running Jobs

The `src/retail_lakehouse/jobs/` directory contains entry points that a Databricks Workflow can call:

```python
# In a Databricks job task:
from retail_lakehouse.jobs.full_pipeline_job import run
run(env="dev")
```

You won't need jobs until Phase 6 of the course. Focus on notebooks first.
