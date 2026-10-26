# Overview

| | |
|---|---|
| **Template** | `MINIO_Vendor_Template_10192026.xlsx` from SOA: 61 columns, tabs Field Restrictions, Vendor Template, Vendor Category |
| **Required** | Company Name (marked red). First and Last Name are required instead when the vendor is an individual |
| **Source of truth** | Sage Intacct vendor detail export, 1,770 active vendors |
| **Enrichment** | Ramp vendor export, 578 vendors. 551 carry the Sage vendor ID, so the link is exact |
| **Not loaded** | Bank details (ACH and wire). The template has no bank fields |
| **Status** | Mapping drafted. Waiting on scope and the open questions below |
