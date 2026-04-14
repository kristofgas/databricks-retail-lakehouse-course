# Retail Lakehouse

A hands-on Databricks course built around a realistic retail analytics project.

You will learn PySpark, Delta Lake, and the medallion architecture (bronze / silver / gold) by working inside a production-shaped codebase — not by reading slides.

> **Repo layout:** The project code lives in the `retail-lakehouse/` directory. Course meta-files (for Cursor-guided learning and course maintenance) live at the repository root.

## Who Is This For?

Software developers who are new to Databricks. You should already be comfortable with Python, Git, and working in structured codebases. No prior Spark or data engineering experience is required.

## What You Will Learn

- PySpark DataFrame operations (read, transform, aggregate, write)
- Delta Lake tables and the lakehouse model
- Medallion architecture: bronze (raw), silver (cleaned), gold (aggregated)
- Unity Catalog concepts: catalogs, schemas, tables
- Data quality checks and validation patterns
- How notebooks, reusable packages, and jobs fit together in a real project
- How to turn exploration code into production-ready pipelines

---

## Quick Start

```bash
git clone <repo-url>
cd <repo-name>/retail-lakehouse
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest                     # verify your setup works
```

Then open `retail-lakehouse/docs/learning-roadmap.md` and follow Phase 1.

Full setup instructions: [docs/setup.md](retail-lakehouse/docs/setup.md)

---

## Choose Your Learning Mode

Pick the path that fits your situation. All three use the same codebase.

### Self-guided

Work through the numbered notebooks and implement the TODOs on your own. Use the docs for orientation, the SQL files for validation, and the tests to check your work.

**Start here:** [docs/learning-roadmap.md](retail-lakehouse/docs/learning-roadmap.md)

### Cursor-guided (AI-assisted)

Use Cursor IDE with the built-in course spec. Cursor gives you one task at a time, reviews your solutions like a senior engineer, and adapts to your progress.

**Start here:** [docs/cursor-guide.md](retail-lakehouse/docs/cursor-guide.md)

### Databricks-first

Import the repo into a Databricks workspace and run notebooks directly against a cluster. Best if you already have workspace access and want to work with real Delta tables from the start.

**Start here:** [docs/databricks-guide.md](retail-lakehouse/docs/databricks-guide.md)

### Local-first

Work entirely on your local machine using a local SparkSession. Good for learning PySpark and transformations without needing a Databricks workspace. Move to Databricks later when you're ready for Delta tables and Unity Catalog.

**Start here:** [docs/setup.md](retail-lakehouse/docs/setup.md)

---

## Repository Structure

```
<repo-root>/
├── databricks-course.md       # Course spec (Cursor / maintainers)
├── notes.md                   # Learning tracker (Cursor / maintainers)
├── project-setup.md           # Repo generation spec (maintainers)
├── README-for-cursor-usage.md # Cursor integration notes (maintainers)
│
└── retail-lakehouse/          # ← all project code lives here
    ├── conf/                  # Environment configs (dev, test, prod)
    ├── data/sample/           # Small CSV datasets for development
    ├── docs/                  # Setup, Databricks, Cursor, and learning docs
    ├── notebooks/             # Numbered Databricks notebooks (01–06)
    ├── sql/                   # Validation and analytics queries
    ├── src/retail_lakehouse/  # Reusable Python/PySpark package
    │   ├── ingestion/         #   Bronze layer: raw data loading
    │   ├── transformations/   #   Silver & gold layer logic
    │   ├── quality/           #   Data quality checks
    │   ├── jobs/              #   Entry points for scheduled pipelines
    │   └── utils/             #   Path and naming helpers
    └── tests/                 # pytest unit tests
```

For a detailed breakdown of what goes where: [docs/repository-guide.md](retail-lakehouse/docs/repository-guide.md)

For the data flow and medallion architecture: [docs/architecture.md](retail-lakehouse/docs/architecture.md)

---

## Learning Path

The course is organized into six phases. Each phase has a notebook and corresponding code in `src/`.

| Phase | Notebook | Topic | Your work |
|---|---|---|---|
| 1 | `01_repo_orientation.py` | Explore the repo, config, and sample data | Read-only |
| 2 | `02_ingest_bronze.py` | Load CSVs into bronze Delta tables | Run and observe |
| 3 | `03_build_silver.py` | Clean, deduplicate, enrich | Implement `clean_customers`, `enrich_orders_with_customers` |
| 4 | `04_build_gold.py` | Build business aggregates | Implement `build_revenue_by_category`, `build_customer_lifetime_value` |
| 5 | `05_quality_checks.py` | Validate silver and gold tables | Implement `check_accepted_values`, `check_positive_values`, gold checks |
| 6 | `06_run_pipeline_as_job.py` | Run the full pipeline as a job | Complete `silver_job.py`, `gold_job.py` |

Detailed phase guide with day-1 instructions: [docs/learning-roadmap.md](retail-lakehouse/docs/learning-roadmap.md)

---

## What Is Implemented vs. What Is Left for You

The repository is intentionally **partially implemented**. A senior engineer set up the skeleton and completed reference implementations. You fill in the rest.

### Already working

| Component | File |
|---|---|
| Config loading | `config.py` |
| CSV readers | `ingestion/readers.py` |
| Bronze ingestion with metadata | `ingestion/bronze_loader.py` |
| Silver orders: dedup, cast, total | `transformations/silver.py` (top half) |
| Gold daily revenue | `transformations/gold.py` (`build_daily_revenue`) |
| Null and uniqueness checks | `quality/checks.py` (top half) |
| Bronze job | `jobs/bronze_job.py` |
| Full pipeline orchestrator | `jobs/full_pipeline_job.py` |
| Tests for the above | `tests/test_bronze.py`, parts of others |

### Left as exercises (marked with `TODO`)

| Exercise | File |
|---|---|
| Clean customers | `transformations/silver.py` |
| Enrich orders with customer data | `transformations/silver.py` |
| Revenue by category | `transformations/gold.py` |
| Customer lifetime value | `transformations/gold.py` |
| Accepted values check | `quality/checks.py` |
| Positive values check | `quality/checks.py` |
| Gold quality check suite | `quality/checks.py` |
| Silver customers in job | `jobs/silver_job.py` |
| Remaining gold tables in job | `jobs/gold_job.py` |
| Test cases for all the above | `tests/test_silver.py`, `test_gold.py`, `test_quality_checks.py` |

---

## File Guide

### Essential for all learners

All paths below are inside `retail-lakehouse/`.

| File / Directory | Purpose |
|---|---|
| `docs/` | Setup, architecture, Databricks guide, learning roadmap |
| `notebooks/` | Numbered learning notebooks (01–06) |
| `src/retail_lakehouse/` | The PySpark package you'll work in |
| `tests/` | Unit tests you'll extend |
| `conf/` | Environment configs |
| `data/sample/` | Source CSV files |
| `sql/` | Validation and analytics queries |

### For Cursor-guided learning and course maintainers

These root-level files are **not required** for self-guided learners. They drive the AI-assisted teaching mode in Cursor.

| File | Purpose | Who needs it |
|---|---|---|
| `databricks-course.md` | Course specification — tells Cursor how to teach, what tasks to give, how to review | Cursor users, course maintainers |
| `project-setup.md` | Repo generation spec — how this project was scaffolded | Course maintainers only |
| `notes.md` | Adaptive learning tracker — Cursor reads this to personalize tasks | Cursor users |
| `README-for-cursor-usage.md` | Internal doc explaining how Cursor interacts with the repo | Course maintainers only |
| `.cursor/rules/` | Cursor IDE rules for this workspace | Cursor users |

If you're learning without Cursor, you can safely ignore all of these.

---

## Tech Stack

- Python 3.10+
- PySpark 3.5+
- Delta Lake
- PyYAML
- pytest + chispa (for testing)
- Databricks notebooks (optional — works locally too)

---

## Documentation Index

| Doc | What it covers |
|---|---|
| [docs/setup.md](retail-lakehouse/docs/setup.md) | Install dependencies, run tests, inspect data, local vs. Databricks |
| [docs/learning-roadmap.md](retail-lakehouse/docs/learning-roadmap.md) | Full course navigation, day-1 guide, phase details, TODO inventory |
| [docs/architecture.md](retail-lakehouse/docs/architecture.md) | Medallion layers, data flow, code organization |
| [docs/repository-guide.md](retail-lakehouse/docs/repository-guide.md) | What goes where, naming conventions |
| [docs/databricks-guide.md](retail-lakehouse/docs/databricks-guide.md) | Importing into Databricks, catalogs, schemas, running notebooks |
| [docs/cursor-guide.md](retail-lakehouse/docs/cursor-guide.md) | Working with Cursor, prompts, review workflow, notes.md |

---

## License

This is a teaching project. Use it, fork it, adapt it for your team.
