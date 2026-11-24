# Procure to Pay

Workbook: `MinIO_Procure_to_Pay_Test_Scripts_UAT.xlsx`. 13 tests: P1 Vendors (2) and P2 Procure to Pay (11). SOA owners Tristan / Josh, MinIO owner Richard.

**Summary:** almost every step is tested twice, once in Ramp and once in NetSuite, but the workbook never says which one is MinIO's process. It also stops at the bill. The parts that need checking most are paying the bill and Ramp and NetSuite agreeing on what has been paid. Paying covers Ramp Bill Pay for US vendors and FISPAN-JPMC for India and Singapore. The workbook doesn't reflect the vendor sync design we agreed for the vendor load.

## SOA's Review Notes: our position

| # | Test | SOA note | Our position |
|---|---|---|---|
| 1 | P2 (new) | Gap: bill payment, FISPAN wires, NetSuite payments showing in Ramp | Agree, and this is the top priority in the workbook. Test each payment path: Ramp Bill Pay; FISPAN-JPMC for India and Singapore; and BofA payments from NetSuite, out of scope per the 2026-11-10 email (I10-09). Test that a bill paid in one system shows as paid in the other, so it can't be paid twice |
| 2 | P2 (new) | Gap: 1099 vendors and reporting | Agree. The vendor load sets 1099 Eligible from Sage, and Ramp holds the tax classification. The test should check that 1099 status syncs from Ramp and that the 1099 report picks up the right vendors and amounts |
| 3 | P2 (new) | Gap: Ramp card, amortization templates and fixed asset coding | Agree. Card is in I8-07. Amortization and fixed assets need a Ramp-to-NetSuite test. See R2R-09 and R2R-13 |
| 4 | P2-03 | Confirm: roles and approval limits | Agree |
| 5 | P2-05 | Fix: step title | Agree |
| 6 | P2 | Info: IDs renumbered | Fine |
| 7 | P1-01, P1-02 | Info: status mapped to Not Run | Fine |

## Our findings

### P2P-01 · P1-02 · Confirm · High

**Comment for SOA:** For the vendor load we agreed that Ramp vendors sync to NetSuite, and their Vendor ID and External ID come through as SYNCED FROM RAMP. Sage-only vendors were loaded with their Sage IDs. P1-02 creates a vendor directly in NetSuite, with approval. A vendor created in NetSuite doesn't exist in Ramp, so its bills can't be approved or paid there. It will also be duplicated if the vendor is later added in Ramp. Please confirm when, if ever, a vendor is created in NetSuite: for example, only for vendors paid through FISPAN. Then limit P1-02 to that case, or mark it N/A and test that the NetSuite path is restricted.

**Why:** Vendor load decisions, 2026-10-28 (`dataload/vendors/README.md`). See X-09.

**Posted:** No

### P2P-02 · P1-01 · Gap · Medium

**Comment for SOA:** "Vendor synced into NetSuite with correct information" needs the fields to check: subsidiary, Vendor ID and External ID, Source System "Synced from Ramp", 1099 eligibility, terms, category, default expense account and currency. Please also add two negative tests. First, a vendor marked Inactive in Ramp is not added to the sync. Second, a vendor that already exists in NetSuite (one of the 53 Sage-only vendors we loaded) is matched, not created again.

**Why:** `dataload/vendors/README.md`.

**Posted:** No

### P2P-03 · P1 (new) · Gap · Medium

**Comment for SOA:** We loaded every vendor under MinIO, Inc. The FISPAN tests (I9-06, I9-07) pay India and Singapore vendors from those subsidiaries, so those vendors need the right subsidiary and currency. How are India and Singapore vendors created: through a Ramp entity for each subsidiary, or in NetSuite? Please add a vendor test for each.

**Posted:** No

### P2P-04 · P2-01 to P2-05 · Confirm · Medium

**Comment for SOA:** Which purchases at MinIO need a PO, and which need a receipt before the bill is paid? Most of our spend is software and services. If receipts and matching won't be used, please cut P2-04 and P2-05 (and the NetSuite PO, P2-02) down to the cases MinIO will run. Please state the PO approval limits in P2-01 and P2-03.

**Posted:** No

### P2P-05 · P2-08 · Fix · Medium

**Comment for SOA:** Step 3, "Vendor Bill Approval", uses Ramp navigation (Bill Pay > Bills > For Approval) in a NetSuite test. Please give the NetSuite approval steps, the approval limits, and what happens when the person who entered the bill tries to approve it.

**Posted:** No

### P2P-06 · P2 (new) · Gap · Medium

**Comment for SOA:** Please add a duplicate bill test:
- a second bill with the same vendor and reference number, entered in NetSuite (duplicate number warning);
- a bill that comes through Ramp after the same invoice was entered in NetSuite.

**Posted:** No

### P2P-07 · P2 (new) · Gap · Medium

**Comment for SOA:** All P2P tests run in MinIO, Inc. Please add a bill, a vendor credit and a payment in MinIO Pvt. Ltd. (INR) and MinIO Singapore Pte. Ltd. (SGD), including a foreign-currency bill paid at a different exchange rate, so the realized gain or loss can be checked.

**Posted:** No

### P2P-08 · P2-01, P2-06, P2-07 · Gap · Medium

**Comment for SOA:** "Approval process happens within Ramp" should be part of the expected result: the approver should match MinIO's approval policy for the amount and department. Ramp routes approvals by the manager hierarchy that comes from the HR system. We have seen approvals go to the wrong person when managers weren't up to date.

**Posted:** No

### P2P-09 · Several · Fix · Low

**Comment for SOA:** Small corrections:
- **P2-03:** "the Purchase Order created in P2" should say P2-02.
- **P2-05:** the expected result says "Item is successfully created". It should say Item Receipt.
- **P2-11:** the Inventory/Items reports don't apply, and "format is as expected" should name the expected format.
- **Typos:** "Standaralone" (P2-07), "Purhcases" (P2-02, P2-05), "NetSutie" (P2-09), "NetSUite" (P2-08).

**Posted:** No
