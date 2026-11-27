import pandas as pd
from pathlib import Path

RAW = Path("data/processed/raw_combined.parquet")
ACCEPTED = Path("data/processed/accepted.parquet")
QUARANTINE = Path("data/quarantine/quarantine.parquet")
OUT = Path("docs/quality_summary.md")

def main():
    raw = pd.read_parquet(RAW)
    acc = pd.read_parquet(ACCEPTED)
    quar = pd.read_parquet(QUARANTINE)

    source_rows = len(raw)
    dup_rows = source_rows - len(acc) - len(quar)

    lines = ["# Quality Summary\n"]

    lines.append("## Row reconciliation")
    lines.append("| Measure | Rows | % of source |")
    lines.append("|---|---|---|")
    for label, n in [
        ("Source rows", source_rows),
        ("Accepted", len(acc)),
        ("Quarantined", len(quar)),
        ("Exact duplicates removed", dup_rows),
    ]:
        lines.append(f"| {label} | {n:,} | {n / source_rows:.2%} |")
    lines.append(f"\nReconciles: **{len(acc) + len(quar) + dup_rows == source_rows}**\n")

    lines.append("## Quarantine reasons")
    lines.append("```\n" + quar["reject_reason"].value_counts().to_string() + "\n```\n")

    lines.append("## Flags in accepted data")
    lines.append(f"- Cancelled / returned lines: {int(acc['is_cancelled'].sum()):,}")
    lines.append(f"- Zero-price lines: {int(acc['zero_price'].sum()):,}")
    lines.append(f"- Missing description: {int(acc['missing_description'].sum()):,}")
    lines.append(f"- Missing customer_id: {int(acc['customer_id'].isna().sum()):,}")

    lines.append("\n## Date range (accepted)")
    lines.append(f"- Min: {acc['invoice_ts'].min()}")
    lines.append(f"- Max: {acc['invoice_ts'].max()}")

    lines.append("\n## Non-product stock codes in accepted data")
    non_product = acc[acc["stock_code"].str.contains(r"^[A-Za-z]", regex=True, na=False)
                      & ~acc["stock_code"].str.match(r"^\d", na=False)]
    codes = non_product["stock_code"].value_counts().head(10)
    lines.append("```\n" + codes.to_string() + "\n```")
    lines.append("These are mostly postage, fees and manual entries. They will be reviewed in the SQL metrics stage.")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    main()