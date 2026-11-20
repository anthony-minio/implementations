# Fixed assets

Fixed asset load to NetSuite Fixed Assets Management (FAM). Asana FS-140: https://app.asana.com/1/163565154279805/project/1219443754801875/task/1220361265682450

The plan:

1. List the assets that are fully depreciated and send it out to confirm which ones still exist.
2. Load the assets still depreciating, plus the fully depreciated assets still in use, using SOA's two templates.

The register goes in `data/`, which is not committed.

## Files

| File | What it is |
|---|---|
| `MINIO_FAM_CSVTemplate_Mid-life Asset Record.xlsx` | SOA template for importing assets part way through their life (tab `FAM_Mid-life Asset `), with reference tabs: Notes, COA, FAM_Asset Type, Depreciation Rules, Dep Method |
| `MINIO_ FAM_DHR.xlsx` | SOA template for depreciation history records (DHR): `DHR Import Template`, with examples `Sample Asset Records`, `FAM_DHR_lumpsum` (one row per asset) and `FAM_DHR_monthly` (one row per asset per month) |
| `data/fixed-assets-oct-2026-recon-E100.xlsx` | MinIO's register, `15000-16999 - Fixed Assets - Oct 2026 - recon E100 entity` from Asana, prepared by Richard Li, reviewed by Ming Fu, 2026-11-06. Tab `ALL FA`: one row per asset with depreciation, accumulated depreciation and NBV by month from 2021-01 to 2026-10 |
| `tools/build.py` | Builds the outputs below from the register |
| `tools/validate_load.py` | Checks the outputs against the register, independently of the build |
| `sections/`, `doc.env`, `tools/build.sh` and the other create-doc tools | Fully depreciated assets document. `tools/build_doc_sections.py` writes sections 02 to 04 from `data/assets.json` (written by `tools/build.py`). `tools/style_docx.py` keeps the column widths set by the dashes under a table's header |
| `output/` | Generated document: `fully-depreciated-assets.html` (published as an Artifact: https://claude.ai/artifact/D2FuHC2TkGemAzD25wwp7V), `.docx` and `-preview.pdf`. Never edit by hand |
| `soa-loads/` | Document for SOA walking through the asset types (FAM_Asset Type) and the two draft loads, every template column for the 32 depreciating assets, and the questions. `tools/build_load_doc_sections.py` writes sections 02 to 04 from the draft workbooks; `soa-loads/tools/build.sh` builds `soa-loads/output/fixed-asset-loads-soa.html` (published as an Artifact: https://claude.ai/artifact/6nnyN1dQ3cAX9KQiGfyvEo), `.docx` (landscape, `ORIENTATION` in `soa-loads/doc.env`) and `-preview.pdf` |

## The two SOA templates

How we read them, to confirm with SOA:

- **Mid-life Asset Record** creates each asset in NetSuite with its cost, lifetime, last depreciation period and current NBV. NetSuite carries on depreciating it from there.
- **DHR** loads the depreciation already taken against each asset, so NetSuite's asset reports show it. The lump sum form has one Depreciation row per asset for the total to date. The monthly form has one row per month. The register has monthly figures only from 2021-01, so lump sum is what we filled.

## Outputs (in `data/`)

`python3 tools/build.py`, then `python3 tools/validate_load.py`.

| File | For |
|---|---|
| `MinIO_Fully_Depreciated_Assets_for_Review_<date>.xlsx` | Sending out: 50 fully depreciated assets, with yellow columns for Still in use?, Where / who has it, and Notes |
| `MinIO_Fixed_Asset_Load_Working_<date>.xlsx` | Every asset with its treatment, the figures behind the load, flags, and the open questions |
| `MINIO_FAM_CSVTemplate_Mid-life Asset Record - DRAFT <date>.xlsx` | SOA's template with the import tab filled |
| `MINIO_ FAM_DHR - DRAFT <date>.xlsx` | SOA's template with `DHR Import Template` filled, lump sum |

Ref `FA-069` is row 69 of `ALL FA`.

## Register as of 2026-10-31

| Treatment | Assets | Cost | NBV |
|---|---|---|---|
| Load: depreciating | 32 | 1,724,131.20 | 638,123.30 |
| Review: fully depreciated, loaded only if still in use | 50 | 655,279.44 | 0.00 |
| Held: no depreciation yet, start date to confirm (FA-101) | 1 | 12,100.76 | 12,100.76 |
| Not loaded: leasehold improvements before 2022, not in the GL | 13 | 121,238.22 | 0.00 |
| Total | 96 | 2,512,749.62 | 650,224.06 |

Without the 13 leasehold improvements, the cost ties to Sage 15000-15300 (2,391,511.58) and the NBV is within 0.12 of Sage (650,224.18), as on the leadsheet.

## Decisions

- 2026-11-13 (Ming, Slack, asked which accounts to use for write-off and gain/loss on disposal): 79200 (Gain) / Loss on Sale of Asset, which maps to 72400 in NetSuite. On SOA's FAM_Asset Type tab, 72400 goes in Write Off Account and, proposed, Disposal Cost Account. No account yet for Write Down Account.
- 2026-11-17: the 13 leasehold improvements from 2017 to 2019 are not loaded. The leadsheet leaves them out of 15300 and 16300. To confirm with Richard and Ming.
- 2026-11-17: Subsidiary MinIO, Inc. Quantity 1. Residual 0. Asset types: Computer Hardware to Equipment, Furniture to Furniture & Fixtures, Lease Improvement to Leasehold Improvements.
- 2026-11-17: each month's depreciation is the change in accumulated depreciation, not the Dep column. FA-087 has Dep formulas from 2024-08 that are not added to its total. It was bought in 2025-03.
- 2026-11-17: FA-076 and FA-082 were sped up to finish at the end of the lease (2028-06). Their lifetime is months done plus months left (44 and 42), not 60.

## Open questions

The full list is on the Questions tab of the working workbook.

For SOA:

- Lump sum or monthly DHR?
- In the lump sum example, Depreciation Period is 1. Is that right?
- Is DHR Name filled after the asset import?
- SOA's asset types use the Disposal rule, but MinIO depreciates from the month an asset goes into service (the Acquisition rule).
- What depreciation method for FA-076 and FA-082? Straight Line Remaining?
- Should we load Department, Class and Location?
- Which accounts for write-off, write-down and disposal cost?
- What asset type for FA-036, the purchased software?

For Richard and Ming:

- What are FA-098 to FA-101? They have a GL date of 2022-10 and depreciation from 2026-10. FA-098 may duplicate FA-094.
- FA-096 and FA-097 have a Dep Date of 2027-10. Typo?
- FA-093 was bought in 2025-03 but depreciates from 2026-03. Confirm.
- FA-073 finishes in 2029-03, after the lease ends. Shorten it?
- FA-077 and FA-078 have the same name. Make them unique?

Others:

- Sendhil Mandala: which assets have been disposed of.
- The register must be rolled forward to the month before go-live, then the load rebuilt.

## Load log

| Date | File | Records | Errors | Outcome |
|---|---|---|---|---|
