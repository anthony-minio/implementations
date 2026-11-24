# Purchase request questionnaire

Building a unified program questionnaire for purchase requests in Ramp: combine the multi-path intake into a single path, or fewer paths, with logical question flow and conditional question presentation.

## Asana

| Ticket | Name | Relation |
|---|---|---|
| FS-76 | Propose new intake question list and logic in Ramp | This project. https://app.asana.com/1/163565154279805/project/1219443754801875/task/1219908053038854 |
| FS-141 | Ramp modifcations following 11/9 meeting | Related. Sets the before spend approval matrix and PO routing the purchase request workflow has to follow. https://app.asana.com/1/163565154279805/project/1219443754801875/task/1220393082705369 |

Steps, from FS-76:

1. Capture questions posed in each path
2. Revise questions
3. Determine conditional gating
4. Determine any workflow updates needed
5. Demo
6. Launch

From FS-141, the parts that touch purchase requests (verbatim):

- Before spend workflows approval matrix
  - Sheng approves everything
  - Sheng + Jasmine >=$1,000 ($5,000 for purchase request)
  - Sheng + Jasmine + Garima >=$10,000
- Before spend workflows functional changes
  - Anything coded to benefits (check COA) goes to Tamara in addition to Susie (POs)
  - Anything coded to external recruiting / contingent workforce (check COA) goes to Erik Berg (POs)
  - IT spend should go to Mikey (should already but double check) (POs)

## Plan

Agreed with Anthony 2026-11-20.

| Group | Programs | Goal |
|---|---|---|
| A | General Procurement Request, Software / SaaS Purchase Request, Professional Services Purchase Request | Combine into one program if possible |
| Out of scope | Referral Partner Request | Excluded 2026-11-24: referral payouts should be handled a different way. Captured in `REFERRAL-PARTNER.md` for reference |
| Out of scope | PO from Signed Contracts, Confidential Procurement Request Form (was group B) | Dropped from scope 2026-11-24 |

Order of work:

1. Questions and program descriptions, for all programs in both groups. Starting with General Procurement Request.
   1. Capture every program first.
   2. Then discuss, across all of them: optimized question flow, question logic, optimizing the questions themselves, and anything else that comes up.
   3. Method (agreed 2026-11-24): group every question into high-level categories, then review the questions one by one, category by category. Open points such as the event questions and the SOC 2 description are settled in that review.
2. Approval workflows, after the questions are settled.

The final draft proposal also covers, for each program:

- Change order form questions (Ramp has a separate change order form per program)
- AI instructions (Ramp's "Guide how AI prefills requests from uploaded documents", up to 2,000 characters)

## Files

| File | Purpose |
|---|---|
| `PROGRAMS.md` | Current Ramp procurement programs: the paths being combined |
| `CATEGORIES.md` | Every in-scope question grouped into categories, with a proposed category flow. The working list for the review |
| `GENERAL-PROCUREMENT.md` | General Procurement Request as it is set up in Ramp today |
| `PROFESSIONAL-SERVICES.md` | Professional Services Purchase Request as it is set up in Ramp today |
| `SOFTWARE-SAAS.md` | Software / SaaS Purchase Request as it is set up in Ramp today |
| `REFERRAL-PARTNER.md` | Referral Partner Request as it is set up in Ramp today |
| `second-icon-explainer.png` | Shows the approval icon (left of the branch icon): the question is used in approval conditions |
| `screenshots/` | Source screenshots from Ramp, named `YYYYMMDD-<what>` |

## Status

Step 1 in progress. Program list captured 2026-11-20. General Procurement Request captured 2026-11-20. Professional Services Purchase Request captured 2026-11-23. Software / SaaS Purchase Request captured 2026-11-24. Referral Partner Request captured 2026-11-24. Group A capture complete. Questions grouped into categories 2026-11-24 (`CATEGORIES.md`); review next. Group B (PO from Signed Contracts, Confidential Procurement Request Form) not captured.

## Log

| Date | Change |
|---|---|
| 2026-11-20 | Project folder created |
| 2026-11-20 | Program list captured from Ramp (Procurement > Programs, All tab) |
| 2026-11-20 | Plan agreed: group A and group B, questions and descriptions before approval workflows |
| 2026-11-20 | Professional Services Purchase Request added to group A |
| 2026-11-20 | General Procurement Request: description, form settings and questions 1 to 5 captured |
| 2026-11-20 | General Procurement Request: questions 6 to 9 and the #6 condition captured, 10 to 12 seen blurred |
| 2026-11-20 | General Procurement Request: questions 10 to 12, #9 and #11 conditions captured |
| 2026-11-20 | General Procurement Request: questions 13 and 14, conditions on #12 to #14 captured |
| 2026-11-20 | General Procurement Request: questions 15 to 17 captured |
| 2026-11-20 | General Procurement Request: questions 18 to 22 captured |
| 2026-11-20 | General Procurement Request: questions 23 to 25, #22 and #23 conditions captured |
| 2026-11-20 | General Procurement Request: questions 26 to 28 and their conditions captured |
| 2026-11-20 | General Procurement Request: change order form and AI instructions captured, both empty. Both added to the final draft scope |
| 2026-11-21 | Professional Services Purchase Request: description, form settings and questions 1 to 5 captured |
| 2026-11-21 | Professional Services Purchase Request: questions 6 to 9 captured |
| 2026-11-21 | Professional Services Purchase Request: questions 10 to 14 captured |
| 2026-11-21 | Professional Services Purchase Request: questions 15 to 17 and their conditions captured |
| 2026-11-21 | Professional Services Purchase Request: questions 18 to 22 captured |
| 2026-11-21 | Professional Services Purchase Request: questions 23 to 25, #22 and #24 conditions captured |
| 2026-11-21 | Professional Services Purchase Request: questions 26 and 27, conditions on #25 to #27 captured |
| 2026-11-21 | Professional Services Purchase Request: questions 28 to 30 and their conditions captured |
| 2026-11-21 | Professional Services Purchase Request: questions 31 and 32 captured |
| 2026-11-23 | Professional Services Purchase Request: complete. #32 is the last question; change order form blank; no AI instructions |
| 2026-11-23 | Software / SaaS Purchase Request: description, form settings and questions 1 to 4 captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 5 to 8 captured (#7 condition only) |
| 2026-11-23 | Software / SaaS Purchase Request: #7 confirmed |
| 2026-11-23 | Software / SaaS Purchase Request: questions 9 to 13 captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 14 to 16, #13 and #14 conditions captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 17 to 20, #20 condition captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 21 to 24, #21 condition captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 25 to 27 and their conditions captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 28 to 30 and their conditions captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 31 to 33 (SOC 2), #31 and #32 conditions captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 34 to 36, #33 and #36 conditions captured |
| 2026-11-23 | Software / SaaS Purchase Request: questions 37 to 39 and their conditions captured |
| 2026-11-23 | Software / SaaS Purchase Request: question 40 captured |
| 2026-11-24 | Software / SaaS Purchase Request: complete. #40 is the last question; change order form blank; no AI instructions |
| 2026-11-24 | Referral Partner Request: description, form settings and questions 1 to 5 captured |
| 2026-11-24 | Referral Partner Request: questions 6 to 9, #7 condition captured |
| 2026-11-24 | Referral Partner Request: complete. 10 questions; change order form has 1 question; no AI instructions |
| 2026-11-24 | Scope: group B dropped; Referral Partner excluded. Review method agreed: categorise, then review one by one |
| 2026-11-24 | Approval icon identified (used in approval conditions). `CATEGORIES.md` added: 100 questions in 10 categories plus Other |
| 2026-11-24 | Ramp docs checked: no person picker, no submit-on-behalf for new requests; Boolean and Number types exist. Noted in `CATEGORIES.md` |
| 2026-11-24 | `CATEGORIES.md` de-duplicated: 100 questions come down to 49 distinct questions; full list kept as an appendix. Corrected: Ramp has a user picker question (Anthony's test) |
