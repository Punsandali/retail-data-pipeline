import hashlib
import pandas as pd
from pathlib import Path

RAW = Path("data/processed/raw_combined.parquet")
OUT_DIR = Path("data/processed")
QUAR_DIR = Path("data/quarantine")

HASH_COLS = [
    "invoice_no", "stock_code", "description", "quantity",
    "invoice_ts", "unit_price", "customer_id", "country",
]

def add_row_hash(df):
    # One fingerprint per row, built from the original business columns.
    # Identical rows get identical hashes, so we can detect exact duplicates.
    joined = df[HASH_COLS].astype("string").fillna("").agg("|".join, axis=1)
    return joined.map(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest())

def clean_frame(df):
    df = df.copy()

    # Trim whitespace
    for col in ["invoice_no", "stock_code", "description", "country"]:
        df[col] = df[col].str.strip()

    # Flags and calculated fields
    df["is_cancelled"] = df["invoice_no"].str.upper().str.startswith("C", na=False) | (df["quantity"] < 0)
    df["line_amount"] = df["quantity"] * df["unit_price"]
    df["missing_description"] = df["description"].isna()
    df["zero_price"] = df["unit_price"] == 0

    df["row_hash"] = add_row_hash(df)

    # Quarantine rules (first matching reason wins)
    reason = pd.Series(pd.NA, index=df.index, dtype="string")
    reason = reason.mask(df["invoice_no"].isna() | (df["invoice_no"] == ""), "missing_invoice_no")
    reason = reason.mask(reason.isna() & (df["stock_code"].isna() | (df["stock_code"] == "")), "missing_stock_code")
    reason = reason.mask(reason.isna() & df["invoice_ts"].isna(), "missing_invoice_ts")
    reason = reason.mask(reason.isna() & df["quantity"].isna(), "missing_quantity")
    reason = reason.mask(reason.isna() & df["unit_price"].isna(), "missing_unit_price")
    reason = reason.mask(reason.isna() & (df["unit_price"] < 0), "negative_unit_price")
    df["reject_reason"] = reason

    quarantine = df[df["reject_reason"].notna()].copy()
    valid = df[df["reject_reason"].isna()].drop(columns=["reject_reason"])

    # Exact duplicates among valid rows: keep the first, count the rest
    dup_mask = valid.duplicated(subset=["row_hash"], keep="first")
    duplicates = valid[dup_mask]
    accepted = valid[~dup_mask]

    return accepted, quarantine, duplicates

def main():
    df = pd.read_parquet(RAW)
    source_rows = len(df)

    accepted, quarantine, duplicates = clean_frame(df)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QUAR_DIR.mkdir(parents=True, exist_ok=True)
    accepted.to_parquet(OUT_DIR / "accepted.parquet", index=False)
    quarantine.to_parquet(QUAR_DIR / "quarantine.parquet", index=False)

    # Reconciliation: every source row must be accounted for
    total = len(accepted) + len(quarantine) + len(duplicates)
    print(f"Source rows:        {source_rows:,}")
    print(f"Accepted:           {len(accepted):,}")
    print(f"Quarantined:        {len(quarantine):,}")
    print(f"Exact duplicates:   {len(duplicates):,}")
    print(f"Reconciles:         {total == source_rows}")
    print()
    print("Quarantine reasons:")
    print(quarantine["reject_reason"].value_counts().to_string())
    print()
    print(f"Accepted rows flagged cancelled:   {int(accepted['is_cancelled'].sum()):,}")
    print(f"Accepted rows with zero price:     {int(accepted['zero_price'].sum()):,}")
    print(f"Accepted rows missing description: {int(accepted['missing_description'].sum()):,}")

if __name__ == "__main__":
    main()