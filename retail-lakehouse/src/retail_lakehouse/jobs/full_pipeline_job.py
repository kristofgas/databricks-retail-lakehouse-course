"""Run the full pipeline: bronze → silver → gold.

This is the top-level entry point a Databricks job would call
to execute the entire pipeline end-to-end.
"""

from retail_lakehouse.jobs import bronze_job, silver_job, gold_job


def run(env: str = "dev") -> None:
    print(f"=== Full Pipeline [{env}] ===\n")

    print("--- Stage 1: Bronze Ingestion ---")
    bronze_job.run(env)

    print("\n--- Stage 2: Silver Transformations ---")
    silver_job.run(env)

    print("\n--- Stage 3: Gold Aggregations ---")
    gold_job.run(env)

    print("\n=== Pipeline Complete ===")


if __name__ == "__main__":
    run()
