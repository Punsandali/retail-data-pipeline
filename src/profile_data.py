import pandas as pd
from pathlib import Path

SRC = Path("data/raw/online_retail_II.xlsx")
OUT = Path("docs/data_profile.md")

# sheet_name=None reads every sheet into a dict
sheets = pd.read_excel(SRC, sheet_name=None)

lines = ["# Data Profile: Online Retail II\n"]
lines.append(f"Sheets found: {list(sheets.keys())}\n")

frames = []
for name, df in sheets.items():
    lines.append(f"## Sheet: {name}")
    lines.append(f"- Shape: {df.shape}")
    lines.append(f"- Columns: {list(df.columns)}\n")
    frames.append(df)

df = pd.concat(frames, ignore_index=True)

lines.append("## Combined dataset")
lines.append(f"- Total rows: {len(df):,}")
lines.append("\n### Null counts")
lines.append("```\n" + df.isna().sum().to_string() + "\n```")
lines.append(f"\n### Exact duplicate rows: {df.duplicated().sum():,}")

lines.append(f"\n### Date range\n- Min: {df['InvoiceDate'].min()}\n- Max: {df['InvoiceDate'].max()}")

inv = df["Invoice"].astype(str)
lines.append(f"\n### Cancellations\n- Invoices starting with C: {inv.str.startswith('C').sum():,}")
lines.append(f"- Rows with Quantity < 0: {(df['Quantity'] < 0).sum():,}")
lines.append(f"- Rows with Price <= 0: {(df['Price'] <= 0).sum():,}")
overlap = (inv.str.startswith("C") & (df["Quantity"] < 0)).sum()
lines.append(f"- Overlap (C-prefix AND negative qty): {overlap:,}")

lines.append("\n### Numeric summary")
lines.append("```\n" + df[["Quantity", "Price"]].describe().to_string() + "\n```")

lines.append(f"\n### Distinct values\n- Countries: {df['Country'].nunique()}\n- Stock codes: {df['StockCode'].nunique():,}")

OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))