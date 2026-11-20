# Overview

A draft of the two FAM templates for MinIO, Inc., and the asset types they use, to walk through before the final load. It holds the assets still depreciating. Fully depreciated assets are out for review and are added once we know which are still in use.

| | |
|---|---|
| **In this draft** | 32 assets: cost 1,724,131.20, accumulated depreciation 1,086,007.90, net book value 638,123.30 |
| **As of** | 2026-10-31, the last month depreciated in Sage. Rebuilt for the month before go-live (question 11) |
| **Source** | MinIO's fixed asset register, 15000-16999 - Fixed Assets - Oct 2026 - recon E100 entity, reconciled to Sage by Richard Li and Ming Fu, 2026-11-06 |
| **Not in this draft** | 50 fully depreciated assets (in review), FA-101 (not yet depreciating; start date to confirm), 13 leasehold improvements from 2017 to 2019 no longer in the GL |
| **Ties to Sage** | Net book value in the register 650,224.06: these 32 (638,123.30) plus FA-101 (12,100.76). Sage 650,224.18 |
| **Files** | MINIO_FAM_CSVTemplate_Mid-life Asset Record - DRAFT 20261117.xlsx and MINIO_ FAM_DHR - DRAFT 20261117.xlsx: SOA's templates with the import tabs filled, and the FAM_Asset Type tab completed |

## How we read the two templates

- **Mid-life Asset Record** creates each asset in NetSuite part way through its life. NetSuite carries on depreciating it from the Last Depreciation Period.
- **DHR** records the depreciation already taken, so NetSuite's asset reports show it.

[TBC: SOA to confirm this reading (question 1)]
