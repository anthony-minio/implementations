# Software / SaaS Purchase Request - current setup

Captured: 2026-11-23, from the program editor in Ramp (Procurement > Programs > Software / SaaS Purchase Request > edit). Text is copied as it appears in Ramp, including its dashes and spacing.

Screenshots: `screenshots/20261123-software-saas-*.png`.

## Program

| Setting | Value |
|---|---|
| Program name | Software / SaaS Purchase Request |
| Program type | Requests from employees that result in purchase orders |
| Who can request? | All employees |
| PO Accounting fields | Off (greyed out) |
| Line items | On |
| Line item details | Description*, Quantity*, Rate*, Amount* |
| Line item accounting fields | None |

Form settings are the same as General Procurement Request and Professional Services Purchase Request.

## Program description

> This form is used to request the purchase, renewal, or evaluation of software and SaaS tools across all departments.
>
> Please use this form for platforms such as SaaS subscriptions, cloud tools, development software, HR and finance systems, security tools, or other business applications. The information you provide will help Procurement and supporting teams review business needs, assess integrations, manage approvals, and ensure vendor compliance and risk alignment.

## Questions

In the order shown. Same conventions as `GENERAL-PROCUREMENT.md`. `GP` and `PS` are the matching General Procurement and Professional Services questions.

| # | Title | Ramp field type | Description | Required | Conditional logic | GP / PS |
|---|---|---|---|---|---|---|
| 1 | REQUEST DETAILS – Give this request a name | Request name | None | Yes | None shown | GP #1, PS #1, same |
| 2 | REQUEST DETAILS – Is this a one-time or recurring request? | Frequency | None | Locked | None shown | GP #2, PS #2, worded differently |
| 3 | SPEND DETAILS – What is the expected spend amount? | Amount | None | Locked | None shown | GP #3, PS #3, worded differently |
| 4 | REQUEST TYPE – What type of request is this? | Single select | None | Always required | Branch icon shown. What it drives not yet seen | GP #8 in name only: GP's options are event types, these are the purchase lifecycle |
| 5 | VENDOR – Specify the vendor for this request | Vendor | None | Always required | None shown. Restrict available vendors: Off | GP #4, same; PS #4 |
| 6 | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | Multi select | If "No", contact Procurement before submitting by emailing: Procurement@minio.io | Always required | Drives #7 | GP #5, same; PS #5 |
| 7 | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | Paragraph | Provide a brief summary of any prior negotiations you personally conducted with this vendor. Include the negotiated pricing, terms, discounts, or special considerations, and indicate whether Procurement participated or assisted. | Always required | Shown if #6 is "Yes — I have already discussed or negotiated with the vendor (please provide details in the justification field)" | GP #6, same; PS #6 |
| 8 | BUSINESS NEED – Describe the business need and the proposed solution | Paragraph | None | Always required | None shown | GP #7, PS #8 in purpose, worded differently. |

### Options

#4 REQUEST TYPE:

1. New software purchase
2. Renewal
3. Amendment to existing agreement
4. Trial or Pilot

#6 NEGOTIATIONS: same two options as GP #5 (option 2 cut off).

## Not yet captured

- Questions after #8, with their conditions.
- What #4 drives.
- Change order form and AI instructions.
