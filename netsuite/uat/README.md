# NetSuite UAT

Review of SOA's UAT test scripts: feedback based on NetSuite practice and on MinIO's business and operations.

UAT is scheduled for 2026-12-08 to 2026-12-10 and the week of 2026-12-14 (per the scripts).

## Files

| Path | Purpose |
|---|---|
| `soa-scripts/` | Copies of SOA's five workbooks as received on 2026-11-24. Reference only: the masters are on SOA's SharePoint, and every edit or comment is made there |
| `review/00-ACROSS-ALL-FILES.md` | Findings that apply to more than one workbook, and the overall priority list |
| `review/01-DESIGN-TO-BUILD.md` | Findings on the Design to Build workbook |
| `review/02-ORDER-TO-CASH.md` | Findings on the Order to Cash workbook |
| `review/03-PROCURE-TO-PAY.md` | Findings on the Procure to Pay workbook |
| `review/04-RECORD-TO-REPORT.md` | Findings on the Record to Report workbook |
| `review/05-INTEGRATIONS.md` | Findings on the Integration Sandbox workbook |

## Process

1. Review each workbook on its own.
2. Review them together for cross-file gaps and inconsistencies.
3. Walk through the findings file by file with Anthony, who posts the agreed comments to the SharePoint files.
4. Mark each finding Posted, Changed or Dropped in its review file as we go.

Each finding has an ID, the test it applies to, a type and a priority. The types follow the Type column on SOA's Review Notes tab (Gap, Fix, Confirm, Info), so a finding can be added there as a row or posted as a cell comment. Each review file also gives our position on SOA's own Review Notes.

## Status

| Workbook | Tests | SOA review notes | Our findings | Posted |
|---|---|---|---|---|
| Design to Build | 7 | 5 | 8 | 0 |
| Order to Cash | 15 | 8 | 12 | 0 |
| Procure to Pay | 13 | 7 | 9 | 0 |
| Record to Report | 66 | 10 | 18 | 0 |
| Integration Sandbox | 94 | none | 31 | 0 |
| Across all files | - | - | 16 | 0 |
