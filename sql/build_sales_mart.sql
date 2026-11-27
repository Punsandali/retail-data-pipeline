-- dim_product: one row per stock_code
CREATE OR REPLACE TABLE `retail-data-pipeline-516009.retail_mart.dim_product` AS
SELECT
  stock_code,
  REGEXP_CONTAINS(stock_code, r'^[0-9]{5}') AS is_product,
  ARRAY_AGG(description IGNORE NULLS ORDER BY invoice_ts DESC LIMIT 1)[SAFE_OFFSET(0)] AS description,
  COUNT(*) AS line_count
FROM `retail-data-pipeline-516009.retail_mart.fact_sales`
GROUP BY stock_code;

-- dim_country: one row per country
CREATE OR REPLACE TABLE `retail-data-pipeline-516009.retail_mart.dim_country` AS
SELECT
  country,
  COUNT(*) AS line_count
FROM `retail-data-pipeline-516009.retail_mart.fact_sales`
GROUP BY country;

-- agg_daily_sales: one row per date and country
CREATE OR REPLACE TABLE `retail-data-pipeline-516009.retail_mart.agg_daily_sales` AS
SELECT
  DATE(invoice_ts) AS sales_date,
  country,
  COUNT(DISTINCT invoice_no) AS invoice_count,
  SUM(IF(NOT is_cancelled AND line_amount > 0, line_amount, 0)) AS gross_sales,
  SUM(IF(is_cancelled, ABS(line_amount), 0)) AS returns_value,
  SUM(IF(NOT is_cancelled AND line_amount > 0, line_amount, 0))
    - SUM(IF(is_cancelled, ABS(line_amount), 0)) AS net_sales,
  SUM(IF(NOT is_cancelled AND quantity > 0, quantity, 0)) AS units_sold
FROM `retail-data-pipeline-516009.retail_mart.fact_sales`
GROUP BY sales_date, country;