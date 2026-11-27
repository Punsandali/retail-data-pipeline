# Data Profile: Online Retail II

Sheets found: ['Year 2009-2010', 'Year 2010-2011']

## Sheet: Year 2009-2010
- Shape: (525461, 8)
- Columns: ['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'Country']

## Sheet: Year 2010-2011
- Shape: (541910, 8)
- Columns: ['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'Country']

## Combined dataset
- Total rows: 1,067,371

### Null counts
```
Invoice             0
StockCode           0
Description      4382
Quantity            0
InvoiceDate         0
Price               0
Customer ID    243007
Country             0
```

### Exact duplicate rows: 34,335

### Date range
- Min: 2009-12-01 07:45:00
- Max: 2011-12-09 12:50:00

### Cancellations
- Invoices starting with C: 19,494
- Rows with Quantity < 0: 22,950
- Rows with Price <= 0: 6,207
- Overlap (C-prefix AND negative qty): 19,493

### Numeric summary
```
           Quantity         Price
count  1.067371e+06  1.067371e+06
mean   9.938898e+00  4.649388e+00
std    1.727058e+02  1.235531e+02
min   -8.099500e+04 -5.359436e+04
25%    1.000000e+00  1.250000e+00
50%    3.000000e+00  2.100000e+00
75%    1.000000e+01  4.150000e+00
max    8.099500e+04  3.897000e+04
```

### Distinct values
- Countries: 43
- Stock codes: 5,305