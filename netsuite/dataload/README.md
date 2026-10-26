# NetSuite data loads

Working folder for configuring NetSuite data uploads. One subfolder per load, each with its load file, a review page built from `sections/`, and a load log.

| Folder | Load | Status |
|---|---|---|
| `noninventory-items/` | Non-inventory Item for Sale, 11 items | Waiting on the license delivery trigger and the portal question |

## Reference values

Shared by the loads. Names as given by Anthony on 2026-10-26; they must match NetSuite exactly.

Subsidiaries:

- MinIO, Inc. (parent)
- MinIO Pvt. Ltd.
- MinIO Singapore Pte. Ltd.

Classes for load to production:

- License
- Support
- Training
- Professional Services (no items yet)

Revenue accounts, from COA Draft v1:

- 41100 License Revenue
- 41200 Support Revenue
- 42100 Professional Services Revenue
- 42200 Training Revenue

Source workbook: `MINIO-Dimensions-from-sage-20260825` (tabs COA Draft v1, Departments Draft v1, Items, Revenue Types-->Class). Not kept in this repo.

## Load order

Classes and subsidiaries must exist in the target account before any load that references them.
