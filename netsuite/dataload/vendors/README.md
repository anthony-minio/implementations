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

## Ramp export (2026-10-25)

`data/ramp-vendors-sensitive-20261025.csv`: 578 Ramp vendors, 58 columns. Holds TINs, tax classification, tax address and bank details (ACH for 181): never display those values. Useful non-sensitive fields: Sage Intacct ID, Ramp category, owner, department, legal name, payment method, net terms, contacts, check mailing address, spend (30 day, 365 day, YTD, lifetime), last spend date, contract dates and amounts.

- 551 Ramp vendors carry a Sage Intacct ID, all active in Sage, no duplicates: an exact link between the systems.
- 27 Ramp vendors have no Sage ID (for example KPMG LLP, Baker Botts LLP, Oracle America, Navan, ClickHouse).

Activity of the 1,770 active Sage vendors, using the latest of Sage last bill, Sage last payment and Ramp last spend:

| | In Ramp | Not in Ramp | Total |
|---|---|---|---|
| Active since 2024-10-26 | 478 | 85 | 563 |
| Last activity before 2024-10-26 | 8 | 292 | 300 |
| No activity recorded | 65 | 842 | 907 |

## Review table

`tools/build_review.py` maps the 1,770 active Sage vendors to the template, links Ramp by Sage vendor ID, and writes `data/vendor-review.html` (from `tools/review-template.html`, published privately at https://claude.ai/artifact/43aBdfBgsyuiGNHAtGPSsw) and `data/vendor-load.csv` (the 1,219 not in Ramp, full tax IDs). Bank numbers and tax IDs are masked wherever they appear on the page; two Sage "Number" fields that hold bank account numbers are not loaded. `data/coa-sage-map.json` maps Sage accounts to COA Draft v1.

## Validation

`tools/validate_load.py` checks every row of the review workbook against the raw Sage detail export, the Sage vendor list report and the Ramp export, independently of the build: row set (every active Sage vendor once, every Ramp-only vendor once), unique Vendor IDs, and each value traced to its own source record (name, IDs, category, phone, email, comments, fax, address, legal name, terms, expense account, tax ID, 1099, currency, Ramp link, bank details, last bill, last payment, balance, Ramp created, Ramp last spend, Ramp category and owner). It also checks the masked page matches the workbook row for row. 2026-10-26: no issues; a test with deliberately swapped values was caught.

## Load log

| Date | File | Records | Errors | Outcome |
|---|---|---|---|---|
