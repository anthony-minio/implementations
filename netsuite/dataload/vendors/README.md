# Vendors

Vendor load, built the same way as `../customers/`: Sage is the source of truth for vendors, the load fills the NetSuite vendor template, and a review page and workbook go out for review before import.

Raw exports go in `data/`, which is not committed. Vendor records can hold bank details.

## Reference values

From the workbook `MINIO-Dimensions-from-sage-20260825`:

- Vendor types (equivalent to NetSuite Vendor Category): 1099 Vendor, AR reseller, Audit and Compliance, Consultants and Advisers, Consultants-Contractors, Credit Cards, Customer Reimbursements, Events, Events Incidental Expenses (under Events), Law Firms, Legal, MinIO employee, Public Relations, Tax.
- Terms: 15 days, Due on Receipt, Net 10, Net 150, Net 30, Net 45, Net 60.
- Subsidiaries: MinIO, Inc.; MinIO Pvt. Ltd. (INR); MinIO Singapore Pte. Ltd. (SGD).
- Currencies: AED, CAD, EUR, GBP, INR, KRW, SAR, SEK, SGD, USD.

## Sage exports (2026-10-25)

- `data/sage-vendors-active-export-20261025.csv`: default vendor list view, active vendors, 1,775 (5 flagged One-time use).
- `data/sage-vendors-all-detail-20261025.csv`: all fields, 1,770 active vendors (the 5 one-time-use vendors are not in it), 241 columns with structured addresses, contacts, terms, 1099, payment method, last bill and payment dates, and ACH bank details (164 vendors). Build from this file; never display bank details.
- `data/sage-vendor-list-report-20261025.csv`: print-layout vendor list report, 1,788 vendors (1,775 active, 13 inactive).

Profile of the 1,770:

| | Count |
|---|---|
| Never billed in Sage | 1,220 |
| Last billed before 2024-10 | 332 |
| Billed since 2024-10 | 218 |
| Vendor type Credit Cards (418 never billed) | 427 |
| Vendor type MinIO employee | 136 |
| Vendor type AR reseller (125 never billed) | 127 |
| Vendor type blank | 922 |
| Terms set | 132 |
| Email / street address / tax ID | 514 / 429 / 232 |
| Form 1099 type (NEC 17, MISC 4) | 21 |

IDs: V-##### (1,394), older V##### (339), RMP_# (37, created from Ramp).

## Load log

| Date | File | Records | Errors | Outcome |
|---|---|---|---|---|
