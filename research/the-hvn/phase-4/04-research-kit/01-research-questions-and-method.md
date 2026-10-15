# Research Kit 01 · Research Questions and the Observed-vs-Opinion Method

**Kit status:** prepared, 15 October 2026. **Not started.** Needs approvals AP10 (usability) and AP11 (interviews) in `../08-approval-register.md`.

> **Simulated agents are not participants.** MiroFish outputs only told us *what to ask*. They are never counted, quoted or mixed with real findings.

## 1. Research questions

| RQ | Question | Hypotheses (`../../validation-plan.md`) | Usability | Interviews | Analytics / log |
|---|---|---|---|---|---|
| RQ1 | What makes people hesitate or stop before booking a first appointment? | H01, H03, H09 | Tasks 1–2, 5 | Q3, Q4 | Enquiry reason tags |
| RQ2 | Can people work out roughly what a course of care would cost, and does it matter to them? | H01, H02 | Task 2 | Q3, probe P1 | `price_block_view` → `booking_click` |
| RQ3 | How do people judge whether a clinic and its practitioners can be trusted? | H04, H05, H07, H12, H13 | Task 3 | Q2, probes P3–P4 | `cqc_link_click` (after T05) |
| RQ4 | Can someone with perimenopausal symptoms find relevant support, and how do they choose between a specialist and an integrated clinic? | H08 | Task 4 | Women's-health module | F2 funnel |
| RQ5 | How do people contact or book on a phone, and where does that fail? | H09, H10 | Task 5 | Q3 | `tel_click`; booking test |
| RQ6 | What did clients expect from, and take away from, the first consultation? | H01, H11 | — | Q4, Q5 | Consultation-to-plan conversion (F6) |
| RQ7 | How do people see paying per visit vs a membership? | H06 | — | Probe P5 | — |
| RQ8 | How much do setting, atmosphere and experience matter compared with verifiable information? | H13 | — | Q2, Q6, probe P6 | — |

## 2. Separating observed behaviour from opinion

### 2.1 Evidence codes (every note gets exactly one)

| Code | Name | Definition | Example | Weight |
|---|---|---|---|---|
| **OBS** | Observed behaviour | Something the researcher **saw the participant do** in the session (click, scroll, hesitate, give up), or a system record (analytics, booking export) | "Scrolled past the price table twice, then opened the Contact page" | **Strongest** |
| **REP** | Reported past behaviour | The participant describes a **specific past episode** with time, place and actions | "Last spring I emailed two clinics, and booked the one that sent prices first" | Strong if specific |
| **OPN** | Opinion or attitude | A judgement, preference or feeling, not tied to an episode | "I think clinics should show prices" | Moderate: context only |
| **HYP** | Hypothetical or future intention | What they say they *would* do | "I would definitely book if…" | **Weakest**: never decision-grade alone |

**Rules:**
1. **A finding is decision-grade only if** it rests on OBS or specific REP evidence from at least 3 participants (usability), or 4 of 8–12 (interviews), **and** isn't contradicted by analytics.
2. HYP statements can **generate** hypotheses but never **confirm** them. (MiroFish outputs are effectively all HYP.)
3. Record whether a statement was **unprompted**, **after a probe**, or **after a stimulus**. Only unprompted mentions count towards "people raise X themselves".
4. Note-takers write what they see and hear, not interpretations: "clicked 'Bookings'; paused 9 s; said 'where is menopause?'", not "was confused".
5. Contradictions are recorded, not resolved, in `templates/evidence-register.csv` (`n_contradicting`).
6. Triangulate: each decision-grade finding should be checked against at least one analytics or log source once available.

### 2.2 Confidence scale for findings

| Confidence | Criteria |
|---|---|
| **High** | OBS or REP from ≥ 3 usability / ≥ 4 interview participants, unprompted, consistent across segments, supported by analytics |
| **Medium** | OBS/REP from 2–3 participants, or mostly prompted, or not yet triangulated |
| **Low** | Mostly OPN/HYP; single participant; or contradicted |

### 2.3 Bias controls
- **Neutral questions first; probes later; stimulus last.** S2a showed that leading questions produce echoes.
- One moderator and one note-taker. The moderator doesn't defend The HVN or explain the site during tasks.
- Rotate task order for tasks 2–4 across participants.
- Clinicians are not moderators (avoids deference effects).
- Don't reveal which changes are planned.
- Record moderator deviations from the guide in the notes.

## 3. Outputs
1. `templates/task-results.csv` and `templates/usability-observation-log.csv` (usability).
2. `templates/interview-notes.csv` (interviews, coded).
3. `templates/evidence-register.csv`: one row per finding, with confidence and decision implication.
4. A short read-out (≤ 10 pages) answering RQ1–RQ8, with decisions mapped to `../../validation-plan.md` §5.
