# Task 3 – Customer Data Cleansing  
**Ataccama Pre-Interview Assessment**

---

## How to run

**Requirements:** Python 3.10+ and `pandas`

```bash
pip install pandas

# Place customers.csv in the same directory as the script, then:
python cleanse_customers.py
```

The script reads `customers.csv` and writes `customers_cleansed.csv` to the same directory.

---

## What the script does

| Step | Detail |
|------|--------|
| **Load** | Reads the semicolon-delimited CSV with all columns as strings to avoid pandas mis-typing. |
| **Name cleansing** | Strips leading/trailing whitespace → collapses internal duplicate spaces → applies Title Case. |
| **Date parsing** | Tries four common formats in order (`M/D/YYYY`, `YYYY-MM-DD`, `D/M/YYYY`, `D.M.YYYY`). Empty or unparseable values become `NaT` (null). |
| **`days_until_next_control`** | Integer: *(src_date_next_control − today)*. Negative = already past. `NaT` next-control date → `NaN`. |
| **`control_status`** | `OVERDUE` (< 0 days), `DUE_SOON` (0–30 days), `OK` (> 30 days), `UNKNOWN` (date missing/invalid). |
| **Export** | Writes the cleansed file with dates in ISO `YYYY-MM-DD` format for portability. |

---

## Assumptions

1. **Delimiter** is `;` (semicolon), as found in the source file.  
2. **Date format** in the source is primarily `M/D/YYYY`.  Multiple formats are tried so the script is resilient to mixed formats in the same column.  
3. **Missing dates** (empty string or truly unparseable) are treated as `NaT`; the derived `control_status` is set to `UNKNOWN` rather than raising an error.  
4. **`DUE_SOON` window** is 30 days. This is configurable via the `DUE_SOON_DAYS` constant at the top of the script.  
5. **Name normalisation** uses Title Case (`MC RAE HOLDINGS LTD` → `Mc Rae Holdings Ltd`). If the business requires a different casing convention (e.g., all-caps for legal names) this is a one-line change.  
6. **No rows are dropped** – even rows with invalid/missing dates are retained in the output (with nulls) so no data is silently lost.
