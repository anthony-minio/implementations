# Asset types

Tab **FAM_Asset Type** of the mid-life template. SOA filled everything except Description and the last three accounts. **Write Off Account** is 72400 (Gain) / Loss on Sale of Asset. Asked which accounts to use for write-off and gain/loss on disposal, Ming Fu answered Sage 79200 on 2026-11-13; 79200 is 72400 in NetSuite. **Disposal Cost Account** has the same account [TBC: Ming to confirm 72400 for disposal costs]. The COA has no write-down or impairment account [TBC: which account for Write Down Account (Revaluation)]. Description is left blank.

| **Field** | **Equipment** | **Furniture & Fixtures** | **Leasehold Improvements** | **Internally Developed Software** | **Software in Development in Progress** |
|------------------|----------------|----------------|----------------|----------------|----------------|
| **Residual Percentage** | 0 | 0 | 0 | 0 | N/A |
| **Asset Lifetime** | 36 | 36 | 36 | 36 | N/A |
| **Accounting Method** | Straightline | Straightline | Straightline | Straightline | N/A |
| **Depreciation Active** | TRUE | TRUE | TRUE | TRUE | FALSE |
| **Revision Rules** | Remaining Life | Remaining Life | Remaining Life | Remaining Life | N/A |
| **Depreciation Rules** | Disposal | Disposal | Disposal | Disposal | N/A |
| **Depreciation Period** | Monthly | Monthly | Monthly | Monthly | N/A |
| **Asset Account** | 15110-Equipment | 15120-Furniture & Fixtures | 15130-Leasehold Improvements | 15140-Internally Developed Software | 15145-Software in Development in Progress |
| **Depreciation Account** | 15510 -Accum. Depreciation - Equipment | 15520 - Accum. Depreciation - Furniture & Fixtures | 15530 - Accum. Depreciation - Leasehold Improvements | 15540 - Accum. Amortization - Internally Dev. Software | N/A |
| **Depreciation Charge Account** | 69100 - Depreciation Expense | 69100 - Depreciation Expense | 69100 - Depreciation Expense | 69100 - Depreciation Expense | N/A |
| **Write Off Account** | 72400 - (Gain) / Loss on Sale of Asset | 72400 - (Gain) / Loss on Sale of Asset | 72400 - (Gain) / Loss on Sale of Asset | 72400 - (Gain) / Loss on Sale of Asset | N/A |
| **Write Down Account** | TBC | TBC | TBC | TBC | N/A |
| **Disposal Cost Account** | 72400 - (Gain) / Loss on Sale of Asset | 72400 - (Gain) / Loss on Sale of Asset | 72400 - (Gain) / Loss on Sale of Asset | 72400 - (Gain) / Loss on Sale of Asset | N/A |

Lifetime and depreciation rules: questions 6 and 7. SOA's tab names 69100 Depreciation Expense; the COA names it 69100 Depreciation.
