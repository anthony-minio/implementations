# Referral Partner Request - current setup

Captured: 2026-11-24, from the program editor in Ramp (Procurement > Programs > Referral Partner Request > edit). Text is copied as it appears in Ramp, including its dashes and spacing.

Screenshots: `screenshots/20261124-referral-partner-*.png`.

## Program

| Setting | Value |
|---|---|
| Program name | Referral Partner Request |
| Program type | Requests from employees that result in purchase orders |
| Who can request? | All employees |
| PO Accounting fields | Off (greyed out) |
| Line items | On |
| Line item details | Description*, Quantity*, Rate*, Amount* |
| Line item accounting fields | None |

Form settings are the same as the other group A programs.

## Program description

> Use this request to onboard a referral partner, complete vendor due diligence and compliance checks, and route the referral agreement for review and signature. This request should be submitted before any referral agreement is executed.

## Questions

10 questions; #10 is the last (confirmed by Anthony 2026-11-24). In the order shown. Same conventions as `GENERAL-PROCUREMENT.md`. `GP`, `PS` and `SW` are the matching General Procurement, Professional Services and Software / SaaS questions.

| # | Title | Ramp field type | Description | Required | Conditional logic | GP / PS / SW |
|---|---|---|---|---|---|---|
| 1 | Give this request a descriptive name | Request name | None | Yes | None shown | #1 in all three; no section prefix here |
| 2 | Is it one-time or recurring? | Frequency | None | Locked | None shown | #2 in all three; no section prefix here |
| 3 | What is the estimated total referral payout under this agreement? | Amount | None | Locked | None shown | #3 in all three, worded for referral payouts |
| 4 | CONTRACT- Upload contracts or documents | File upload | None | No | None shown | GP #22, PS #16, SW #20; conditional on Signed Contract there, always shown and optional here |
| 5 | PROGRAM – Referral Program & Opportunity Description | Paragraph | None | Always required | None shown | None |
| 6 | PARTNER – Referral Partner Company | Vendor | None | Always required | Drives #7. Restrict available vendors: Off | GP #4, PS #4, SW #5 |
| 7 | PARTNER – Referral Partner Company Point of Contact | Vendor contact | None | Always required | Shown if Vendor (#6) is "New vendor" | GP #26, PS #30, SW #38 |
| 8 | BUSINESS – Business Owner / Internal Sponsor | Text | None | Always required | None shown | GP #19, PS #13, SW #16 (REQUESTER) |
| 9 | BUSINESS – Department | Department | None | No | None shown | GP #20, PS #14, SW #17; required in all three |
| 10 | APPROVALS – Message for Approvers | Text | None | No | None shown | GP #28, PS #32, SW #40 (APPROVAL NOTES) |

## Change order form

One question. This is the only group A program with a change order form set up.

| # | Title | Ramp field type | Description | Required |
|---|---|---|---|---|
| 1 | Why are you making this change | Reason | None | Always required |

## AI instructions

Empty. Confirmed by Anthony 2026-11-24.

## Not captured

- No vendor address question (asked for new vendors in the other three programs).
