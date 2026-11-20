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

In the order shown. Ramp field type is the tag on the question. Required: `Locked` means the Required box is ticked and greyed out (a Ramp system field).

| # | Title | Ramp field type | Description | Required | Options | Conditional logic |
|---|---|---|---|---|---|---|
| 1 | REQUEST DETAILS – Give this request a name | Request name | None | Yes | n/a | None shown |
| 2 | REQUEST DETAILS – Is it one-time or recurring? | Frequency | None | Locked | Not shown | None shown |
| 3 | SPEND – What is the spend amount? | Amount | None | Locked | n/a | None shown |
| 4 | VENDOR – Specify the vendor for this request | Vendor | None | Always required | Restrict available vendors: Off | None shown |
| 5 | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | Multi select | If "No", contact Procurement before submitting by emailing: Procurement@minio.io | Always required | See below | Branch icon shown on the question. Rules not captured |

Question 5 options (both cut off in the screenshot):

1. Yes — I have already discussed or negotiated with the vendor (please provide detai...
2. No — I have not engaged with the vendor. I will contact Procurement (Procurement(...

## Not yet captured

- Questions after #5, if any.
- Whether anything sits between #4 and #5 (the screenshots don't overlap).
- Full text of the two #5 options.
- The conditional rules on #5: what shows, or what happens, for each answer.
- Options for #2 Frequency.
- Page 2 of the program editor (the dots at the top show 2 pages; likely approvals).
