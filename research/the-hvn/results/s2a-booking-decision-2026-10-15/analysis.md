# S2a Booking Decision (current offer): Evidence-Checked Analysis

**Run:** 15 Oct 2026 · Reddit mode · `claude-haiku-5-5` only · 11 invented agents · 24/24 rounds (round 1 = 09:00) · English · graph memory off · native report skipped · graph `mirofish_e2321b595fb24b06`
**Activity:** 11/11 agents authored content · 4 new posts + 45 comments (42 replies) · 49 meaningful items · 43 likes · 11 interviews
**Cost:** $0.127 (87 requests, 0 errors) · full metrics in `run-metrics.json` · verbatim thread in `thread.md` (IDs below: P = post, C = comment)

> **[SIMULATED]** = said by LLM agents; hypotheses, not customer evidence. **[VERIFIED]** = live-site crawl or Phase 0 evidence (15 Oct 2026). **[NEEDS TESTING]** = unconfirmed.

## Simulated insights, with evidence checks

| # | Insight [SIMULATED] | Trace | Evidence check | Verdict |
|---|---|---|---|---|
| A1 | **"I won't pay a consultation fee just to find out the total."** 7 of 11 agents said this almost verbatim in reply to the entry-point question. | C7, C9, C11, C12, C13, C23, C41 | Programme prices other than 8R "from £3,000" are not published; old programme pages 404 **[VERIFIED]** | **Strong.** Core conversion barrier hypothesis |
| A2 | **A written range is enough; exact figures are not required.** "It doesn't need to be exact, but a range in writing…" (Emma); "A range in writing would be enough for me to decide" (Daniel). | C28, C44, C21 | — | **Actionable.** Publish indicative ranges per pathway |
| A3 | **Card before explanation feels like club admission.** Card-on-file and 24-hour cancellation are acceptable *only if* the total is clear first (Helena: "a rough total in writing before any card is taken is a dealbreaker"). | P3 (11 likes), C38, C8, C42; Natalie interview | Card required to confirm; 24 h notice **[VERIFIED: /terms-of-service/]** | **Supported** |
| A4 | **Fee-credit rules matter**: whether the first consultation fee is credited against later spend. Raised in most replies. | C5, C7, C12, C17, C20, C23 | Credit wording only on the £350 Discovery page (£100); none on £175 or £400 pages **[VERIFIED: crawl]** | **Supported** (repeats S1 run 2) |
| A5 | **Course totals for fertility and hormonal acupuncture.** Priya (mid-IVF) won't put a card on file without the course total; 6 agents answered with the same request. | P4, C2, C6, C14, C18, C24, C30 | **Correction:** course pricing "from £1,620" **is published** on the fertility page and 5 other acupuncture pages **[VERIFIED]**, but it was **omitted from the S2 briefing**, so this complaint partly reflects the seed, not the site. Session count per course **[NEEDS TESTING]** | **Partly an artefact.** Still useful: put course price and session count where buyers decide |
| A6 | **Named clinician and registration before booking**; exclusions listed alongside inclusions. | C40, P8 checklist | Same site-wide practitioner block on every page **[VERIFIED]** | **Supported** (repeats S1 run 2) |
| A7 | **Speed trigger**: "I'd book… only if a doctor calls back the same day" (Helena). | Helena interview, C43 | Concierge contact model **[VERIFIED]**; response time **[NEEDS TESTING]** | **Hypothesis.** Test with a mystery shop |
| A8 | **Per-session with a clear plan beats a large upfront package** for cautious buyers. | C36 (Claire), C33 | No membership; programmes unpriced **[VERIFIED]** | **Hypothesis** |
| A9 | **Atmosphere and being listened to drive return visits** for the holistic persona; "a written outline… feels like a kind of respect". | P5 (6 likes), C4, C35 | — | **Hypothesis** (segment-specific) |
| A10 | **Sticker shock from summing the ladder**: one agent added every published item to a "visible floor" of £2,675 (plus 8R ≥ £3,000). | C23, C41 | Arithmetic correct for the items listed **[VERIFIED]**, but no client would buy everything | **Weak signal.** Without pathways, visitors build worst-case totals |

## Data-quality notes
- **Stereotyped voice:** Khalid's posts open with "As-salamu alaykum" and close with "Inshallah" (C1, C15, C16). The persona brief asked for none of this; it is a model bias and is excluded from interpretation.
- **Memory loss in interviews:** 5 of 11 interviewees said they "don't know what The HVN is" (Priya, Isla, Claire, Sofia, Emma), a sign of 8K context truncation. The thread is weighted above interviews.
- **Factual slips:** Helena's interview says The HVN "offers… sleep and skin programmes" (those pages are retired); Priya's interview calls it "Wellness & Longevity Clinic" (an entity label from the graph).
- **No fabricated competitor experiences.** C30 cites the directory price for fertility acupuncture (about £90) as "in my own records", correctly hedged.
- The 4 opening posts were generated from the briefing; their authors matched the personas without changes.
