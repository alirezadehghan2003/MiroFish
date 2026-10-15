# Research Kit 06 · Analysis, Evidence Templates and Reporting

## 1. Templates (in `templates/`)

| File | Use | Contains personal data? |
|---|---|---|
| `screener-tracker.csv` | Recruitment status by pseudonymous reference | **No** (the key is held by The HVN or the panel) |
| `consent-log.csv` | Consent versions and options per participant ID | No names |
| `usability-observation-log.csv` | Timestamped observed actions (OBS) | No |
| `task-results.csv` | Task completion, time, SEQ, confidence | No |
| `interview-notes.csv` | Coded statements (OBS/REP/OPN/HYP; prompted or not) | No; health details omitted |
| `evidence-register.csv` | One row per finding, with confidence and decision | No |
| `enquiry-log.csv` | Ongoing enquiry reasons and response times (measurement spec §8) | No (pseudonymous IDs) |
| `booking-flow-test-log.csv` | Non-transactional booking test (`../02-booking-journey-audit.md` §7) | No |

## 2. Analysis steps
1. **Within 24 h of each session:** complete the logs; note the 3 strongest OBS/REP items.
2. **After all sessions:** code themes (issue codes from Kit 04 §5; theme codes from the hypotheses).
3. **Build the evidence register:**
   - one finding per row;
   - count supporting and contradicting participants;
   - record the evidence mix (OBS/REP/OPN/HYP);
   - assign confidence (Kit 01 §2.2).
4. **Triangulate** with the GA4 baseline, the enquiry log and booking exports once available (`../03-measurement-spec.md`).
5. **Map to decisions** using `../../validation-plan.md` §5 (e.g. H01 supported → publish ranges, R11).
6. **Write the read-out:**

| Section | Content |
|---|---|
| 1 | What we did (sample, dates, which tickets were live) |
| 2 | Answers to RQ1–RQ8, each with confidence and evidence mix |
| 3 | Usability task table (completion, time, SEQ, severity-3/4 issues) |
| 4 | Decisions: supported / not supported / unclear, per hypothesis |
| 5 | Changes to the roadmap and register |
| 6 | Limitations (sample size, recruitment bias, prompted vs unprompted) |
| 7 | Appendix: evidence register |

## 3. Reporting rules
- Never present opinions (OPN) or intentions (HYP) as behaviour.
- With 5–12 people, use counts ("4 of 6"), not percentages.
- Quote only with consent, anonymised.
- **Never combine with or compare against MiroFish counts as if they were the same kind of evidence.** If useful, add one line noting whether a real finding matched or contradicted a simulated hypothesis.
