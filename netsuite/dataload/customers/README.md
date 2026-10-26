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

## Sage customer list report (2026-10-25)

Sage Intacct "Customer list" report, 652 customers. Laid out for print: a header row per customer (type, term, tax ID, credit limit, balance, status, on hold, currency, territory, rep, last invoice date, delivery options), then Display, Primary, Bill-to and Ship-to contact blocks with address, phone and email. `tools/parse_sage_report.py` flattens it to one row per customer: `data/sage-customers-flat-20261025.csv`.

- Status is Active on 648 of 652, so it cannot tell which customers to load. Activity has to come from last invoice date, balance, or contract dates.
- Active with an invoice since 2024-10-26 or a non-zero balance: 289. Since 2025-10-26: 270.
- No invoice in Sage: 283, of which 148 are type Chargebee (portal customers, billed outside Sage invoicing).
- Bill-to contact differs from the customer on 205 customers, usually a reseller (for example billed to Insight).
- Currency is blank on 566 and USD on 82. Terms are blank on 227 and use Sage names (30 Days, Due on Receipt, Due per Contract).

## Salesforce accounts export (2026-10-25)

449 accounts, all Lifecycle = Customer. 11 columns: Account Name, Lifecycle, Subnet Account Id, Billing State, Phone, Owner, Account Record Type, Partner Type, Domain, Website. No Account ID and no full address. 251 active Sage customers match a Salesforce account by normalized name.

## Review page

`tools/build_review.py` maps active Sage customers to the template columns, matches Salesforce by name, flags issues, and writes `data/customer-review.html` from `tools/review-template.html`. The page holds customer data, so it stays in `data/` and is published privately at https://claude.ai/artifact/GemCL1YnPNaMYaVQNbsDVB. Rebuild with `python3 tools/build_review.py` from this folder, then republish.

## Salesforce reports (2026-10-25, copied from Salesforce Classic)

- `data/sfdc-accounts-customers-20261025.xlsx`: Lifecycle = Active or Customer, 1,271 accounts with Account ID, parent, billing and shipping address, Subnet ID, phone, website. 15-character Account IDs: 7 pairs differ only by case, so the Salesforce Account ID column uses the 18-character case-safe ID, computed from the 15-character ID.
- `data/sfdc-accounts-with-partners-20261025.xlsx`: 1,418 account-partner rows.
- Matching Sage to Salesforce by name: 276 exact, 37 likely (to confirm), 335 no match. 967 Salesforce accounts have no Sage customer and are not loaded.

## Decisions

- 2026-10-26: Load every Sage customer not marked inactive (648). No activity cutoff.
- 2026-10-26: External ID left blank. Sage Customer ID, Salesforce Account ID and Subnet ID are their own fields in the load.
- 2026-10-26: Spell out reseller billing in added columns (Billed To (Reseller), Reseller Address, Reseller Invoice Email, Salesforce Partners) for SOA to map to their best practice. Customer Invoice Email holds the customer's own email.

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
