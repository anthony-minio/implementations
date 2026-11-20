# Questions

## For SOA

1. **Are we reading the templates right?** Mid-life Asset Record creates the assets; DHR loads the depreciation already taken.
2. **Will a lump sum DHR load?** Oracle's current help says to create a DHR for every depreciation entry, monthly, quarterly or annually. Older Oracle help and practitioners use one catch-up record per asset.
3. **DHR Asset Name and load order.** Oracle's format for Asset Name is the NetSuite asset ID plus the name (FAM00001 Chairs), and assets are imported before DHRs. Our plan: import the assets, export their IDs, complete Asset Name, then import the DHRs. Does that match yours?
4. **Added columns.** Cumulative Depreciation, Accounting Method and Department are added at the end of the mid-life import tab. They are fields on the NetSuite asset record, but Oracle's list of import fields does not show Accounting Method. Do all three import?
5. **Straight Line Remaining.** FA-076 and FA-082 use it, to finish at the end of the lease: (NB-RV)/(AL-CP+1) gives 10,392.67/20 = 519.63 and 4,955.62/20 = 247.78 a month. Oracle describes it as a method linked after another method. Does it work as an asset's only method?
6. **Server scripts on CSV import.** Oracle: with **Run Server SuiteScript and Trigger Workflows** and FAM's **Run Server Scripts on CSV Import** both on, Cumulative Depreciation, Last Depreciation Date and Last Depreciation Period import as 0. Please check both settings before the import.
7. **Name mapping.** Oracle: delete the default Name = ID mapping, because a Name over 30 characters in ID causes an error. 17 of the 32 names are still longer than 30 characters after shortening (the longest is 41). Is there a length limit on Asset Description? The longest here is 295 characters.
8. **Sample Asset Records.** The DHR file's Sample Asset Records tab looks like the full list of asset record fields. Is it a load, or an example? It is not filled.

## For MinIO accounting

These are in the draft as the register has them.

1. **FA-098 to FA-100** have a GL date of 2022-10, depreciation from 2026-10, and a Sage vendor code as the description. FA-098 has the same cost and vendor as FA-094 (AMAX, 63,995.00), so it may be a duplicate.
2. **FA-096 and FA-097** have a Dep Date of 2027-10-01 but started depreciating in 2026-10. Loaded from 2026-10.
3. **FA-093** was bought on 2025-03-05 and depreciates from 2026-03.
4. **FA-073** finishes in 2029-03, after the lease ends in 2028-06. ASC 842 has leasehold improvements depreciated over the shorter of their useful life and the remaining lease term. Shorten it like FA-076 and FA-082?

## Decided

- **DHR:** lump sum, one row per asset. Depreciation Period is the asset's Last Depreciation Period. DHR Name is filled.
- **Added to the mid-life load:** Cumulative Depreciation, Accounting Method and Department.
- **Names:** shortened for brevity and clarity; the register Description is kept at the end of Asset Description after "Original name:".
- **Asset types:** Depreciation Rules Acquisition. Write Off, Write Down and Disposal Cost Account 72400 (Gain) / Loss on Sale of Asset (Ming Fu, 2026-11-13). Default lifetimes stay at 36 months for now; MinIO accounting sets them once NetSuite is in use.
- **As of:** 2026-10-31 for this load.
- **Department for the sales laptops:** FA-070, FA-071 and FA-089, on D110 in the register, go to 2100 Sales - Leadership.
- **Fully depreciated assets:** a separate load, by the same process: net book value 0, last depreciation as of the month they finished.
