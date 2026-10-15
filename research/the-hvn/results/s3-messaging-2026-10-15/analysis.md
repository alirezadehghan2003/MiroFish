# S3 Website Messaging: Evidence-Checked Analysis

**Run:** 15 Oct 2026 · Reddit mode · `claude-haiku-5-5` only · 12 invented agents · 24/24 rounds (round 1 = 09:00) · English · graph memory off · native report skipped · graph `mirofish_b5d37ea035d74d76`
**Activity:** 12/12 agents authored content · 1 new post + 31 comments (29 replies) · 32 meaningful items · 24 likes · 12 messaging-specific interviews
**Cost:** $0.102 (71 requests, 0 errors) · `run-metrics.json` · verbatim `thread.md`

## Critical limitation: the TEST MESSAGES were not tested
The three alternative taglines (TM1 "doctor-led, one plan", TM2 "evidence first", TM3 "sanctuary") were in the briefing, but **MiroFish's generated opening posts only mentioned that they existed, not their text**. Agents see the feed, not the briefing, so **11 of 12 interviewees said they had not seen TM1–TM3 and declined to rank them**. One (Natalie) judged by the labels alone: TM2 most trusted, TM3 at risk of selling "a feeling". **No conclusion about the test messages can be drawn.** Next time, put each test message verbatim into an opening post.

What S3 *did* test well: **reactions to The HVN's real website wording [VERIFIED quotes]**.

## Simulated insights about the real copy

| # | Insight [SIMULATED] | Trace | Evidence | Verdict |
|---|---|---|---|---|
| M1 | **"London's leading" is a slogan without a named source, date and criteria.** Most-liked post in the run (11 likes). | P2, C5, C11, C14, C18; 10 of 12 interviews | The line appears on 212/212 pages **[VERIFIED]**; substantiation risk (audit W4) | **Strong** |
| M2 | **"Transformational" and "unparalleled client experiences" read as spa-brochure filler** that "tell you how to feel, not what to expect". | P3, C6, C9, C15, P4; interviews | About-page wording **[VERIFIED]** | **Strong** |
| M3 | **Concrete items earn attention**: acupuncture, Fotona laser, and especially the "10 minute consultation with one of our doctors" before IV. | C3, C9, C11, P3 | IV page wording **[VERIFIED]** | **Supported.** The most valuable line on the site |
| M4 | **…but "10 minutes" needs defining**: what it covers (history, examination, contraindications), who decides, who prescribes and supervises, plus the ingredient and dose list. "Ten minutes is a duration, not a standard." | P3 thread: C1, C4, C7, C8, C10, C16, C17, C26, C31 | Content of the IV consultation not described **[VERIFIED: page]** | **Actionable.** Publish a short "what happens before your drip" outline |
| M5 | **Name the practitioner for each treatment**; the home page lists services "in one breath" with no named owner. | C9, C13, C14, C28 | Site-wide identical practitioner block **[VERIFIED]** | **Strong** (3rd scenario in a row) |
| M6 | **"We don't know yet" beats an overconfident promise**: say what the evidence does and doesn't support. | P4, C20, C22, C23, C25, C27 | IV claim wording **[VERIFIED]**; ASA context **[REGULATOR]** | **Strategic.** Supports the "evidence first" positioning direction |
| M7 | **Link the CQC entry and state plainly "registered, not yet inspected"**; don't "let the registration do the talking". | C5, C9, C11, C20 | Badge unlinked on 212/212 pages **[VERIFIED]** | **Strong** |
| M8 | **"What would make you advise me not to proceed?"** suggested as a trust test. | C21 (in a comment otherwise excluded, see below) | — | **Hypothesis.** Useful consultation-script idea |
| M9 | **Separate consultation fee vs drip price**: show the first-visit total. | C7, C19, C26, C31 | IV page shows the infusion price; consultation included "brief 10 minute" **[VERIFIED]**; whether charged separately **[NEEDS TESTING]** | **Actionable** |

## Data-quality notes (fabrications excluded)
- **Isla (C24, interview):** "I've booked a consultation at HVN… greeted by name, offered tea". **Fabricated** experience of The HVN; **excluded**. Isla's C2 and C6 ("my first consultation somewhere else") are generic backstory.
- **Sofia (C21, C29):** "My best experience at Sanctuary in Knightsbridge… my injector…". "Sanctuary" is the TM3 label that the knowledge graph turned into an entity; the experience is **fabricated** and **excluded**. Only the generic question in M8 is kept.
- **Priya (C25):** her own IVF clinic experience; generic backstory, no named provider.
- Interview memory: most interviewees could see only the quoted lines from the feed, not the full copy.
