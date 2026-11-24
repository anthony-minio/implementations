# Across all files

Findings that apply to more than one workbook. Post each one on the workbook it names first, or raise it with SOA as a general note.

Reviewed 2026-11-24 against SOA's workbooks as received that day: 195 tests (Design to Build 7, Order to Cash 15, Procure to Pay 13, Record to Report 66, Integration Sandbox 94).

## Overall picture

The scripts are well organized, and SOA's own Review Notes already catch several real gaps. Three things stand out:

1. **The parts of the design that matter most to MinIO are the parts not yet tested.** These include revenue recognition (license at a point in time, support over time, multi-year deals, short- and long-term deferred revenue), the license delivery trigger, reseller and portal sales, and the approval workflows. Each one is waiting on a design decision, a module, or "add later". Generic NetSuite tests run at full length while these get none.
2. **Much of the content comes from other clients' templates.** It shows Australian fiscal years and GST reports, UK and warehouse roles, inventory items, and another client's role name. That suggests the steps have not yet been checked against MinIO's design.
3. **Most expected results can't fail.** "Transaction successfully saved" and "Correct GL entries have been created" don't tell the tester what correct looks like.

## Priority list

The findings to raise first, across all files:

| # | Finding | Why first |
|---|---|---|
| 1 | X-02 Revenue recognition untested | Core to MinIO's revenue and audit. Nothing tests it today |
| 2 | X-01 Readiness list for design not yet final | UAT starts 2026-12-08. Missing designs will block tests |
| 3 | X-03 No data migration validation | Opening balances and open items have no UAT test |
| 4 | R2R-01 Fiscal year set up as Australian (July) | Hard to fix once transactions post |
| 5 | INT-24 Portal (Chargebee) revenue has three different answers | Same flow, conflicting design |
| 6 | X-04 Tests run as Administrator or template roles | Permission and segregation of duties gaps won't show |
| 7 | X-13 Reseller, marketplace and portal sales not scripted | About a third of Sage customers buy through a reseller |
| 8 | P2P-01 / X-09 Which system creates vendors, bills and payments | Risk of duplicates and double payment between Ramp and NetSuite |
| 9 | X-11 Recorded results without a defect logged | The Summary shows 0 open defects while BofA mapping has failed |
| 10 | X-07 India and Singapore not covered | Three subsidiaries, tested as one |

---

### X-01 · All workbooks · Confirm · High

**Comment for SOA:** Several tests depend on design that isn't final yet: revenue allocation and ARM (D2B note 1 and 4, O2C note 5), revenue recognition rules, the license delivery trigger, the vendor approval workflow (P1-02), the PO approval workflow (P2-03), JE approval (R2R note 9), the Multi-Book change order (R7-44, R7-45) and the scope of BofA payments (I10-09). Please add a readiness list: each dependency, who owns it, and the date it will be ready. Please also mark which tests stay Blocked if it isn't ready by 2026-12-08. We'd like to agree a cut-off date so these tests can be written in full before UAT starts.

**Posted:** No

### X-02 · O2C, D2B, Integrations · Gap · High

**Comment for SOA:** No test anywhere checks revenue recognition on a real MinIO transaction. That covers license revenue at a point in time, support recognized over time, multi-year deals billed annually, the short- and long-term deferred revenue split, and revenue starting when the license key is issued. For MinIO this is the highest-risk part of the implementation. We'd like it treated as a go-live requirement, not something to "add once the module is provisioned". Please confirm when ARM will be provisioned in the sandbox and add the scenarios listed under O2C-04, O2C-06 and O2C-10.

**Why:** Our item load still has no revenue recognition rules set up (`dataload/noninventory-items`, open question 11), and the license delivery trigger is still open (open question 9).

**Posted:** No

### X-03 · All workbooks · Gap · High

**Comment for SOA:** None of the five workbooks tests whether the migrated data is right. Is there a separate data migration validation script? If not, please add tests for:
- the opening trial balance by subsidiary, tied to Sage;
- open A/R by customer and open A/P by vendor, tied to Sage aging;
- deferred revenue balances and their schedules;
- the fixed asset register: cost, accumulated depreciation and net book value;
- record counts for customers (632 loaded), vendors and items, compared with the load files.

**Why:** The Data migration action item tracker exists, but no UAT script covers it.

**Posted:** No

### X-04 · All workbooks · Fix · High

**Comment for SOA:** Tests name a mix of MinIO roles (MinIO - A/R Analyst, MinIO - A/P Analyst, MinIO - Controller, MinIO - Item Manager) and roles from templates: Administrator, Controller, Financial Controller, Accountant, Inventory Manager, A/P Clerk / A/P Purchasing, FF PRM - Item Manager, A/P Analyst - UK, Warehouse Associate - US/UK, Accounting Manager - US. Please list the roles MinIO will have at go-live and run every test with the role the user will actually have. Keep Administrator for setup only. Testing as Administrator hides missing permissions.

Please also add negative tests for segregation of duties:
- the person who enters a bill or JE can't approve it;
- A/P and A/R roles can't post journals or reopen periods;
- only authorized roles can change vendor bank details. I9-10 already tests this for FISPAN.

**Posted:** No

### X-05 · R2R, O2C, P2P · Fix · Medium

**Comment for SOA:** Several steps come from other clients' templates and don't apply to MinIO:
- **Australian content:**
  - Fiscal year starting in July (R3-02, R3-03).
  - The BAS statement (R3-05).
  - "Create Debtors Tax Invoice" (R3-01).
  - DD/MM/YYYY dates (R5-02).
  - The "Cash at Bank" account (R6-01).
  - "Amortisation" and "Memorise" (R6).
- **UK and warehouse content:** roles and barcode-scanning fulfillment (R2-01).
- **Inventory content:** inventory items and Inventory/Items reports (R7-09, P2-11).
- **Another client's role:** "FF PRM" (R7-13).

Please check each workbook against MinIO's design before UAT, not only the rows flagged in the Review Notes.

**Posted:** No

### X-06 · O2C, P2P, R2R · Fix · Medium

**Comment for SOA:** Most expected results can't fail: "Transaction successfully saved", "Correct GL entries have been created by the system", "Report loads successfully", "Report format is as expected". Please give the expected accounts and amounts for each key transaction, using MinIO's chart of accounts. For example, invoicing a license item should debit A/R and credit 23100 Deferred Revenue - ST, because our items carry 23100 as the deferred revenue account. Revenue should move to 41100 License Revenue when recognized. For reports, please name the report and what the tester should compare it to.

**Posted:** No

### X-07 · All workbooks · Gap · Medium

**Comment for SOA:** MinIO has three subsidiaries: MinIO, Inc., MinIO Pvt. Ltd. and MinIO Singapore Pte. Ltd. Most tests don't name a subsidiary, so in practice they will all run in MinIO, Inc. Please name the subsidiary on each test. Please run P2P (bill, vendor credit, payment), period close, FX revaluation, Navan expenses and bank reconciliation at least once in India and once in Singapore.

Also, R2R Review Note 1 lists MinIO's entities as "US, Singapore, India and Saudi Arabia". We have three subsidiaries on record. Please confirm whether a Saudi Arabia entity is in scope.

**Why:** Subsidiary names are in `netsuite/dataload/README.md`, as given on 2026-10-26.

**Posted:** No

### X-08 · R2R, Integrations · Gap · Medium

**Comment for SOA:** Nothing tests foreign currency beyond setting up exchange rates. Please add tests for:
- realized gain or loss on a foreign-currency payment;
- period-end revaluation of open foreign-currency balances;
- consolidated exchange rates;
- the cumulative translation adjustment in the consolidated balance sheet.

India and Singapore keep their books in INR and SGD, so this will run every month.

**Posted:** No

### X-09 · P2P, Integrations, R2R · Confirm · High

**Comment for SOA:** P2P tests both a Ramp path and a NetSuite path for vendors, POs, receipts, bills and vendor credits. R7 also buys and pays for assets directly in NetSuite. Please confirm which path is MinIO's process for each. If Ramp is the system of record for A/P, anything entered in NetSuite skips Ramp's approvals and can't be paid from Ramp. It also risks a duplicate when the same vendor or bill later comes through Ramp. Please test only the allowed path, and test that the other is restricted or limited to named exceptions, such as India or Singapore bills paid through FISPAN.

**Posted:** No

### X-10 · D2B, P2P, Integrations · Fix · Low

**Comment for SOA:** Several cross-references still use IDs from before the reformat:
- **D1-04:** OTC01.
- **D1-06:** MD02 and PTP01.
- **P2-03:** "the PO created in P2", which means P2-02.
- **Integration tabs:** TC02, TC03 and TC04 in I7, I8, I11, I12, I13 and I14.

Please replace them with the new IDs so testers can follow the chain.

**Posted:** No

### X-11 · Integrations · Fix · Medium

**Comment for SOA:** Some results are already recorded but don't match the instructions:
- **I7-01:** Pass, with Actual Result "Passed", Executed By "Tony" and no date.
- **I10-01:** Pass, but the comment says the GL accounts don't match.
- **I10-02:** Fail, with Defect ID "Yes", but there's nothing in the Defect Log. The Summary therefore shows 0 open defects.
- **I10-01 and I10-02:** Executed By "Yes".

Please log the BofA mapping issue as a defect (D-001, assigned to SOA), put its ID on I10-02, and complete the Actual Result, Executed By and Execution Date on the rows already run.

**Note for Anthony:** "Tony" and the BofA rows dated 2026-11-11 may have been entered on our side. Check before posting, and if so, correct them ourselves.

**Posted:** No

### X-12 · Summaries · Confirm · Low

**Comment for SOA:** MinIO owners as listed:
- **Anthony C:** all 66 Record to Report tests and all 94 integration tests, 160 of 195.
- **Tory Li:** Design to Build and Order to Cash, 22.
- **Richard:** Procure to Pay, 13.

We'll confirm the MinIO owner for each area before UAT. Record to Report in particular needs an accounting owner to run the tests and sign them off.

**Note for Anthony:** Decide the owners first. Our vendor notes spell the name "Tori". Check the spelling on the Summary tabs.

**Posted:** No

### X-13 · O2C, Integrations · Gap · High

**Comment for SOA:** The Order to Cash tests cover only a direct sale. Of MinIO's customers in Sage:
- 263 are Direct Sales;
- 193 are Direct Sales with Reseller;
- 149 are Chargebee (portal);
- 12 are Reseller;
- 6 are Marketplace.

Please add end-to-end tests for:
- **A reseller-billed order:** the end customer and the reseller as agreed in the customer design, the invoice going to the reseller, and tax handled through the reseller's resale exemption.
- **A marketplace sale:** including the marketplace surcharge fee item, which is still TBD on the Items tab.
- **A portal sale:** see INT-24.

**Why:** Customer types are from the Sage export of 2026-10-26 (`dataload/customers/README.md`).

**Posted:** No

### X-14 · Integrations, O2C · Confirm · Low

**Comment for SOA:** The integration workbook starts at I7. Where are I1 to I6: tested elsewhere, out of scope, or not yet written? O2-02 has the Salesforce opportunity ID, quote number and contract ID typed in by hand, so please confirm that no Salesforce integration is planned for go-live. Please also confirm how the license key issue date reaches NetSuite. It is in BigQuery, from Subnet, and we'd expect it to drive invoicing and the start of revenue.

**Posted:** No

### X-15 · D2B, O2C, P2P, R2R · Gap · Medium

**Comment for SOA:** The integration tabs include negative tests, but the process workbooks have almost none. Please add at least:
- posting to a locked or closed period with each role;
- a duplicate vendor bill reference number;
- approving over the limit, or approving your own transaction;
- an inactive customer, vendor or item on a new transaction (D1-07 covers items only);
- a credit memo or refund larger than the invoice.

**Posted:** No

### X-16 · O2C, P2P, R2R, Integrations · Confirm · Low

**Comment for SOA:** Steps ask for Location on sales order fulfillment, credit memos, refunds, purchase orders, Ramp coding (P2-01, P2-06, P2-07, P2-09) and asset disposal. Will MinIO use the Location segment? If not, please remove it from the steps so testers don't guess at a value.

**Posted:** No
