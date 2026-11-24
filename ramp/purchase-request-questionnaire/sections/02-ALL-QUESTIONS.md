# All questions

Every question as it is in Ramp today, by category. Rows are in the order of the distinct questions in the summary. **Program**: GP General Procurement, PS Professional Services, SW Software / SaaS. Titles are copied from Ramp; `...` means the title was cut off in the screenshot. **Approval** after the type means Ramp uses the answer in approval conditions.

## 1. Request basics

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **GP1** | REQUEST DETAILS – Give this request a name | GP | Request name | Yes | Always |
| **PS1** | REQUEST DETAILS – Give this request a name | PS | Request name | Yes | Always |
| **SW1** | REQUEST DETAILS – Give this request a name | SW | Request name | Yes | Always |
| **GP2** | REQUEST DETAILS – Is it one-time or recurring? | GP | Frequency | Yes (Ramp field) | Always |
| **PS2** | REQUEST DETAILS – Is it one-time or recurring? | PS | Frequency | Yes (Ramp field) | Always |
| **SW2** | REQUEST DETAILS – Is this a one-time or recurring request? | SW | Frequency | Yes (Ramp field) | Always |
| **GP3** | SPEND – What is the spend amount? | GP | Amount | Yes (Ramp field) | Always |
| **PS3** | SPEND – What is the spend amount? | PS | Amount | Yes (Ramp field) | Always |
| **SW3** | SPEND DETAILS – What is the expected spend amount? | SW | Amount | Yes (Ramp field) | Always |

## 2. Request type

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **GP8** | REQUEST TYPE – What best describes this request? | GP | Multi select | Yes | Always |
| **GP9** | REQUEST TYPE – If other, please explain | GP | Paragraph | Yes | Shown if GP8 is "Other" |
| **SW4** | REQUEST TYPE – What type of request is this? | SW | Single select | Yes | Always |

## 3. Vendor and negotiations

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **GP4** | VENDOR – Specify the vendor for this request | GP | Vendor | Yes | Always |
| **PS4** | VENDOR- Specify the vendor for this request | PS | Vendor | Yes | Always |
| **SW5** | VENDOR – Specify the vendor for this request | SW | Vendor | Yes | Always |
| **GP5** | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | GP | Multi select | Yes | Always |
| **PS5** | NEGOTIATIONS- Have you already engaged in discussions or negotiations with the vendor? | PS | Multi select | Yes | Always |
| **SW6** | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | SW | Multi select | Yes | Always |
| **GP6** | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | GP | Paragraph | Yes | Shown if GP5 is "Yes" |
| **PS6** | NEGOTIATIONS- If YES → Provide justification and describe what was discussed or negotiated... | PS | Paragraph | Yes | Shown if PS5 is "Yes" |
| **SW7** | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | SW | Paragraph | Yes | Shown if SW6 is "Yes" |
| **GP26** | VENDOR – Vendor contact | GP | Vendor contact | Yes | Shown if Vendor (GP4) is "New vendor" |
| **PS30** | VENDOR – Vendor contact | PS | Vendor contact | Yes | Shown if Vendor (PS4) is "New vendor" |
| **SW38** | VENDOR – Vendor contact | SW | Vendor contact | Yes | Shown if Vendor (SW5) is "New vendor" |
| **GP27** | VENDOR – Vendor address | GP | Vendor address | Yes | Shown if Vendor (GP4) is "New vendor" |
| **PS31** | VENDOR – Vendor address | PS | Vendor address | Yes | Shown if Vendor (PS4) is "New vendor" |
| **SW39** | VENDOR – Vendor address | SW | Vendor address | Yes | Shown if Vendor (SW5) is "New vendor" |

## 4. Business need and impact

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **GP17** | SERVICES / GOODS – Please describe the nature of the goods or services being requested | GP | Paragraph | Yes | Always |
| **PS7** | SERVICES – Please describe the nature of the external services being requested. | PS | Paragraph | Yes | Always |
| **GP7** | BUSINESS PURPOSE – Describe the business purpose | GP | Paragraph | Yes | Always |
| **PS8** | BUSINESS PURPOSE – What is the purpose of these external services? | PS | Paragraph | Yes | Always |
| **SW8** | BUSINESS NEED – Describe the business need and the proposed solution | SW | Paragraph | Yes | Always |
| **SW9** | BUSINESS NEED – What business problem does this software or service solve? | SW | Paragraph | Yes | Always |
| **GP10** | BUSINESS IMPACT – What is the primary expected outcome? | GP | Multi select | Yes | Always |
| **GP11** | BUSINESS IMPACT – What is the expected business impact of this request? | GP | Paragraph | Yes | Shown if GP8 is "Other" |
| **PS10** | BUSINESS IMPACT – What business impact is expected from this engagement? | PS | Paragraph | Yes | Always |
| **SW10** | BUSINESS IMPACT – What is the expected business impact? | SW | Paragraph | Yes | Always |
| **PS11** | SUCCESS METRICS – How will success be measured for this engagement? | PS | Paragraph | Yes | Always |

## 5. Alternatives and existing tools

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **SW11** | BUSINESS NEED – Is this replacing an existing tool or adding a new capability? | SW | Text | Yes | Always |
| **SW12** | ALTERNATIVES – What alternative tools (including existing internal tools) were considered? | SW | Paragraph | Yes | Always |
| **SW13** | ALTERNATIVES – Have you checked if we already have an existing tool or service that meets thi... | SW | Multi select | Yes | Shown if SW4 is "New software purchase" |
| **SW14** | ALTERNATIVES – If yes, please explain why a new tool or service is still required | SW | Paragraph | Yes | Shown if SW13 is "Yes" |

## 6. Revenue and GTM

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **GP12** | BUSINESS IMPACT – What pipeline impact is expected (net-new, expansion, or renewal)? | GP | Paragraph | Yes | Shown if GP8 is any event type (any option except "Other") |
| **GP13** | BUSINESS IMPACT –EXPECTED ROI / PIPELINE IMPACT – What is the anticipated financial retu... | GP | Paragraph | No | Shown if GP8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship" or "Conference / trade show", or GP10 is "Relationship building / customer engagement", "Pipeline progression / sales follow-up", "Lead generation" or "Brand awareness" |
| **GP14** | CUSTOMERS / TARGET ACCOUNTS – Which priority customers or target accounts are expect... | GP | Paragraph | Yes | Shown if GP8 is any event type (any option except "Other") |
| **PS9** | CUSTOMERS / TARGET ACCOUNTS – Which priority customers, partners, or target accounts w... | PS | Paragraph | Yes | Always |
| **GP15** | GTM ALIGNMENT – How does this request support current GTM priorities or revenue objective... | GP | Paragraph | Yes | Shown if GP8 is any event type (any option except "Other") |

## 7. Owner, department and timing

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **GP18** | TIMELINE – Is there a target date or deadline by which this purchase or contract needs to be co... | GP | Date | No | Always |
| **PS12** | TIMELINE – Is there a target date or deadline by which this purchase or contract needs to be co... | PS | Date | No | Always |
| **SW15** | TIMELINE – Is there a target date or deadline by which this purchase needs to be completed? | SW | Date | No | Always |
| **GP19** | REQUESTER – Who is the internal business owner/requester? | GP | Text | Yes | Always |
| **PS13** | REQUESTER – Who is the internal business owner/requester? | PS | Text | Yes | Always |
| **SW16** | REQUESTER – Who is the internal business owner/requester? | SW | Text | Yes | Always |
| **GP20** | DEPARTMENT – Which department is this request for? | GP | Department | Yes | Always |
| **PS14** | DEPARTMENT – Which department will be using this service? | PS | Department | Yes | Always |
| **SW17** | DEPARTMENT – Which department will use this software? | SW | Department | Yes | Always |

## 8. Contract and commercial terms

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **GP21** | PURCHASE METHOD – How will this purchase be made? | GP | Multi select, **Approval** | Yes | Always |
| **PS15** | PURCHASE METHOD – How will this purchase be made? | PS | Single select, **Approval** | Yes | Always |
| **SW19** | PURCHASE METHOD – How will this software purchase be made? | SW | Multi select, **Approval** | Yes | Always |
| **GP22** | CONTRACTS / DOCUMENTATION – Please upload all contracts and documents | GP | File upload | Yes | Shown if GP21 is "Signed Contract" |
| **PS16** | DOCUMENTATION – Please upload all related contracts and documents. | PS | File upload | Yes | Shown if PS15 is "Signed Contract" |
| **SW20** | CONTRACTS / DOCUMENTATION – Please upload all related contracts and documents. | SW | File upload | Yes | Shown if SW19 is "Signed Contract" |
| **GP23** | CONTRACTS / DOCUMENTATION – Include relevant links (such as terms or pricing) | GP | Link | Yes | Shown if GP21 is "Online click-through agreement" |
| **PS17** | SUPPORTING LINKS – Please provide any relevant online links related to this request. | PS | Link | Yes | Shown if PS15 is "Online click-through agreement" |
| **SW21** | CONTRACTS / DOCUMENTATION – Please provide any relevant online links related to this purc... | SW | Link | Yes | Shown if SW19 is "Online click-through agreement" |
| **GP24** | CONTRACTS / DOCUMENTATION- Include relevant links (such as terms or pricing) Continued | GP | Link | No | Always |
| **PS18** | SUPPORTING LINKS – Links Continued | PS | Link | No | Always |
| **SW22** | CONTRACTS / DOCUMENTATION – Links continued | SW | Link | No | Always |
| **GP25** | PAYMENT TERMS – What are the net payment terms? | GP | Net payment terms | No | Always |
| **PS29** | PAYMENT TERMS – What are the net payment terms? | PS | Net payment terms | No | Always |
| **SW37** | PAYMENT TERMS – What are the net payment terms? | SW | Net payment terms | No | Always |

## 9. Security and compliance

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **SW23** | DATA USAGE – What type of data will be used, uploaded, or stored in this system? | SW | Paragraph | Yes | Always |
| **PS20** | DATA ACCESS – Will this vendor require access to sensitive data, systems, or confidential company information? | PS | Multi select, **Approval** | Yes | Always |
| **SW24** | DATA ACCESS – Will this vendor require access to sensitive data, systems, or confidential company information? | SW | Multi select, **Approval** | Yes | Always |
| **PS19** | DATA ACCESS – Please briefly describe the type of access or data involved? | PS | Paragraph | Yes | Always |
| **SW25** | DATA ACCESS – Please briefly describe the type of access or data involved? | SW | Paragraph | Yes | Shown if SW24 is "Yes" |
| **PS21** | SYSTEM INTEGRATION – Will this vendor integrate with any MinIO systems? | PS | Multi select, **Approval** | Yes | Always |
| **SW26** | SYSTEM INTEGRATION – Will this vendor integrate with any MinIO systems? | SW | Multi select, **Approval** | Yes | Always |
| **PS22** | SYSTEM INTEGRATION – Please describe which MinIO systems the vendor will integrate with. | PS | Paragraph | Yes | Shown if PS21 is "Yes" |
| **SW27** | SYSTEM INTEGRATION – Please describe which MinIO systems the vendor will integrate with | SW | Paragraph | No | Shown if SW26 is "Yes" |
| **PS25** | SYSTEM INTEGRATION – Please describe the type of access, integration, or connection require... | PS | Paragraph | Yes | Shown if PS21 is "Yes" |
| **SW30** | SYSTEM INTEGRATION – Please describe the type of access, integration, or connection require... | SW | Paragraph | Yes | Shown if SW26 is "Yes" |
| **PS23** | THIRD-PARTY SERVICES – Does this vendor use any subcontractors or third-party service providers? | PS | Multi select | Yes | Always |
| **SW28** | THIRD-PARTY SERVICES – Does this vendor use any subcontractors or third-party service provider | SW | Multi select | Yes | Always |
| **PS24** | THIRD-PARTY SERVICES – If yes, please explain. | PS | Paragraph | Yes | Shown if PS23 is "Yes" |
| **SW29** | THIRD-PARTY SERVICES – If yes, please explain | SW | Paragraph | Yes | Shown if SW28 is "Yes" |
| **PS26** | SECURITY / COMPLIANCE – Does the vendor have a SOC 2 Type II report? | PS | Multi select, **Approval** | Yes | Shown if PS20 is "Yes" or PS21 is "Yes" |
| **SW31** | SECURITY / COMPLIANCE – Does the vendor have a SOC 2 Type II report? | SW | Multi select, **Approval** | Yes | Shown if SW24 is "Yes" or SW26 is "Yes" |
| **PS27** | SECURITY / COMPLIANCE –If Yes, Please upload the SOC 2 Type II  report | PS | File upload | Yes | Shown if PS26 is "Yes" |
| **SW32** | SECURITY / COMPLIANCE – If yes, please upload the SOC 2 Type II report | SW | File upload | Yes | Shown if SW31 is "Yes" |
| **PS28** | SECURITY / COMPLIANCE –If no, Please explain why | PS | Paragraph | No | Shown if PS26 is "No" |
| **SW33** | SECURITY / COMPLIANCE – If no, please explain why | SW | Paragraph | Yes | Shown if SW31 is "No" |
| **SW34** | IT/ SECURITY  - Will this vendor access, process, store, or integrate with MinIO systems, confide... | SW | Multi select | Yes | Always |

## 10. Software and IT

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **SW18** | USERS – Approximately how many users will need access to this software? | SW | Text | Yes | Always |
| **SW35** | AUTHENTICATION – Does this system support Single Sign-On (SSO)? | SW | Multi select | Yes | Always |
| **SW36** | AUTHENTICATION – Please specify which SSO providers are supported | SW | Paragraph | Yes | Shown if SW35 is "Yes" |

## Other

| **ID** | **Question** | **Program** | **Type** | **Required** | **Shown when** |
|---|---|---|---|---|---|
| **GP16** | VENDOR RELATIONSHIP – What is the current status of our relationship with this vendor? | GP | Paragraph | No | Shown if GP8 is any event type (any option except "Other") |
| **GP28** | APPROVAL NOTES – Add a message for approvers to review | GP | Text | No | Always |
| **PS32** | APPROVAL NOTES – Add a message for approvers to review | PS | Paragraph | No | Always |
| **SW40** | APPROVAL NOTES – Add a message for approvers to review | SW | Paragraph | No | Always |
