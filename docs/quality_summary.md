# Quality Summary

## Row reconciliation
| Measure | Rows | % of source |
|---|---|---|
| Source rows | 1,067,371 | 100.00% |
| Accepted | 1,033,031 | 96.78% |
| Quarantined | 5 | 0.00% |
| Exact duplicates removed | 34,335 | 3.22% |

Reconciles: **True**

## Quarantine reasons
```
reject_reason
negative_unit_price    5
```

## Flags in accepted data
- Cancelled / returned lines: 22,497
- Zero-price lines: 6,014
- Missing description: 4,275
- Missing customer_id: 235,146

## Date range (accepted)
- Min: 2009-12-01 07:45:00
- Max: 2011-12-09 12:50:00

## Non-product stock codes in accepted data
```
stock_code
POST            2086
DOT             1425
M               1387
C2               277
D                173
S                101
BANK CHARGES     100
ADJUST            67
AMAZONFEE         36
DCGS0058          31
```
These are mostly postage, fees and manual entries. They will be reviewed in the SQL metrics stage.