# Overview

| | |
|---|---|
| **Template** | `MINIO_Vendor_Template_10192026.xlsx` from SOA: 61 columns, tabs Field Restrictions, Vendor Template, Vendor Category |
| **Required** | Company Name (marked red). First and Last Name are required instead when the vendor is an individual |
| **Source of truth** | Sage Intacct vendor detail export, 1,770 active vendors |
| **Enrichment** | Ramp vendor export, 578 vendors. 551 carry the Sage vendor ID, so the link is exact |
| **Not loaded** | Bank details (ACH and wire). The template has no bank fields |
| **Review table** | Every active Sage vendor mapped to the template, with Ramp coverage and flags: https://claude.ai/artifact/43aBdfBgsyuiGNHAtGPSsw |
| **Status** | Scope and rules agreed 2026-10-26. Load plan and remaining questions below |
