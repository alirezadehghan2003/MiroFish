# The HVN: Real-World Validation Plan

**Version:** 1.0, 15 October 2026 · **Status:** design only. **Nothing in this plan has started.** No client, enquirer, competitor or research participant has been contacted. Every step that involves people, or changes the website or booking system, needs your approval first (gates G1–G3).

## 1. Principles

1. **Simulated agents are not customers.** The MiroFish runs produced *hypotheses about what to ask*, not evidence about what clients think. They are never counted as respondents, never quoted as customer views, and never mixed with real data.
2. **Learn from the simulation's main flaw: leading questions.** S2a's opening post asked "Would you pay a consultation fee just to find out the total?", and most agents echoed it (`report-audit.md` D1). Real interviews must use **open, neutral questions first**, with specific probes only afterwards.
3. **Measure before changing.** The analytics baseline (R07) runs before, or alongside, the first fixes so effects can be seen.
4. **Small and cheap.** About 6 weeks, **about £1,000–£1,800 external spend** plus about 8–10 staff days.
5. **Privacy and ethics.** Recruitment is done by The HVN under UK GDPR with a lawful basis and explicit consent. No clinical details are recorded unless needed. Recordings only with consent. Incentives are neutral (gift card or charity donation), never treatment credit, which would bias answers. Complete a DPIA screening before interviews.

## 2. Hypotheses to validate

**Source** names the simulation run or evidence. **Prior** is today's confidence: H = high, M = medium, L = low.

| ID | Hypothesis | Source | Prior | Method(s) | Supported if… | Refuted if… | Drives |
|---|---|---|---|---|---|---|---|
| **H01** | Not knowing the total cost of a plan stops prospective clients booking a paid consultation | S1 run 2, S2a (primed), S2b; verified gap | M (gap) / L (reaction) | Interviews (lapsed enquirers), usability task 2, enquiry log | ≥ 4 of 8–12 interviewees raise total cost **unprompted** as a barrier; "price/total" is a top-3 enquiry tag | Cost is rarely raised unprompted; clients expect to learn it in consultation | R11, R12 |
| **H02** | A published **range** is enough; an exact quote isn't needed | S2a A2 | L | Interviews (probe), usability (show range vs none) | Most participants say a range would let them book | Ranges are seen as bait or ignored | R11 |
| **H03** | Unclear fee-credit rules deter booking | S1 run 2, S2a, S2b; verified gap | M | Enquiry log ("credit" tag), interviews | Credit questions are frequent; interviewees misread the rules | Rarely asked; not a factor | R08 |
| **H04** | Naming the clinician for each treatment increases trust and booking intent | All 5 full runs; verified gap | M | Usability (A/B mock-up), interviews | Participants prefer, and recall, a named clinician; intent rises in the mock-up | No difference | R13 |
| **H05** | Prospects look at CQC status; "not yet rated" (if true) deters some | S1 run 2, S3, S4 (primed); **status unverified** | L | **First verify status (R05)**; then interviews and usability | Participants look for and act on the status | Nobody looks; badge is ignored | R05 |
| **H06** | "No membership / pay as you go" is a positive differentiator vs clubs | S4 10/11 (primed) | L | Interviews (neutral comparison), later copy A/B (gated) | Most see it as freedom or value | Most read it as "less exclusive", or don't care | R16, R15 |
| **H07** | Unsupported superlatives lower credibility; concrete safeguards (e.g. the doctor's 10-minute IV check) raise it | S3 | L–M | Usability: compare two hero versions (mock-ups only) | Concrete version rated more credible | No difference | R15, R14 |
| **H08** | Single-need women's-health and fertility clients prefer specialists, but an integrated doctor-led route can win once the pages are fixed | S4 (drift-affected); verified W1 | L | Search Console (demand), interviews with women's-health clients | Demand exists; clients value coordination | Low demand, or a strong specialist preference | R17 |
| **H09** | Card-on-file and 24 h cancellation are acceptable if the £ charge is shown | S2a A3, S2b B4 | L | Internal booking test, Pabau abandonment data | Abandonment at the card step falls after the change | No change | R09 |
| **H10** | A same-day response converts time-poor enquirers | S2a A7 (single run) | L | Enquiry log: response time vs booking | Faster replies book more often | No relationship | R19 |
| **H11** | A priced starter pathway would convert hesitant buyers, if follow-on costs are shown | S2b (hypothetical; thin) | L | Interviews (concept test), only after H01–H02 | Clear interest, with acceptable price and terms | Little interest; cannibalisation risk | R23 |
| **H12** | Gatekeepers (PAs, family offices) need a documentation pack: registration, CQC, insurance, terms | S1 run 2, S4 | L | 2–3 interviews with gatekeepers (if The HVN has them) | They ask for these items | Not needed | R05, R13 |
| **H13** | Atmosphere and luxury cues matter less than verifiability | S1 run 2 (model bias likely) | L | Interviews: ask what made them choose The HVN | Verifiability dominates | Setting and experience dominate (the simulation's cautious voice misled us) | R15 positioning |

## 3. Workstreams

### A. Analytics baseline (no participants; start immediately after approval)
- **What:**
  - GA4 events: `book_click`, `tel_click`, `whatsapp_click`, `form_submit`, `price_section_view`;
  - a 404 tracking view;
  - Search Console page groups (concerns, service lines, women's health);
  - Pabau reports: bookings by service and source, consultation-to-plan within 30 days, cancellations and no-shows, 90-day repeats;
  - an enquiry log with reason tags (price/total, credit, practitioner, CQC/safety, availability, other) and first-response time.
- **Who:** marketing lead + analytics agency; operations lead for Pabau and the log.
- **Cost:** staff time only (about 3–5 days); Looker Studio is free.
- **Output:** a baseline dashboard for the KPIs in `customer-journey-map.md` §5. Tests H01, H03 and H10 (enquiry log) and H08 (demand).

### B. Internal booking-flow test (no customers; gate G1)
- **What:** two staff run the Pabau journey on mobile and desktop for (a) the £350 Discovery Consultation and (b) an NAD infusion, **stopping before payment**. Record steps, fields, deposit and cancellation wording, and screenshots.
- **Cost:** about half a day.
- **Tests:** H09; feeds R09.

### C. Moderated usability tests: 5–6 **non-client** participants (gate G2)
- **Recruit:** a UK research panel, screened for London residents aged 30–60 who have paid for private health or aesthetic services in the last 2 years. Mix: 2 women's health, 2 aesthetics, 2 executive/longevity.
- **Format:** 45 min, remote, phone screen-share, think-aloud, **on the live site only, no booking or payment**. Optional: two static mock-ups (named clinician; price range).
- **Tasks:**
  1. "You've been feeling exhausted for months. Find out whether The HVN could help and what you'd do first."
  2. "Find out roughly what that would cost you over three months."
  3. "Find out who would treat you and whether the clinic is regulated."
  4. "You're perimenopausal. Find relevant support."
  5. "Contact the clinic from your phone."
- **Measures:** task success, time, errors, confidence (1–5), and verbatim quotes.
- **Cost:** about £60–£100 per participant (panel fee plus incentive), so **£400–£600** in total.
- **Tests:** H01, H02, H04, H05, H07.

### D. Client and enquirer interviews: 8–12 people (gate G3)
- **Recruit (by The HVN, with consent):**
  - 4–6 recent clients across segments;
  - 3–4 recent enquirers who didn't book (from the enquiry log or Pabau);
  - 1–2 gatekeepers, if any.
- **Format:** 30 min by video or phone; neutral £50 gift card or a charity donation.
- **Cost:** **£400–£600** incentives, plus optional transcription of about £100.
- **Guide (open questions first, then probes):**
  1. "Tell me about the last time you looked for help with [need]. What started it?"
  2. "How did you decide where to go? What did you look at?" (Don't mention price, CQC or membership.)
  3. "What, if anything, nearly stopped you booking, or did stop you?"
  4. "What did you expect the first appointment to give you?"
  5. "After the first appointment, how did you decide what to do next?"
  6. **Probes, only after the open questions:**
     - total cost and ranges;
     - fee credits;
     - who treats you;
     - regulation;
     - membership vs pay as you go;
     - the setting.
  7. Show two short hero statements (current vs a concrete, doctor-led version): "Which is more believable, and why?"
- **Tests:** H01–H08, H11–H13.

### E. Copy or page tests after fixes (gate G4, later)
Only after the claims review (R04) and your approval:
- a hero or proposition A/B test, or a pre/post comparison on pages changed by R01, R11 and R13;
- primary metric: booking intent rate;
- **minimum run:** 4 weeks, or until each variant has enough booking-intent events to see a meaningful difference.

## 4. Timeline and budget

| Week | A Analytics | B Booking test | C Usability | D Interviews | Decisions |
|---|---|---|---|---|---|
| 1 | Set up events and enquiry log | Run test | Screener and panel booking | Consent materials, DPIA screen | G1 approval |
| 2 | Baseline | — | 5–6 sessions | Recruitment by The HVN | G2 / G3 approvals |
| 3 | Baseline | — | Synthesis | 4–6 interviews | — |
| 4 | Baseline complete | — | — | 4–6 interviews | — |
| 5 | Monitor fixes (R01, R02, R06, R10) | — | — | Synthesis | Hypothesis read-out |
| 6 | Report | — | — | — | Go / no-go on R11, R15, R16, R17, R23 |

| Item | Estimate |
|---|---|
| Usability panel and incentives (5–6) | £400–£600 |
| Interview incentives (8–12 × £50) | £400–£600 |
| Transcription (optional) | £0–£200 |
| Contingency | £200–£400 |
| **External total** | **≈ £1,000–£1,800** |
| Staff time | ≈ 8–10 days across marketing, operations and the medical director |

Estimates are indicative; confirm panel quotes before G2.

## 5. Decision rules: how results change the plan

| If… | Then… |
|---|---|
| H01 and H02 are supported | Publish ranges (R11) and first-year examples (R12); consider R23 |
| H01 is refuted | Keep entry prices; invest in the consultation experience (R20) instead of ranges |
| H04 is supported | Prioritise R13 across all service pages |
| H06 is supported | Use "no membership" in the proposition (R15/R16) |
| H06 is refuted | Drop it from headlines; keep it as a factual line in FAQs |
| H08 is supported | Build the women's-health hub (R17) |
| H13 is refuted (setting matters most) | Rebalance the positioning towards experience; treat simulation-derived trust messages with more caution |
| CQC status (R05) shows "not yet rated" | Use a plain, accurate status line; feature the rating once issued |
| CQC status shows a rating | Feature it prominently and update H05 |

## 6. Approval gates

| Gate | Needs your approval for | Before |
|---|---|---|
| **G1** | Staff running the booking-flow test (no payment); GA4 / tag changes on the live site | Workstreams A–B |
| **G2** | Recruiting non-client panel participants; incentive spend | Workstream C |
| **G3** | The HVN contacting clients and enquirers; consent wording; DPIA | Workstream D |
| **G4** | Any live A/B or copy test; any website deployment | Workstream E and all website recommendations |
| **G5** | Any competitor enquiry or mystery shop | `competitor-benchmark.md` §6 |
