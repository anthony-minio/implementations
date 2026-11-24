# Record to Report

Workbook: `MinIO_Record_to_Report_Test_Scripts_UAT.xlsx`. 66 tests on seven tabs: R1 Setup and Configuration (3), R2 Intercompany (1), R3 Period Close (6), R4 Budgets (3), R5 Bank and Cards (3), R6 Journals and Amortization (5), R7 Fixed Assets (45). SOA owner Danna Bandales, MinIO owner Anthony C.

**Summary:** this workbook carries the most template residue: an Australian fiscal year and GST reports, UK and warehouse roles. Its balance is off as well. Fixed assets have 45 of the 66 tests, while the monthly close MinIO will actually run has one generic test. That close covers three subsidiaries, two foreign currencies, deferred revenue reclass, intercompany and consolidation. The fiscal year setup is the one finding that is hard to undo after go-live.

## SOA's Review Notes: our position

| # | Test | SOA note | Our position |
|---|---|---|---|
| 1 | R2-01 | Fix: rewrite intercompany with MinIO entities | Agree. Use MinIO, Inc., MinIO Pvt. Ltd. and MinIO Singapore Pte. Ltd. SOA lists Saudi Arabia as an entity. We have three on record, so please confirm (X-07). Keep invoice and bill pairing only if MinIO bills between entities |
| 2 | R3-05 | Fix: BAS doesn't apply | Agree. Mark it N/A. The US sales tax reconciliation is in I7-12 |
| 3 | R3-03 | Confirm: tax reporting periods with Avalara | Depends on R2R-17. If India or Singapore GST is filed from NetSuite, tax periods are needed. If not, mark it N/A |
| 4 | R7-13 | Fix: FF PRM role | Agree |
| 5 | R7-08 | Fix: no expected result for compound asset | Agree, and R7-24 is the same test (R2R-14). Likely N/A |
| 6 | R7-44, R7-45 | Confirm: Multi-Book depends on the change order | Agree. N/A unless the change order is approved before UAT |
| 7 | R7-34 to R7-38 | Confirm: lease accounting in scope | Needs MinIO accounting to answer: does MinIO have leases that fall under ASC 842, and will they be tracked in NetSuite or outside it? |
| 8 | R7 (new) | Gap: fixed asset roll-forward saved search | Agree |
| 9 | R1/R6 (new) | Gap: JE approval, year-end adjustment period, intercompany revenue and expense accounts, monthly trial balance | Agree. All four are needed before UAT |
| 10 | R6 | Info: spelling | Agree, along with the other Australian and UK wording (X-05) |

## Our findings

### R2R-01 · R3-02, R3-03 · Fix · High

**Comment for SOA:** Both tests set up the year with "standard for Australia": first fiscal month July. MinIO's fiscal year starts February 1, with Q1 running February to April. Please correct the test data to First Fiscal Month February, and confirm that the accounting periods already set up in the sandbox follow the same calendar. This is hard to change once transactions post, so we'd like it checked before any UAT transactions are entered.

**Note for Anthony:** The February start comes from the BizApps sprint reports (`bizapps-docs/sprints/README.md`). Confirm it's the fiscal calendar Finance uses before posting.

**Posted:** No

### R2R-02 · R1-01, R1-02 · Fix · Medium

**Comment for SOA:** "Validate ... configured correctly" needs something to compare against. Please name the approved source for each check:
- three subsidiaries with their base currencies (USD, INR, SGD);
- departments per the signed-off department update;
- classes License, Support, Training and Professional Services;
- the final chart of accounts from COA Draft v1;
- whether an elimination subsidiary is needed, if Automated Intercompany Management is used.

**Posted:** No

### R2R-03 · R3 (new) · Gap · High

**Comment for SOA:** Please add a mock month-end close for one period, run across all three subsidiaries in the order MinIO will use. It should cover:
- amortization journals;
- depreciation;
- the deferred revenue reclass from short-term to long-term (23100 to 23200);
- revaluation of foreign-currency balances;
- intercompany elimination;
- consolidated exchange rates and the cumulative translation adjustment;
- the Avalara tax liability reconciliation;
- bank and Ramp card reconciliations;
- locking A/R and A/P, and closing the period.

The expected result is a consolidated trial balance, P&L and balance sheet that we review. R3-01 covers the mechanics of closing a period, but not MinIO's close.

**Posted:** No

### R2R-04 · R3-01 · Fix · Medium

**Comment for SOA:** Step 3 uses "Create Debtors Tax Invoice", which is a localized form name. Please use the MinIO invoice form. The expected result, "record not saved/popup appears", should say what happens for each role: which MinIO roles, if any, may post to a closed period, and which are blocked.

**Posted:** No

### R2R-05 · R5-01, R5-02 · Fix · Medium

**Comment for SOA:** R5-01 says bank feeds must be tested in production, but I10 is testing the BofA feed in the sandbox. Please agree which applies. R5-01 and R5-02 largely repeat each other. Please merge them into one test per bank (BofA and JPMC) that uses a real statement period. Please use the statement's actual ending balance, not "5000". R5-02 also assumes the Australian DD/MM/YYYY date format.

**Posted:** No

### R2R-06 · R5-03 · Confirm · Medium

**Comment for SOA:** Which card accounts will be reconciled in NetSuite? We expect the Ramp card liability account, reconciled to the Ramp statement (see I8-11). If so, please name it in the test. The note about "Bill Payment ... using the Credit Card" doesn't fit how Ramp card spend arrives.

**Posted:** No

### R2R-07 · R6-04 · Fix · High

**Comment for SOA:** This test contradicts itself. It names the template "12 month SL Amortisation" with Amortisation Period 12. The step then says this "will set the expense to amortise over 2 months", and the expected result looks for a template called "2 month SL Amortisation". A tester following it exactly will fail. Please correct it to 12 months throughout.

**Posted:** No

### R2R-08 · R6-01 · Fix · Medium

**Comment for SOA:** Please replace "Cash at Bank" with a MinIO account. Please add the JE approval workflow (SOA note 9), with the approver and the limit, and a JE CSV import, which we will use for close entries. Is the deferred ("Defer Entry") journal something MinIO will use? If not, please drop it. Reversing journals for accruals should stay.

**Posted:** No

### R2R-09 · R6-03, R6-04, R6-05 · Gap · Medium

**Comment for SOA:** The R6 scope note lists Ramp amortization templates, but no step uses Ramp. Please test a prepaid bill coded in Ramp with an amortization template, through to the amortization schedule in NetSuite and the monthly amortization journal. Please also check R6-03 against the prepaid scenarios in the prepaids discussion notes.

**Posted:** No

### R2R-10 · R6-02 · Confirm · Low

**Comment for SOA:** Does MinIO allocate costs by statistical account, for example by headcount across departments or subsidiaries? "9952 Headcount" comes from the template. If MinIO doesn't allocate, please mark R6-02 N/A. If it does, where does headcount come from: Rippling?

**Posted:** No

### R2R-11 · R7 · Confirm · High

**Comment for SOA:** Fixed assets have 45 of the 66 R2R tests. Please size them to MinIO's fixed asset register. We'd suggest a core set:
- setup: asset types, accounts and depreciation methods;
- an asset created from a Ramp bill coded to a fixed asset account, through proposal;
- depreciation;
- disposal by write-off;
- the roll-forward and register reports;
- the mid-life import of existing assets (R2R-12).

Mark N/A unless MinIO confirms they are needed:
- **R7-09:** inventory item. MinIO doesn't use inventory.
- **R7-08 and R7-24:** compound assets.
- **R7-30:** revaluation. Under US GAAP, assets can't be revalued upward, only written down for impairment.
- **R7-34 to R7-38:** leases.
- **R7-44 and R7-45:** Multi-Book.
- **R7-07 and R7-29:** alternate methods. These are needed only if tax depreciation is kept in NetSuite rather than by the tax preparer.

**Posted:** No

### R2R-12 · R7-41, R7-42, R7-43 · Gap · High

**Comment for SOA:** The mid-life import is the fixed asset test that matters most at cutover, but R7-42 and R7-43 only export saved searches. Please make the expected result a tie-out: for each asset, cost, accumulated depreciation, net book value and remaining life agree with the Sage fixed asset register at cutover. Totals by asset type and subsidiary should also agree with the opening trial balance. The first depreciation run after import should match the Sage schedule.

**Posted:** No

### R2R-13 · R7-12 to R7-15 · Fix · Low

**Comment for SOA:** These tests buy, receive, bill and pay for an asset directly in NetSuite. MinIO buys through Ramp. Please replace them with a Ramp bill coded to the fixed asset account that syncs to NetSuite and produces an asset proposal (P2P Review Note 3). Keep the NetSuite path only if it's an allowed exception (X-09).

**Posted:** No

### R2R-14 · R7-08, R7-24 · Fix · Low

**Comment for SOA:** R7-08 and R7-24 are the same test (Build Compound Asset). Please remove one.

**Posted:** No

### R2R-15 · R7-28 · Gap · Medium

**Comment for SOA:** "Asset successfully depreciated" should state the expected amount for a test asset (cost, life, method, start date), along with the depreciation journal's accounts and the period it posts to. Please also test depreciation for an asset in India or Singapore, in local currency.

**Posted:** No

### R2R-16 · R4 · Confirm · Medium

**Comment for SOA:** Will MinIO keep budgets in NetSuite for budget-versus-actual reporting, or does FP&A budget elsewhere? If NetSuite, please include department and class in the budget import and test budget versus actual by department. If not, the R4 tests can be cut down or marked N/A.

**Posted:** No

### R2R-17 · R3 (new) · Confirm · Medium

**Comment for SOA:** India GST and TDS and Singapore GST: will these be handled in NetSuite (localization SuiteApps, tax codes, tax periods) or by the local accountants outside NetSuite? No test covers either option. If in NetSuite, please add tests. If outside, please note that and mark R3-03 N/A.

**Posted:** No

### R2R-18 · R3-04, R3-06 · Fix · Medium

**Comment for SOA:** "Verify the output and format of the reports" needs a list. Please test MinIO's reporting package:
- consolidated and per-subsidiary trial balance (the custom monthly TB in SOA note 9);
- P&L by department;
- balance sheet;
- deferred revenue roll-forward;
- intercompany balances by entity pair.

Each should be checked against an expected figure from the test transactions, including the PDF and Excel exports.

**Posted:** No
