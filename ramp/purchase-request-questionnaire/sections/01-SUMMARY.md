# Summary

Program codes: **GP** General Procurement (28 questions), **PS** Professional Services (32), **SW** Software / SaaS (40). The 100 questions in Ramp today come down to 49 distinct questions. **Approval** marks a question Ramp uses in approval conditions.

## Categories

| **#** | **Category** | **Distinct questions** | **In Ramp today** | **Programs** |
|---|---|---|---|---|
| **1** | Request basics | 3 | 9 | All three |
| **2** | Request type | 3 | 3 | GP, SW |
| **3** | Vendor and negotiations | 5 | 15 | All three |
| **4** | Business need and impact | 5 | 11 | All three |
| **5** | Alternatives and existing tools | 4 | 4 | SW |
| **6** | Revenue and GTM | 4 | 5 | GP, PS |
| **7** | Owner, department and timing | 3 | 9 | All three |
| **8** | Contract and commercial terms | 5 | 15 | All three |
| **9** | Security and compliance | 12 | 22 | PS, SW |
| **10** | Software and IT | 3 | 3 | SW |
| **Other** | Other | 2 | 4 | All three |

## Distinct questions

| **ID** | **Question** | **Programs** | **Asked in** | **Response type** | **Dependency** |
|---|---|---|---|---|---|
| **1. Request basics** | | | | | |
| **D1.1** | Give this request a name | All three | GP1, PS1, SW1 | Free response | None |
| **D1.2** | Is it one-time or recurring? (Frequency) | All three | GP2, PS2, SW2 | Multiple choice | None |
| **D1.3** | What is the spend amount? (Amount) | All three | GP3, PS3, SW3 | Number | None |
| **2. Request type** | | | | | |
| **D2.1** | What best describes this request? (event types plus Other) | GP | GP8 | Multiple choice | Shows D2.2, D4.4, D6.1, D6.2, D6.3, D6.4, DO.1 |
| **D2.2** | If other, please explain | GP | GP9 | Free response; conditional | None |
| **D2.3** | What type of request is this? (new, renewal, amendment, trial or pilot) | SW | SW4 | Multiple choice | Shows D5.3 |
| **3. Vendor and negotiations** | | | | | |
| **D3.1** | Specify the vendor for this request | All three | GP4, PS4, SW5 | Vendor picker | Shows D3.4, D3.5 |
| **D3.2** | Have you already engaged in discussions or negotiations with the vendor? | All three | GP5, PS5, SW6 | Yes/No | Shows D3.3 |
| **D3.3** | If yes, provide justification and describe what was discussed or negotiated | All three | GP6, PS6, SW7 | Free response; conditional | None |
| **D3.4** | Vendor contact (new vendor) | All three | GP26, PS30, SW38 | Contact; conditional | None |
| **D3.5** | Vendor address (new vendor) | All three | GP27, PS31, SW39 | Address; conditional | None |
| **4. Business need and impact** | | | | | |
| **D4.1** | Describe the goods or services being requested | GP, PS | GP17, PS7 | Free response | None |
| **D4.2** | Describe the business purpose / need | All three | GP7, PS8, SW8, SW9 | Free response | None |
| **D4.3** | What is the primary expected outcome? (list) | GP | GP10 | Multiple choice | Shows D6.2 |
| **D4.4** | What is the expected business impact? | All three | GP11, PS10, SW10 | Free response; conditional in GP | None |
| **D4.5** | How will success be measured? | PS | PS11 | Free response | None |
| **5. Alternatives and existing tools** | | | | | |
| **D5.1** | Is this replacing an existing tool or adding a new capability? | SW | SW11 | Free response | None |
| **D5.2** | What alternative tools (including existing internal tools) were considered? | SW | SW12 | Free response | None |
| **D5.3** | Have you checked if we already have an existing tool or service that meets this need? | SW | SW13 | Yes/No; conditional | Shows D5.4 |
| **D5.4** | If yes, explain why a new tool or service is still required | SW | SW14 | Free response; conditional | None |
| **6. Revenue and GTM** | | | | | |
| **D6.1** | What pipeline impact is expected (net-new, expansion, or renewal)? | GP | GP12 | Free response; conditional | None |
| **D6.2** | Expected ROI / pipeline impact | GP | GP13 | Free response; conditional | None |
| **D6.3** | Which priority customers or target accounts are expected... | GP, PS | GP14, PS9 | Free response; conditional in GP | None |
| **D6.4** | How does this request support current GTM priorities or revenue objectives? | GP | GP15 | Free response; conditional | None |
| **7. Owner, department and timing** | | | | | |
| **D7.1** | Is there a target date or deadline by which this purchase needs to be completed? | All three | GP18, PS12, SW15 | Date | None |
| **D7.2** | Who is the internal business owner/requester? | All three | GP19, PS13, SW16 | Free response | None |
| **D7.3** | Which department is this request for? | All three | GP20, PS14, SW17 | Department picker | None |
| **8. Contract and commercial terms** | | | | | |
| **D8.1** | How will this purchase be made? (Purchase method) | All three | GP21, PS15, SW19 | Multiple choice | Approval; Shows D8.2, D8.3 |
| **D8.2** | Please upload all related contracts and documents | All three | GP22, PS16, SW20 | File upload; conditional | None |
| **D8.3** | Provide any relevant online links (terms, pricing, DPA...) | All three | GP23, PS17, SW21 | Link; conditional | None |
| **D8.4** | Links continued | All three | GP24, PS18, SW22 | Link | None |
| **D8.5** | What are the net payment terms? | All three | GP25, PS29, SW37 | Number | None |
| **9. Security and compliance** | | | | | |
| **D9.1** | What type of data will be used, uploaded, or stored in this system? | SW | SW23 | Free response | None |
| **D9.2** | Will this vendor require access to sensitive data, systems, or confidential company information? | PS, SW | PS20, SW24 | Yes/No | Approval; Shows D9.3, D9.9 |
| **D9.3** | Please briefly describe the type of access or data involved | PS, SW | PS19, SW25 | Free response; conditional in SW | None |
| **D9.4** | Will this vendor integrate with any MinIO systems? | PS, SW | PS21, SW26 | Yes/No | Approval; Shows D9.5, D9.6, D9.9 |
| **D9.5** | Please describe which MinIO systems the vendor will integrate with | PS, SW | PS22, SW27 | Free response; conditional | None |
| **D9.6** | Please describe the type of access, integration, or connection required | PS, SW | PS25, SW30 | Free response; conditional | None |
| **D9.7** | Does this vendor use any subcontractors or third-party service providers? | PS, SW | PS23, SW28 | Yes/No | Shows D9.8 |
| **D9.8** | If yes, please explain (subcontractors) | PS, SW | PS24, SW29 | Free response; conditional | None |
| **D9.9** | Does the vendor have a SOC 2 Type II report? | PS, SW | PS26, SW31 | Yes/No; conditional | Approval; Shows D9.10, D9.11 |
| **D9.10** | If yes, please upload the SOC 2 Type II report | PS, SW | PS27, SW32 | File upload; conditional | None |
| **D9.11** | If no, please explain why (SOC 2) | PS, SW | PS28, SW33 | Free response; conditional | None |
| **D9.12** | Will this vendor access, process, store, or integrate with MinIO systems, confide... | SW | SW34 | Yes/No | None |
| **10. Software and IT** | | | | | |
| **D10.1** | Approximately how many users will need access to this software? | SW | SW18 | Free response | None |
| **D10.2** | Does this system support Single Sign-On (SSO)? | SW | SW35 | Yes/No | Shows D10.3 |
| **D10.3** | Please specify which SSO providers are supported | SW | SW36 | Free response; conditional | None |
| **Other** | | | | | |
| **DO.1** | What is the current status of our relationship with this vendor? | GP | GP16 | Free response; conditional | None |
| **DO.2** | Add a message for approvers to review | All three | GP28, PS32, SW40 | Free response | None |
