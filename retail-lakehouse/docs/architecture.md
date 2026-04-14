# Architecture

## Medallion Layers

This project follows the **bronze → silver → gold** medallion architecture on Delta Lake.

### Bronze (Raw Ingestion)

- Source: CSV files (or cloud storage in production)
- Format: Delta tables that mirror the raw source schema
- No transformations, no cleaning
- Adds ingestion metadata (`_ingested_at`, `_source_file`)

### Silver (Cleaned & Conformed)

- Deduplication, type casting, null handling
- Standardized column names (snake_case)
- Joins where appropriate (e.g. orders enriched with customer info)
- Business rules applied (e.g. filter cancelled orders for certain views)

### Gold (Business-Ready Aggregates)

- Pre-computed metrics for dashboards and reporting
- Examples: daily revenue, revenue by category, customer lifetime value
- Optimized for read-heavy analytics queries

## Data Flow

```
CSV files (data/sample/)
    │
    ▼
Bronze tables ── raw ingestion, metadata added
    │
    ▼
Silver tables ── cleaned, typed, deduplicated, enriched
    │
    ▼
Gold tables   ── aggregated business metrics
```

## Code Organization

| Layer | Code Location | Entry Point |
|---|---|---|
| Bronze | `src/retail_lakehouse/ingestion/` | `notebooks/02_ingest_bronze.py` |
| Silver | `src/retail_lakehouse/transformations/silver.py` | `notebooks/03_build_silver.py` |
| Gold | `src/retail_lakehouse/transformations/gold.py` | `notebooks/04_build_gold.py` |
| Quality | `src/retail_lakehouse/quality/checks.py` | `notebooks/05_quality_checks.py` |

## Config Strategy

Environment configs live in `conf/` as YAML files. The active environment is selected at runtime (default: `dev`). This keeps catalog names, schema names, and paths out of the transformation code.
