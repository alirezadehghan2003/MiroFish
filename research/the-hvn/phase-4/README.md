# Phase 4: Real-World Validation and Implementation Readiness

**Date:** 15 October 2026 · **Source of truth:** the files in `research/the-hvn/` (report v2.0, recommendations register, roadmap, validation plan).
**Constraints honoured:**
- no MiroFish simulations and no paid Anthropic API calls;
- no website changes deployed;
- no clients, competitors or staff contacted;
- no patient data accessed;
- no bookings, payments or form submissions;
- no external spend.

## Files

| # | File | What it is |
|---|---|---|
| 01 | `01-first-30-day-priorities.md` | All 24 recommendations scored; the first-30-day action set (10 tickets + claims review + research) |
| 02 | `02-booking-journey-audit.md` | Non-transactional audit of the website side of booking; what was blocked; staff test script for the booking platform |
| 03 | `03-measurement-spec.md` + `measurement/` | GA4, Search Console and booking-system specification: 18 events, 7 funnels, KPI catalogue, data requests, QA; draft page-group mapping for 216 URLs |
| 04 | `04-research-kit/` | Usability protocol (5–6), interview guide (8–12), recruitment and screener, consent and privacy, research questions, observed-vs-opinion method, 8 CSV templates |
| 05 | `05-implementation-tickets.md` + `tickets.csv` | 11 implementation-ready tickets with exact URLs, evidence, change, role, acceptance criteria, QA, success metric |
| 06 | `06-draft-copy-womens-health.md` | **DRAFT, not for publication:** replacement copy for Menopause, PCOS and PMDD, pending clinical and compliance approval |
| 07 | `07-cqc-verification-checklist.md` | Checklist to establish the actual CQC facts (status not assumed) |
| 08 | `08-approval-register.md` + `.csv` | 4 research-now items and 18 approval items, with approver, gate, spend and contact flags |
| 09 | `09-execution-dashboard.html` + `09-dashboard-data.json` | Phase 4 tracker: status, dependencies, confidence, responsible roles, next decision |
| — | `evidence/` | `site-recheck-2026-10-15.json` (30 pages) and `broken-links-recheck.csv` (27 URLs) |

## Verified today (public website only)
- 30 key pages fetched (all HTTP 200).
- **All 27 previously broken or retired URLs still return 404.**
- Menopause, PCOS and PMDD still list acne treatments. Their booking buttons use Pabau `category=194249`, **the same as the Aesthetic Consultation button**. What that opens is unverified.
- PCOS and PMDD copy names prescription medicines (metformin, SSRIs, contraceptive pills): a compliance flag.
- Tap-to-call appears only on the home page in the sample.
- **IV booking instructions conflict:** IV pages link to Pabau, while `/book-now/` says to use the contact form.
- Acupuncture packages have two purchase routes.
- Terms: card required; **100%** charge for under-24-hour cancellations and no-shows; cancellations only by phone or the booking platform; 18+ only.
- GTM container `GTM-N7X2W4QF` is referenced. No GA4 ID and no consent banner appear in the static HTML. A Search Console verification meta tag is present.
- Privacy policy: controller named "The HVN Wellness Limited" (the site says "Wellbeing Ltd"); malformed cookie-policy link.
- Clarified: £1,620 acupuncture course = 6 × £270. Blood profiles state 33 / 48 / 56 markers. Earlier docs said "50+ / 60+"; corrected in `../dossier.md` and `../personas.md`.

## Blocked (documented, not worked around)

| System | Result |
|---|---|
| Pabau booking platform | Blocked by the network proxy |
| Headless browser on the-hvn.com | Refused by bot protection, so no rendered mobile or desktop screens |
| googletagmanager.com, cqc.org.uk, competitor sites | Blocked |
| GA4, Search Console, Pabau reports | No access granted |

## Approvals needed to start implementation
See `08-approval-register.md`. In order:

1. **AP07:** read-only access to GTM, GA4, Search Console and Pabau reports.
2. **AP05:** CQC register check by the registered manager.
3. **AP09:** staff walk-through of the booking platform (no booking or payment).
4. **AP12 / AP13 / AP18:** decisions on credit policy, programme tier, phone number and booking rules.
5. **AP01:** deploy low-risk fixes T02, T03, T06 and T07.
6. **AP02 + AP03 → AP04:** clinical review and compliance adviser (spend), then deploy the women's-health pages.
7. **AP14 → AP08:** data protection officer decisions, then tagging and consent.
8. **AP10, AP11:** usability tests and interviews (≈ £800–£1,200 plus contingency).
