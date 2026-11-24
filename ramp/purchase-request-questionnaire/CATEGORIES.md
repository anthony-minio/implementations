# Question categories

Updated: 2026-11-24

Every question in the three in-scope programs, grouped into categories for the review. Source: `GENERAL-PROCUREMENT.md` (GP), `PROFESSIONAL-SERVICES.md` (PS) and `SOFTWARE-SAAS.md` (SW). IDs are program plus question number, so `GP21` is General Procurement question 21. Titles are as in Ramp; `...` means cut off in the screenshot.

In `Shown when`, question numbers refer to the same program.

`Approval` marks questions with the approval icon: Ramp uses the answer in approval conditions (tooltip on GP21, 2026-11-24).

## Summary

| # | Category | Questions | GP | PS | SW | Used in approvals |
|---|---|---|---|---|---|---|
| 1 | Request basics | 9 | 3 | 3 | 3 | - |
| 2 | Request type | 3 | 2 | - | 1 | - |
| 3 | Vendor and negotiations | 15 | 5 | 5 | 5 | - |
| 4 | Business need and impact | 11 | 4 | 4 | 3 | - |
| 5 | Alternatives and existing tools | 4 | - | - | 4 | - |
| 6 | Revenue and GTM | 5 | 4 | 1 | - | - |
| 7 | Owner, department and timing | 9 | 3 | 3 | 3 | - |
| 8 | Contract and commercial terms | 15 | 5 | 5 | 5 | GP21, PS15, SW19 |
| 9 | Security and compliance | 22 | - | 10 | 12 | PS20, PS21, PS26, SW24, SW26, SW31 |
| 10 | Software and IT | 3 | - | - | 3 | - |
| Other | Other | 4 | 2 | 1 | 1 | - |
| | Total | 100 | 28 | 32 | 40 | |

## Proposed category flow

For discussion. Who sees each category in a combined form, if Request type becomes the main branch.

| Order | Category | Who sees it |
|---|---|---|
| 1 | Request basics | Everyone |
| 2 | Request type | Everyone. Drives the rest of the form |
| 3 | Vendor and negotiations | Everyone. New vendor details straight after Vendor |
| 4 | Owner, department and timing | Everyone |
| 5 | Business need and impact | Everyone, with follow-ups by request type |
| 6 | Alternatives and existing tools | New software (and perhaps trials) |
| 7 | Software and IT | Software |
| 8 | Revenue and GTM | Customer-facing events, if kept |
| 9 | Contract and commercial terms | Everyone |
| 10 | Security and compliance | Software and services; perhaps any new vendor |
| 11 | Approval notes | Everyone, optional |

## 1. Request basics

Name, one-time or recurring, amount. Ramp system fields; the first three questions in every program.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| GP1 | REQUEST DETAILS – Give this request a name | Request name | Yes | None shown |  |
| GP2 | REQUEST DETAILS – Is it one-time or recurring? | Frequency | Locked | None shown |  |
| GP3 | SPEND – What is the spend amount? | Amount | Locked | None shown |  |
| PS1 | REQUEST DETAILS – Give this request a name | Request name | Yes | None shown |  |
| PS2 | REQUEST DETAILS – Is it one-time or recurring? | Frequency | Locked | None shown |  |
| PS3 | SPEND – What is the spend amount? | Amount | Locked | None shown |  |
| SW1 | REQUEST DETAILS – Give this request a name | Request name | Yes | None shown |  |
| SW2 | REQUEST DETAILS – Is this a one-time or recurring request? | Frequency | Locked | None shown |  |
| SW3 | SPEND DETAILS – What is the expected spend amount? | Amount | Locked | None shown |  |

Points for the review:

- Same three questions in all programs; only the wording differs ("SPEND" vs "SPEND DETAILS", "Is it" vs "Is this a").

## 2. Request type

What kind of request this is. GP asks what kind of purchase (event types plus Other); SW asks where in the lifecycle (new, renewal, amendment, trial). PS has no type question.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| GP8 | REQUEST TYPE – What best describes this request? | Multi select | Always required | Drives #9 |  |
| GP9 | REQUEST TYPE – If other, please explain | Paragraph | Always required | Shown if #8 is "Other" |  |
| SW4 | REQUEST TYPE – What type of request is this? | Single select | Always required | Drives #13 only (no other question conditions on it) |  |

Points for the review:

- Two different axes under the same name. The combined form needs a "what are you buying" question, and possibly a lifecycle question.
- This is the natural question to branch the whole form on.

## 3. Vendor and negotiations

Who the vendor is, details for a new vendor, and whether the requester has already talked to them.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| GP4 | VENDOR – Specify the vendor for this request | Vendor | Always required | Drives #26 and #27. Restrict available vendors: Off |  |
| GP5 | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | Multi select | Always required | Drives #6 |  |
| GP6 | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | Paragraph | Always required | Shown if #5 is "Yes — I have already discussed or negotiated with the vendor (please provide details in the justification field)" |  |
| GP26 | VENDOR – Vendor contact | Vendor contact | Always required | Shown if Vendor (#4) is "New vendor" |  |
| GP27 | VENDOR – Vendor address | Vendor address | Always required | Shown if Vendor (#4) is "New vendor" |  |
| PS4 | VENDOR- Specify the vendor for this request | Vendor | Always required | Drives #30 and #31. Restrict available vendors: Off |  |
| PS5 | NEGOTIATIONS- Have you already engaged in discussions or negotiations with the vendor? | Multi select | Always required | Drives #6 |  |
| PS6 | NEGOTIATIONS- If YES → Provide justification and describe what was discussed or negotiated... | Paragraph | Always required | Shown if #5 is option 1 |  |
| PS30 | VENDOR – Vendor contact | Vendor contact | Always required | Shown if Vendor (#4) is "New vendor" |  |
| PS31 | VENDOR – Vendor address | Vendor address | Always required | Shown if Vendor (#4) is "New vendor" |  |
| SW5 | VENDOR – Specify the vendor for this request | Vendor | Always required | Drives #38 and #39. Restrict available vendors: Off |  |
| SW6 | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | Multi select | Always required | Drives #7 |  |
| SW7 | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | Paragraph | Always required | Shown if #6 is "Yes — I have already discussed or negotiated with the vendor (please provide details in the justification field)" |  |
| SW38 | VENDOR – Vendor contact | Vendor contact | Always required | Shown if Vendor (#5) is "New vendor" |  |
| SW39 | VENDOR – Vendor address | Vendor address | Always required | Shown if Vendor (#5) is "New vendor" |  |

Points for the review:

- Same in all three programs, apart from dashes, a garbled PS option and multi select used for a Yes/No.
- New vendor contact and address sit at the end of every form, far from the Vendor question that triggers them.

## 4. Business need and impact

What is being bought and why, and what it will achieve.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| GP7 | BUSINESS PURPOSE – Describe the business purpose | Paragraph | Always required | None shown |  |
| GP17 | SERVICES / GOODS – Please describe the nature of the goods or services being requested | Paragraph | Always required | None shown |  |
| GP10 | BUSINESS IMPACT – What is the primary expected outcome? | Multi select | Always required | Drives #13 |  |
| GP11 | BUSINESS IMPACT – What is the expected business impact of this request? | Paragraph | Always required | Shown if #8 is "Other" (condition screenshot sent after #11; confirm it is #11's and not a second capture of #9's) |  |
| PS7 | SERVICES – Please describe the nature of the external services being requested. | Paragraph | Always required | None shown |  |
| PS8 | BUSINESS PURPOSE – What is the purpose of these external services? | Paragraph | Always required | None shown |  |
| PS10 | BUSINESS IMPACT – What business impact is expected from this engagement? | Paragraph | Always required | None shown |  |
| PS11 | SUCCESS METRICS – How will success be measured for this engagement? | Paragraph | Always required | None shown |  |
| SW8 | BUSINESS NEED – Describe the business need and the proposed solution | Paragraph | Always required | None shown |  |
| SW9 | BUSINESS NEED – What business problem does this software or service solve? | Paragraph | Always required | None shown |  |
| SW10 | BUSINESS IMPACT – What is the expected business impact? | Paragraph | Always required | None shown |  |

Points for the review:

- Every program asks purpose and impact, worded differently. SW asks need twice (#8, #9).
- GP asks "what are you buying" last (#17); PS and SW ask it near the top.
- PS adds success metrics (#11); GP adds a primary outcome list (#10).

## 5. Alternatives and existing tools

Whether an existing tool could do the job. Software / SaaS only.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| SW11 | BUSINESS NEED – Is this replacing an existing tool or adding a new capability? | Text | Always required | None shown |  |
| SW12 | ALTERNATIVES – What alternative tools (including existing internal tools) were considered? | Paragraph | Always required | None shown |  |
| SW13 | ALTERNATIVES – Have you checked if we already have an existing tool or service that meets thi... | Multi select | Always required | Shown if #4 is "New software purchase". Drives #14 |  |
| SW14 | ALTERNATIVES – If yes, please explain why a new tool or service is still required | Paragraph | Always required | Shown if #13 is "Yes ( Please Explain why a new tool or service is still needed)" |  |

Points for the review:

- Only #13 is limited to new purchases; #11 and #12 also show for renewals, amendments and trials.
- #12 (alternatives considered) comes before #13 (have you checked for an existing tool).

## 6. Revenue and GTM

Pipeline, ROI, target accounts and GTM alignment. Mostly the GP event path.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| GP12 | BUSINESS IMPACT – What pipeline impact is expected (net-new, expansion, or renewal)? | Paragraph | Always required | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", "Internal meeting / team event" or "Training / enablement" (every option except "Other") |  |
| GP13 | BUSINESS IMPACT –EXPECTED ROI / PIPELINE IMPACT – What is the anticipated financial retu... | Paragraph | No | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship" or "Conference / trade show", or #10 is "Relationship building / customer engagement", "Pipeline progression / sales follow-up", "Lead generation" or "Brand awareness" |  |
| GP14 | CUSTOMERS / TARGET ACCOUNTS – Which priority customers or target accounts are expect... | Paragraph | Always required | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", "Internal meeting / team event" or "Training / enablement" (every option except "Other") |  |
| GP15 | GTM ALIGNMENT – How does this request support current GTM priorities or revenue objective... | Paragraph | Always required | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", "Internal meeting / team event" or "Training / enablement" (every option except "Other") |  |
| PS9 | CUSTOMERS / TARGET ACCOUNTS – Which priority customers, partners, or target accounts w... | Paragraph | Always required | None shown |  |

Points for the review:

- In GP these show for every event type, including internal team events and training.
- PS asks target accounts for every engagement.
- Who uses the answers is not known yet (Anthony, 2026-11-24).

## 7. Owner, department and timing

Who owns the request, which department, and any deadline.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| GP18 | TIMELINE – Is there a target date or deadline by which this purchase or contract needs to be co... | Date | No | None shown |  |
| GP19 | REQUESTER – Who is the internal business owner/requester? | Text | Always required | None shown |  |
| GP20 | DEPARTMENT – Which department is this request for? | Department | Always required | None shown |  |
| PS12 | TIMELINE – Is there a target date or deadline by which this purchase or contract needs to be co... | Date | No | None shown |  |
| PS13 | REQUESTER – Who is the internal business owner/requester? | Text | Always required | None shown |  |
| PS14 | DEPARTMENT – Which department will be using this service? | Department | Always required | None shown |  |
| SW15 | TIMELINE – Is there a target date or deadline by which this purchase needs to be completed? | Date | No | None shown |  |
| SW16 | REQUESTER – Who is the internal business owner/requester? | Text | Always required | None shown |  |
| SW17 | DEPARTMENT – Which department will use this software? | Department | Always required | None shown |  |

Points for the review:

- Same in all three programs. Department is the only coded field the forms collect.
- Requester is free text. Anthony's proposal (2026-11-24): ask "Are you submitting this on behalf of someone else at MinIO?" and, if Yes, pick the person from a dropdown. Depends on what Ramp supports.

## 8. Contract and commercial terms

How the purchase is governed, the documents, and payment terms.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| GP21 | PURCHASE METHOD – How will this purchase be made? | Multi select | Always required | Branch icon shown, plus a approval icon (used in approval conditions). Drives #22 and #23 | Yes |
| GP22 | CONTRACTS / DOCUMENTATION – Please upload all contracts and documents | File upload | Always required | Shown if #21 is "Signed Contract" |  |
| GP23 | CONTRACTS / DOCUMENTATION – Include relevant links (such as terms or pricing) | Link | Always required | Shown if #21 is "Online click-through agreement" |  |
| GP24 | CONTRACTS / DOCUMENTATION- Include relevant links (such as terms or pricing) Continued | Link | No | None shown |  |
| GP25 | PAYMENT TERMS – What are the net payment terms? | Net payment terms | No | None shown |  |
| PS15 | PURCHASE METHOD – How will this purchase be made? | Single select | Always required | Drives #16 and #17. Branch icon plus the approval icon, as GP #21 | Yes |
| PS16 | DOCUMENTATION – Please upload all related contracts and documents. | File upload | Always required | Shown if #15 is "Signed Contract" |  |
| PS17 | SUPPORTING LINKS – Please provide any relevant online links related to this request. | Link | Always required | Shown if #15 is "Online click-through agreement" |  |
| PS18 | SUPPORTING LINKS – Links Continued | Link | No | None shown |  |
| PS29 | PAYMENT TERMS – What are the net payment terms? | Net payment terms | No | None shown |  |
| SW19 | PURCHASE METHOD – How will this software purchase be made? | Multi select | Always required | Drives #20 and #21. Branch icon plus the approval icon | Yes |
| SW20 | CONTRACTS / DOCUMENTATION – Please upload all related contracts and documents. | File upload | Always required | Shown if #19 is "Signed Contract" |  |
| SW21 | CONTRACTS / DOCUMENTATION – Please provide any relevant online links related to this purc... | Link | Always required | Shown if #19 is "Online click-through agreement" |  |
| SW22 | CONTRACTS / DOCUMENTATION – Links continued | Link | No | None shown |  |
| SW37 | PAYMENT TERMS – What are the net payment terms? | Net payment terms | No | None shown |  |

Points for the review:

- Purchase Method is used in approval conditions in all three programs.
- Purchase Method differs: GP multi select with 3 options, PS single select with 3, SW multi select with 2 (no "No contract required").
- The extra link field shows for everyone in all three, even with no contract.

## 9. Security and compliance

Data use and access, system integration, subcontractors, SOC 2. PS and SW only.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| PS19 | DATA ACCESS – Please briefly describe the type of access or data involved? | Paragraph | Always required | None shown (comes before the yes/no question #20) |  |
| PS20 | DATA ACCESS – Will this vendor require access to sensitive data, systems, or confidential company information? | Multi select | Always required | Branch icon plus the approval icon. Drives #26 | Yes |
| PS21 | SYSTEM INTEGRATION – Will this vendor integrate with any MinIO systems? | Multi select | Always required | Branch icon plus the approval icon. Drives #22, #25 and #26 | Yes |
| PS22 | SYSTEM INTEGRATION – Please describe which MinIO systems the vendor will integrate with. | Paragraph | Always required | Shown if #21 is "Yes" |  |
| PS23 | THIRD-PARTY SERVICES – Does this vendor use any subcontractors or third-party service providers? | Multi select | Always required | Drives #24. Branch icon only, no approval icon |  |
| PS24 | THIRD-PARTY SERVICES – If yes, please explain. | Paragraph | Always required | Shown if #23 is "Yes" |  |
| PS25 | SYSTEM INTEGRATION – Please describe the type of access, integration, or connection require... | Paragraph | Always required | Shown if #21 is "Yes" (same condition as #22) |  |
| PS26 | SECURITY / COMPLIANCE – Does the vendor have a SOC 2 Type II report? | Multi select | Always required | Shown if #20 is "Yes" or #21 is "Yes". Branch icon plus the approval icon. Drives #27 and #28 | Yes |
| PS27 | SECURITY / COMPLIANCE –If Yes, Please upload the SOC 2 Type II  report | File upload | Always required | Shown if #26 is "Yes" |  |
| PS28 | SECURITY / COMPLIANCE –If no, Please explain why | Paragraph | No | Shown if #26 is "No" |  |
| SW23 | DATA USAGE – What type of data will be used, uploaded, or stored in this system? | Paragraph | Always required | None shown |  |
| SW24 | DATA ACCESS – Will this vendor require access to sensitive data, systems, or confidential company information? | Multi select | Always required | Drives #25 and #31. Branch icon plus the approval icon | Yes |
| SW25 | DATA ACCESS – Please briefly describe the type of access or data involved? | Paragraph | Always required | Shown if #24 is "Yes" |  |
| SW26 | SYSTEM INTEGRATION – Will this vendor integrate with any MinIO systems? | Multi select | Always required | Drives #27, #30 and #31. Branch icon plus the approval icon | Yes |
| SW27 | SYSTEM INTEGRATION – Please describe which MinIO systems the vendor will integrate with | Paragraph | No | Shown if #26 is "Yes" |  |
| SW28 | THIRD-PARTY SERVICES – Does this vendor use any subcontractors or third-party service provider | Multi select | Always required | Drives #29. Branch icon only |  |
| SW29 | THIRD-PARTY SERVICES – If yes, please explain | Paragraph | Always required | Shown if #28 is "Yes" |  |
| SW30 | SYSTEM INTEGRATION – Please describe the type of access, integration, or connection require... | Paragraph | Always required | Shown if #26 is "Yes" (same condition as #27) |  |
| SW31 | SECURITY / COMPLIANCE – Does the vendor have a SOC 2 Type II report? | Multi select | Always required | Shown if #24 is "Yes" or #26 is "Yes". Drives #32 and #33. Branch icon plus the approval icon | Yes |
| SW32 | SECURITY / COMPLIANCE – If yes, please upload the SOC 2 Type II report | File upload | Always required | Shown if #31 is "Yes" |  |
| SW33 | SECURITY / COMPLIANCE – If no, please explain why | Paragraph | Always required | Shown if #31 is "No" |  |
| SW34 | IT/ SECURITY  - Will this vendor access, process, store, or integrate with MinIO systems, confide... | Multi select | Always required | None shown. No branch icon, no approval icon |  |

Points for the review:

- Data Access, System Integration and SOC 2 are used in approval conditions in both programs.
- PS asks for a description of data access before the Yes/No and from everyone; SW asks it after a Yes.
- An integration Yes opens two describe boxes in both programs.
- SW #34 repeats #24 and #26 and drives nothing.
- SW #31 description ("If Yes → triggers Legal ... review") to be checked in the review.
- GP has none of these questions.

## 10. Software and IT

User count and SSO. Software / SaaS only.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| SW18 | USERS – Approximately how many users will need access to this software? | Text | Always required | None shown |  |
| SW35 | AUTHENTICATION – Does this system support Single Sign-On (SSO)? | Multi select | Always required | Drives #36 |  |
| SW36 | AUTHENTICATION – Please specify which SSO providers are supported | Paragraph | Always required | Shown if #35 is "Yes" |  |

Points for the review:

- User count is also asked in the #9 description.
- SSO is asked for renewals as well as new purchases.

## Other

Questions that don't sit cleanly in a category.

| ID | Question | Type | Required | Shown when | Approval |
|---|---|---|---|---|---|
| GP16 | VENDOR RELATIONSHIP – What is the current status of our relationship with this vendor? | Paragraph | No | Shown if #8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship", "Conference / trade show", "Internal meeting / team event" or "Training / enablement" (every option except "Other") |  |
| GP28 | APPROVAL NOTES – Add a message for approvers to review | Text | No | None shown |  |
| PS32 | APPROVAL NOTES – Add a message for approvers to review | Paragraph | No | None shown |  |
| SW40 | APPROVAL NOTES – Add a message for approvers to review | Paragraph | No | None shown |  |

Points for the review:

- GP #16 (status of our relationship with this vendor) shows only on the event path and is optional. It overlaps the negotiations questions.
- Approval notes is the same optional free-text box in all three programs (Text in GP, Paragraph in PS and SW).
