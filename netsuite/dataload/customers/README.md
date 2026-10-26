# Customers

Template: `Customer_Import_Template_-_Updated_1.xlsx` (tabs Field Restrictions, CustomerTemplate, List). 31 columns.

## Approach

1. Export customers from Sage. Sage is the source of truth for customer data.
2. Export accounts from Salesforce.
3. Match the two, enrich Sage from Salesforce where Sage is blank, and list every conflict for review. Salesforce never overwrites Sage without a decision.
4. Populate the template.

Raw exports go in `data/`, which is not committed.

## Sage export (2026-10-26)

Default Sage Intacct customer list view: 650 customers, 9 columns (Customer ID, Customer name, City, State or territory, ZIP or postal code, Customer type ID, Total due, One-time use, Entity). Custom views with more columns errored. Saved as `data/sage-customers-20261026.csv`; issue list in `data/sage-review-20261026.csv`.

Missing from the export: street address, email, phone, currency, terms, tax, active/inactive status, parent, Salesforce ID. `Total due` exports as the text "View due"; `Entity` is blank on every row.

| Finding | Count |
|---|---|
| Old `C#####` IDs that look like investors or note holders, not customers | 16 |
| Customers sharing an exact name with another | 22 (11 pairs) |
| Similar names, possible duplicates | 6 (3 pairs) |
| No city, state or postal code | 116 |
| No customer type | 6, plus the 16 above |
| One-time use | 2 |
| City ending in a comma | 327 |

Customer types: Direct Sales 263, Direct Sales with Reseller 193, Chargebee 149, Reseller 12, Marketplace 6, Billing Vendor 2, MinIO Training Subscription 2, Event Sponsor 2, blank 21.

## Template lists

| List | Values |
|---|---|
| Subsidiary | MinIO, Inc.; MinIO Pvt. Ltd.; MinIO Singapore Pte. Ltd. |
| Status | CUSTOMER-Lost Customer; CUSTOMER-Closed Won; CUSTOMER-Renewal |
| Type | Company; Individual |
| Category | Direct Customer; Reseller; End Customer; OEM/MSP |

Terms (for example Net 30) must exist in NetSuite before the load. Parent Company needs the parent loaded first, or in an earlier row of the same file.

## Load log

| Date | File | Records | Errors | Outcome |
|---|---|---|---|---|
