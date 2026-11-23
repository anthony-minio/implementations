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
| 5 | VENDOR – Specify the vendor for this request | Vendor | None | Always required | Drives #38 and #39. Restrict available vendors: Off | GP #4, same; PS #4 |
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
| 19 | PURCHASE METHOD – How will this software purchase be made? | Multi select | None | Always required | Drives #20 and #21. Branch icon plus the second icon | GP #21 (multi select), PS #15 (single select); no "No contract required" option here |
| 20 | CONTRACTS / DOCUMENTATION – Please upload all related contracts and documents. | File upload | (Required: vendor proposal, quote, order form,  MSA, DPA) | Always required | Shown if #19 is "Signed Contract" | GP #22; PS #16, same description |
| 21 | CONTRACTS / DOCUMENTATION – Please provide any relevant online links related to this purc... | Link | (For example: pricing page, online terms and conditions, online subscription agreement,privacy policy, Data Processing Agreement (DPA), or product documentation.) | Always required | Shown if #19 is "Online click-through agreement" | GP #23, PS #17, same description |
| 22 | CONTRACTS / DOCUMENTATION – Links continued | Link | (For example: pricing page, online terms and conditions, privacy policy, Data Processing Agreement (DPA), or product documentation.) | No | None shown | GP #24, PS #18 |
| 23 | DATA USAGE – What type of data will be used, uploaded, or stored in this system? | Paragraph | e.g., marketing content, internal documents, prompts, analytics data, customer data, etc.). | Always required | None shown | PS #19 in purpose ("type of access or data involved") |
| 24 | DATA ACCESS – Will this vendor require access to sensitive data, systems, or confidential company information? | Multi select | None | Always required | Drives #25 and #31. Branch icon plus the second icon | PS #20, same |
| 25 | DATA ACCESS – Please briefly describe the type of access or data involved? | Paragraph | None | Always required | Shown if #24 is "Yes" | PS #19, same title; in PS it comes before the yes/no and has no condition |
| 26 | SYSTEM INTEGRATION – Will this vendor integrate with any MinIO systems? | Multi select | None | Always required | Drives #27, #30 and #31. Branch icon plus the second icon | PS #21, same |
| 27 | SYSTEM INTEGRATION – Please describe which MinIO systems the vendor will integrate with | Paragraph | None | No | Shown if #26 is "Yes" | PS #22 (required there) |
| 28 | THIRD-PARTY SERVICES – Does this vendor use any subcontractors or third-party service provider | Multi select | None | Always required | Drives #29. Branch icon only | PS #23; there "providers?" |
| 29 | THIRD-PARTY SERVICES – If yes, please explain | Paragraph | None | Always required | Shown if #28 is "Yes" | PS #24, same |
| 30 | SYSTEM INTEGRATION – Please describe the type of access, integration, or connection require... | Paragraph | None | Always required | Shown if #26 is "Yes" (same condition as #27) | PS #25, same |
| 31 | SECURITY / COMPLIANCE – Does the vendor have a SOC 2 Type II report? | Multi select | If Yes → triggers Legal (and/or Security/Compliance) review | Always required | Shown if #24 is "Yes" or #26 is "Yes". Drives #32 and #33. Branch icon plus the second icon | PS #26, same condition; PS has no description |
| 32 | SECURITY / COMPLIANCE – If yes, please upload the SOC 2 Type II report | File upload | None | Always required | Shown if #31 is "Yes" | PS #27 |
| 33 | SECURITY / COMPLIANCE – If no, please explain why | Paragraph | If unavailable, please provide an explanation (e.g., vendor may not yet have a SOC 2 report) | Always required | Shown if #31 is "No" | PS #28, same description; optional there |
| 34 | IT/ SECURITY  - Will this vendor access, process, store, or integrate with MinIO systems, confide... | Multi select | None | Always required | None shown. No branch icon, no second icon | None; covers the same ground as #24 and #26 together |
| 35 | AUTHENTICATION – Does this system support Single Sign-On (SSO)? | Multi select | e.g, Okta, Azure AD, Google Workspace)? | Always required | Drives #36 | None |
| 36 | AUTHENTICATION – Please specify which SSO providers are supported | Paragraph | None | Always required | Shown if #35 is "Yes" | None |
| 37 | PAYMENT TERMS – What are the net payment terms? | Net payment terms | Number of days | No | None shown | GP #25, PS #29, same |
| 38 | VENDOR – Vendor contact | Vendor contact | None | Always required | Shown if Vendor (#5) is "New vendor" | GP #26, PS #30, same |
| 39 | VENDOR – Vendor address | Vendor address | None | Always required | Shown if Vendor (#5) is "New vendor" | GP #27, PS #31, same |
| 40 | APPROVAL NOTES – Add a message for approvers to review | Paragraph | None | No | None shown | GP #28 (Text there), PS #32, same |

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

#24 DATA ACCESS, #26 SYSTEM INTEGRATION and #28 THIRD-PARTY SERVICES: Yes / No. Full titles of #24 and #28 taken from condition panels; #28 ends "service provider" with no question mark, as in Ramp. #31 SECURITY / COMPLIANCE, #34 IT/ SECURITY and #35 AUTHENTICATION: Yes / No. The #34 title uses a plain hyphen with two spaces before it; the #35 description has a closing bracket with no opening one; the #36 condition panel shows "(SSO)? " and "Yes " with trailing spaces. All as in Ramp. The #23 description has a closing bracket with no opening one, as in Ramp.

## Not yet captured

- Confirm #40 is the last question.
- Full titles of #21, #30 and #34 (cut off).
- What #4 drives.
- Change order form and AI instructions.
