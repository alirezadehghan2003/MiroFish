# Source Log: The HVN Study (Phase 0)

**Compiled:** 15 October 2026. Every source used in `dossier.md`, `website-audit.md`, `competitors.md`, `personas.md` and `seeds/`.

## A. Access method and limits
| Route | Status from this environment (15 Oct 2026) | Used for |
|---|---|---|
| `https://the-hvn.com` via plain HTTP client | **Reachable**; rate-limits parallel requests (HTTP 429), so crawled sequentially with back-off | All [LIVE] evidence |
| `https://the-hvn.com` via headless Chromium (Playwright) | **HTTP 403** (bot protection) | Not used; mobile render marked [NEEDS TESTING] |
| `www.the-hvn.com` | Blocked by environment proxy | 2 internal links unchecked |
| Competitor sites, `cqc.org.uk`, `asa.org.uk`, review platforms, `partner.pabau.com` | **Blocked** (DNS/proxy) | Not loaded; evidence via web search only |
| Web search (engine summaries + result URLs) | Available | Competitor, press, regulator and market evidence |

## B. The HVN, live (crawled 15 Oct 2026)
- Sitemaps: `/sitemap_index.xml` → page (173 URLs), post (30), product (14), plus category, tag and author sitemaps. Page sitemap last modified range 2024-12-06 to 2026-07-23.
- Full per-page data: `hvn-live-crawl-2026-10-15.csv` (216 URLs). Prices: `hvn-price-register-2026-10-15.csv` (342 rows, 148 pages). Links: `hvn-broken-links-2026-10-15.csv`.
- Key pages cited: [/](https://the-hvn.com/), [/about/](https://the-hvn.com/about/), [/contact/](https://the-hvn.com/contact/), [/the-expert-team/](https://the-hvn.com/the-expert-team/), [/consultations/](https://the-hvn.com/consultations/), [/discovery-consultation/](https://the-hvn.com/discovery-consultation/), [/8r-longevity-programme-levitas/](https://the-hvn.com/8r-longevity-programme-levitas/), [/iv-infusions/](https://the-hvn.com/iv-infusions/), [/nad-iv-infusion/](https://the-hvn.com/nad-iv-infusion/), [/immunity-iv-infusion/](https://the-hvn.com/immunity-iv-infusion/), [/muscle-relaxing-injections/](https://the-hvn.com/muscle-relaxing-injections/), [/menopause/](https://the-hvn.com/menopause/), [/pcos/](https://the-hvn.com/pcos/), [/premenstrual-dysphoric-disorder/](https://the-hvn.com/premenstrual-dysphoric-disorder/), [/concerns/fatigue-and-burnout/](https://the-hvn.com/concerns/fatigue-and-burnout/), [/hru-health-performance-assessment/](https://the-hvn.com/hru-health-performance-assessment/), [/hydrobed-reset-massage/](https://the-hvn.com/hydrobed-reset-massage/), [/terms-of-service/](https://the-hvn.com/terms-of-service/), [/functional-medicine-programmes-2/](https://the-hvn.com/functional-medicine-programmes-2/).

## C. Press and trade (via search, 15 Oct 2026)
| Source | Date | Used for | Label |
|---|---|---|---|
| [Cosmetics Business: former Paco Rabanne CEO opens wellness retreat](https://cosmeticsbusiness.com/former-paco-rabanne-ceo-opens-new-wellness-retreat) | 2023 | Opening, founder background | TRADE/PRESS |
| [Globetrender: The HVN "conscious wellbeing"](https://globetrender.com/2024/08/22/the-hvn-is-a-spa-that-promotes-conscious-wellbeing/) | Aug 2024 | 2024 positioning, Fotona, HBOT | TRADE/PRESS |
| [Brummell Magazine](https://www.brummellmagazine.co.uk/discover/a-holistic-cutting-edge-approach-to-wellbeing-is-on-offer-at-the-hvn/) | 2024 | Facilities, Hydrobed "UK's only" | TRADE/PRESS |
| [A Lady in London blog](https://www.aladyinlondon.com/2025/06/weekend-in-knightsbridge.html) | Jun 2025 | Single negative anecdote (skin analysis / upsell) | TRADE/PRESS (anecdote) |
| [Maybourne: Surrenne launch press release (PDF)](https://www.maybourne.com/globalassets/press-releases/pdfs/surrenne_-launch-press-release_april-2024.pdf) | Apr 2024 | Surrenne launch | OFFICIAL-PR |
| [Globetrender: Surrenne](https://globetrender.com/2024/02/19/surrenne-is-a-next-gen-longevity-spa-in-london/) | Feb 2024 | Surrenne longevity offer, price | TRADE/PRESS |
| [The Sybarite: Surrenne](https://thesybarite.co/surrenne-london-wellbeing-club) | 2024 | Opening date | TRADE/PRESS |
| [Welltodo: Maybourne × Virtusan](https://www.welltodoglobal.com/?p=11777) | 2024 | Longevity lounge partner | TRADE/PRESS |
| [Fabric Magazine: Lanesborough](https://fabricmagazine.co.uk/style-and-wellbeing/join-the-club/) | undated | Membership price (conflicting) | TRADE/PRESS |
| [Diplomat Magazine: Lanesborough Club & Spa](https://diplomatmagazine.com/the-lanesborough-club-spa/) | undated | Membership range, cap | TRADE/PRESS |
| [Business Traveller: Lanesborough spa review](https://www.businesstraveller.com/tried-tested/spa-review-lanesborough/) | — | Positioning | TRADE/PRESS |
| [Attractions Mgmt: Harrods Wellness Clinic](https://www.attractionsmanagement.com/attractions-news/Harrods-Wellness-Clinic-aesthetic-dermatology-spa/332097) | 2017 | Clinic format | TRADE/PRESS |
| [Business Wire: REVIV at Harrods](https://www.businesswire.com/news/home/20221219005425/en/REVIV-Launches-an-Opulent-New-Clinic-in-Harrods-and-a-First-in-an-Exclusive-IV-Therapy-Infusion) | Dec 2022 | IV concession | OFFICIAL-PR |
| [Attractions Mgmt: Clinique La Prairie at Harrods](https://www.attractionsmanagement.com/attractions-news/Clinique-La-Prairie-launches-in-Londons-iconic-Harrods-store/351418) | 2023 | Longevity consultation | TRADE/PRESS |
| [Spa Business: Clinique La Prairie × Mandarin Oriental Hyde Park](https://www.spabusiness.com/wellness-news/Clinique-La-Prairie-creates-exclusive-longevity-journeys-for-Mandarin-Oriental-Hyde-Park-London/351075) | 2023 | Knightsbridge hotel longevity | TRADE/PRESS |
| [Spa Business: HUM2N opens at Six Senses London](https://www.spabusiness.com/wellness-news/HUM2N-opens-longevity-clinic-at-Six-Senses-London/363082) | 12 Jun 2026 | HUM2N expansion | TRADE/PRESS |
| [Luxury Travel Advisor: Six Senses London opens](https://www.luxurytraveladvisor.com/hotels/six-senses-london-opens-whiteley) | Mar 2026 | Six Senses Place | TRADE/PRESS |
| [Vingt Sept: Lanserhof at The Arts Club](https://www.vingtseptmagazine.com/post/the-lanserhof-at-the-arts-club-the-detox-spa-the-a-list-trust) | 2022 | Membership price | TRADE/PRESS |
| [Pillar Wellbeing press release (Journal des Palaces)](https://www.journaldespalaces.com/en/pressrelease-76619-pillar-wellbeing-announces-three-month-transformation-programme-at-raffles-london-at-the-owo.html) | 2026 | £15,500 12-week programme | OFFICIAL-PR |
| [Globetrender: Raffles £15k transformation](https://globetrender.com/2026/01/06/raffles-london-15k-transformed-three-months/) | Jan 2026 | Same | TRADE/PRESS |
| [Spear's: Hooke](https://spearswms.com/luxury/health-wellness/hooke-health-clinics-super-rich-live-longer-longevity-wellness/) | Jan 2025 | Hooke pricing | TRADE/PRESS |
| [Four Seasons press: spa & wellness memberships](https://press.fourseasons.com/london/hotel-news/2026/spa-and-wellness-memberships) | 2026 | Substitute | OFFICIAL-PR |
| [Marie Claire: aesthetics clinics](https://www.marieclaire.co.uk/beauty/skincare/best-aesthetics-clinics) | — | Taktouk awards | TRADE/PRESS |
| [Consentz: Taktouk Clinic](https://www.consentz.com/directory/clinics/london/clinic/taktouk-clinic/) | — | Price on request; CQC Good (Mar 2023) | DIRECTORY |
| [TreatCompare: Menopause Clinic London](https://www.treatcompare.com/providers/menopause-clinic-london) | 2026 | £185–£275 consultations | DIRECTORY |
| [WhatClinic: Zita West](https://www.whatclinic.com/fertility/uk/london/zita-west) | — | Fertility acupuncture from £90 | DIRECTORY |
| [Doctify: Dr Ash Kapoor](https://www.doctify.com/uk/specialist/ash-kapoor) | — | Levitas "10R" naming | DIRECTORY |

## D. Regulators and market
| Source | Used for | Label |
|---|---|---|
| [ASA: Healthcare, intravenous nutritional therapy (advice)](https://asa.org.uk/advice-online/healthcare-intravenous-nutritional-therapy.html) | IV claim rules | REGULATOR |
| [ASA ruling: Get A Drip Ltd](https://asa.org.uk/rulings/get-a-drip-ltd-a19-549582-get-a-drip-ltd.html) · [REVIV UK Ltd](https://www.asa.org.uk/rulings/reviv-uk-ltd-a19-562605-reviv-uk-ltd.html) | Precedent (Dec 2023) | REGULATOR |
| [CQC provider page: The HVN Wellbeing Ltd](https://www.cqc.org.uk/provider/1-22154280768/services) | Registered, not yet inspected (v1; not re-verifiable) | REGULATOR (V1) |
| [Clyde & Co: non-surgical cosmetic procedures (2026)](https://www.clydeco.com/en/insights/2026/05/non-surgical-cosmetic-procedures) · [Mishcon de Reya](https://www.mishcon.com/news/non-surgical-aesthetic-treatments-do-they-need-better-regulation) | Licensing status in England | TRADE/PRESS (legal commentary) |
| [Global Wellness Institute: UK report](https://globalwellnessinstitute.org/press-room/press-releases/wellness-economy-reort-uk-2024/) | UK wellness economy | TRADE/PRESS |

## E. Carried from v1 (not re-verifiable on 15 Oct 2026)
HUM2N NAD/HBOT/programme prices; Harrods Wellness Clinic prices (pages ~1,350 days old); Lanesborough treatment prices; Lanserhof 2022 price list; IV Drip Clinic London (directory); The Online GP prices. See `../archive/dossier-v1-2026-10-15.md` §4.2 for the original URLs.
