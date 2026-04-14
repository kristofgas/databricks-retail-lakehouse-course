# Learning Roadmap

Complete guide to progressing through the Retail Lakehouse course.

## Day 1 After Cloning

If you just cloned the repo and have 30 minutes, do this:

1. Follow [docs/setup.md](setup.md) to install dependencies and run `pytest`
2. Open `data/sample/orders.csv` and scan the columns and values
3. Read through `notebooks/01_repo_orientation.py` top to bottom (don't run it yet — just read)
4. Open `src/retail_lakehouse/transformations/silver.py` and read `clean_orders()` — this is an example of what you'll be writing
5. Open `src/retail_lakehouse/transformations/gold.py` and read the TODO docstrings — these are your assignments

You now understand the shape of the project and the type of work ahead.

---

## Course Phases

Work through these in order. Each phase has a notebook, corresponding source code, and — starting from Phase 3 — TODOs for you to implement.

### Phase 1 — Orientation

**Notebook:** `notebooks/01_repo_orientation.py`

**What you do:**
- Load the config and understand how it maps to catalog/schema/table
- Read the three sample CSVs and inspect their schemas
- Count rows, spot the intentional duplicate in orders
- Understand which columns will need cleaning

**Source code to read:**
- `src/retail_lakehouse/config.py` — how config loading works
- `conf/dev.yml` — what the config contains

**Your work:** None — this is read-only exploration.

---

### Phase 2 — Bronze Ingestion

**Notebook:** `notebooks/02_ingest_bronze.py`

**What you do:**
- Use `read_csv()` to load raw data
- Use `ingest_to_bronze()` to write Delta tables with metadata
- Inspect the bronze tables and notice `_ingested_at` and `_source_file`

**Source code to read:**
- `src/retail_lakehouse/ingestion/readers.py` — CSV reading functions
- `src/retail_lakehouse/ingestion/bronze_loader.py` — metadata + write logic

**Your work:** Run and observe. The bronze layer is fully implemented.

---

### Phase 3 — Silver Transformations

**Notebook:** `notebooks/03_build_silver.py`

**What you do:**
- Run `clean_orders()` on bronze data and inspect the result
- Implement `clean_customers()` — your first real coding task
- Implement `enrich_orders_with_customers()` — your first join

**Source code to work in:**
- `src/retail_lakehouse/transformations/silver.py`

**Reference implementation:** `clean_orders()` in the same file shows the pattern you should follow.

**TODOs:**

| Function | What to implement |
|---|---|
| `clean_customers()` | Dedup on customer_id, trim name, lowercase segment, cast date, drop metadata |
| `enrich_orders_with_customers()` | Left join orders with customers on customer_id, avoid duplicate columns |

**Tests to complete:**
- `tests/test_silver.py` — uncomment and implement `TestCleanCustomers`

---

### Phase 4 — Gold Aggregations

**Notebook:** `notebooks/04_build_gold.py`

**What you do:**
- Run `build_daily_revenue()` and inspect the result
- Implement the two remaining gold aggregations

**Source code to work in:**
- `src/retail_lakehouse/transformations/gold.py`

**Reference implementation:** `build_daily_revenue()` in the same file.

**TODOs:**

| Function | What to implement |
|---|---|
| `build_revenue_by_category()` | Join completed orders with products to compute per-category totals |
| `build_customer_lifetime_value()` | Compute per-customer lifetime metrics from completed orders |

**Tests to complete:**
- `tests/test_gold.py` — uncomment and implement `TestBuildRevenueByCategory` and `TestBuildCustomerLifetimeValue`

---

### Phase 5 — Quality Checks

**Notebook:** `notebooks/05_quality_checks.py`

**What you do:**
- Run the existing silver order checks and observe pass/fail output
- Implement the missing check functions
- Build a complete gold quality check suite

**Source code to work in:**
- `src/retail_lakehouse/quality/checks.py`

**Reference implementations:** `check_no_nulls()` and `check_unique()` in the same file.

**TODOs:**

| Function | What to implement |
|---|---|
| `check_accepted_values()` | Verify column values are within an allowed set |
| `check_positive_values()` | Verify numeric column has only positive values |
| `run_gold_daily_revenue_checks()` | Combine checks for the gold daily revenue table |

**Also:** Wire `check_accepted_values` and `check_positive_values` into `run_silver_orders_checks()` (the commented TODO lines).

**Tests to complete:**
- `tests/test_quality_checks.py` — uncomment and implement the TODO test classes

---

### Phase 6 — Jobs and Pipeline

**Notebook:** `notebooks/06_run_pipeline_as_job.py`

**What you do:**
- Run the full pipeline end-to-end
- Understand how `full_pipeline_job.py` chains bronze → silver → gold
- Complete the missing job implementations

**Source code to work in:**
- `src/retail_lakehouse/jobs/silver_job.py` — add silver customers processing
- `src/retail_lakehouse/jobs/gold_job.py` — add revenue by category and CLV tables

**Your work:** These jobs depend on the functions you implemented in Phases 3–5. If those work, the jobs are straightforward wiring.

---

## After the Notebooks

Once you've completed all six phases:

1. **Run the full test suite:** `pytest -v` — all tests should pass
2. **Run the full pipeline:** execute `notebooks/06_run_pipeline_as_job.py` end-to-end
3. **Validate with SQL:** run `sql/validation_queries.sql` to verify table contents
4. **Explore analytics:** run `sql/analytics_queries.sql` to see business-level insights

---

## Complete TODO Inventory

Every exercise in the repo, organized by file:

### `src/retail_lakehouse/transformations/silver.py`
- [ ] `clean_customers()`
- [ ] `enrich_orders_with_customers()`

### `src/retail_lakehouse/transformations/gold.py`
- [ ] `build_revenue_by_category()`
- [ ] `build_customer_lifetime_value()`

### `src/retail_lakehouse/quality/checks.py`
- [ ] `check_accepted_values()`
- [ ] `check_positive_values()`
- [ ] `run_gold_daily_revenue_checks()`
- [ ] Wire remaining checks into `run_silver_orders_checks()`

### `src/retail_lakehouse/jobs/silver_job.py`
- [ ] Silver customers processing

### `src/retail_lakehouse/jobs/gold_job.py`
- [ ] Revenue by category table
- [ ] Customer lifetime value table

### `tests/test_silver.py`
- [ ] `TestCleanCustomers` class

### `tests/test_gold.py`
- [ ] `TestBuildRevenueByCategory` class
- [ ] `TestBuildCustomerLifetimeValue` class

### `tests/test_quality_checks.py`
- [ ] `TestCheckAcceptedValues` class
- [ ] `TestCheckPositiveValues` class

### `sql/analytics_queries.sql`
- [ ] Uncomment revenue by category query
- [ ] Uncomment customer lifetime value query
