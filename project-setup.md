# Databricks Project Setup Specification

## Purpose

You are generating a realistic Databricks learning project repository.

This repository should feel like a real team codebase, but it must remain understandable and suitable for guided learning.

The goal is to create a project skeleton and initial partial implementation that supports a hands-on course.

This is not a toy notebook dump.

This is not a fake over-engineered enterprise monstrosity.

It should be a practical, clean, production-shaped learning repository.

---

## Project Name

Use this project name:

**retail-lakehouse**

---

## Core Objective

Generate a project that teaches Databricks through a realistic retail analytics use case.

The project should ingest sample retail/order data, transform it through bronze / silver / gold layers, and expose business-friendly outputs.

The student should be able to learn Databricks by working within this repository.

---

## Required Technology Choices

Use:

- Python
- PySpark
- SQL
- Delta Lake concepts
- Databricks-friendly notebook structure
- lightweight configuration patterns

Do not introduce:

- machine learning
- streaming
- advanced orchestration platforms
- Terraform
- CI/CD pipelines
- advanced infrastructure code
- unnecessary framework complexity

---

## Project Design Principles

The repository must be:

- realistic
- modular
- teachable
- explicit
- easy to navigate
- close to how a real team repository might look

The repository must not be:

- giant for no reason
- overly abstract
- dependent on hidden code generation
- built around magical helpers that obscure Spark logic

---

## Repository Structure

Create a structure similar to this:

retail-lakehouse/
  README.md
  databricks-course.md
  project-setup.md
  notes.md
  pyproject.toml
  requirements.txt
  .gitignore

  docs/
    architecture.md
    repository-guide.md
    learning-roadmap.md

  conf/
    dev.yml
    test.yml
    prod.yml

  data/
    sample/
      orders.csv
      customers.csv
      products.csv

  notebooks/
    01_repo_orientation.py
    02_ingest_bronze.py
    03_build_silver.py
    04_build_gold.py
    05_quality_checks.py
    06_run_pipeline_as_job.py

  sql/
    validation_queries.sql
    analytics_queries.sql

  src/
    retail_lakehouse/
      __init__.py
      config.py
      constants.py

      ingestion/
        __init__.py
        readers.py
        bronze_loader.py

      transformations/
        __init__.py
        bronze.py
        silver.py
        gold.py

      quality/
        __init__.py
        checks.py

      jobs/
        __init__.py
        bronze_job.py
        silver_job.py
        gold_job.py
        full_pipeline_job.py

      utils/
        __init__.py
        paths.py
        naming.py

  tests/
    test_bronze.py
    test_silver.py
    test_gold.py
    test_quality_checks.py

If small adjustments improve clarity, that is acceptable, but keep the same spirit.

---

## Sample Domain

Use a simple retail domain with data such as:

### orders.csv
Fields can include:
- order_id
- customer_id
- product_id
- order_timestamp
- quantity
- unit_price
- currency
- country
- order_status

### customers.csv
Fields can include:
- customer_id
- customer_name
- customer_segment
- signup_date
- country

### products.csv
Fields can include:
- product_id
- product_name
- category
- brand

Include enough realistic data for transformation practice, but keep it small.

---

## Initial Repository Content Rules

Create the initial repository content so that:

- the structure is complete
- the files are meaningful
- the project is partially implemented
- there are TODOs for the student
- the student can run and inspect things progressively
- not everything is already solved

Important:
- Do not fully complete all transformation logic
- Do not fully complete all tests
- Do not leave everything empty
- Strike a balance between scaffold and challenge

It should feel like:
“A senior engineer prepared the project skeleton and left implementation work for the student.”

---

## Notebook Rules

The notebooks should:

- be Databricks-friendly
- be used for learning and orchestration
- include explanatory markdown cells or comments where useful
- call reusable code where appropriate
- still make Spark behavior visible

The notebooks should not become giant all-in-one scripts.

Each notebook should have a clear purpose.

---

## Python Package Rules

The `src/retail_lakehouse` package should hold reusable logic.

Keep transformation logic in visible, plain PySpark functions.

Avoid unnecessary classes unless there is a clear reason.

Prefer function-based design unless a class makes the code materially clearer.

---

## SQL Rules

Include SQL files for:
- validation queries
- business analytics queries

These should support the learning process and help the student inspect the resulting tables.

---

## Config Rules

The config files should be simple and understandable.

Use them to represent environment-specific values conceptually, such as:
- catalog
- schema
- raw data paths
- bronze/silver/gold target names

Keep this lightweight.

---

## Tests Rules

Include tests that demonstrate realistic validation of transformations.

Tests should be:
- readable
- focused
- incomplete where appropriate
- aligned with the tutorial

Some tests may include TODO comments or missing assertions to be completed by the student.

---

## Documentation Rules

Generate docs that explain:
- architecture
- repository purpose
- role of notebooks vs package code
- learning progression

Docs should be practical, not fluffy.

---

## README Requirements

The README should include:
- project overview
- repository structure
- how the student is expected to use the repo
- how the course and notes files fit in
- the intended learning journey
- a disclaimer that this is a teaching-oriented but realistic project

---

## Important Constraints

Do not over-engineer the project.

Specifically avoid:
- complex dependency injection
- too many helper layers
- architecture that obscures PySpark operations
- pretending to solve enterprise deployment concerns in full

The repository should look real, but it should remain a teaching asset.

---

## Output Behavior

When asked to generate the project:
- first propose the repository tree
- then create or populate files in a sensible order
- explain major structure decisions briefly
- preserve room for student implementation