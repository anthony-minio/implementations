# Integration Sandbox

Workbook: `MinIO_Integration_Sandbox_Test_Scripts_UAT.xlsx`. 94 tests across nine integrations: I7 Avalara (12), I8 Ramp (11), I9 FISPAN-JPMC (11), I10 Bank of America (10), I11 Navan (11), I12 Rippling (10), I13 Chargebee (12), I14 Carta (9), I15 Okta (8). MinIO owner Anthony C on all nine. This workbook has no Review Notes tab.

**Summary:** this is the strongest of the five workbooks. Each integration has connectivity, configuration, positive, negative and reconciliation tests, and most expected results are specific. The gaps are about MinIO's own setup:
- reseller and international sales tax;
- India and Singapore through Navan, FISPAN and Rippling;
- which system pays a bill, so nothing is paid twice;
- Chargebee portal revenue, where three parts of the design give three different answers.

Testing has already started: I7-01 and I10-01 pass, and I10-02 fails. See X-11 for the housekeeping on those rows.

## Our findings

### Avalara (I7)

#### INT-01 · I7-03 · Fix · Medium

**Comment for SOA:** The item list ("subscription, support, professional services, hardware") doesn't match MinIO's items. We sell license, support and training (11 items), with Professional Services to come. Please use the loaded items. Taxability of electronically delivered software, software maintenance and training varies by state. The approved tax code for each item should come from MinIO's tax advisor, and the test should compare against that list.

**Posted:** No

#### INT-02 · I7 (new) · Gap · High

**Comment for SOA:** Please add a reseller sale. When we bill a reseller who is buying for resale, the reseller's resale certificate should exempt the invoice. Ship-to (the end customer's location) and bill-to (the reseller) can be in different states. The test should confirm which address Avalara uses, and that the exemption is applied and recorded. 205 Sage customers are billed through someone else, usually a reseller.

**Posted:** No

#### INT-03 · I7 (new) · Gap · Medium

**Comment for SOA:** Please add an invoice from MinIO, Inc. to a customer outside the US. We have customers in Poland, Cote d'Ivoire, Singapore and elsewhere on MinIO, Inc. Expected: no US sales tax, and the Avalara document shows why. This is different from I7-06 (a US state where we have no nexus) and from I7-10 (a non-US subsidiary).

**Posted:** No

#### INT-04 · I7 (new) · Gap · Medium

**Comment for SOA:** Please check that estimates and sales orders calculate tax without committing a document in Avalara, and that only the invoice commits. Otherwise Avalara would overstate the liability for orders not yet billed.

**Posted:** No

#### INT-05 · I7-11 · Confirm · Low

**Comment for SOA:** "Void (or delete, per policy)": please agree the policy before UAT. Will MinIO void invoices, and with or without the Void Transactions Using Reversing Journals preference? Or will it delete them, or credit them? Then test that one path. The Avalara result differs for each.

**Posted:** No

#### INT-06 · I7-02 · Fix · Low

**Comment for SOA:** The precondition says "nexus states confirmed by MinIO tax team". We sent SOA the production nexus list in October. Please name that list as the test data, so the comparison is against what we provided.

**Posted:** No

### Ramp (I8)

#### INT-07 · I8-04, I8-05 · Fix · Medium

**Comment for SOA:** The test data uses department names that aren't MinIO's: "R&D", and "Engineering, Sales, G&A". Please use the departments from the signed-off department update. I8-02 and I8-08 should then confirm that the old departments are inactive and can't be selected in Ramp.

**Posted:** No

#### INT-08 · I8-01 · Gap · Medium

**Comment for SOA:** "Select the subsidiary to sync": will Ramp cover MinIO Pvt. Ltd. and MinIO Singapore Pte. Ltd. as Ramp entities? If so, please test that each entity maps to its own subsidiary and currency, with a bill and a card transaction for each. If Ramp is US only, please say how India and Singapore spend reaches NetSuite.

**Posted:** No

#### INT-09 · I8-03 · Gap · Medium

**Comment for SOA:** Please check the new vendor against the vendor sync design from the vendor load:
- Vendor ID and External ID SYNCED FROM RAMP;
- Source System "Synced from Ramp";
- a vendor marked Inactive in Ramp is not synced;
- an existing NetSuite vendor is matched, not duplicated.

Ramp holds tax IDs and bank details. Please confirm which of these sync to NetSuite. We'd expect bank details only where NetSuite pays the vendor (FISPAN), visible only to restricted roles (I9-10).

**Why:** `dataload/vendors/README.md`.

**Posted:** No

#### INT-10 · I8-06 · Gap · High

**Comment for SOA:** I8-06 covers a bill paid in Ramp showing as paid in NetSuite. Please add the reverse: a Ramp-synced bill paid in NetSuite (through FISPAN for India or Singapore, or recorded by hand) must show as paid in Ramp, so it can't be paid again from Ramp Bill Pay. Please also say what happens to a bill entered directly in NetSuite (P2-08) that Ramp never sees. See X-09.

**Posted:** No

#### INT-11 · I8-09 · Confirm · Medium

**Comment for SOA:** The expected result is "sync error ... (or the bill posts to the next open period, per agreed design)". Please agree the design before UAT and write the single expected result. It affects how A/P is cut off at month end.

**Posted:** No

### FISPAN-JPMC (I9)

#### INT-12 · I9-06, I9-07 · Confirm · Medium

**Comment for SOA:** Where do the India and Singapore bills paid through FISPAN come from: Ramp, or entered in NetSuite? Where do the vendor bank details (account, IFSC, SWIFT) come from, and who keeps them up to date? The answers decide whether INT-10 (paid status back to Ramp) and P2P-03 (vendor subsidiary) apply.

**Posted:** No

#### INT-13 · I9-08 · Fix · Medium

**Comment for SOA:** Please state the payment approval rules being tested: who can create a payment, who can approve it, the limits, and whether a second approval is needed above a threshold. Please also test that the person who creates a payment can't approve it.

**Posted:** No

### Bank of America (I10)

#### INT-14 · I10-01, I10-02 · Fix · High

**Comment for SOA:** I10-02 failed because the GL accounts don't match, and I10-01 records the same issue in its comment. Please log it as a defect and fix the mapping against MinIO's BofA account list and the final chart of accounts. Account 10020 - BoA (operating) is already used in O2-09. Once fixed, please re-run I10-01 and I10-02.

**Posted:** No

#### INT-15 · I10-09 · Info · Low

**Comment for SOA:** Agree with marking I10-09 N/A while BofA payments from NetSuite are out of scope (2026-11-10 email). Please set the status to N/A with that reason in Comments, so the Summary can reach Ready for Sign-off.

**Posted:** No

### Navan (I11)

#### INT-16 · I11-07 · Fix · Medium

**Comment for SOA:** The expected result assumes every expense converts to USD. For employees of MinIO Pvt. Ltd. and MinIO Singapore Pte. Ltd., expenses should post to their own subsidiary in INR or SGD. Please add a test for each subsidiary, and keep the USD conversion test for a US employee spending abroad.

**Posted:** No

#### INT-17 · I11-05 · Confirm · Medium

**Comment for SOA:** Which card pays Navan bookings? If it's a Ramp card, the same charge also syncs from Ramp (I8-07), and it would be recorded twice. Please agree which system posts travel bookings, and test that only one does.

**Posted:** No

#### INT-18 · I11-10 · Confirm · Low

**Comment for SOA:** "Process reimbursement per the agreed method": please name the method (Navan, Ramp, payroll or a NetSuite payment), so the expected result can be checked in both systems.

**Posted:** No

#### INT-19 · I11-02 · Fix · Low

**Comment for SOA:** Employee mapping depends on the Rippling employee sync (I12-02), so please run I12 before I11. If India or Singapore employees aren't in Rippling, please say how they get into NetSuite for Navan.

**Posted:** No

### Rippling (I12)

#### INT-20 · I12-07 · Confirm · Medium

**Comment for SOA:** "Employees in more than one entity (if applicable)": does Rippling run payroll for India and Singapore? If not, how does their payroll reach NetSuite (manual JE, provider file)? Please add a test for that path. Please also cover contractors paid through Rippling and their 1099 reporting (P2P Review Note 2).

**Posted:** No

#### INT-21 · I12-03, I15-05 · Gap · High

**Comment for SOA:** Please test the full leaver flow across the three systems. An employee terminated in Rippling should be deactivated in Okta and lose NetSuite access, including the direct NetSuite login. The NetSuite employee record should become inactive. MinIO's direction is for the HR system to drive Okta provisioning, so this is the path we'll rely on.

**Posted:** No

#### INT-22 · I12-05, I12-10 · Gap · Medium

**Comment for SOA:** Please name the cash and clearing accounts the payroll JE credits, and add a check that payroll funding in the bank (BofA feed) matches the payroll JE. Department mapping in I12-04 should use the departments from the signed-off update.

**Posted:** No

### Chargebee (I13)

#### INT-23 · I13-03 · Gap · High

**Comment for SOA:** We loaded the Chargebee customers from Sage: 149 are of type Chargebee. I13-03 only tests a new customer. Please add a returning customer: someone already loaded from Sage who buys again in Chargebee must be matched to the existing NetSuite customer, by Subnet ID, email or a stored Chargebee ID per design, and not created again.

**Posted:** No

#### INT-24 · I13-02, I13-09 · Confirm · High

**Comment for SOA:** Portal revenue has three different answers in the design so far:
- I13-09 expects an ARM revenue plan over the service period.
- The I13 scope note says "no rev rec".
- Our item notes have portal sales recognized immediately. That would mean either a separate portal item with Direct Revenue Posting, or no item at all if portal sales reach NetSuite as a summary journal from the payment processor.

Please agree one design with MinIO accounting before UAT, then rewrite I13-02, I13-04 and I13-09 to match.

**Why:** Item load open question 10.

**Posted:** No

#### INT-25 · I13-06 · Gap · Medium

**Comment for SOA:** Portal payments arrive through a payment gateway, paid out in batches and net of fees. Please test the payout as well as the payment: the payment posts to a clearing account, the payout is matched to the bank deposit (BofA feed), and the gateway fees are recorded as an expense.

**Posted:** No

#### INT-26 · I13-05 · Confirm · Medium

**Comment for SOA:** "Tax approach agreed (Chargebee tax vs Avalara)" is a precondition, but it isn't agreed yet as far as we know. Please confirm the decision and owner. Whichever system calculates tax, the test should confirm that Avalara records the liability once, for I7-12.

**Posted:** No

### Carta (I14)

#### INT-27 · I14-03 · Gap · Medium

**Comment for SOA:** Stock-based compensation expense needs to post by department, and by subsidiary if employees of MinIO Pvt. Ltd. or MinIO Singapore Pte. Ltd. hold awards. Please add department and subsidiary to the JE lines checked in I14-03 and I14-04.

**Posted:** No

#### INT-28 · I14-07 · Confirm · Low

**Comment for SOA:** I14-07 assumes JE approval is enabled. That depends on the JE approval workflow still to be designed (R2R Review Note 9). Please link the two.

**Posted:** No

### Okta (I15)

#### INT-29 · I15-08 · Fix · Medium

**Comment for SOA:** "Behave as configured" needs the values. MinIO has asked for 8 to 12 hour Okta sessions. Please state the Okta session length and NetSuite's own session timeout, and check that they work together, so users aren't sent back to log in partway through the day.

**Note for Anthony:** The 8 to 12 hour session request is still PENDING on the WIP canvas. Confirm the number before posting.

**Posted:** No

#### INT-30 · I15-02, I15-07 · Gap · Medium

**Comment for SOA:** Please add a test that SSO users can't get round Okta by signing in on the NetSuite login page with a password. Only the break-glass admin should be able to. For I15-07, the expected result should include NetSuite's own two-factor authentication on the break-glass login, as well as the login being recorded.

**Posted:** No

#### INT-31 · I15 (new) · Confirm · Low

**Comment for SOA:** How will NetSuite users and their roles be created and changed at go-live: by hand by an administrator, or provisioned from Okta? If by hand, please add a test of the joiner, mover and leaver steps, so role changes are approved and logged.

**Posted:** No
