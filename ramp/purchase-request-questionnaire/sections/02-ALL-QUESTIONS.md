# All questions

Every question as it is in Ramp today, by category. Rows are in the order of the distinct questions in the summary. **Program**: GP General Procurement, PS Professional Services, SW Software / SaaS. Titles are copied from Ramp; `...` means the title was cut off in the screenshot. **Response type** shows Ramp's own type in brackets. **Shown when** says whether the question is conditional. **Dependency**: *Approval* means Ramp uses the answer in approval conditions; *Shows* lists the questions that appear only for certain answers to it.

## 1. Request basics

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **GP1** | REQUEST DETAILS – Give this request a name | GP | Free response (Ramp Request name field) | Yes | Always | None |
| **PS1** | REQUEST DETAILS – Give this request a name | PS | Free response (Ramp Request name field) | Yes | Always | None |
| **SW1** | REQUEST DETAILS – Give this request a name | SW | Free response (Ramp Request name field) | Yes | Always | None |
| **GP2** | REQUEST DETAILS – Is it one-time or recurring? | GP | Multiple choice (Ramp Frequency field) | Yes (Ramp field) | Always | None |
| **PS2** | REQUEST DETAILS – Is it one-time or recurring? | PS | Multiple choice (Ramp Frequency field) | Yes (Ramp field) | Always | None |
| **SW2** | REQUEST DETAILS – Is this a one-time or recurring request? | SW | Multiple choice (Ramp Frequency field) | Yes (Ramp field) | Always | None |
| **GP3** | SPEND – What is the spend amount? | GP | Number (Ramp Amount field) | Yes (Ramp field) | Always | None |
| **PS3** | SPEND – What is the spend amount? | PS | Number (Ramp Amount field) | Yes (Ramp field) | Always | None |
| **SW3** | SPEND DETAILS – What is the expected spend amount? | SW | Number (Ramp Amount field) | Yes (Ramp field) | Always | None |

## 2. Request type

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **GP8** | REQUEST TYPE – What best describes this request? | GP | Multiple choice (several answers) | Yes | Always | Shows GP9, GP11, GP12, GP13, GP14, GP15, GP16 |
| **GP9** | REQUEST TYPE – If other, please explain | GP | Free response (long) | Yes | Shown if GP8 is "Other" | None |
| **SW4** | REQUEST TYPE – What type of request is this? | SW | Multiple choice (one answer) | Yes | Always | Shows SW13 |

## 3. Vendor and negotiations

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **GP4** | VENDOR – Specify the vendor for this request | GP | Vendor picker (Ramp Vendor field) | Yes | Always | Shows GP26, GP27 |
| **PS4** | VENDOR- Specify the vendor for this request | PS | Vendor picker (Ramp Vendor field) | Yes | Always | Shows PS30, PS31 |
| **SW5** | VENDOR – Specify the vendor for this request | SW | Vendor picker (Ramp Vendor field) | Yes | Always | Shows SW38, SW39 |
| **GP5** | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | GP | Yes/No (multi select) | Yes | Always | Shows GP6 |
| **PS5** | NEGOTIATIONS- Have you already engaged in discussions or negotiations with the vendor? | PS | Yes/No (multi select) | Yes | Always | Shows PS6 |
| **SW6** | NEGOTIATIONS – Have you already engaged in discussions or negotiations with the vendor? | SW | Yes/No (multi select) | Yes | Always | Shows SW7 |
| **GP6** | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | GP | Free response (long) | Yes | Shown if GP5 is "Yes" | None |
| **PS6** | NEGOTIATIONS- If YES → Provide justification and describe what was discussed or negotiated... | PS | Free response (long) | Yes | Shown if PS5 is "Yes" | None |
| **SW7** | NEGOTIATIONS – If yes, provide justification and describe what was discussed or negotiated w... | SW | Free response (long) | Yes | Shown if SW6 is "Yes" | None |
| **GP26** | VENDOR – Vendor contact | GP | Contact (Ramp Vendor contact field) | Yes | Shown if Vendor (GP4) is "New vendor" | None |
| **PS30** | VENDOR – Vendor contact | PS | Contact (Ramp Vendor contact field) | Yes | Shown if Vendor (PS4) is "New vendor" | None |
| **SW38** | VENDOR – Vendor contact | SW | Contact (Ramp Vendor contact field) | Yes | Shown if Vendor (SW5) is "New vendor" | None |
| **GP27** | VENDOR – Vendor address | GP | Address (Ramp Vendor address field) | Yes | Shown if Vendor (GP4) is "New vendor" | None |
| **PS31** | VENDOR – Vendor address | PS | Address (Ramp Vendor address field) | Yes | Shown if Vendor (PS4) is "New vendor" | None |
| **SW39** | VENDOR – Vendor address | SW | Address (Ramp Vendor address field) | Yes | Shown if Vendor (SW5) is "New vendor" | None |

## 4. Business need and impact

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **GP17** | SERVICES / GOODS – Please describe the nature of the goods or services being requested | GP | Free response (long) | Yes | Always | None |
| **PS7** | SERVICES – Please describe the nature of the external services being requested. | PS | Free response (long) | Yes | Always | None |
| **GP7** | BUSINESS PURPOSE – Describe the business purpose | GP | Free response (long) | Yes | Always | None |
| **PS8** | BUSINESS PURPOSE – What is the purpose of these external services? | PS | Free response (long) | Yes | Always | None |
| **SW8** | BUSINESS NEED – Describe the business need and the proposed solution | SW | Free response (long) | Yes | Always | None |
| **SW9** | BUSINESS NEED – What business problem does this software or service solve? | SW | Free response (long) | Yes | Always | None |
| **GP10** | BUSINESS IMPACT – What is the primary expected outcome? | GP | Multiple choice (several answers) | Yes | Always | Shows GP13 |
| **GP11** | BUSINESS IMPACT – What is the expected business impact of this request? | GP | Free response (long) | Yes | Shown if GP8 is "Other" | None |
| **PS10** | BUSINESS IMPACT – What business impact is expected from this engagement? | PS | Free response (long) | Yes | Always | None |
| **SW10** | BUSINESS IMPACT – What is the expected business impact? | SW | Free response (long) | Yes | Always | None |
| **PS11** | SUCCESS METRICS – How will success be measured for this engagement? | PS | Free response (long) | Yes | Always | None |

## 5. Alternatives and existing tools

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **SW11** | BUSINESS NEED – Is this replacing an existing tool or adding a new capability? | SW | Free response (short) | Yes | Always | None |
| **SW12** | ALTERNATIVES – What alternative tools (including existing internal tools) were considered? | SW | Free response (long) | Yes | Always | None |
| **SW13** | ALTERNATIVES – Have you checked if we already have an existing tool or service that meets thi... | SW | Yes/No (multi select) | Yes | Shown if SW4 is "New software purchase" | Shows SW14 |
| **SW14** | ALTERNATIVES – If yes, please explain why a new tool or service is still required | SW | Free response (long) | Yes | Shown if SW13 is "Yes" | None |

## 6. Revenue and GTM

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **GP12** | BUSINESS IMPACT – What pipeline impact is expected (net-new, expansion, or renewal)? | GP | Free response (long) | Yes | Shown if GP8 is any event type (any option except "Other") | None |
| **GP13** | BUSINESS IMPACT –EXPECTED ROI / PIPELINE IMPACT – What is the anticipated financial retu... | GP | Free response (long) | No | Shown if GP8 is "Customer-facing sales meeting / dinner", "Marketing event / sponsorship" or "Conference / trade show", or GP10 is "Relationship building / customer engagement", "Pipeline progression / sales follow-up", "Lead generation" or "Brand awareness" | None |
| **GP14** | CUSTOMERS / TARGET ACCOUNTS – Which priority customers or target accounts are expect... | GP | Free response (long) | Yes | Shown if GP8 is any event type (any option except "Other") | None |
| **PS9** | CUSTOMERS / TARGET ACCOUNTS – Which priority customers, partners, or target accounts w... | PS | Free response (long) | Yes | Always | None |
| **GP15** | GTM ALIGNMENT – How does this request support current GTM priorities or revenue objective... | GP | Free response (long) | Yes | Shown if GP8 is any event type (any option except "Other") | None |

## 7. Owner, department and timing

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **GP18** | TIMELINE – Is there a target date or deadline by which this purchase or contract needs to be co... | GP | Date | No | Always | None |
| **PS12** | TIMELINE – Is there a target date or deadline by which this purchase or contract needs to be co... | PS | Date | No | Always | None |
| **SW15** | TIMELINE – Is there a target date or deadline by which this purchase needs to be completed? | SW | Date | No | Always | None |
| **GP19** | REQUESTER – Who is the internal business owner/requester? | GP | Free response (short) | Yes | Always | None |
| **PS13** | REQUESTER – Who is the internal business owner/requester? | PS | Free response (short) | Yes | Always | None |
| **SW16** | REQUESTER – Who is the internal business owner/requester? | SW | Free response (short) | Yes | Always | None |
| **GP20** | DEPARTMENT – Which department is this request for? | GP | Department picker (Ramp Department field) | Yes | Always | None |
| **PS14** | DEPARTMENT – Which department will be using this service? | PS | Department picker (Ramp Department field) | Yes | Always | None |
| **SW17** | DEPARTMENT – Which department will use this software? | SW | Department picker (Ramp Department field) | Yes | Always | None |

## 8. Contract and commercial terms

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **GP21** | PURCHASE METHOD – How will this purchase be made? | GP | Multiple choice (several answers) | Yes | Always | Approval; Shows GP22, GP23 |
| **PS15** | PURCHASE METHOD – How will this purchase be made? | PS | Multiple choice (one answer) | Yes | Always | Approval; Shows PS16, PS17 |
| **SW19** | PURCHASE METHOD – How will this software purchase be made? | SW | Multiple choice (several answers) | Yes | Always | Approval; Shows SW20, SW21 |
| **GP22** | CONTRACTS / DOCUMENTATION – Please upload all contracts and documents | GP | File upload | Yes | Shown if GP21 is "Signed Contract" | None |
| **PS16** | DOCUMENTATION – Please upload all related contracts and documents. | PS | File upload | Yes | Shown if PS15 is "Signed Contract" | None |
| **SW20** | CONTRACTS / DOCUMENTATION – Please upload all related contracts and documents. | SW | File upload | Yes | Shown if SW19 is "Signed Contract" | None |
| **GP23** | CONTRACTS / DOCUMENTATION – Include relevant links (such as terms or pricing) | GP | Link | Yes | Shown if GP21 is "Online click-through agreement" | None |
| **PS17** | SUPPORTING LINKS – Please provide any relevant online links related to this request. | PS | Link | Yes | Shown if PS15 is "Online click-through agreement" | None |
| **SW21** | CONTRACTS / DOCUMENTATION – Please provide any relevant online links related to this purc... | SW | Link | Yes | Shown if SW19 is "Online click-through agreement" | None |
| **GP24** | CONTRACTS / DOCUMENTATION- Include relevant links (such as terms or pricing) Continued | GP | Link | No | Always | None |
| **PS18** | SUPPORTING LINKS – Links Continued | PS | Link | No | Always | None |
| **SW22** | CONTRACTS / DOCUMENTATION – Links continued | SW | Link | No | Always | None |
| **GP25** | PAYMENT TERMS – What are the net payment terms? | GP | Number (Ramp Net payment terms field) | No | Always | None |
| **PS29** | PAYMENT TERMS – What are the net payment terms? | PS | Number (Ramp Net payment terms field) | No | Always | None |
| **SW37** | PAYMENT TERMS – What are the net payment terms? | SW | Number (Ramp Net payment terms field) | No | Always | None |

## 9. Security and compliance

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **SW23** | DATA USAGE – What type of data will be used, uploaded, or stored in this system? | SW | Free response (long) | Yes | Always | None |
| **PS20** | DATA ACCESS – Will this vendor require access to sensitive data, systems, or confidential company information? | PS | Yes/No (multi select) | Yes | Always | Approval; Shows PS26 |
| **SW24** | DATA ACCESS – Will this vendor require access to sensitive data, systems, or confidential company information? | SW | Yes/No (multi select) | Yes | Always | Approval; Shows SW25, SW31 |
| **PS19** | DATA ACCESS – Please briefly describe the type of access or data involved? | PS | Free response (long) | Yes | Always | None |
| **SW25** | DATA ACCESS – Please briefly describe the type of access or data involved? | SW | Free response (long) | Yes | Shown if SW24 is "Yes" | None |
| **PS21** | SYSTEM INTEGRATION – Will this vendor integrate with any MinIO systems? | PS | Yes/No (multi select) | Yes | Always | Approval; Shows PS22, PS25, PS26 |
| **SW26** | SYSTEM INTEGRATION – Will this vendor integrate with any MinIO systems? | SW | Yes/No (multi select) | Yes | Always | Approval; Shows SW27, SW30, SW31 |
| **PS22** | SYSTEM INTEGRATION – Please describe which MinIO systems the vendor will integrate with. | PS | Free response (long) | Yes | Shown if PS21 is "Yes" | None |
| **SW27** | SYSTEM INTEGRATION – Please describe which MinIO systems the vendor will integrate with | SW | Free response (long) | No | Shown if SW26 is "Yes" | None |
| **PS25** | SYSTEM INTEGRATION – Please describe the type of access, integration, or connection require... | PS | Free response (long) | Yes | Shown if PS21 is "Yes" | None |
| **SW30** | SYSTEM INTEGRATION – Please describe the type of access, integration, or connection require... | SW | Free response (long) | Yes | Shown if SW26 is "Yes" | None |
| **PS23** | THIRD-PARTY SERVICES – Does this vendor use any subcontractors or third-party service providers? | PS | Yes/No (multi select) | Yes | Always | Shows PS24 |
| **SW28** | THIRD-PARTY SERVICES – Does this vendor use any subcontractors or third-party service provider | SW | Yes/No (multi select) | Yes | Always | Shows SW29 |
| **PS24** | THIRD-PARTY SERVICES – If yes, please explain. | PS | Free response (long) | Yes | Shown if PS23 is "Yes" | None |
| **SW29** | THIRD-PARTY SERVICES – If yes, please explain | SW | Free response (long) | Yes | Shown if SW28 is "Yes" | None |
| **PS26** | SECURITY / COMPLIANCE – Does the vendor have a SOC 2 Type II report? | PS | Yes/No (multi select) | Yes | Shown if PS20 is "Yes" or PS21 is "Yes" | Approval; Shows PS27, PS28 |
| **SW31** | SECURITY / COMPLIANCE – Does the vendor have a SOC 2 Type II report? | SW | Yes/No (multi select) | Yes | Shown if SW24 is "Yes" or SW26 is "Yes" | Approval; Shows SW32, SW33 |
| **PS27** | SECURITY / COMPLIANCE –If Yes, Please upload the SOC 2 Type II  report | PS | File upload | Yes | Shown if PS26 is "Yes" | None |
| **SW32** | SECURITY / COMPLIANCE – If yes, please upload the SOC 2 Type II report | SW | File upload | Yes | Shown if SW31 is "Yes" | None |
| **PS28** | SECURITY / COMPLIANCE –If no, Please explain why | PS | Free response (long) | No | Shown if PS26 is "No" | None |
| **SW33** | SECURITY / COMPLIANCE – If no, please explain why | SW | Free response (long) | Yes | Shown if SW31 is "No" | None |
| **SW34** | IT/ SECURITY  - Will this vendor access, process, store, or integrate with MinIO systems, confide... | SW | Yes/No (multi select) | Yes | Always | None |

## 10. Software and IT

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **SW18** | USERS – Approximately how many users will need access to this software? | SW | Free response (short) | Yes | Always | None |
| **SW35** | AUTHENTICATION – Does this system support Single Sign-On (SSO)? | SW | Yes/No (multi select) | Yes | Always | Shows SW36 |
| **SW36** | AUTHENTICATION – Please specify which SSO providers are supported | SW | Free response (long) | Yes | Shown if SW35 is "Yes" | None |

## Other

| **ID** | **Question** | **Program** | **Response type** | **Required** | **Shown when** | **Dependency** |
|---|---|---|---|---|---|---|
| **GP16** | VENDOR RELATIONSHIP – What is the current status of our relationship with this vendor? | GP | Free response (long) | No | Shown if GP8 is any event type (any option except "Other") | None |
| **GP28** | APPROVAL NOTES – Add a message for approvers to review | GP | Free response (short) | No | Always | None |
| **PS32** | APPROVAL NOTES – Add a message for approvers to review | PS | Free response (long) | No | Always | None |
| **SW40** | APPROVAL NOTES – Add a message for approvers to review | SW | Free response (long) | No | Always | None |
