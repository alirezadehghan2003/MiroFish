# Phase 4 · Management Approval Register

**Date:** 15 October 2026 · **Machine-readable:** `08-approval-register.csv` (fill in the decision, decided_by and date columns).

**Nothing listed here has been done.** Items marked *Research now* need no approval: they use public information only, involve no contact and cost nothing. Everything else needs an explicit decision from the named role.

## A. Can be researched now (no approval needed)

| ID | Item | What exactly | Status |
|---|---|---|---|
| RN01 | Repeat public website re-crawl and link check | Re-fetch public pages sequentially; re-run link and price checks | Ready |
| RN02 | Desk review of public regulator guidance | Read published CAP/ASA guidance on health and acupuncture claims and CQC display-of-ratings guidance (needs normal browser access; blocked here) | Blocked in this environment |
| RN03 | Public competitor website check | View competitors' public pages only; record prices with dates; no enquiries | Blocked in this environment |
| RN04 | Internal review of Phase 4 documents | Management reads the spec, tickets, draft copy and research kit | Ready |

## B. Requires explicit approval

| ID | Item | Approver (role) | Gate | External spend | Contacts people? | Changes live systems? | Blocked by / status |
|---|---|---|---|---|---|---|---|
| AP01 | Deploy website fixes T02, T03, T06, T07, T10 (T02,T03,T06,T07,T10) | Management (CEO/Founder) | G4 | Developer time (internal/agency) | No | Yes | Awaiting decision |
| AP02 | Clinical review of women's-health draft copy (T01) | Management; then clinicians | — | None | Yes (staff) | No | Awaiting decision |
| AP03 | Engage a CAP-code / advertising-compliance adviser (T01,R04) | Management (CEO/Finance) | — | Yes (quote needed) | Yes (external adviser) | No | Awaiting decision |
| AP04 | Deploy women's-health page replacement (T01) | Management after AP02+AP03+AP14 sign-offs | G4 | Developer time | No | Yes | Blocked by AP02, AP03 |
| AP05 | CQC register check by the registered manager (T05) | Management | — | None | Yes (staff) | No | Awaiting decision |
| AP06 | Publish CQC badge link and status line (T05) | Registered manager + Management | G4 | Developer time | No | Yes | Blocked by AP05 |
| AP07 | Grant read access to GTM, GA4, Search Console and Pabau reports (T09) | Management + data protection officer | G1 | None | Yes (agency/staff) | No (read-only) | Awaiting decision |
| AP08 | Implement tags and the consent banner change (T09) | Data protection officer + Management | G4 | Agency time; consent tool may have a fee | No | Yes | Blocked by AP07, AP14 |
| AP09 | Non-transactional booking-flow test on Pabau (T10,R09) | Management | G1 | None | Yes (staff) | No | Awaiting decision |
| AP10 | Usability tests with 5–6 non-clients (Research kit) | Management | G2 | £400–£600 (panel + incentives) | Yes (participants) | No | Awaiting decision |
| AP11 | Interviews with 8–12 clients and non-bookers (Research kit) | Management + data protection officer | G3 | £400–£600 incentives (+ optional transcription) | Yes (clients) | No | Awaiting decision |
| AP12 | Consultation credit policy (T08) | CEO + Finance | — | None | No | No | Awaiting decision |
| AP13 | Programme-tier decision (T04) | CEO + Medical Director | — | None | No | No | Awaiting decision |
| AP14 | Privacy and consent hygiene decisions (T11) | Data protection officer | — | None | No | Yes (after decision) | Awaiting decision |
| AP15 | Competitor enquiries / mystery shopping (R24) | Management | G5 | Possible | Yes (competitors) | No | Not requested |
| AP16 | Any paid media or new campaign (R04) | Management | — | Yes | No | No | On hold |
| AP17 | BigQuery export for Search Console/GA4 (T09) | Management | — | Possible | No | No | Optional |
| AP18 | Phone number and booking-rule decisions (T06,T10) | Operations lead + Management | — | None | No | No | Awaiting decision |

## C. Recommended decision order

1. **AP07** read-only access, **AP05** CQC check and **AP09** booking-flow test. These unblock verification at no external cost.
2. **AP12** credit policy, **AP13** programme tier, **AP18** phone number and booking rules. Management decisions, no spend.
3. **AP01** deploy the low-risk fixes (T02, T03, T06, T07, T10).
4. **AP02** clinical review and **AP03** compliance adviser (spend), then **AP04** deploy the women's-health pages.
5. **AP14** privacy decisions, then **AP08** tags and consent.
6. **AP10** usability tests and **AP11** interviews (≈ £800–£1,200 incentives and panel, plus contingency).

**Not recommended now:** AP15 (competitor contact), AP16 (paid media before the claims review).

| Gate | Meaning (from `../validation-plan.md`) |
|---|---|
| G1 | Staff booking-flow test; tagging access |
| G2 | Recruiting non-client participants; incentive spend |
| G3 | The HVN contacting clients/enquirers; DPIA |
| G4 | Any website deployment or live test |
| G5 | Any competitor enquiry |
