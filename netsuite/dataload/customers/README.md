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

## Validation

`tools/validate_load.py` checks every value in `data/customer-load-draft.csv` against the raw Sage report, the Sage customer list and the Salesforce accounts file, independently of the parser and build: row set, unique IDs, names, address text, city/state/postal code, country, emails, reseller emails, terms, currency, VAT ID, Salesforce ID, Subnet ID, parent, stray characters, label text, encoding and NetSuite field lengths. Run it after every rebuild. 2026-10-26: no issues. 2026-10-27: extended to the decisions below (row set without investors and StoreManager, one-time customers, L3Harris split rows, categories, Nisha's Subnet IDs), full country names, phone format and trace to source, and address text moved between fields (no word invented, none lost); no issues, and a test copy with 8 planted errors had all 8 caught.

## Review page

`tools/build_review.py` maps active Sage customers to the template columns, matches Salesforce by name, flags issues, and writes `data/customer-review.html` from `tools/review-template.html`. The page holds customer data, so it stays in `data/` and is published privately at https://claude.ai/artifact/GemCL1YnPNaMYaVQNbsDVB. Rebuild with `python3 tools/build_review.py` from this folder, then republish.

## Salesforce reports (2026-10-25, copied from Salesforce Classic)

- `data/sfdc-accounts-customers-20261025.xlsx`: Lifecycle = Active or Customer, 1,271 accounts with Account ID, parent, billing and shipping address, Subnet ID, phone, website. 15-character Account IDs: 7 pairs differ only by case, so the Salesforce Account ID column uses the 18-character case-safe ID, computed from the 15-character ID.
- `data/sfdc-accounts-with-partners-20261025.xlsx`: 1,418 account-partner rows.
- Matching Sage to Salesforce by name: 276 exact, 37 likely (to confirm), 335 no match. 967 Salesforce accounts have no Sage customer and are not loaded.

## Decisions

- 2026-10-26: Load every Sage customer not marked inactive (648). No activity cutoff.
- 2026-10-26: Customer ID keeps Sage C-##### numbers; the 16 non-conforming Sage IDs (C00001 to C00016) get C-00642 to C-00657. External ID = Customer ID. NetSuite auto-numbers new customers as C-##### from C-00658. Sage Customer ID, Salesforce Account ID and Subnet ID are their own fields in the load.
- 2026-10-26: Spell out reseller billing in added columns (Billed To (Reseller), Reseller Address, Reseller Invoice Email, Salesforce Partners) for SOA to map to their best practice. Customer Invoice Email holds the customer's own email.
- 2026-10-26: Status CUSTOMER-Closed Won for every customer (all are active in Sage). Renewals to be set from deal data later.
- 2026-10-26: Customer Invoice Email is the first AP or purchasing address, else the first address; all other addresses go to an added Additional Emails column.
- 2026-10-26: Terms mapped to the NetSuite list: Due on Receipt, Net 10, Net 15, Net 30, Net 45, Net 60, Net 150. Other Sage day counts become new Net N terms (Net 20, 28, 59, 65, 75, 90, 120) to create in NetSuite. 5 years becomes Net 1825. Due per Contract stays as in Sage, to research.
- 2026-10-26: Added Question Categories column. Investors listed first (by name), then likely Salesforce matches to review (by name), then everyone else by Customer ID.
- 2026-10-26: Investor records (C00001 to C00016) moved to the notes as an open question for SOA.
- 2026-10-26: Subsidiary MinIO, Inc. for every customer.
- 2026-10-26: Salesforce parents that are not Sage customers are left out (no billing history); Parent Company blank for those 35 customers.
- 2026-10-26: Customers whose Sage type has no obvious Customer Category (Chargebee, Marketplace, Billing Vendor, Training Subscription, Event Sponsor, no type) are left blank and marked "SOA Category Unknown" in Question Categories, listed after the Salesforce matches.
- 2026-10-26: Likely Salesforce matches reviewed: 35 confirmed; C-00044 Ministry of Defence (Singapore) and C-00142 Bae Systems not matched.
- 2026-10-26: Sage corrections in the load: C-00387 Proctor & Gamble city Lodz (address is in Poland; replaces the earlier United States correction), C-00253 Orange Cote d'Ivoire (Abidjan, Cote d'Ivoire), C-00108 NSN Brasil (city, postal code and attention), garbled accents repaired, five US postal codes with a lost leading zero restored.
- 2026-10-26: Leidos C-00489 (Chargebee, never invoiced, same email) merges into Leidos Holdings C-00516; Reston address is primary.
- 2026-10-26: Subnet IDs are a key identifier: one NetSuite customer per Subnet account; records with different Subnet IDs are never merged. Applied Materials, Davidson, L3Harris (incl. C-00333 L3 Technologies) and Saudi Telecom have several Subnet accounts; their 9 Sage records are kept separate and marked "Subnet ID to assign".
- 2026-10-26: Subnet IDs paired by date (earlier Sage record with earlier Subnet account): C-00103 348, C-00462 879, C-00371 755, C-00592 1067, C-00241 537, C-00542 998. Records with different Subnet IDs are never merged. L3Harris proposed: C-00333 695, C-00385 784, C-00562 1026; 716 and 720 have no Sage record.
- 2026-10-26: Duplicates merged, 14 groups, 16 records: keep the most recently invoiced record (else more data, then lower ID); merged records' Sage IDs, different addresses (Second and Third Address) and emails carried to the kept record. Added by email domain: Hollister into C-00640, Bank of Nova Scotia C-00039 and C-00049 into C-00405, SITE C-00465 into C-00204 (Subnet ID 478 carried), MoD C-00629 into C-00481. BMC Software and BMC Helix kept separate. `data/customer-load.csv` holds the 632 customers to load.
- 2026-10-26: VAT ID holds VAT/GST registration numbers only, formatted with the country prefix; US EINs and company registration numbers moved to an added Other Tax ID column.
- 2026-10-26: Count bridge: 650 active in the first Sage export, minus 2 one-time-use customers not in the customer list report (C-00012, C-00021; open question) = 648, minus 16 merged duplicates = 632 (616 without the 16 investor records).

- 2026-10-27 (meeting with Ming, Nisha, Richard, Tory, Sheng; Nisha on Slack): investor records C00001 to C00016 not loaded, so no renumbering. New categories Chargebee, Marketplace and Other (Event Sponsor, Billing Vendor); MinIO Training Subscription is Direct Customer. AEG Worldwide End Customer, Subnet 779 (the Asana note says 77); Exness Direct Customer, Subnet 669; M S International Direct Customer, Subnet 754; StoreManager C-00036 not loaded. L3Harris: C-00333 695, new C-00642 716 (contract CN-SO0565), new C-00643 720 (CN-SO0603), C-00385 784, C-00562 1026; the new customers copy C-00333. Next number C-00644.
- 2026-10-27: One-time-use customers C-00012 and C-00021 not loaded: no category and no invoices in the exports (first loaded, then reversed the same day). Due per Contract terms left blank. New L3Harris customers named "L3 Technologies Inc. -01" and "-02". AEG Subnet 779 confirmed (Asana note corrected).
- 2026-10-27: Phone: US numbers of US customers (999) 999-9999, all others including Canada international (+44 20 7885 8888); Sage first, else Salesforce; numbers not valid in the source left out. Needs `pip install phonenumbers`.
- 2026-10-27: Country names with a comma (Korea, Republic of) were cut to "Republic of" by the parser; fixed. Addresses with parts in the wrong field corrected by moving Sage's own text (`ADDRESS_FIX` in `tools/build_review.py`); country follows the address; no address means no country.
- 2026-10-27: Workbook `data/MinIO_Customer_Load_to_NetSuite_20261027.xlsx` (tabs Notes, Customers-Draft): 633 rows, 617 to load (650 active - 16 investors - StoreManager - 2 one-time + 2 L3Harris split = 633; - 16 merged = 617). Notes give each decision as scenario, decision and change. Built by `tools/build_delivery.py`; the review page's notes are no longer maintained.

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
