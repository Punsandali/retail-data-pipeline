import pandas as pd
from pathlib import Path
from google.cloud import bigquery

PROJECT_ID = "retail-data-pipeline-516009"
TABLE_ID = f"{PROJECT_ID}.retail_raw.raw_transactions"
ACCEPTED = Path("data/processed/accepted.parquet")

def main():
    df = pd.read_parquet(ACCEPTED)

    # Add lineage columns the guide asks for
    now = pd.Timestamp.now("UTC")
    df["batch_date"] = now.date()
    df["ingested_at"] = now

    # BigQuery loads work best with plain Python-friendly types
    df["customer_id"] = df["customer_id"].astype("Int64")
    df["source_sheet"] = df["source_sheet"].astype("string")

    client = bigquery.Client(project=PROJECT_ID)

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # safe to rerun: replaces the table
    )

    job = client.load_table_from_dataframe(df, TABLE_ID, job_config=job_config)
    job.result()  # wait for completion

    table = client.get_table(TABLE_ID)
    print(f"Loaded {table.num_rows:,} rows into {TABLE_ID}")
    print(f"Columns: {[f.name + ':' + f.field_type for f in table.schema]}")

if __name__ == "__main__":
    main()