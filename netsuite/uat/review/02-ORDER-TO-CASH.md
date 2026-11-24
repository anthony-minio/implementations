# Order to Cash

Workbook: `MinIO_Order_to_Cash_Test_Scripts_UAT.xlsx`. 15 tests: O1 Customers (1) and O2 Order to Cash (14). SOA owner Danna Bandales, MinIO owner Tory Li.

**Summary:** the workbook walks through a generic sales order, invoice, payment and credit. It doesn't test how MinIO actually sells and earns revenue: through resellers, multi-year deals billed annually, revenue starting when the license key is issued, renewals and change orders, and the customer-facing invoice. The customer test doesn't match the customer design we loaded.

## SOA's Review Notes: our position

| # | Test | SOA note | Our position |
|---|---|---|---|
| 1 | O2-07 | Fix: no expected result | Agree |
| 2 | O2-11 | Fix: no expected result | Agree |
| 3 | O2-03, O2-04 | Confirm: Inventory Manager role, set to N/A if MinIO doesn't fulfill physical items | Partly agree. MinIO doesn't ship physical goods, but fulfillment may be how a license delivery is recorded (option a of the license delivery trigger). Please don't set these N/A until that's decided. If option a is chosen, these become the key tests, run by the role that issues license keys |
| 4 | O2-13, O2-14 | Fix: amortization belongs in R2R | Agree |
| 5 | O2 (new) | Gap: revenue allocation (ARM) | Agree, and this is the highest priority in the workbook. See X-02, O2C-04, O2C-06 and O2C-10 |
| 6 | O2 (new) | Gap: intercompany invoice and bill pairing | Agree, if MinIO bills between entities. Otherwise cross-reference R2 once it's rewritten |
| 7 | O2 (new) | Info: tax in I7 | Agree. The invoice tests here should still show tax calculated, using the Preview Tax step that's already in O2-02 |
| 8 | O1-01 | Info: reset to Not Run | Agree |

## Our findings

### O2C-01 · O1-01 · Fix · Medium

**Comment for SOA:** Please line up the customer test with the customer design we loaded:
- **Subsidiary:** MinIO, Inc. for every customer. Step 2 says to pick the subsidiary with the most transactions.
- **Status:** CUSTOMER-Closed Won.
- **Category:** use the agreed list, including the categories SOA is still defining for Chargebee, Marketplace and similar types.
- **Terms:** from the agreed terms list.
- **Customer Invoice Email:** plus the additional emails.
- **Fields to fill in:** Subnet ID, Salesforce Account ID (18-character), Sage Customer ID, and the reseller billing fields.

Please also add a duplicate check. Subnet ID is our key: one NetSuite customer per Subnet account. Creating a second customer with the same Subnet ID, name or email should be caught by duplicate detection, or by a rule SOA proposes.

**Why:** Decisions of 2026-10-26 in `dataload/customers/README.md`.

**Posted:** No

### O2C-02 · O1-01 · Confirm · Low

**Comment for SOA:** Step 3 adds one or two currencies to the customer. In Sage almost every customer is USD or has no currency set. Will MinIO invoice any customer in a currency other than USD? If not, please drop this step. If so, please add a foreign-currency invoice and payment test.

**Posted:** No

### O2C-03 · O2 (new) · Gap · High

**Comment for SOA:** Please add a reseller-billed order from sales order to payment. 205 customers in Sage are billed to someone other than the customer, usually a reseller such as Insight. The test should show:
- where the end customer and the reseller sit on the transaction, per SOA's recommendation for the reseller fields in our customer load;
- that the invoice goes to the reseller's invoice email;
- that the reseller's resale exemption is applied in Avalara;
- the reseller margin discount (D2B-04).

**Why:** `dataload/customers/README.md`. See also X-13.

**Posted:** No

### O2C-04 · O2-01, O2-02 · Gap · High

**Comment for SOA:** O2-01 only creates an annual billing schedule. Please add a multi-year deal with license and support, billed annually in advance. The test should cover:
- the sales order with the billing schedule;
- the first invoice and its deferred revenue;
- the period-end reclass of the amount earned more than 12 months out from 23100 Deferred Revenue - ST to 23200 Deferred Revenue - LT;
- the year-2 invoice generated through Billing Operations (O2-06, O2-07).

Please also confirm whether the Unbilled, Billed and Paid accounts under 23200 are still needed.

**Why:** Item load open question 7.

**Posted:** No

### O2C-05 · O2-02 · Fix · Medium

**Comment for SOA:** The steps leave key fields to the tester: "select the order type", "select the status", "enter the pro-rated amount", and start and end date "(optional)". On support and subscription lines, the start and end dates drive revenue, so they should be required and checked. Please give the test data: which customer, which items, quantities, prices, dates and billing schedule. The expected result should be more than "Transaction successfully Saved".

**Posted:** No

### O2C-06 · O2 (new) · Gap · High

**Comment for SOA:** Please add a test for the license delivery trigger. License keys are issued by hand, and the issue date (in BigQuery, from Subnet) should drive invoicing and the start of license revenue. Whichever option is chosen needs a test that revenue starts on the issue date and not on the order date:
- (a) an item fulfillment posted when the key is issued;
- (b) a custom revenue recognition event;
- (c) the revenue start date set on the order line.

**Why:** Item load open question 9.

**Posted:** No

### O2C-07 · O2-09 · Fix · Medium

**Comment for SOA:** Step 4 mixes up two fields. It says the A/R Account defaults to "Cash Account 10020 - BoA (operating) #5336". The A/R Account should be A/R. The deposit goes to Undeposited Funds or the bank account. Please correct the step and confirm 10020 against the final chart of accounts. Please also add the payment cases we see:
- one payment applied across several invoices;
- an international wire that arrives short because of bank fees, with the fee or write-off handled;
- an overpayment left as an unapplied credit.

**Posted:** No

### O2C-08 · O2 (new) · Gap · Medium

**Comment for SOA:** P2P and R2R test PDF outputs, but O2C doesn't, and the invoice is the document customers see. Please add a test of the invoice PDF and email. It should cover:
- MinIO branding, legal entity and address;
- remit-to bank details for the right subsidiary and bank;
- customer PO number, Subnet ID or contract reference if wanted;
- terms and due date;
- tax shown by line;
- delivery to the Customer Invoice Email, or to the reseller.

**Posted:** No

### O2C-09 · O2-10, O2-11 · Fix · Medium

**Comment for SOA:** For the credit memo, the expected result should include the tax reversal (and the matching return document in Avalara, I7-08). It should also show the deferred revenue or revenue reversed for the credited line. For the refund, please name the bank account the refund comes from, and the expected entries to A/R and the bank. SOA has already flagged the missing expected result on O2-11.

**Posted:** No

### O2C-10 · O2 (new) · Gap · High

**Comment for SOA:** Please add tests for renewals and change orders, following the change order and renewal process notes:
- a renewal order;
- a mid-term upsell co-termed to the existing end date;
- a downgrade or cancellation with a credit.

Each test should check billing and, once ARM is in place, the revenue result.

**Posted:** No

### O2C-11 · O2-12 · Fix · Low

**Comment for SOA:** Please name the reports and what each is checked against. Beyond A/R aging, A/R register and payment history, MinIO will need:
- A/R aging by subsidiary;
- customer statements;
- a deferred revenue roll-forward or waterfall;
- revenue by class (License, Support, Training).

**Posted:** No

### O2C-12 · O2 (new) · Info · Low

**Comment for SOA:** Portal sales through Chargebee are tested in the integration workbook (I13). Please cross-reference I13 here, so the O2C sign-off covers the portal channel once its design is settled. See INT-24.

**Posted:** No
