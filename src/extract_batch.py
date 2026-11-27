import pandas as pd
from pathlib import Path

SRC = Path("data/raw/online_retail_II.xlsx")
OUT = Path("data/processed/raw_combined.parquet")

RENAME = {
    "Invoice": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_ts",
    "Price": "unit_price",
    "Customer ID": "customer_id",
    "Country": "country",
}

def main():
    sheets = pd.read_excel(SRC, sheet_name=None)
    frames = []
    for sheet_name, df in sheets.items():
        df = df.rename(columns=RENAME)
        # keep lineage: which sheet and which row in that sheet
        df["source_sheet"] = sheet_name
        df["source_row_number"] = range(2, len(df) + 2)  # row 1 is the header
        frames.append(df)

    df = pd.concat(frames, ignore_index=True)

    # Store IDs and codes as text so values like "85123A" and "C536379" stay intact
    for col in ["invoice_no", "stock_code", "description", "country"]:
        df[col] = df[col].astype("string")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    print(f"Saved {len(df):,} rows to {OUT}")
    print(df.dtypes)

if __name__ == "__main__":
    main()