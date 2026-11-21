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
| 10 | BUSINESS IMPACT – What business impact is expected from this engagement? | Paragraph | None | Always required | None shown | #11, worded for services, no examples; in GP it shows only for "Other" |
| 11 | SUCCESS METRICS – How will success be measured for this engagement? | Paragraph | None | Always required | None shown | None. Closest is part of the #13 description ("how success will be evaluated") |
| 12 | TIMELINE – Is there a target date or deadline by which this purchase or contract needs to be co... | Date | None | No | None shown | #18, same |
| 13 | REQUESTER – Who is the internal business owner/requester? | Text | None | Always required | None shown | #19, same |
| 14 | DEPARTMENT – Which department will be using this service? | Department | None | Always required | None shown | #20, worded for services |
| 15 | PURCHASE METHOD – How will this purchase be made? | Single select | None | Always required | Drives #16 and #17. Branch icon plus the same unidentified second icon as GP #21 | #21, same options, but single select here (multi select in GP) |
| 16 | DOCUMENTATION – Please upload all related contracts and documents. | File upload | (Required: vendor proposal, quote, order form,  MSA, DPA) | Always required | Shown if #15 is "Signed Contract" | #22, adds a description listing required documents |
| 17 | SUPPORTING LINKS – Please provide any relevant online links related to this request. | Link | (For example: pricing page, online terms and conditions, online subscription agreement,privacy policy, Data Processing Agreement (DPA), or product documentation.) | Always required | Shown if #15 is "Online click-through agreement" | #23, same description, different title |
| 18 | SUPPORTING LINKS – Links Continued | Link | (For example: pricing page, online terms and conditions, privacy policy, Data Processing Agreement (DPA), or product documentation.) | No | None shown | #24, has a description here |
| 19 | DATA ACCESS – Please briefly describe the type of access or data involved? | Paragraph | None | Always required | None shown (comes before the yes/no question #20) | None |
| 20 | DATA ACCESS – Will this vendor require access to sensitive data, systems, or confidential comp... | Multi select | None | Always required | Branch icon plus the second icon. What it drives not yet seen | None |
| 21 | SYSTEM INTEGRATION – Will this vendor integrate with any MinIO systems? | Multi select | None | Always required | Branch icon plus the second icon. Drives #22 | None |
| 22 | SYSTEM INTEGRATION – Please describe which MinIO systems the vendor will integrate with. | Paragraph | None | Always required | Shown if #21 is "Yes" | None |
| 23 | THIRD-PARTY SERVICES – Does this vendor use any subcontractors or third-party service providers? | Multi select | None | Always required | Drives #24. Branch icon only, no second icon | None |
| 24 | THIRD-PARTY SERVICES – If yes, please explain. | Paragraph | None | Always required | Shown if #23 is "Yes" | None |
| 25 | SYSTEM INTEGRATION – Please describe the type of access, integration, or connection require... | Paragraph | None | Always required | Shown with 1 condition. Rule not opened; possibly #20 | None |

### Options

#5 NEGOTIATIONS (option 2 cut off; option 1 full text from the #6 condition panel):

1. Yes ( Please provide the JustificationYes — I have already discussed or negotiated with the vendor (please provide details in the justification field)
2. No — I have not engaged with the vendor. I will contact Procurement (Procurement(...

Option 1 differs from GP #5: it starts with "Yes ( Please provide the Justification" run straight into the GP wording.

#15 PURCHASE METHOD (option 3 cut off; same as GP #21):

1. Online click-through agreement
2. Signed Contract
3. No contract required (PO / invoice-based purchase; no vendor terms, no data acce...

The description's "MinIO terms" governance option is not among them.

#20 DATA ACCESS, #21 SYSTEM INTEGRATION and #23 THIRD-PARTY SERVICES: Yes / No. #23 full title taken from the #24 condition panel.

## Not yet captured

- Questions after #25, with their conditions.
- What #20 drives, and the #25 condition.
- Full titles of #20 and #25 (cut off).
- Full titles of #6 and #9, and #5 option 2 (cut off).
- Change order form and AI instructions.
- Page 2 of the program editor.
