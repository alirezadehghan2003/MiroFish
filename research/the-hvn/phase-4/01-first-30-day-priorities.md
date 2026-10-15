# Phase 4 · First-30-Day Priority Selection

**Date:** 15 October 2026 · **Source of truth:** `../recommendations-register.md` (24 recommendations), updated with the Phase 4 re-checks (`02-booking-journey-audit.md`, `evidence/`).

## 1. Selection rules
A recommendation enters the first 30 days only if it meets all of these:
1. **Evidence is verified** on the live site (confidence High), or the action *is* the verification.
2. **It doesn't depend on customer validation** (that comes later).
3. **Effort is small or medium**, and the change is **reversible**.
4. **It reduces risk or removes a dead end**, or it is a **precondition for measuring** anything else.

## 2. Scoring of all 24 recommendations

| ID | Recommendation | Verified? | Needs validation first? | Effort | Risk reduction / precondition | **First 30 days?** |
|---|---|---|---|---|---|---|
| R01 | Fix Menopause/PCOS/PMDD pages | Yes, re-checked today; booking button also uses the aesthetic category (B1) | No | S | High (credibility, compliance) | **Yes → T01** |
| R02 | Repair broken navigation and links | Yes: 27 URLs re-checked, all 404 | No | S | Medium | **Yes → T02, T03** |
| R03 | Decide programme tier; redirect retired URLs | Yes (8 retired URLs 404) | No | M (decision) | Medium | **Yes → T04** (decision + redirects) |
| R04 | CAP-code claims review | Yes (+ new: PCOS/PMDD name prescription medicines; "particularly effective" acupuncture claims) | No | M (external) | High | **Yes, commission** (needs spend approval) |
| R05 | Verify CQC; link badge; status line | Badge unlinked (verified); status unknown | No | S | High | **Yes → T05** (verification first; `07-cqc-verification-checklist.md`) |
| R06 | One number; tap-to-call; mobile bar | Yes (tel: on home only) | No | S | Medium | **Yes → T06** |
| R07 | Analytics and funnel baseline | GTM ID present; GA4 and consent unverified | No | M | **Precondition** | **Yes → T09** (`03-measurement-spec.md`) |
| R08 | Fees and credits table | Yes | No (policy decision) | S | Medium | **Yes → T08** |
| R09 | Cancellation charge at booking | Terms verified (100%); booking screen unknown | No | S | Medium | **Research only:** booking test (G1); change later |
| R10 | Price conflicts; course sessions | Yes, and clarified (see T07) | No | S | Medium | **Yes → T07** |
| R11 | Pathway price ranges | Gap verified; effect unknown | **Yes** (H01, H02) | M | — | No: days 31–60 |
| R12 | First-year examples | — | Yes | S | — | No |
| R13 | "Who will treat me" | Yes | Partly (H04) | M | Medium | No: days 31–60 (start content gathering) |
| R14 | IV explainer | Yes | No, but after R04 | S | Medium | No: after the claims review |
| R15 | Proposition and titles | Yes | Yes (H06, H07, H13) | S | Low | **Partial:** only the factual title fix ("Skin & Hair" on Contact/Booking) → T10 |
| R16 | No-membership messaging test | — | Yes | S | — | No |
| R17 | Women's-health hub | Partly | Yes (H08) | M | — | No |
| R18 | Structured data | Yes | No | S | Low | No: days 31–60 |
| R19 | Speed-to-lead measurement | Unknown | No | S | Precondition | **Yes (measurement only):** enquiry log in T09 |
| R20 | Written consultation plan | Unknown | Check practice first | M | — | No |
| R21 | Review rating | Unknown | No | S | Low | No: days 31–60 |
| R22 | Mobile performance | Partly (headless browser blocked) | No | M | Low | No: needs a real-device test |
| R23 | Starter pathway | — | Yes | L | — | No (gated) |
| R24 | Quarterly competitor check | — | No | S | Low | No: days 61–90 |

**New from Phase 4** (not in the original 24):
- **N1 · Booking-route consistency** (B1–B3, B5, B8): IV online vs form, two package routes, women's-health button category, "Skin & Hair" titles → **T10**.
- **N2 · Privacy and consent hygiene** (B6; measurement §2): consent banner not found in static HTML; controller name mismatch; malformed cookie-policy link; enquiry forms without a privacy field → **T11** (privacy owner review, no copy changes until signed off).

## 3. The first-30-day action set

| Order | Ticket | Action | Can start now (research/preparation) | Needs explicit approval to implement |
|---|---|---|---|---|
| 1 | T05 | CQC verification (checklist) | Prepared checklist | Staff time for the check; any wording change on the site |
| 2 | T09 | Measurement baseline (GTM/GA4/consent check, enquiry log, booking-platform questions) | Spec, event dictionary, page mapping | Access to GTM/GA4/Pabau; any tag deployment; consent-banner change |
| 3 | T01 | Women's-health pages | Draft copy (`06-draft-copy-womens-health.md`) | Clinical sign-off; compliance sign-off; deployment |
| 4 | T02, T03 | Broken menu and internal links | Exact URL lists | Deployment |
| 5 | T06 | Phone and tap-to-call | Spec | Choice of number; deployment |
| 6 | T07 | Price consistency | Exact conflicts | Price owner sign-off; deployment |
| 7 | T08 | Fees and credits table | Draft table structure | Credit-policy decision; deployment |
| 8 | T04 | Programme decision and redirects | URL list | Management decision; deployment |
| 9 | T10 | Booking-route consistency and titles | Findings + booking-test script | Booking-system answers; deployment |
| 10 | T11 | Privacy and consent hygiene | Issue list | Data protection officer review; deployment |
| — | R04 | Claims review | Brief contents (in T01, T11) | **External spend** |
| — | Research kit | Usability tests and interviews | Full kit in `04-research-kit/` | G2/G3: recruitment, incentives, contacting anyone |
