# The HVN: Customer Segments and Personas

**Version:** 2.0, 15 October 2026. Phase 0 deliverable. Contains no simulated content.

> **Read first.** No customer, CRM, booking or review data was available. Each persona combines two kinds of statement, labelled separately:
> - **Targeting evidence [LIVE-VERIFIED 2026-10-15]:** The HVN publishes pages, services and prices aimed at this need. This shows *what The HVN offers*, not who buys.
> - **Persona attributes [HYPOTHESIS]:** age, triggers, decision criteria and objections, inferred from the offer, price points, location and competitor set. They are **not** observed customer behaviour and must be validated (§4) before business use.
>
> Personas are written as archetypes for MiroFish agents. They describe no real person.

---

## 1. Segment map

| # | Segment | Primary HVN entry points (live) | Entry spend (published) | Typical next step (published) | Main rival tiers |
|---|---|---|---|---|---|
| P1 | Burnt-Out Executive | `/concerns/fatigue-and-burnout/`, `/concerns/insomnia-and-poor-sleep/`, IV menu, Hydrobed | NAD+ £375 (concern page) / £350 (NAD page); Hydrobed £250 | Discovery Consultation £350 → functional medicine packages (unpriced) | 2, 4 |
| P2 | Longevity Optimiser | `/8r-longevity-programme-levitas/`, blood profiles, `/hru-health-performance-assessment/`, NAD tiers | 8R consultation £400; profiles £450 / £550 (+£150 doctor follow-up); HRU £750 | 8R programme from £3,000 | 2 |
| P3 | Aesthetics-First Client | 50+ face, skin and body pages; `/aesthetic-consultation/` | Consultation £175; injections from £260 | Per-treatment courses | 1, 3 |
| P4 | **Women's Health & Hormonal Wellbeing** *(new)* | `/menopause/`, `/pcos/`, `/premenstrual-dysphoric-disorder/`, `/acupuncture-for-perimenopause-menopause/`, `/acupuncture-for-female-hormonal-health/`, `/hormonal-balance-with-susan-gu/`, `/womens-health-with-susan-gu/` | Acupuncture from £200; Discovery Consultation £350 | Acupuncture courses; functional testing | 3 |
| P5 | **Fertility & Pregnancy Journey** *(new)* | `/acupuncture-for-fertility-ivf/`, `/ivf-and-fertility-susan-gu/`, `/fertility-panel/`, `/pregnancy-ritual/`, `/pregnancy-facial-peel/`, `/new-mother-ritual/`, `/concerns/post-pregnancy-changes/` | Acupuncture from £200; fertility panel (see price register) | Acupuncture course alongside an IVF cycle | 3 |
| P6 | International / Visiting Client | Jet Lag IV £375; Hydrobed; hotel-concierge press (Quintessentially, Elite Traveler, CN Traveller logos) | IV £275–£425 | Repeat visits per London stay | 1, 4 |
| P7 | Holistic Wellbeing Seeker | TCM, reflexology, rituals, energy healing, cupping | Rituals / acupuncture from ~£195–£200 | Courses | 4 |
| P8 | **Bridal & Pre-Event Client** *(new)* | `/bridal-preparation-at-the-hvn/` (Bridal Consultation in nav), skin boosters, facials | Consultation | Multi-week treatment plan before a date | 1, 3 |
| P9 | Gatekeeper (PA, spouse, family office) | Contact, Terms (24 h cancellation), CQC badge, phone numbers | n/a (books for P1/P2/P6) | — | all |

*Prices from the live price register (`evidence/hvn-price-register-2026-10-15.csv`). Where a page shows two prices for the same service (NAD £375 on the fatigue page vs £350 on the NAD page), both are reported; see website audit finding W-PRICE.*

---

## 2. Personas

### P1: The Burnt-Out Executive
- **Targeting evidence [LIVE-VERIFIED]:** Fatigue & Burnout and Insomnia concern pages bundle NAD+, nutrition consultation (£350), acupuncture and rituals; late opening hours.
- **Attributes [HYPOTHESIS]:** 40–58, senior role in the City, Mayfair or Belgravia, frequent flyer; low time and high cash; often referred by a PA (P9).
- **Triggers:** exhaustion, poor sleep, a health scare, a partner's push.
- **Decision criteria:** speed to first appointment; discretion; a named doctor; a clear plan with measurable outcomes; evening and weekend slots.
- **Objections:** "Is IV/NAD evidence-based?"; unclear programme price after the £350 Discovery Consultation; 24-hour cancellation with card on file.
- **Simulation voice:** blunt, time-poor, compares to an executive health check at a private hospital.

### P2: The Longevity Optimiser
- **Targeting evidence [LIVE-VERIFIED]:** 8R programme with Levitas (from £3,000), blood profiles with 50+ / 60+ biomarkers, HRU assessment ("230 physiological markers", £750), tiered NAD.
- **Attributes [HYPOTHESIS]:** 35–60, data-driven, follows longevity podcasts, already tracks with wearables.
- **Decision criteria:** diagnostic depth, a published test list, clinician credentials, follow-up cadence, value per biomarker.
- **Objections:** compares against HUM2N (monthly), The Online GP (£645–£1,400 panels), Surrenne and Hooke; sceptical of spa elements; wants an annual/membership path, which is not published.
- **Simulation voice:** cites studies, asks "what's the protocol?", sceptical of marketing language.

### P3: The Aesthetics-First Client
- **Targeting evidence [LIVE-VERIFIED]:** the largest content cluster (Fotona lifts, injectables, Profhilo, polynucleotides, exosomes, threads, peels, skin boosters); £175 consultation; per-area injection pricing published.
- **Attributes [HYPOTHESIS]:** 30–55; values natural results and practitioner skill.
- **Decision criteria:** named injector, before/afters, reviews, safety, convenience.
- **Objections:** many award-winning Knightsbridge alternatives (Taktouk, Harrods operators); £175 consultation vs fee-free consultations elsewhere; skin-analysis "upsell" risk (one public 2025 blog anecdote, see dossier §5.4).
- **Simulation voice:** compares practitioners by name and result, price-per-area aware.

### P4: The Women's Health & Hormonal Wellbeing Client *(new)*
- **Targeting evidence [LIVE-VERIFIED]:** dedicated pages for menopause, perimenopause acupuncture, PCOS, premenstrual dysphoric disorder (PMDD), female hormonal health and emotional wellbeing, led by a named TCM practitioner.
- **Attributes [HYPOTHESIS]:** 38–58 (peri/menopause) or 25–40 (PCOS/PMDD); often already under a GP or menopause specialist; seeking complementary, whole-person support.
- **Decision criteria:** practitioner continuity and empathy; how TCM fits alongside HRT and medical care; evidence honesty; a clear course cost.
- **Objections:** specialist menopause consultations cost £185–£275 elsewhere [DIRECTORY]; "Is acupuncture proven for this?"; is there a doctor in the loop? (The team page lists a surgeon-and-GP aesthetic doctor covering menopause and women's health [LIVE], but the Menopause, PCOS and PMDD pages currently list acne treatments instead (website audit W1).)
- **Simulation voice:** experienced with the healthcare system, wary of being sold to, values being listened to.

### P5: The Fertility & Pregnancy Journey Client *(new)*
- **Targeting evidence [LIVE-VERIFIED]:** IVF/fertility acupuncture pages, fertility panel, pregnancy and new-mother rituals, post-pregnancy concerns page.
- **Attributes [HYPOTHESIS]:** 30–45, often mid-IVF at another clinic, emotionally invested, highly research-driven.
- **Decision criteria:** coordination with the IVF clinic's timeline, practitioner experience, gentle environment, pregnancy-safe treatments.
- **Objections:** specialist fertility-acupuncture competition (Zita West from £90 per session [DIRECTORY]); weekly session cost over months; fear of false hope.
- **Simulation voice:** careful and hopeful, asks about evidence and safety.

### P6: The International / Visiting Client
- **Targeting evidence [LIVE-VERIFIED]:** Jet Lag IV (£375), Hydrobed; press logos from travel and concierge titles. (The retired Anti-Jetlag Programme page now returns 404.)
- **Attributes [HYPOTHESIS]:** GCC, US or European HNW visitor staying in Knightsbridge hotels; booked via a hotel concierge or PA.
- **Decision criteria:** availability this week, prestige, discretion, multilingual service, packaged half-days.
- **Objections:** 24-hour cancellation with card on file; no published visitor package; hotel spas (Mandarin Oriental, Lanesborough, Six Senses) are closer at hand.

### P7: The Holistic Wellbeing Seeker
- **Targeting evidence [LIVE-VERIFIED]:** TCM, cupping, reflexology, energy-healing ritual, purification/detox ritual, forest-bathing-inspired interiors (press).
- **Attributes [HYPOTHESIS]:** 30–60, values warmth, ritual and continuity over clinical metrics.
- **Objections:** clinical/medical language may feel cold; course cost; hotel spas as substitutes.

### P8: The Bridal & Pre-Event Client *(new)*
- **Targeting evidence [LIVE-VERIFIED]:** `/bridal-preparation-at-the-hvn/` page and "Bridal Consultation" in the main navigation.
- **Attributes [HYPOTHESIS]:** 28–40 (or the mother of the bride), 3–6 months before an event, budgeted.
- **Decision criteria:** a reliable timeline, no-risk treatments close to the date, visible results, a package price.

### P9: The Gatekeeper
- **Targeting evidence [LIVE-VERIFIED]:** Terms (24-hour cancellation), CQC "Regulated" badge (image, not linked to the register), two phone numbers in use.
- **Attributes [HYPOTHESIS]:** PA, spouse or family-office manager vetting on behalf of P1, P2 or P6.
- **Decision criteria:** regulation, clear pricing and terms, reviews, a single point of contact.
- **Objections:** no inspection rating visible; inconsistent contact numbers; programme prices no longer published.

---

## 3. Non-customer voices for simulation (not segments)

| Voice | Purpose in simulation | Constraint |
|---|---|---|
| Sceptical evidence-based GP | Stress-tests medical and IV claims | Uses only the seed's evidence and ASA context |
| Wellness journalist | Probes positioning and luxury cues | Cites only seed press facts |
| Competitor member (e.g. Surrenne or HUM2N member) | Surfaces switching reasons | Competitor facts limited to `competitors.md`, with caveats |
| The HVN (brand account) | States published facts only | No invented offers, prices or claims |

---

## 4. Validation plan (to replace hypotheses with evidence)

| Method | What it validates | Owner | Effort |
|---|---|---|---|
| 8–12 client interviews (2 per priority segment) | Triggers, decision criteria, objections | The HVN marketing | 2–3 weeks |
| Booking and enquiry data from Pabau (by service and entry page) | Real segment mix, consultation → programme conversion | The HVN ops | 1 week |
| GA4 / Search Console (landing pages, queries) | Which concern pages actually attract demand | The HVN digital/agency | 2 days |
| Google review text analysis (from the widget's source) | Praise and complaint themes by segment | Analyst | 2 days |
| Mystery shop (phone + online) of The HVN and 2 rivals | Booking friction, consultation-to-programme pitch | Analyst | 1 week |
