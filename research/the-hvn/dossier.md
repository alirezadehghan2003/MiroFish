# The HVN: Business & Marketing Intelligence Dossier

**Version:** 2.0 (Phase 0), compiled **15 October 2026**
**Subject:** The HVN Wellbeing Ltd, 57–63 Knightsbridge, London SW1X 7BF ([the-hvn.com](https://the-hvn.com))
**Purpose:** Evidence base for the HVN study and its MiroFish simulations. Not medical, legal or investment advice.
**Supersedes:** `archive/dossier-v1-2026-10-15.md` (retired claims listed in `archive/README.md`).

---

## 0. How to read this dossier

### 0.1 Evidence labels
| Label | Meaning | Confidence |
|---|---|---|
| **[LIVE]** | Loaded directly from the-hvn.com on 15 Oct 2026 (full sitemap crawl, 216 URLs) | High, as of that date |
| **[OFFICIAL-PR]** | Organisation's own press release, found by search | Medium–High |
| **[TRADE/PRESS]** | Independent press or trade media | Medium |
| **[REGULATOR]** | Regulator's register, rulings or guidance | High at time of publication |
| **[DIRECTORY]** | Aggregator / directory | Low |
| **[V1-NOT-REVERIFIED]** | Carried from v1 (search-indexed); could not be re-checked from this environment | Low–Medium |
| **[HYPOTHESIS]** | Analyst inference | Not evidence |
| **[NEEDS TESTING]** | Requires a live session, booking test, analytics or primary research | — |
| **[SIMULATED]** | MiroFish output. **None exist yet.** Never to be quoted as customer data. | — |

### 0.2 Method and limits
1. **Website:** all 216 URLs in The HVN's XML sitemap were fetched politely (sequential, with back-off after the site rate-limited parallel requests), plus 45 internal link targets not in the sitemap. Derived data is in `evidence/`; raw HTML was not committed.
2. **Competitors, regulators, reviews:** competitor sites, cqc.org.uk, asa.org.uk, review platforms and the Pabau booking domain were **blocked by this environment's network policy**. Evidence comes from web search results, press releases and directories, labelled accordingly.
3. **No customer data** (CRM, bookings, analytics, review text) was available. All personas and behavioural statements are hypotheses.
4. **No personal data** was collected. Clinicians are referred to by role, except where a name is part of a page URL or title.
5. The full source log is in `evidence/sources.md`.

---

## 1. Executive summary of Phase 0 findings

| # | Finding | Label |
|---|---|---|
| 1 | **The programme tier has disappeared from the website.** The 360° (£14,500), Sleep (£8,000), Skin (£12,000), Body and Anti-Jetlag programme pages and the hyperbaric page all return 404. `/functional-medicine/` redirects to an orphan page titled "Functional Medicine Programmes Updated" (not in the sitemap, no H1, no prices). Only 8R ("from £3,000") remains. | [LIVE] |
| 2 | **The women's-health pages show the wrong treatments.** Menopause, PCOS and PMDD pages promise "evidence-based care" but their treatment block is headed "Explore our specialised solutions for rosacea, acne, and acne scarring" and lists acne lasers and peels. | [LIVE] |
| 3 | **Price transparency is a real asset.** 149 of 151 service pages display a price, unusual at this tier, where rivals use membership or "price on request". | [LIVE] + [TRADE/PRESS] |
| 4 | **The step from first visit to plan is unpriced.** Consultations £175 / £350 / £400 and tests £180–£750 are priced, but the next step (functional medicine packages) has no published price. The £350 Discovery Consultation's £100 credit applies only to those unpriced packages. | [LIVE] |
| 5 | **Brand language has shifted.** "Conscious wellbeing / conscious luxury" (v1 positioning, still in 2024 press) now appears only on the sustainability page. The site-wide line is "London's leading Wellness & Longevity Clinic", a superlative, while the Contact and Booking page titles say "Skin & Hair". | [LIVE] |
| 6 | **Health-claim exposure.** Immune or "boost" wording appears on 19 of 20 IV/IM pages (immune: 16; boost: 18); one product is named "Fat Burner"; NAD and glutathione pages cite "anti-ageing", "cellular repair" and "detoxification". The ASA has ruled against comparable IV claims elsewhere. Needs review by a qualified adviser. | [LIVE] + [REGULATOR] |
| 7 | **Trust signals are present but under-used.** A "CQC Regulated" badge is on 212/212 pages but links to the CQC register on none. A Google-reviews widget is on 157/212 pages. "Evidence-based" or "science-backed" wording appears on 18 pages. | [LIVE] |
| 8 | **The competitive model gap is membership.** Tier 1–2 rivals (Surrenne £10k/yr + £5k, Lanesborough, Lanserhof, Pillar, Hooke, HUM2N monthly) sell belonging and continuity. The HVN sells per visit. | [TRADE/PRESS] |
| 9 | **The £15k / 12–16-week programme price point exists in the market** (Pillar at Raffles OWO, 2026), at about the price of The HVN's retired 360° programme. | [OFFICIAL-PR] |
| 10 | **New 2026 supply:** HUM2N opened inside Six Senses London (June 2026). Four Seasons Park Lane launched spa and wellness memberships. | [TRADE/PRESS] / [OFFICIAL-PR] |

Full website findings: `website-audit.md`. Competitors: `competitors.md`. Segments: `personas.md`.

---

## 2. Brand and positioning

### 2.1 Verified facts
| Fact | Label | Source |
|---|---|---|
| Trading entity "The HVN Wellbeing Ltd", 57–63 Knightsbridge SW1X 7BF; hours Mon–Sat 08:30–21:30, Sun 10:00–18:00; enquiries to a "Concierge Team" (concierge@ email) | [LIVE] | [/contact/](https://the-hvn.com/contact/) |
| Opened October 2023 | [TRADE/PRESS] | [Cosmetics Business](https://cosmeticsbusiness.com/former-paco-rabanne-ceo-opens-new-wellness-retreat), [Globetrender](https://globetrender.com/2024/08/22/the-hvn-is-a-spa-that-promotes-conscious-wellbeing/) |
| Founder and CEO formerly CEO of a global fashion and fragrance house | [TRADE/PRESS] | Cosmetics Business |
| Site-wide line: "LONDON'S LEADING WELLNESS & LONGEVITY CLINIC"; home banners "REGENERATIVE AESTHETICS IN KNIGHTSBRIDGE", "DOCTOR-LED FOTONA LASER 5D FACE LIFT", "NOW OFFERING ACUPUNCTURE WITH [senior TCM practitioner]" | [LIVE] | [Home](https://the-hvn.com/) |
| About: "wellness is not just a goal—it's an ongoing journey … clinical innovation is perfectly balanced with unbridled attention to care … bespoke treatment plans"; every journey "begins with a personalised consultation" | [LIVE] | [/about/](https://the-hvn.com/about/) |
| Team: Medical Director (BM, MRCGP, DCH, DRCOG; "global award-winning laser specialist"); a second aesthetic doctor (surgeon and GP; aesthetics, menopause, women's health); senior TCM practitioner and acupuncturist; osteopath (also delivers the HRU assessment); aesthetic nurse; aesthetic practitioner; holistic and massage therapists | [LIVE] | [/the-expert-team/](https://the-hvn.com/the-expert-team/), [/about/](https://the-hvn.com/about/) |
| Partnership: 8R Longevity Programme with Levitas, "from £3,000"; 8R consultation £400 (up to 90 min) | [LIVE] | [/8r-longevity-programme-levitas/](https://the-hvn.com/8r-longevity-programme-levitas/), [/consultations/](https://the-hvn.com/consultations/) |
| Levitas's medical director is described elsewhere as founder of "Nomad & **10R** Longevity Plans" (naming differs from The HVN's "8R") | [DIRECTORY] | [Doctify](https://www.doctify.com/uk/specialist/ash-kapoor) |
| 2023–24 press framed The HVN as "the home of conscious wellbeing", "not a spa"; reported 6 treatment suites, 2 recovery pods, a Hydrobed described as the UK's only one, Fotona laser, a medical-grade hyperbaric chamber | [TRADE/PRESS] | [Brummell](https://www.brummellmagazine.co.uk/discover/a-holistic-cutting-edge-approach-to-wellbeing-is-on-offer-at-the-hvn/), Globetrender |
| "Conscious wellbeing / luxury" wording now appears only on `/sustainability-strategy/` | [LIVE] | crawl |
| CQC: provider registered, **not yet inspected** (no rating) | [V1-NOT-REVERIFIED] (REGULATOR, Oct 2026 via search) | [CQC provider page](https://www.cqc.org.uk/provider/1-22154280768/services) |

### 2.2 Positioning analysis [HYPOTHESIS]
- **From "conscious wellbeing" to "leading longevity clinic".** The brand has moved from a values-led, spa-adjacent idea towards a clinical superlative. That suits longevity buyers, but "leading" is unsubstantiated on the page, and "Skin & Hair" titles on Contact and Booking pull the other way.
- **Category breadth remains the core ambiguity.** Five service families (aesthetics, TCM, IV, testing/longevity, rituals) are offered under one roof, with 150+ service pages. For first-time visitors, "what is it for?" is answered by the navigation, not by a single proposition.
- **The most defensible differentiation is integration plus transparency.** A doctor-led team spanning aesthetics, TCM, osteopathy and testing, at one Knightsbridge address, with no membership and published prices. Individual modalities (IV, NAD, lasers, injectables) are available from many rivals (`competitors.md`).
- **The credibility stack is strong but partly invisible.** A named GP-trained Medical Director, doctor screening before IV (a "10 minute consultation with one of our doctors"), CQC registration, Google reviews and press are all present. The CQC badge doesn't link to the register; there is no inspection rating; the reviews widget's rating isn't visible in page source.

---

## 3. Offer and price architecture [LIVE, 15 Oct 2026]

Full register (342 price points on 148 pages): `evidence/hvn-price-register-2026-10-15.csv`.

| Layer | Offer (examples) | Published price |
|---|---|---|
| **Consultations** | Aesthetic consultation (60 min) | £175 |
| | Discovery Consultation (up to 60 min; £100 redeemable against functional medicine packages) | £350 |
| | Nutrition consultation (60 min) | £350 |
| | 8R Longevity Consultation with Levitas (up to 90 min) | £400 |
| **Diagnostics** | Igloo blood reader | £60 |
| | Vitamins & minerals profile / Essential wellness profile | £180 / £220 |
| | Complete Wellness profile (50+ biomarkers) / Elite Functional Health (60+) | £450 / £550 (+£150 doctor follow-up call) |
| | Fertility panel | £500 |
| | HRU Health & Performance Assessment (35 min, "230 physiological markers") | £750 |
| **IV / IM** | 14 IV infusions, 60–90 min | £275–£425 |
| | NAD+ tiers (90 / 150 / 240 min); NAD + bespoke | £350 / £500 / £800; £675 |
| | Iron infusion (with a partner provider) | from £895 |
| **Aesthetics** | Muscle-relaxing injections (per-area price table) | from £260 |
| | Dermal fillers / Profhilo / Polynucleotides | from £450 / £450 / from £450 |
| | Fotona 5D Lift / Exosomes / PRP | from £850 / from £500 / from £550 |
| | HydrO2 facial | from £200 (also £145 / £245 variants) |
| **TCM & therapies** | Acupuncture (15-min consultation + 30 min needling) / course | from £200 / from £1,620 |
| | Osteopathy / Reflexology / Oxygen-ozone therapy | from £260 / £230 / from £210 |
| | Hydrobed Reset Massage, 60 / 90 min with facial ("dry flotation & holistic massage") | £250 / £375 |
| **Programmes** | 8R Longevity Programme with Levitas | from £3,000 |
| | Functional medicine "packages" | **not published** |
| **Retail** | 14 product pages (candles, diffusers, room spray etc.) | priced in shop |

**Booking terms [LIVE]:** online booking via Pabau on every page; card required to confirm; 24-hour cancellation notice ([/terms-of-service/](https://the-hvn.com/terms-of-service/)).

**Analysis [HYPOTHESIS]:** the ladder is fully priced up to about £750 and then becomes opaque. The "commitment cliff" tested in v1 has turned into a **"price fog"**: a client cannot learn what a full plan costs without first paying £175–£400. This is the main conversion question for S2.

---

## 4. Website, discovery and conversion
Summarised here; full evidence in `website-audit.md`.

| Area | Status | Label |
|---|---|---|
| Crawl health | 216 sitemap URLs: 212 × 200, 2 × 301, 2 × 302 (basket/checkout) | [LIVE] |
| Retired pages | Programme and HBOT pages 404; broken internal links listed in the audit | [LIVE] |
| Women's-health content | 3 pages show acne treatments | [LIVE] |
| SEO metadata | No duplicate titles; 6 titles over 60 characters; Fotona title says "4D" while the H1 says "5D®"; generic titles such as "Menopause - The HVN" | [LIVE] |
| Structured data | Organization / WebSite / WebPage / Breadcrumb only; **no MedicalClinic or LocalBusiness**, no address, hours or service markup | [LIVE] |
| Page weight | Median 713 KB of HTML and 55 images per page | [LIVE] |
| Trust | CQC badge 212/212 (not linked); reviews widget 157/212; 2 phone numbers | [LIVE] |
| Booking flow | Pabau widget; steps, deposit and mobile UX | [NEEDS TESTING] (domain blocked) |

---

## 5. Customers and market

### 5.1 Segments
Nine hypothesised segments (`personas.md`). New in v2, based on live site content: **Women's Health & Hormonal Wellbeing**, **Fertility & Pregnancy Journey**, **Bridal & Pre-Event**. All persona attributes are [HYPOTHESIS].

### 5.2 Competitive set
Tiered in `competitors.md`:
- Tier 1 direct: Surrenne, The Lanesborough Club & Spa, The Wellness Clinic at Harrods.
- Tier 2 longevity substitutes: HUM2N, Lanserhof at The Arts Club, Pillar at Raffles OWO, Hooke, Clinique La Prairie partners, The Online GP.
- Tier 3 service specialists: aesthetics, IV, menopause, fertility acupuncture.
- Tier 4 hotel substitutes.
- Levitas is a **partner**, not a competitor.

### 5.3 Market and regulation
- **UK wellness economy:** US$224 bn (2022), about US$261 bn (2024), 5th globally [TRADE/PRESS: [Global Wellness Institute](https://globalwellnessinstitute.org/press-room/press-releases/wellness-economy-reort-uk-2024/)]. This is a whole-economy figure; **no reliable figure for the London luxury clinic segment exists**, and none is estimated.
- **IV advertising:** medicinal claims are not permitted for IV nutritional therapy. The ASA warns against extrapolating supplementation studies to one-off infusions and has upheld complaints about immune-boosting claims [REGULATOR: [ASA guidance](https://asa.org.uk/advice-online/healthcare-intravenous-nutritional-therapy.html), [Get A Drip ruling](https://asa.org.uk/rulings/get-a-drip-ltd-a19-549582-get-a-drip-ltd.html), [REVIV ruling](https://www.asa.org.uk/rulings/reviv-uk-ltd-a19-562605-reviv-uk-ltd.html)]. No 2025–26 IV rulings were found by search.
- **Aesthetics licensing (England):** DHSC responded to its consultation in August 2025 (mandatory training, indemnity, premises standards, risk-tiered procedures). Government confirmed on 17 Oct 2025 that it intends to legislate; **no commencement date** had been found as of mid-2026 [TRADE/PRESS: [Clyde & Co, 2026](https://www.clydeco.com/en/insights/2026/05/non-surgical-cosmetic-procedures); [Mishcon de Reya](https://www.mishcon.com/news/non-surgical-aesthetic-treatments-do-they-need-better-regulation)]. Scotland is moving faster.

### 5.4 Reputation signals
- 2023–25 lifestyle and trade press is positive (Brummell, Globetrender, City A.M., Quintessentially) [TRADE/PRESS].
- One June 2025 personal blog describes a skin-analysis result later disputed by a dermatologist, and a sense of being upsold [TRADE/PRESS, single anecdote: [A Lady in London](https://www.aladyinlondon.com/2025/06/weekend-in-knightsbridge.html)]. [HYPOTHESIS] Treat it as a theme to monitor, not a pattern.
- Google reviews are embedded on site, but rating and volume are not visible in page source [NEEDS TESTING].

---

## 6. Simulation findings
**None.** Runs S1–S4 are specified in `simulation-plan.md`. Results will be appended to `results/` labelled [SIMULATED], with model, agent count, rounds and actual cost.

## 7. Open questions and validation backlog
| # | Question | How |
|---|---|---|
| 1 | Were the programmes withdrawn, repriced or just unpublished? Which annual or membership options exist? | Ask management |
| 2 | Pabau booking flow: steps, deposit, which services are bookable online, mobile UX | Allow `partner.pabau.com`, or a manual test booking stopping before payment |
| 3 | Current CQC status of The HVN and Tier 1 rivals | Allow `cqc.org.uk` |
| 4 | Google review rating, volume and themes | Google Business Profile access |
| 5 | Which landing pages and queries drive enquiries | GA4 / Search Console |
| 6 | IV and IM wording, the "London's leading" claim and the botulinum-toxin page | Qualified advertising / regulatory adviser |
| 7 | Live competitor prices | Allow competitor domains (`competitors.md` §8) |
| 8 | Real segment mix and conversion | Pabau data; 8–12 client interviews |

## 8. Change log
- **v2.0 (15 Oct 2026):** first live-site version; v1 claims retired (`archive/README.md`); added women's-health, fertility and bridal segments, tiered competitors, website audit, price register, and simulation seeds S1–S4.
- **v1.0 (15 Oct 2026, earlier):** search-index-only dossier (archived).
