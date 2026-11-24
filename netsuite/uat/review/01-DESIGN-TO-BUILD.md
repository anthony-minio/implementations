# Design to Build

Workbook: `MinIO_Design_to_Build_Test_Scripts_UAT.xlsx`. 7 tests on one tab (D1 Item Master). SOA owner Danna Bandales, MinIO owner Tory Li.

**Summary:** the tests cover building generic items. They don't test the 11 items we loaded, or the item settings MinIO's revenue depends on: deferred revenue account, class, revenue recognition rules, and the license fulfillment setting. These are the item decisions still open in `netsuite/dataload/noninventory-items`.

## SOA's Review Notes: our position

| # | Test | SOA note | Our position |
|---|---|---|---|
| 1 | D1-04 | Gap: add a kit item test once allocation is provisioned | Agree. The kit (license and support, with fair values) should exist before UAT and be the item used in the O2C revenue tests. Until then, the item group test in D1-04 tells us little |
| 2 | D1-01, D1-02 | Confirm: add an Avalara tax code check | Agree. The approved tax code for each item group (License, Support, Training, later Professional Services) should come from MinIO's tax advisor, because software and maintenance are taxed differently from state to state. See INT-01 |
| 3 | D1-06 | Info: MD02 should be P1-02 | Agree |
| 4 | D1 (new) | Gap: revenue recognition settings, add once the design is final | Agree with the gap, but not with waiting. The 11 loaded items have no revenue recognition rule yet (item load open question 11), and they need one before they are used on a transaction. This should be ready before UAT. See D2B-03 |
| 5 | D1 (new) | Info: fixed asset items are in R7 | Agree |

## Our findings

### D2B-01 · D1-01, D1-02, D1-03, D1-05 · Fix · Medium

**Comment for SOA:** Please replace the placeholders with MinIO's values, so the test checks the design:
- Subsidiary: MinIO, Inc. with Include Children, as loaded.
- Class: License, Support or Training.
- Income account: 41100 License Revenue, 41200 Support Revenue or 42200 Training Revenue.
- Deferred Revenue account: 23100 Deferred Revenue - ST.

D1-01 doesn't check Class or Deferred Revenue Account at all. Every MinIO item for sale carries both.

**Why:** Values by item group, from `dataload/noninventory-items/sections/03-VALUES-BY-GROUP.md`.

**Posted:** No

### D2B-02 · D1-01 · Confirm · High

**Comment for SOA:** Step 3 says to uncheck Can Be Fulfilled/Received. For license items this is still an open decision. If license key issuance drives revenue through an item fulfillment (option a in our item notes), the box must be checked on license items. Please don't set it in the test until the license delivery trigger is decided. Please also confirm whether the setting can be changed after an item has been used on transactions.

**Why:** Item load open question 9.

**Posted:** No

### D2B-03 · D1 (new) · Gap · High

**Comment for SOA:** Please add tests on the items we loaded, not only on new test items:
- spot-check the 11 loaded items against the load file (class, income account, deferred revenue account, subsidiary);
- run the update import that adds revenue recognition rules and forecast rules, keyed on External ID;
- confirm that an item with a deferred revenue account but no rule behaves as SOA expects.

**Why:** Item load open questions 11 and 1 (account format on import).

**Posted:** No

### D2B-04 · D1-03 · Gap · Medium

**Comment for SOA:** The discount item MinIO needs is the reseller margin shown as a discount. It is still TBD on the Items tab. Please base D1-03 on that, and name the account it posts to: a contra-revenue account, or another per design. Once ARM is in place, please also test a discount line on a license and support order, because discounts change how revenue is allocated between the lines.

**Why:** Item load open question 5.

**Posted:** No

### D2B-05 · D1-05, D1-06 · Confirm · Low

**Comment for SOA:** MinIO buys through Ramp, coded to GL accounts. Will items for purchase be used at all, apart from the fixed asset item in R7-10? If not, please mark D1-05 and D1-06 N/A. Then we don't keep purchase items, vendor price lists or the Multiple Vendors feature that nobody uses.

**Posted:** No

### D2B-06 · D1 (new) · Gap · Medium

**Comment for SOA:** Please add a check of the Show Display Name with Item Codes preference (Setup > Company > General Preferences). If it is turned on, later CSV imports that reference items need the display name as well, or they fail with Invalid Parent Reference Key. We'd like it decided and tested before the sales order and invoice loads.

**Why:** Item load open question 8.

**Posted:** No

### D2B-07 · D1 (new) · Gap · Low

**Comment for SOA:** Portal sales (small businesses and individuals buying AIStor through the portal) are recognized immediately. If portal invoices reach NetSuite line by line, they need a separate portal item with Direct Revenue Posting and no deferred revenue account. Please add that item test once the portal design is decided. See INT-24.

**Why:** Item load open question 10.

**Posted:** No

### D2B-08 · D1-02 · Confirm · Low

**Comment for SOA:** We loaded all 11 items for sale, including Support and Training, as Non-inventory Item for Sale. Will MinIO use Service items at all, for example for Professional Services SKUs when there are any? If not, please mark D1-02 N/A or move it to the item type we will actually use.

**Posted:** No
