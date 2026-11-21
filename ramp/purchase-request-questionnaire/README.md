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
| A | General Procurement Request, Software / SaaS Purchase Request, Referral Partner Request, Professional Services Purchase Request | Combine into one program if possible |
| B | PO from Signed Contracts, Confidential Procurement Request Form | Compare what each does, then decide whether they can be combined |

Order of work:

1. Questions and program descriptions, for all programs in both groups. Starting with General Procurement Request.
   1. Capture every program first.
   2. Then discuss, across all of them: optimized question flow, question logic, optimizing the questions themselves, and anything else that comes up.
2. Approval workflows, after the questions are settled.

The final draft proposal also covers, for each program:

- Change order form questions (Ramp has a separate change order form per program)
- AI instructions (Ramp's "Guide how AI prefills requests from uploaded documents", up to 2,000 characters)

## Files

| File | Purpose |
|---|---|
| `PROGRAMS.md` | Current Ramp procurement programs: the paths being combined |
| `GENERAL-PROCUREMENT.md` | General Procurement Request as it is set up in Ramp today |
| `PROFESSIONAL-SERVICES.md` | Professional Services Purchase Request as it is set up in Ramp today |
| `screenshots/` | Source screenshots from Ramp, named `YYYYMMDD-<what>` |

## Status

Step 1 in progress. Program list captured 2026-11-20. General Procurement Request captured 2026-11-20. Professional Services Purchase Request in progress.

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
