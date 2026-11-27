import argparse
import pandas as pd
from pathlib import Path
from google.cloud import bigquery

PROJECT_ID = "retail-data-pipeline-516009"
STAGE_TABLE = f"{PROJECT_ID}.retail_stage.stg_sales_batch"
FACT_TABLE = f"{PROJECT_ID}.retail_mart.fact_sales"
ACCEPTED = Path("data/processed/accepted.parquet")

COLS = """invoice_no, stock_code, description, quantity, invoice_ts, unit_price,
  customer_id, country, is_cancelled, line_amount, missing_description,
  zero_price, source_sheet, source_row_number, row_hash, batch_date, ingested_at"""

REBUILD_SQL = f"""
CREATE OR REPLACE TABLE `{FACT_TABLE}`
CLUSTER BY invoice_ts, country, stock_code
AS
SELECT {COLS} FROM (
  SELECT {COLS} FROM `{FACT_TABLE}`
  WHERE row_hash NOT IN (SELECT row_hash FROM `{STAGE_TABLE}`)
  UNION ALL
  SELECT {COLS} FROM `{STAGE_TABLE}`
)
"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", required=True, help="inclusive, YYYY-MM-DD")
    p.add_argument("--end", required=True, help="exclusive, YYYY-MM-DD")
    args = p.parse_args()

    df = pd.read_parquet(ACCEPTED)
    batch = df[(df["invoice_ts"] >= args.start) & (df["invoice_ts"] < args.end)].copy()

    if batch.empty:
        print(f"STATUS: no_data for {args.start} to {args.end}. Nothing loaded.")
        return

    now = pd.Timestamp.now("UTC")
    batch["batch_date"] = pd.Timestamp(args.start).date()
    batch["ingested_at"] = now
    batch["customer_id"] = batch["customer_id"].astype("Int64")
    batch["source_sheet"] = batch["source_sheet"].astype("string")

    client = bigquery.Client(project=PROJECT_ID)

    # 1. Stage the batch (replaces any previous staging contents)
    job = client.load_table_from_dataframe(
        batch, STAGE_TABLE,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
    )
    job.result()
    print(f"Staged {len(batch):,} rows for {args.start} to {args.end}")

    # 2. Rebuild the fact table: existing rows not in batch + batch
    client.query(REBUILD_SQL).result()

    total = client.get_table(FACT_TABLE).num_rows
    print(f"fact_sales now has {total:,} rows")

if __name__ == "__main__":
    main()