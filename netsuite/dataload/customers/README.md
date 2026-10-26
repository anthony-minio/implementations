# Customers

Template: `Customer_Import_Template_-_Updated_1.xlsx` (tabs Field Restrictions, CustomerTemplate, List). 31 columns.

## Approach

1. Export customers from Sage. Sage is the source of truth for customer data.
2. Export accounts from Salesforce.
3. Match the two, enrich Sage from Salesforce where Sage is blank, and list every conflict for review. Salesforce never overwrites Sage without a decision.
4. Populate the template.

Raw exports go in `data/`, which is not committed.

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
