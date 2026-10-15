# Research Kit 04 · Usability-Test Protocol (5–6 participants)

**Needs approval:** AP10 (gate G2) and DPO sign-off (Kit 03). **Not started.**

## 1. Set-up

| Item | Detail |
|---|---|
| Participants | 5–6 non-clients (Kit 02 §1); at least 4 on their own phone |
| Format | 45 min remote video call; participant shares their screen; think-aloud |
| Roles | Moderator (runs the session, neutral); note-taker (codes OBS in `templates/usability-observation-log.csv`) |
| Site | The **live** the-hvn.com. If fixes have shipped, note the release date. Optional: two static mock-ups (Task 6) |
| Hard rules | **No booking, no payment, no form submission, no personal data.** If the participant reaches a card or personal-details screen, stop: "That's as far as we go." |
| Pilot | Run one pilot session with a colleague who has never seen the site; adjust timings |
| Order | Task 1 first; rotate tasks 2–4; Task 5 last |

## 2. Session script

**Intro (3 min):**
> Thanks for joining. We're testing the website, not you, so there are no wrong answers. Please think aloud: tell me what you're looking for, what you expect and what surprises you. I didn't design the site, so you won't hurt my feelings. Please don't book, pay or type personal details anywhere. I'll stop you if we get close. Any questions before we start?

Confirm recording consent (Kit 03). Ask them to open the browser on their device.

**Warm-up (2 min):**
> When you last looked for a private health or beauty appointment, how did you go about it? (Code as REP.)

## 3. Tasks

For each task, read the scenario exactly. Don't help. If they're stuck for 2 minutes, ask "What would you do now in real life?" and record that as an assist.

| Task | Scenario (read aloud) | Start | Success criterion (observable) | Note especially |
|---|---|---|---|---|
| **T1 Orientation** | "Imagine a friend sent you this clinic's link. Take a minute and tell me what kind of place this is and who it's for." | Home page | States a category in their own words within 60 s | Words used; where they look; reaction to "London's leading" |
| **T2 Cost** | "You've been feeling exhausted for months. Find out whether this clinic could help, and roughly what it would cost you over the next three months." | Home page | Identifies a first step **and** gives a cost estimate, or says it can't be found | Time to the first price; whether they find the fatigue page; reactions to unpriced plans and fee credits |
| **T3 Trust** | "Before you'd go anywhere, you'd want to know who would treat you and whether the clinic is properly regulated. Find out." | Any page | Names a practitioner relevant to a service **and** states what they learnt about regulation | Clicks on the CQC badge (unlinked today); team page use |
| **T4 Women's health** | "You're in your late 40s and think you may be perimenopausal. See what this clinic offers and decide what you'd book first." | Google-style start: give the URL `the-hvn.com/menopause/` | Picks a relevant service and can say why | Reaction to the acne-treatment block (until T01 ships); where "Book a consultation" leads (**stop before personal details**) |
| **T5 Contact on the go** | "You're between meetings on your phone and want to speak to someone today. Get in touch, but stop before actually calling or sending anything." | Any service page | Finds a way to call or message within 60 s | Whether the number is tappable; WhatsApp; forms |
| **T6 (optional) Compare** | Show mock-up A (current hero) and mock-up B (concrete version: named doctor, "doctor check before every IV", clear prices). "Which is more believable, and why?" | Static images | — | Code as OPN; secondary only |

**After each task (30 s):**
- "On a scale of 1–7, how easy or difficult was that?" (SEQ: 1 very difficult, 7 very easy.)
- "How confident are you in your answer?" (1–5)

## 4. Debrief (5 min)
1. "What, if anything, would stop you booking here?" (OPN; note if unprompted)
2. "What would you need to see to feel confident?" (OPN)
3. "If you were choosing between this clinic and another, what would decide it?" (OPN/HYP)
4. Thank, explain the incentive, end the recording.

## 5. Observation guidance
- Log **actions with timestamps and URLs**: clicks, scrolls, back-button use, pauses over 5 s, pinch-zoom, mis-taps.
- Use the moderator's exact wording for any assist.
- **Severity:**
  - 1 = cosmetic;
  - 2 = minor delay;
  - 3 = major delay or wrong path;
  - 4 = blocked or abandoned.

### Issue codes

| Code | Issue |
|---|---|
| NAV | Navigation |
| 404 | Dead end |
| PRC | Price unclear or missing |
| CRD | Fee credit unclear |
| TRS | Trust or verification |
| CTA | Booking button or route |
| MOB | Mobile layout or tapping |
| CNT | Content mismatch (e.g. acne treatments on menopause) |
| CPY | Wording or claims |
| OTH | Other |

## 6. Metrics reported per task

| Metric | Formula |
|---|---|
| Completion rate | completed ÷ attempted (partial counted separately) |
| Median time | seconds |
| Assists | count |
| SEQ | median (1–7) |
| Severity-3/4 issues | count by code |

With 5–6 participants, report **counts, not percentages**. A problem that blocks 2 or more people is treated as real.

## 7. Materials checklist
- [ ] DPO-approved information sheet and consent (Kit 03)
- [ ] Panel bookings and quota sheet (`templates/screener-tracker.csv`)
- [ ] Mock-ups A/B (optional; compliance check of mock-up B wording, since it may be read as an advert)
- [ ] Observation log, task-results sheet
- [ ] Release log (which tickets were live on test days)
