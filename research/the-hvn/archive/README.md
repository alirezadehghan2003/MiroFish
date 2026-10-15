# Archive: superseded v1 research files

**Archived:** 15 October 2026. **Do not use these files as a simulation seed or as current facts.**

| File | Was | Why archived |
|---|---|---|
| `dossier-v1-2026-10-15.md` | `dossier.md` | Compiled from search-engine summaries only (no live page access). The live check on 15 Oct 2026 found its programme catalogue and several prices are out of date (see below). Superseded by `../dossier.md` (v2). |
| `hvn-seed-v1-2026-10-15.md` | `seed/hvn-seed.md` | Built from v1 and describes programmes that no longer have live pages. Simulating on it would test an offer that is no longer published. Superseded by `../seeds/`. |
| `simulation-plan-v1-2026-10-15.md` | `simulation-plan.md` | Single-phase plan with unverified cost assumptions. Superseded by `../simulation-plan.md` (v2). |

## v1 claims retired after the live check (15 Oct 2026)

| v1 claim | Live status, 15 Oct 2026 | Evidence |
|---|---|---|
| HVN 360° Proactive Health Programme, £14,500 / 16 weeks | Page returns **404**; not in sitemap or navigation | `GET /hvn-360-proactive-health-programme/` → 404 |
| Sleep, Rest, Recover, De-Stress Programme, £8,000 / 10 weeks | **404** | `GET /hvn-sleep-rest-recover-de-stress-programme/` → 404 |
| Skin Prevent, Rejuvenate & Restore Programme, £12,000 / 12 weeks | **404** | `GET /hvn-skin-prevent-rejuvenate-restore-programme/` → 404 |
| Body Rebalance & Reshape Programme | **404** | `GET /hvn-body-rebalance-reshape-programme/` → 404 |
| Baseline Wellness £999 / Signature Wellness £3,500 / Annual Longevity Programme | `/functional-medicine/` now 301-redirects to `/functional-medicine-programmes-2/`, a page titled "Functional Medicine Programmes Updated" with no H1, no meta description and **no prices** | Live fetch |
| Anti-Jetlag Programme (incl. HBOT), £375 | **404** (a Jet Lag IV infusion at £375 exists instead) | `GET /anti-jetlag-programme/` → 404; `/iv-infusions/` |
| Hyperbaric oxygen therapy page | `/pages/hyperbaric-oxygen-therapy` and `/hyperbaric-oxygen-therapy/` → **404**; no HBOT page in the sitemap | Live fetch; sitemap |
| Functional Medicine Discovery Session £100 | Now **Discovery Consultation £350**, of which £100 is redeemable against future functional medicine packages | `/discovery-consultation/` |
| IV infusions "£275 (Hydration) to £400 (Vital AA)"; NAD "from £350"; NAD 500 mg add-on £250 | IV menu £275–£425; NAD tiers £350 / £500 / £800, NAD + bespoke £675 | `/iv-infusions/`, `/nad-iv-infusion/` |
| "No independent reviews found" | A Google-reviews widget (Trustindex) is embedded across the site; overall rating not visible in page source | Site HTML |
| `/pages/...` duplicate URL scheme indexed | Those URLs now return 404 (legacy URLs no longer live, but may still be linked externally) | Live fetch |

Claims in v1 that were **not** contradicted are carried forward in v2 with their original labels, and are marked "not re-verified" where they could not be re-checked.
