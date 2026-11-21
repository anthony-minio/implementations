# Professional Services Purchase Request - current setup

Captured: 2026-11-21, from the program editor in Ramp (Procurement > Programs > Professional Services Purchase Request > edit, page 1 of 2). Text is copied as it appears in Ramp, including its dashes and spacing.

Screenshots: `screenshots/20261121-professional-services-*.png`.

## Program

| Setting | Value |
|---|---|
| Program name | Professional Services Purchase Request |
| Program type | Requests from employees that result in purchase orders |
| Who can request? | All employees |
| PO Accounting fields | Off (greyed out) |
| Line items | On |
| Line item details | Description*, Quantity*, Rate*, Amount* |
| Line item accounting fields | None |

Form settings are the same as General Procurement Request.

## Program description

> Professional Services refer to project-based, time-bound, or expertise-driven engagements provided by external vendors or contractors. These services are typically non-recurring, involve a defined scope of work, and may be governed by a Statement of Work (SOW) or service agreement.
>
> Common examples include:
>
> Consulting
>
> Training or onboarding support
>
> Implementation services
>
> Strategic advisory
>
> Creative, design, or marketing services
>
> Technical assessments or audits
>
> Professional services may be delivered remotely or on-site and can vary in complexity and risk. Depending on the nature of the engagement, Compliance review may be required — especially if the vendor will access MinIO systems, customer data, or subcontract any portion of the work.
>
> To initiate a professional services engagement, a procurement request must be submitted with details including scope, duration, cost, and how the purchase will be governed (e.g., vendor contract, MinIO terms, or online click-through). This ensures alignment with internal compliance, budget, and risk management requirements.

## Questions

In the order shown. Same conventions as `GENERAL-PROCUREMENT.md`. `GP` is the matching General Procurement question.

| # | Title | Ramp field type | Description | Required | Conditional logic | GP |
|---|---|---|---|---|---|---|
| 1 | REQUEST DETAILS – Give this request a name | Request name | None | Yes | None shown | #1, same |
| 2 | REQUEST DETAILS – Is it one-time or recurring? | Frequency | None | Locked | None shown | #2, same |
| 3 | SPEND – What is the spend amount? | Amount | None | Locked | None shown | #3, same |
| 4 | VENDOR- Specify the vendor for this request | Vendor | None | Always required | None shown. Restrict available vendors: Off | #4, no space before the dash |
| 5 | NEGOTIATIONS- Have you already engaged in discussions or negotiations with the vendor? | Multi select | If "No", contact Procurement before submitting by emailing: Procurement@minio.io | Always required | Drives #6 | #5, no space before the dash, leading space in the title field |
| 6 | NEGOTIATIONS- If YES → Provide justification and describe what was discussed or negotiated... | Paragraph | Provide a brief summary of any prior negotiations you personally conducted with this vendor. Include the negotiated pricing, terms, discounts, or special considerations, and indicate whether Procurement participated or assisted. | Always required | Shown if #5 is option 1 | #6, same description, title worded differently |
| 7 | SERVICES – Please describe the nature of the external services being requested. | Paragraph | None | Always required | None shown | #17, worded for services |
| 8 | BUSINESS PURPOSE – What is the purpose of these external services? | Paragraph | None | Always required | None shown | #7, worded differently, no description |
| 9 | CUSTOMERS / TARGET ACCOUNTS – Which priority customers, partners, or target accounts w... | Paragraph | None | Always required | None shown | #14, adds "partners"; in GP it shows only for events, here always |

### Options

#5 NEGOTIATIONS (option 2 cut off; option 1 full text from the #6 condition panel):

1. Yes ( Please provide the JustificationYes — I have already discussed or negotiated with the vendor (please provide details in the justification field)
2. No — I have not engaged with the vendor. I will contact Procurement (Procurement(...

Option 1 differs from GP #5: it starts with "Yes ( Please provide the Justification" run straight into the GP wording.

## Not yet captured

- Questions after #9, with their conditions.
- Full titles of #6 and #9, and #5 option 2 (cut off).
- Change order form and AI instructions.
- Page 2 of the program editor.
