# Questions

## For SOA

1. **Are we reading the templates right?** Mid-life Asset Record creates the assets; DHR loads the depreciation already taken.
2. **Lump sum or monthly DHR?** We filled the lump sum form. The register has monthly figures only from 2021-01, so a monthly DHR for older assets would have to be rebuilt.
3. **Depreciation Period in the lump sum DHR.** SOA's example has Depreciation Period 1 and Period-1 0 for 18 months of depreciation. We did the same. Should it be the Last Depreciation Period instead?
4. **DHR Name and load order.** DHR Name is blank in the lump sum example, and ID plus Name in Sample Asset Records. Is it filled after the asset import, using the IDs NetSuite gives the assets? Assets first, then DHR? FA-077 and FA-078 are both named PowerEdge R7615 server, so a match on Asset Name alone would not tell them apart.
5. **Depreciation method for FA-076 and FA-082.** Both were sped up to finish at the end of the lease, 2028-06. Straight Line, (CC-RV)/AL, would give 22,270.00/44 = 506.14 and 10,253.00/42 = 244.12 a month instead of 519.63 and 247.78. Use Straight Line Remaining, (NB-RV)/(AL-CP+1), for these two? The mid-life template has no method column.
6. **Depreciation rule.** SOA's asset types use Disposal, so depreciation starts the month after an asset goes into service. MinIO's register depreciates from the month it goes into service (Acquisition). This decides when depreciation starts on assets bought after go-live.
7. **Default lifetimes.** SOA's asset types default to 36 months. MinIO uses 60 months for furniture and leasehold improvements (36 for trade booths). Each loaded asset carries its own lifetime, so this only affects new assets.
8. **Department, Class, Location, Asset Serial Number.** SOA's Sample Asset Records have them; the mid-life template does not. The register has a department on every asset (such as D-E420) and serial numbers for FA-069 and FA-075 only. Should we load them?
9. **Disposal accounts.** Write Off Account is 72400 (Gain) / Loss on Sale of Asset (Ming Fu, 2026-11-13; Sage 79200). Disposal Cost Account is filled with the same account, to confirm with Ming. Write Down Account (Revaluation) is blank: the COA has no write-down or impairment account. Which account?
10. **Fully depreciated assets.** Those still in use will go through the same templates with Asset Status Fully Depreciated, net book value 0 and the last depreciation as of the month they finished. The template's Notes tab also lists Depreciation Active (FALSE for these), but the import tab has no such column. Is anything else needed?
11. **Cutover date.** Which month-end should the load be as of? We rebuild from the register for that month.
12. **Sample Asset Records.** This tab of the DHR file has 29 fields, more than the mid-life import, including Depreciation Active, Depreciation Rules, Depreciation Method and Target Depreciation Date. Is it a load, or an example of the records the mid-life import creates? It is not filled.

## Being confirmed with MinIO accounting

These are in the draft as the register has them.

1. **FA-098 to FA-100** have a GL date of 2022-10, depreciation from 2026-10, and a Sage vendor code as the description. FA-098 has the same cost and vendor as FA-094 (AMAX, 63,995.00), so it may be a duplicate.
2. **FA-096 and FA-097** have a Dep Date of 2027-10-01 but started depreciating in 2026-10. Loaded from 2026-10.
3. **FA-093** was bought on 2025-03-05 and depreciates from 2026-03.
4. **FA-073** finishes in 2029-03, after the lease ends in 2028-06. It may be shortened like FA-076 and FA-082.
