# Column mapping

Same approach as the customer load: Sage first, Ramp fills gaps, rules marked as rules.

| **Template column** | **Field** | **Source** |
|---|---|---|
| **ExternalID** | externalId | Same as Vendor ID |
| **Vendor ID** | vendorId | Sage vendor ID. V-##### kept; older V##### (339) and Ramp-created RMP_# (37) get the next numbers after V-01768 [TBC: same rule as customers] |
| **Individual** | isPerson | Sage "This vendor is an individual person" (34 are) |
| **First Name, Middle Name, Last Name** | firstName, middleName, lastName | Sage contact name, individuals only |
| **Company Name** | companyName | Sage vendor name. Required |
| **Vendor Category** | category | Sage vendor type, mapped to the template list: AR reseller to AR Reseller, Tax to Tax agency, MinIO employee to MinIO Employee. 922 vendors have no type |
| **Primary Subsidiary** | subsidiary | MinIO, Inc. [TBC: vendors with INR (9) or SGD (1) currency may belong to MinIO Pvt. Ltd. or MinIO Singapore Pte. Ltd.] |
| **Phone, Fax** | phone, fax | Sage, else Ramp contact phone |
| **Email** | email | Sage email, else Ramp contact email. Field holds 300 characters |
| **Comments** | comments | Sage comments |
| **Email Preference, Send Transaction Via Email / Fax / Print** | emailpreference, emailTransactions, faxTransactions, printTransactions | Blank, NetSuite defaults |
| **Address 1 (Label, Attention, Addressee, Phone, Address 1 and 2, City, State, Zip, Country, Default Shipping, Default Billing)** | address1_* | Sage pay-to address, else primary contact address, else Ramp check mailing address. Label "Remit-to", Default Billing TRUE |
| **Address 2 (same fields)** | address2_* | Sage return-to address where different from address 1. Label "Return-to", Default Shipping TRUE |
| **Legal Name** | legalName | Ramp vendor legal name (149), else Sage 1099 name |
| **Account** | accountNumber | Sage "Number": the account number the vendor assigned to MinIO (26 vendors) |
| **Terms** | terms | Sage term, else Ramp net terms, mapped to the NetSuite list (Due on Receipt, Net 10, Net 15, Net 30, Net 45, Net 60, Net 150). 132 vendors have terms in Sage |
| **Default Expense Account** | defaultExpenseAccount | Sage default expense account, mapped through the Sage# column of COA Draft v1 (for example Sage 62000 to 62600 Consultants). Set on 109 vendors; 2 Sage accounts have no mapping |
| **Default Payables Account** | defaultPayablesAccount | 20100 Accounts Payable - Trade [TBC] |
| **Credit Limit, Incoterm** | creditLimit, incoterm | Blank. Sage has none |
| **Tax ID** | taxIdNum | Sage tax ID (232), else Ramp TIN (140). Sensitive [TBC: load in this file or enter separately] |
| **1099 Eligible** | is1099Eligible | TRUE when Sage has a Form 1099 type (21) or the vendor type is 1099 Vendor (88) |
| **Vendor Bill tolerances (6 columns)** | purchaseorder*, receipt* | Blank. MinIO does not use purchase orders or item receipts |
| **Primary Currency** | currency | Sage default currency, else USD |
| **Additional Currency 1, 2** | additionalCurrency1, 2 | Blank |
| **Legacy Vendor ID** | Legacy Vendor ID | Sage vendor ID as it is in Sage |
| **Source System** | Source System | Sage Intacct, or "Sage Intacct; Ramp" where Ramp filled a value |

## Added columns

Not in the template, kept for review and for the record, as on the customer load: Question Categories, Duplicate Action, Ramp Vendor ID, Ramp Category, Owner, Department, Last activity (latest of Sage last bill, Sage last payment, Ramp last spend), Ramp 365-day spend, Flags.
