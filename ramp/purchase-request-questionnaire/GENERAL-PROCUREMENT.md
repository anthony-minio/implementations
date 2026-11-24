# General Procurement Request - current setup

Captured: 2026-11-20, from the program editor in Ramp (Procurement > Programs > General Procurement Request > edit, page 1 of 2). Text is copied as it appears in Ramp, including its dashes.

Screenshots: `screenshots/20261120-general-procurement-*.png`.

## Program

| Setting | Value |
|---|---|
| Program name | General Procurement Request |
| Program type | Requests from employees that result in purchase orders |
| Who can request? | All employees |
| PO Accounting fields | Off (greyed out) |
| Line items | On |
| Line item details | Description*, Quantity*, Rate*, Amount* |
| Line item accounting fields | None |

## Program description

> This form is intended for procurement needs that do not fall under new SaaS/software subscriptions or professional services engagements. It covers a broad range of physical goods and general services, including:
>
> Marketing materials or branded merchandise
>
> Hotel or venue contracts
>
> Maintenance or operational services
>
> Shipping, logistics, or courier services
>
> Add-on licenses or seat increases for existing tools or subscriptions
>
> Any other non-technical or non-consulting purchase not already covered under SaaS or Professional Services
>
> Please use this form to initiate a request for internal review and approval. If you're unsure which form to use, contact the Procurement team at Procurement@minio.io

## Questions

In the order shown. Ramp field type is the tag on the question. Required: `Locked` means the Required box is ticked and greyed out (a Ramp system field). `...` means the text is cut off in the screenshot.

| # | Title | Ramp field type | Description | Required | Conditional logic |
|---|---|---|---|---|---|
| 1 | REQUEST DETAILS – Give this request a name | Request name | None | Yes | None shown |
| 2 | REQUEST DETAILS – Is it one-time or recurring? | Frequency | None | Locked | None shown |
| 3 | SPEND – What is the spend amount? | Amount | None | Locked | None shown |
| 4 | VENDOR – Specify the vendor for this request | Vendor | None | Always required | Drives #26 and #27. Restrict available vendors: Off |
| 5 | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | Multi select | If "No", contact Procurement before submitting by emailing: Procurement@minio.io | Always required | Drives #6 |
| 6 | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | Paragraph | Provide a brief summary of any prior negotiations you personally conducted with this vendor. Include the negotiated pricing, terms, discounts, or special considerations, and indicate whether Procurement participated or assisted. | Always required | Shown if #5 is "Yes — I have already discussed or negotiated with the vendor (please provide details in the justification field)" |
| 7 | BUSINESS PURPOSE – Describe the business purpose | Paragraph | Briefly describe the business purpose (e.g., customer engagement, pipeline advancement, brand awareness). One–two sentences is sufficient. | Always required | None shown |
| 8 | REQUEST TYPE – What best describes this request? | Multi select | None | Always required | Drives #9 |
| 9 | REQUEST TYPE – If other, please explain | Paragraph | None | Always required | Shown if #8 is "Other" |
| 10 | BUSINESS IMPACT – What is the primary expected outcome? | Multi select | None | Always required | Drives #13 |
| 11 | BUSINESS IMPACT – What is the expected business impact of this request? | Paragraph | (Examples: efficiency gains, cost savings or avoidance, risk reduction, revenue enablement, compliance, or scalability.) | Always required | Shown if #8 is "Other" (condition screenshot sent after #11; confirm it is #11's and not a second capture of #9's) |
| 12 | BUSINESS IMPACT – What pipeline impact is expected (net-new, expansion, or renewal)? | Paragraph | (Include current active pipeline with this partner, expected incremental pipeline $, and expected number of deal registrations or influenced deals. | Always required | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", "Internal meeting / team event" or "Training / enablement" (every option except "Other") |
| 13 | BUSINESS IMPACT –EXPECTED ROI / PIPELINE IMPACT – What is the anticipated financial retu... | Paragraph | For revenue-generating activities, include projected pipeline value, expected opportunities, conversion assumptions, and historical or comparable performance. If financial ROI cannot be quantified, describe the expected measurable business value and how success will be evaluated. | No | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship" or "Conference / trade show", or #10 is "Relationship building / customer engagement", "Pipeline progression / sales follow-up", "Lead generation" or "Brand awareness" |
| 14 | CUSTOMERS / TARGET ACCOUNTS – Which priority customers or target accounts are expect... | Paragraph | None | Always required | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", "Internal meeting / team event" or "Training / enablement" (every option except "Other") |
| 15 | GTM ALIGNMENT – How does this request support current GTM priorities or revenue objective... | Paragraph | None | Always required | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", "Internal meeting / team event" or "Training / enablement" (every option except "Other") |
| 16 | VENDOR RELATIONSHIP – What is the current status of our relationship with this vendor? | Paragraph | None | No | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", "Internal meeting / team event" or "Training / enablement" (every option except "Other") |
| 17 | SERVICES / GOODS – Please describe the nature of the goods or services being requested | Paragraph | None | Always required | None shown |
| 18 | TIMELINE – Is there a target date or deadline by which this purchase or contract needs to be co... | Date | None | No | None shown |
| 19 | REQUESTER – Who is the internal business owner/requester? | Text | None | Always required | None shown |
| 20 | DEPARTMENT – Which department is this request for? | Department | None | Always required | None shown |
| 21 | PURCHASE METHOD – How will this purchase be made? | Multi select | None | Always required | Branch icon shown, plus the approval icon (used in approval conditions). Drives #22 and #23 |
| 22 | CONTRACTS / DOCUMENTATION – Please upload all contracts and documents | File upload | None | Always required | Shown if #21 is "Signed Contract" |
| 23 | CONTRACTS / DOCUMENTATION – Include relevant links (such as terms or pricing) | Link | (For example: pricing page, online terms and conditions, online subscription agreement,privacy policy, Data Processing Agreement (DPA), or product documentation.) | Always required | Shown if #21 is "Online click-through agreement" |
| 24 | CONTRACTS / DOCUMENTATION- Include relevant links (such as terms or pricing) Continued | Link | None | No | None shown |
| 25 | PAYMENT TERMS – What are the net payment terms? | Net payment terms | Number of days | No | None shown |
| 26 | VENDOR – Vendor contact | Vendor contact | None | Always required | Shown if Vendor (#4) is "New vendor" |
| 27 | VENDOR – Vendor address | Vendor address | None | Always required | Shown if Vendor (#4) is "New vendor" |
| 28 | APPROVAL NOTES – Add a message for approvers to review | Text | None | No | None shown |

The blurred background of the #6 condition panel confirms nothing sits between #4 and #5. The #12 description has an opening bracket with no closing one, and the #13 title has no space after the first dash, both as in Ramp. A condition listing several answers is read as "any of these". The #12 and #14 condition screenshots are identical; they are matched to questions by the order they were sent.

The approval icon is the small icon to the left of the branch icon. Its tooltip on #21 reads: "Used in 2 approval conditions. Used by rules on "CONTRACTS / DOCUMENTATION – Please upload all contracts and documents" and "CONTRACTS / DOCUMENTATION – Include relevant links (such as terms or pricing)"" (screenshot `20261124-general-procurement-43-approval-icon-tooltip.png`, 2026-11-24). So questions with that icon feed the approval policy.

### Options

#5 NEGOTIATIONS (option 2 cut off):

1. Yes — I have already discussed or negotiated with the vendor (please provide details in the justification field)
2. No — I have not engaged with the vendor. I will contact Procurement (Procurement(...

#8 REQUEST TYPE:

1. Customer-facing sales meeting / dinner
2. Marketing event / sponsorship
3. Conference / trade show
4. Internal meeting / team event
5. Training / enablement
6. Other

#10 BUSINESS IMPACT - primary expected outcome:

1. Relationship building / customer engagement
2. Pipeline progression / sales follow-up
3. Lead generation
4. Brand awareness
5. Internal alignment
6. Not applicable (routine activity)

#21 PURCHASE METHOD (option 3 cut off):

1. Online click-through agreement
2. Signed Contract
3. No contract required (PO / invoice-based purchase; no vendor terms, no data acce...

## Change order form

Section "What's on the change order form?". No questions set up (empty state: "Add questions - Upload a list of existing questions or add new ones here").

## AI instructions

Section "AI instructions - Guide how AI prefills requests from uploaded documents". Ramp's help text: "Guide how AI prefills requests from uploaded documents and helps requesters complete this program's form, including what to look up". Empty (0/2000 characters). Note under the box: "Requesters can review and edit prefilled values".

## Not yet captured

- Confirm the #11 condition.
- Full titles of #13, #14, #15 and #18, and #21 option 3 (cut off).
- Confirm #18 to #22 belong to this program (sent without the program header). #28 is taken as the last question; the change order section was sent next.
- Full text of #5 option 2.
- Options for #2 Frequency.
- Page 2 of the program editor (the dots at the top show 2 pages; likely approvals).
