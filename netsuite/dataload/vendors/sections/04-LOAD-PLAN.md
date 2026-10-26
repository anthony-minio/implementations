# Load plan

Agreed 2026-10-26: every active Sage vendor ends up in NetSuite, with Ramp syncing its vendors.

1. **Ramp sync.** Ramp syncs its 578 vendors to NetSuite, including the 27 Ramp vendors not in Sage (added in Ramp from 2025-08 on, 23 with no spend yet).
2. **Sage vendors not in Ramp.** This load: the 1,219 active Sage vendors that are not in Ramp, mapped as above.
3. **Enrichment.** The 551 vendors in both systems get Sage values Ramp does not hold: Sage Vendor ID, Vendor Category, default expense account, 1099 flag, tax ID where Ramp has none, and bank details where Ramp has none.

## Bank details

| | **Vendors** |
|---|---|
| **ACH details in Sage** | 164 |
| **ACH details in Ramp (vendors with a Sage ID)** | 174 |
| **In both** | 70 (last 4 digits agree on 65, differ on 5) |
| **Sage only** | 94 (13 in Ramp without bank details, 81 not in Ramp) |
| **Ramp only** | 104 |

Ramp's details are the more recent where both exist. The vendor template has no bank fields, so bank details need their own NetSuite import (vendor bank details record), from Sage for the 94 and from Ramp for the rest if Ramp does not sync them.

## Vendor types against Ramp

| **Sage vendor type** | **Vendors** | **In Ramp** | **Note** |
|---|---|---|---|
| **Credit Cards** | 427 | 123 | "Never billed" means no AP bill in Sage: card purchases are booked from the card feed, not as bills. 122 of the 123 in Ramp have Ramp spend. The other 304 are card merchants from before Ramp, plus the card accounts themselves (for example Mastercard - 3584, CHASE CC - ALL CREDIT CARDS) |
| **MinIO employee** | 136 | 1 | 74 were reimbursed through Sage bills. Ramp reimbursements sync to NetSuite as vendor bills with the employee as the vendor (or one default reimbursement vendor), so employee vendor records are the right home |
| **AR reseller** | 127 | 9 | 2 billed in Sage |
