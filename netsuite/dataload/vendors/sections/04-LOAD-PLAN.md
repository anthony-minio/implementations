# Load plan

Agreed 2026-10-26: Ramp syncs first, then NetSuite is enriched with what Ramp does not push. Every active Sage vendor ends up in NetSuite.

1. **Ramp sync.** Ramp syncs its 578 vendors to NetSuite, including the 27 Ramp vendors not in Sage (added in Ramp from 2025-08 on, 23 with no spend yet).
2. **Sage vendors not in Ramp.** This load: the 1,219 active Sage vendors that are not in Ramp, mapped as above.
3. **Enrichment.** The 551 vendors in both systems get Sage values Ramp does not hold: Sage Vendor ID, Vendor Category, default expense account, 1099 flag, tax ID where Ramp has none. Ramp-created NetSuite vendors carry no Sage ID, so after the sync the enrichment file is matched to them by Ramp vendor name and Ramp Vendor ID, then re-keyed to the NetSuite internal ID before import.
4. **Bank details.** Ramp does not push bank details to NetSuite, so every vendor's bank details are imported separately: Ramp's where Ramp has them (Ramp is primary), else Sage's.

## Bank details

| | **Vendors** |
|---|---|
| **ACH details in Sage** | 164 |
| **ACH details in Ramp (vendors with a Sage ID)** | 174 |
| **In both** | 70 (last 4 digits agree on 65, differ on 5) |
| **Sage only** | 94 (13 in Ramp without bank details, 81 not in Ramp) |
| **Ramp only** | 104 |

Ramp is primary where both exist, including the 5 that differ. The vendor template has no bank fields, so bank details need their own NetSuite import (vendor bank details record): 268 vendors, Ramp's details for 174 and Sage's for 94.

## Vendor types against Ramp

| **Sage vendor type** | **Vendors** | **In Ramp** | **Note** |
|---|---|---|---|
| **Credit Cards** | 427 | 123 | "Never billed" means no AP bill in Sage: card purchases are booked from the card feed, not as bills. 122 of the 123 in Ramp have Ramp spend. The other 304 are card merchants from before Ramp, plus the card accounts themselves (for example Mastercard - 3584, CHASE CC - ALL CREDIT CARDS) |
| **MinIO employee** | 136 | 1 | 74 were reimbursed through Sage bills. Ramp reimbursements sync to NetSuite as vendor bills with the employee as the vendor (or one default reimbursement vendor), so employee vendor records are the right home |
| **AR reseller** | 127 | 9 | 2 billed in Sage |
