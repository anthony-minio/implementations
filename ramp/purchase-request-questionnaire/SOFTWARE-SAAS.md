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
| 4 | REQUEST TYPE – What type of request is this? | Single select | None | Always required | Drives #13 (other targets not yet seen) | GP #8 in name only: GP's options are event types, these are the purchase lifecycle |
| 5 | VENDOR – Specify the vendor for this request | Vendor | None | Always required | None shown. Restrict available vendors: Off | GP #4, same; PS #4 |
| 6 | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | Multi select | If "No", contact Procurement before submitting by emailing: Procurement@minio.io | Always required | Drives #7 | GP #5, same; PS #5 |
| 7 | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | Paragraph | Provide a brief summary of any prior negotiations you personally conducted with this vendor. Include the negotiated pricing, terms, discounts, or special considerations, and indicate whether Procurement participated or assisted. | Always required | Shown if #6 is "Yes — I have already discussed or negotiated with the vendor (please provide details in the justification field)" | GP #6, same; PS #6 |
| 8 | BUSINESS NEED – Describe the business need and the proposed solution | Paragraph | None | Always required | None shown | GP #7, PS #8 in purpose, worded differently. |
| 9 | BUSINESS NEED – What business problem does this software or service solve? | Paragraph | (Primary use case and number of users.) | Always required | None shown | None; overlaps #8 |
| 10 | BUSINESS IMPACT – What is the expected business impact? | Paragraph | (Revenue enablement, cost savings, efficiency gains, risk reduction, or compliance.) | Always required | None shown | GP #11 (shown only for "Other" there), PS #10 |
| 11 | BUSINESS NEED – Is this replacing an existing tool or adding a new capability? | Text | (If replacing, name the tool being sunset.) | Always required | None shown | None |
| 12 | ALTERNATIVES – What alternative tools (including existing internal tools) were considered? | Paragraph | None | Always required | None shown | None |
| 13 | ALTERNATIVES – Have you checked if we already have an existing tool or service that meets thi... | Multi select | Before requesting a new purchase, confirm whether an existing tool in our company can meet this need. Reach out to Procurement is you are usure. | Always required | Shown if #4 is "New software purchase". Drives #14 | None |
| 14 | ALTERNATIVES – If yes, please explain why a new tool or service is still required | Paragraph | None | Always required | Shown if #13 is "Yes ( Please Explain why a new tool or service is still needed)" | None |
| 15 | TIMELINE – Is there a target date or deadline by which this purchase needs to be completed? | Date | None | No | None shown | GP #18, PS #12; "purchase or contract" there |
| 16 | REQUESTER – Who is the internal business owner/requester? | Text | None | Always required | None shown | GP #19, PS #13, same |
| 17 | DEPARTMENT – Which department will use this software? | Department | None | Always required | None shown | GP #20, PS #14, reworded |
| 18 | USERS – Approximately how many users will need access to this software? | Text | None | Always required | None shown | None; #9 description also asks for number of users |
| 19 | PURCHASE METHOD – How will this software purchase be made? | Multi select | None | Always required | Drives #20. Branch icon plus the second icon | GP #21 (multi select), PS #15 (single select); no "No contract required" option here |
| 20 | CONTRACTS / DOCUMENTATION – Please upload all related contracts and documents. | File upload | (Required: vendor proposal, quote, order form,  MSA, DPA) | Always required | Shown if #19 is "Signed Contract" | GP #22; PS #16, same description |

### Options

#4 REQUEST TYPE:

1. New software purchase
2. Renewal
3. Amendment to existing agreement
4. Trial or Pilot

#6 NEGOTIATIONS: same two options as GP #5 (option 2 cut off).

#13 ALTERNATIVES (option 2 cut off). The #13 description's "is you are usure" is as in Ramp. The #13 condition panel shows the #4 option as "New software purchase " with a trailing space.

1. Yes ( Please Explain why a new tool or service is still needed)
2. No- Please contact Procurement before submitting by emailing: Procurement@min...

#19 PURCHASE METHOD:

1. Online click-through agreement
2. Signed Contract

## Not yet captured

- Questions after #20, with their conditions.
- What #4 drives.
- Change order form and AI instructions.
