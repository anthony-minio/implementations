# Vendors

Vendor load, built the same way as `../customers/`: Sage is the source of truth for vendors, the load fills the NetSuite vendor template, and a review page and workbook go out for review before import.

Raw exports go in `data/`, which is not committed. Vendor records can hold bank details.

## Reference values

From the workbook `MINIO-Dimensions-from-sage-20260825`:

- Vendor types (equivalent to NetSuite Vendor Category): 1099 Vendor, AR reseller, Audit and Compliance, Consultants and Advisers, Consultants-Contractors, Credit Cards, Customer Reimbursements, Events, Events Incidental Expenses (under Events), Law Firms, Legal, MinIO employee, Public Relations, Tax.
- Terms: 15 days, Due on Receipt, Net 10, Net 150, Net 30, Net 45, Net 60.
- Subsidiaries: MinIO, Inc.; MinIO Pvt. Ltd. (INR); MinIO Singapore Pte. Ltd. (SGD).
- Currencies: AED, CAD, EUR, GBP, INR, KRW, SAR, SEK, SGD, USD.

## Load log

| Date | File | Records | Errors | Outcome |
|---|---|---|---|---|
