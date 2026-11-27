CREATE TABLE IF NOT EXISTS `retail-data-pipeline-516009.retail_mart.fact_sales` (
  invoice_no          STRING,
  stock_code          STRING,
  description         STRING,
  quantity            INT64,
  invoice_ts          TIMESTAMP,
  unit_price          FLOAT64,
  customer_id         INT64,
  country             STRING,
  is_cancelled        BOOL,
  line_amount         FLOAT64,
  missing_description BOOL,
  zero_price          BOOL,
  source_sheet        STRING,
  source_row_number   INT64,
  row_hash            STRING,
  batch_date          DATE,
  ingested_at         TIMESTAMP
)
CLUSTER BY invoice_ts, country, stock_code;