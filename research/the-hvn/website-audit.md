# The HVN: Website Audit (live)

**Audit date:** 15 October 2026 · **Site:** https://the-hvn.com (WordPress on Apache; booking via Pabau)
**Coverage:** all 216 sitemap URLs fetched, plus 45 internal link targets not in the sitemap. 290 unique internal link targets analysed.
**Data:** `evidence/hvn-live-crawl-2026-10-15.csv` (per-page metrics), `evidence/hvn-broken-links-2026-10-15.csv`, `evidence/hvn-price-register-2026-10-15.csv`.
**Labels:** findings are **[LIVE]** unless marked. Recommendations are analyst judgement. Regulatory points are flagged for qualified review, **not** legal findings.

### Method limits
- **Mobile rendering and booking flow could not be tested.** The site returned **HTTP 403 to an automated headless browser** (bot protection) from this network, and the Pabau booking domain is blocked by the environment. Both are **[NEEDS TESTING]** on a real phone. Mobile findings below are static (from HTML).
- Crawling was rate-limited (HTTP 429) and done sequentially with back-off. No pages were missed.

---

## 1. Scorecard

| Area | Rating | Headline |
|---|---|---|
| Crawl health (sitemap) | 🟢 Good | 212 × 200; no broken sitemap URLs except a redirect into a 404 (W3) |
| Internal links | 🔴 Poor | **19 broken internal links**, including **2 menu links on every page**; 22 links go through redirects |
| Service discovery | 🔴 Poor | Programme tier gone; women's-health pages show acne treatments; orphan functional-medicine page |
| Messaging consistency | 🟠 Mixed | "London's leading Wellness & Longevity Clinic" vs "Skin & Hair" titles; positioning drift |
| Pricing transparency | 🟢 Strong | 149 of 151 service pages show prices |
| Trust signals | 🟠 Mixed | CQC badge everywhere but unlinked; Google reviews on 157/212 pages; two phone numbers |
| Claims risk | 🔴 Review | Immune or "boost" wording on 19/20 IV/IM pages; "Fat Burner" IV; prescription-medicine naming with prices |
| SEO technical | 🟠 Mixed | Clean titles and canonicals; no clinic/local schema; 4D/5D mismatch; generic women's-health titles |
| Mobile (static) | 🟠 Mixed | Viewport and lazy-loading on all pages; **click-to-call on 1 of 212 pages**; heavy pages (median 713 KB HTML, 55 images) |
| Booking friction | ⚪ Untested | Pabau link on every page; flow [NEEDS TESTING]; terms: card on file, 24 h cancellation |

---

## 2. Findings and recommendations (prioritised)

Priority: **P1** fix within 2 weeks (revenue, trust or compliance exposure) · **P2** within 30–60 days · **P3** backlog.

### W1 · P1 · Women's-health pages recommend acne treatments
- **Evidence:** `/menopause/`, `/pcos/` and `/premenstrual-dysphoric-disorder/` each say "At The HVN, we provide expert, evidence-based care…", then an "OUR AVAILABLE TREATMENTS" block headed "Explore our specialised solutions for **rosacea, acne, and acne scarring**", listing Fotona Active Acne (£475), Acne Scarring (from £600), ZO peel, microneedling, exosomes and HydrO2. The block is copied from `/concerns/rosacea-acne-and-acne-scarring/` (the only other page carrying it).
- **Impact [HYPOTHESIS]:** for the women's-health segment (P4), the page appears to sell acne lasers for menopause. This undermines the "evidence-based" promise and wastes relevant demand.
- **Fix:** replace the block with the real pathway: women's-health doctor consultation, menopause/hormone acupuncture (from £200), relevant blood profiles, fertility panel (£500). Rename titles from "Menopause - The HVN" to e.g. "Menopause Support in Knightsbridge, London | The HVN".

### W2 · P1 · Site-wide menu links are broken
- **Evidence:** `/clinical-treatments/` ("Clinical Treatments") and `/holistic-rituals/` ("Holistic Rituals") are linked from all 212 pages and return **404** (re-checked twice).
- **Fix:** point them at `/treatments/` filters or create the hub pages; add 301s for both paths.

### W3 · P1 · The programme tier has vanished; the functional-medicine route dead-ends
- **Evidence:**
  - 404: `/hvn-360-proactive-health-programme/`, `/hvn-sleep-rest-recover-de-stress-programme/`, `/hvn-skin-prevent-rejuvenate-restore-programme/`, `/hvn-body-rebalance-reshape-programme/`, `/anti-jetlag-programme/`, `/hyperbaric-oxygen-therapy/`, `/pages/hyperbaric-oxygen-therapy`.
  - `/functional-medicine/` 301-redirects to `/functional-medicine-programmes-2/`, titled "Functional Medicine Programmes Updated", with **no H1, no meta description, no prices**, **not in the sitemap**. It looks like an unfinished draft.
  - The Discovery Consultation (£350) promises "£100 redeemable against future Functional Medicine Packages", but no package is described or priced anywhere.
  - Hyperbaric oxygen, a 2024 press highlight, appears on no live service page.
- **Impact [HYPOTHESIS]:** the highest-value journey (consultation → plan) has no visible destination, and old programme URLs still circulating in press and search lead to 404s.
- **Fix:** decide which programmes exist. Publish them with "from" prices, or a clear "priced after consultation, typically £X–£Y" range. 301 each retired URL to its nearest live equivalent. Remove or finish the "Updated" page.

### W4 · P1 · Health-claim wording needs regulatory review
- **Evidence:**
  - "Immune/immunity" wording on 16 of 20 IV/IM pages and "boost" wording on 18 of 20 (19 of 20 have one or both; only Hydration has neither), e.g. Immunity IV: "enhances your body's ability to fight off infections and inflammation".
  - NAD: "cellular repair … healthy ageing".
  - Glutathione: "anti-ageing", "detoxification".
  - Product names "Fat Burner IV" and "Under the Weather".
  - `/muscle-relaxing-injections/` names the medicine ("botulinum toxin") alongside a per-area price table.
  - The site-wide superlative "London's leading Wellness & Longevity Clinic".
- **Context [REGULATOR]:** ASA guidance says IV nutritional therapy must not make medicinal claims and that immune-boosting claims have been ruled problematic ([ASA IVNT guidance](https://asa.org.uk/advice-online/healthcare-intravenous-nutritional-therapy.html)). UK rules restrict advertising prescription-only medicines to the public. Superlatives need substantiation.
- **Positive [LIVE]:** IV bookings include "a brief 10 minute consultation with one of our doctors", which is good practice worth featuring.
- **Fix:** commission a CAP-code review of all IV/IM, injectables and superlative wording **before** any paid media or simulation-derived messaging goes live. This audit makes no legal determination.

### W5 · P2 · Positioning is inconsistent across titles and copy
- **Evidence:**
  - Home title: "Wellness & Longevity Clinic London | Acupuncture | The HVN". About: "Integrative Wellness & Longevity Clinic". Contact: "Expert **Skin & Hair** Clinic Support". Booking: "Book Your **Skin & Hair** Treatment Appointment".
  - "Conscious wellbeing / luxury" (2023–24 brand idea) now appears only on `/sustainability-strategy/`.
  - The home H1 is "HOW THE HVN CAN HELP" (no category or proposition).
- **Fix:** one proposition line, used consistently in the home H1, About and the titles of Contact and Booking. Messaging is tested in S3 before being chosen.

### W6 · P2 · Internal link and redirect hygiene
- **Evidence:** 19 internal links → 404 (full list in `evidence/hvn-broken-links-2026-10-15.csv`). Examples:
  - `/visia-skin-analysis/` (linked from the Discovery Consultation page);
  - `/scalp-mesotherapy/`, `/fotona-refresh-revitalise-peel/` (5 pages);
  - `/reflexology-ritual-face-hands-feet/` (6 pages);
  - `/smootheye-lift/`, `/vitamin-iv-infusion/`, `/anti-burnout-consultation/`.
- **Redirect into a 404:** sitemap URL `/fotona-3d-peel/` → 301 → `/fotona-refresh-revitalise-peel` → 404.
- **22 links rely on redirects**, including three on every page: `/body-rituals/`, `/hair-tonic-iv-infusion/`, and the misspelt `/hru-health-performance-assesssment/` (210 pages).
- **Fix:** update menu and in-body links to final URLs; fix the 3D-peel chain; add a 404 monitor.

### W7 · P2 · Trust signals are present but not working hard enough
- **Evidence:**
  - "CQC Regulated" badge image on 212/212 pages, **linking to the CQC register on 0**. CQC status: registered, not yet inspected [V1, REGULATOR; not re-verifiable here].
  - Google-reviews widget on 157/212 pages; rating and count are not in page HTML (script-rendered).
  - Two phone numbers: 020 8015 7987 (home, contact, booking, concerns) and 020 7160 0003 (About).
  - Press links (Forbes, Condé Nast Traveller, Hello!, City A.M., Elite Traveller, Quintessentially) on 157/212 pages.
  - The Medical Director's credentials (BM MRCGP DCH DRCOG) appear on the team page.
- **Fix:**
  - Link the badge to the CQC profile and state "Registered with the CQC; first inspection pending".
  - Show the review rating in HTML with Review/AggregateRating schema (if the platform's terms allow).
  - Use one phone number.
  - Put a short "Who will treat me" doctor credential strip on consultation and IV pages.

### W8 · P2 · The step from first visit to plan is unpriced
- **Evidence:**
  - Consultations £175 / £350 / £400 and diagnostics £60–£750 are all priced. After that, only 8R "from £3,000" is published.
  - The same NAD+ service shows **£375 / 60 min** on `/concerns/fatigue-and-burnout/` and **£350 / 90 min** on `/nad-iv-infusion/`.
- **Fix:** publish indicative plan ranges and a defined first-step bundle (tested as hypothetical S2b), and align duplicate price displays.

### W9 · P2 · No clinic or local structured data
- **Evidence:** schema on all pages is Organization / WebSite / WebPage / BreadcrumbList (generated by the Yoast SEO plugin, present on 212/212 pages). **No** `MedicalClinic`, `MedicalBusiness` or `LocalBusiness`, no `openingHours`, no `address` or `geo`, no `Service` or `Offer` on treatment pages (`Offer` only on 13 shop products). `Person` schema on 29 pages.
- **Fix:** add `MedicalClinic` with address, geo, hours, phone and `sameAs`, plus `Service`/`Offer` on service pages and `Physician` for the clinicians.

### W10 · P2 · Mobile friction (static evidence)
- **Evidence:**
  - Viewport meta on 212/212 ✓; image lazy-loading on 212/212 ✓.
  - **A `tel:` click-to-call link on only 1 of 212 pages**; no live chat; WhatsApp mentioned on 18 pages.
  - Median page HTML 713 KB (max 1.1 MB), median 55 images per page.
- **Impact [HYPOTHESIS]:** concierge-style clients on phones (P6, P9) can't tap to call from service pages. Heavy HTML may slow first render on mobile networks.
- **Fix:** sticky mobile bar with "Call" and "Book"; trim inline markup and repeated press-logo blocks; run Lighthouse / Core Web Vitals from a normal connection [NEEDS TESTING].

### W11 · P3 · Metadata details
- 6 titles over 60 characters, two with a doubled brand ("| The HVN - The HVN").
- `/fotona-5d-lift/` title says "Fotona **4D**" while the H1 says "Fotona 5D®" (unchanged since v1).
- Missing meta descriptions on `/scalp-prp-platelet-rich-plasma/` (service page), `/my-account/`, `/thank-you/`.
- One duplicated meta description (polynucleotides pages).
- No duplicate titles; canonicals consistent on every page.

### W12 · ⚪ Booking flow [NEEDS TESTING]
- **Known [LIVE]:**
  - A Pabau online-booking link (`partner.pabau.com/online-bookings/the-hvn`) on every page, plus a separate `/book-now-acupuncture/` page.
  - Terms: a card is needed to confirm and 24 hours' notice is needed to cancel.
- **Unknown:** number of steps; whether consultations, IV and programmes are bookable online; deposit amounts; mobile usability; confirmation emails.
- **Test:** one mobile and one desktop booking, stopping before payment, for (a) the £350 Discovery Consultation and (b) a NAD infusion.

---

## 3. Service discovery map

| Journey | Entry page | Next step shown | Gap |
|---|---|---|---|
| Fatigue / burnout (P1) | `/concerns/fatigue-and-burnout/` | NAD £375, nutrition consultation £350, acupuncture, rituals | No priced plan; NAD price conflicts with the NAD page |
| Longevity (P2) | `/8r-longevity-programme-levitas/`, blood profiles, HRU | 8R from £3,000 | No annual or membership option; HBOT gone |
| Aesthetics (P3) | 50+ face and body pages | £175 consultation, per-treatment prices | Strong; minor broken links (VISIA, SmoothEye) |
| Women's health (P4) | `/menopause/`, `/pcos/`, `/premenstrual-dysphoric-disorder/` | **Acne treatments (wrong)** | W1 |
| Fertility (P5) | `/acupuncture-for-fertility-ivf/`, `/fertility-panel/` | Acupuncture from £200; fertility panel £500 | Course pricing only on some pages (from £1,620) |
| Visitor (P6) | Jet Lag IV, Hydrobed | Single treatments | No visitor package; no click-to-call |
| Functional medicine | `/functional-medicine/` | Redirects to an unfinished page | W3 |
| Navigation | Menu "Clinical Treatments", "Holistic Rituals" | **404** | W2 |
