# Phase 4 · Conversion Measurement Specification (GA4, Search Console, booking system)

**Version:** 1.0, 15 October 2026 · **Status:** specification only. **Nothing has been installed or changed.**
**Files:**
- `measurement/event-dictionary.csv`: every event, its trigger, parameters and privacy rule.
- `measurement/page-group-mapping-draft.csv`: 216 URLs classified into page types and service lines by rule. **Draft, needs review.**

> **No integration is claimed to be active.** §2 lists exactly what was observed in the public HTML and what could not be verified.

## 1. Measurement goals

| Question | Primary KPI | Recommendations it serves |
|---|---|---|
| Do service pages produce booking intent? | Booking-intent rate | R01, R06, R13 |
| Do fixes remove dead ends? | 404 page views; nav clicks on broken items | R02 |
| Does price clarity change behaviour? | Booking-intent rate on priced vs unpriced pathways; price-question enquiries | R08, R10, R11 |
| Does intent become real bookings and plans? | Booking completions; consultation-to-plan conversion | R03, R11, R20 |
| Does search bring the right demand (e.g. menopause)? | Clicks and impressions by page group and query theme | R01, R17, R18 |

## 2. Current state: what was verified on 15 Oct 2026

| Item | Observation | Status |
|---|---|---|
| Google Tag Manager | Container ID **`GTM-N7X2W4QF`** appears in the `<noscript>` iframe on every sampled page | **Present in HTML.** The JavaScript loader is not visible in the static HTML (the site uses a page-optimisation plugin that may defer or encode scripts). **Whether GTM fires, and which tags it holds, is unverified**: googletagmanager.com is blocked here |
| GA4 | No `G-` measurement ID and no `gtag()` in the static HTML | **Unknown.** GA4 may be configured inside GTM. Verify in GTM/GA4 admin |
| Universal Analytics | No `UA-` ID | Not present (and retired by Google in any case) |
| Search Console | `<meta name="google-site-verification" …>` on the home page | **A verification tag exists.** Which property it verifies, who has access, and whether data is used is **unknown** |
| Cookie consent | **No consent banner or consent-management platform found in the static HTML.** The cookie policy describes acceptance cookies, and the privacy policy mentions Facebook/Instagram ads "based on your acceptance of cookies" | **Unverified.** A banner may be injected by JavaScript (e.g. through GTM). Must be checked in a normal browser. Analytics cookies need prior consent under UK PECR |
| Ad or other pixels | No Meta pixel (`fbq`) in the static HTML; TikTok/Instagram/Facebook appear only as profile links | Static HTML only |
| Reviews | Trustindex Google-reviews widget | Rating not in HTML |
| Enquiry forms | Gravity Forms IDs 1 (newsletter), 2 (book now), 4 (speak to an expert), 5 (contact), 15 (acupuncture packages); a `/thank-you/` page exists in the sitemap | Submission behaviour (AJAX vs redirect) **not tested** |
| Booking | Off-site on `partner.pabau.com` (blocked here) | **Whether Pabau pages carry The HVN's GTM/GA4, or pass on UTM parameters, is unknown** |

## 3. GA4 configuration (to implement after approval G4 and the consent check)

### 3.1 Property and data stream
- One GA4 property, web data stream for `https://the-hvn.com` (and `www` if used).
- **Consent:** a UK-compliant consent banner with **Google Consent Mode v2**. GA4 and any ad tags load only after consent. Basic-mode tags send no data before consent.
- Data retention 14 months. Google signals off unless approved. No user-ID (no logins).
- **Internal traffic filter** for clinic and agency IPs. Developer-traffic filter for testing.
- **Referral exclusions:** `partner.pabau.com` (if Pabau returns visitors to the site) and payment providers.

### 3.2 Custom dimensions (event scope)

| Dimension | Parameter | Values |
|---|---|---|
| Page type | `page_type` | home, service, concern, consultation, contact_booking, blog, shop, utility_policy (from `page-group-mapping-draft.csv`, after review) |
| Service line | `service_line` | aesthetics, iv_im, diagnostics_longevity, acupuncture_tcm, womens_health, wellness_rituals, consultations, editorial, retail, mixed |
| Booking category ID | `booking_category_id` | Pabau `category` value from the link |
| Booking group ID | `booking_group_category_id` | Pabau `groupCategory` value |
| CTA text | `cta_text` | Button text, upper-cased |
| Link position | `link_position` | header, hero, body, sticky_bar, footer |
| Form ID | `form_id` | 1, 2, 4, 5, 15 |

`page_type` and `service_line` are set by a GTM lookup table keyed on the page path, using the reviewed mapping file.

### 3.3 Events
See `measurement/event-dictionary.csv` (18 entries).

**Key events (conversions):**
- `booking_click`
- `package_click`
- `tel_click`
- `generate_lead`
- `whatsapp_click` (only once WhatsApp links exist)

**Secondary:** `email_click`, `gift_card_click`, `newsletter_signup`.

**GTM implementation notes:**
- **Booking links:** trigger "Click – Just Links" where Click URL contains `partner.pabau.com`. A custom JavaScript variable parses `category`, `groupCategory`, `serviceType` and `prepaidType` from the URL. Route to `booking_click`, `package_click` or `gift_card_click`.
- **Phone, email, WhatsApp:** Click URL starts with `tel:` / `mailto:`, or contains `wa.me`.
- **Gravity Forms (AJAX):** a Custom HTML tag listens for `gform_confirmation_loaded` and pushes `{event: 'generate_lead', form_id}`. For redirect-style forms, use a page_view of the confirmation page. **Verify on staging first.**
- **404s:** trigger on the WordPress 404 template (confirm the body class or title).

### 3.4 Privacy rules (mandatory)
1. **Never send personal data to GA4.** No names, emails, phone numbers, free-text answers or form field values.
2. **Never send health detail as a parameter.** That includes the acupuncture "Treatment" choice (fertility, menopause) and site-search terms (until privacy sign-off).
3. Page URLs reveal health interest (e.g. `/menopause/`). **Exclude women's-health and fertility pages from any advertising remarketing audiences.** Get privacy sign-off before any ad pixel fires on condition pages.
4. Booking data from Pabau is analysed only **in aggregate**: no clinical notes and no client names in analytics exports.
5. Before tagging, update the privacy and cookie policies to list the actual tools. Note that the privacy policy names "The HVN Wellness Limited" while the site footer and contact page say "The HVN Wellbeing Ltd", and the policy's cookie link is malformed (`https://the-hvn/cookie-policy/`). Refer both to the data protection officer.

## 4. Funnel definitions

| ID | Funnel | Steps | Source | Notes |
|---|---|---|---|---|
| **F1** | Site booking intent | 1 `session_start` → 2 view a page where `page_type` ∈ {service, concern, consultation} → 3 any of `booking_click`, `package_click`, `tel_click`, `generate_lead` | GA4 funnel exploration (open funnel) | The main web KPI |
| **F2** | Women's health | 1 view a page where `service_line` = womens_health → 2 `booking_click` or `generate_lead` (form 4/5) or `tel_click` | GA4 | Before and after T01 |
| **F3** | Price to intent | 1 `price_block_view` → 2 `booking_click` within the session | GA4 | Optional; tests H01 |
| **F4** | Intent to booking (off-site) | 1 `booking_click` (GA4, by `booking_category_id`, by day) → 2 online bookings created in Pabau for that category and day | GA4 + Pabau export, joined on **date × category** (not per person) | Becomes per-session only if Pabau supports GA4/GTM and UTM pass-through (to be confirmed) |
| **F5** | Enquiry to booking | 1 enquiry logged (form, phone, email, WhatsApp) → 2 first response → 3 booked within 14 days | Enquiry log | Manual log (§6) |
| **F6** | Consultation to plan | 1 consultation completed (£175 / £350 / £400) → 2 plan, package, course or programme bought within 30 days by the same client | Pabau (internal, aggregated) | Core commercial KPI |
| **F7** | Retention | 1 first paid visit → 2 second paid visit within 90 days | Pabau | — |

## 5. KPI catalogue

| KPI | Formula | Source | Granularity | Baseline | Owner (role) |
|---|---|---|---|---|---|
| Booking-intent rate | (booking_click + package_click + tel_click + generate_lead) ÷ sessions | GA4 | Weekly; by page_type and service_line | **None yet**: 4 weeks after tagging | Marketing lead |
| Booking clicks per 100 service-page views | booking_click ÷ service-page page_views × 100 | GA4 | By service_line | None | Marketing lead |
| Women's-health intent rate | F2 step 2 ÷ step 1 | GA4 | Weekly | None | Marketing lead |
| 404 views | page_not_found count | GA4 | Weekly | None (expected high until T02) | Web developer |
| Online bookings | Count of bookings created online | Pabau | Weekly; by category; new vs returning | None | Operations lead |
| Click-to-booking ratio | Online bookings ÷ booking_click (same category and week) | GA4 + Pabau | Weekly | None | Analyst |
| Enquiry volume and reasons | Enquiries by channel and reason tag | Enquiry log | Weekly | None | Concierge lead |
| First-response time | Median minutes from enquiry to first reply (opening hours) | Enquiry log | Weekly | None | Concierge lead |
| Consultation-to-plan conversion | F6 step 2 ÷ step 1 | Pabau | Monthly; by consultation type | None | Operations lead + Finance |
| Late-cancel and no-show rate | (late cancels + no-shows) ÷ appointments | Pabau | Monthly | None | Operations lead |
| 90-day repeat rate | F7 | Pabau | Monthly | None | Operations lead |
| Organic clicks by page group | Search Console clicks (regex page filters) | Search Console | Weekly | Available historically once access is granted | Marketing lead |
| Women's-health query impressions | Impressions for queries matching menopause, perimenopause, PCOS, PMDD, hormone, fertility | Search Console | Monthly | Historical | Marketing lead |
| Review volume and rating | New reviews per month; average | Google Business Profile | Monthly | Unknown | Marketing lead |

**Targets are set only after the 4-week baseline.**

## 6. Search Console specification
1. **Confirm access:** who owns the property verified by the meta tag. Recommend a **Domain property** (`the-hvn.com`) covering `www` and `https`.
2. **Sitemaps:** confirm `/sitemap_index.xml` is submitted. Check the Pages report for the 27 known 404s and for the redirect chains.
3. **Saved comparisons and regex page filters:**
   - Women's health: `/(menopause|pcos|premenstrual-dysphoric-disorder|acupuncture-for-(perimenopause-menopause|female-hormonal-health|fertility-ivf)|womens-health|hormonal-balance|fertility-panel|ivf-and-fertility)`
   - IV/IM: `iv-infusion|-iv-|im-(shot|injection)|nad`
   - Diagnostics: `profile|panel|hru|blood`
   - Consultations: `consultation`
4. **Query themes:** menopause, perimenopause, HRT, PCOS, PMDD, fertility acupuncture, NAD, IV drip Knightsbridge, Fotona, brand.
5. **After T02/T07/T10:** annotate release dates, then check Pages (404s fall) and Performance (click-through rate on retitled pages).
6. **Export:** use the Looker Studio connector (free). BigQuery bulk export only with approval (possible cost).

## 7. Booking system (Pabau) data requirements
Pabau could not be accessed. These are **requests to the booking-system administrator**, not findings.

| # | Question or export | Why |
|---|---|---|
| P1 | Which service each online-booking `category` ID opens: at least 194249, 194250, 196297, 196299, 196302, 196307, 195070, 195471 and groups 15717, 15726, 15757 | Make `booking_category_id` readable; confirm whether the menopause/PCOS/PMDD buttons open the aesthetic consultation (B1) |
| P2 | Can the online-booking pages load GTM/GA4, and are UTM parameters kept? | Decides whether F4 can be per-session |
| P3 | Monthly export (aggregated, de-identified): bookings by category × channel (online/staff/phone) × new/returning × status (completed, cancelled, late-cancel, no-show) | Baseline for bookings and no-shows |
| P4 | Consultation-to-plan: for consultations completed in the last 12 months, the share of clients who bought a plan, course, package or treatment within 30 / 90 days, and median value. Counts and values only | F6 baseline; R11 ranges |
| P5 | Is IV bookable online? (`/book-now/` says no; IV pages link to Pabau) | Fix B2 |
| P6 | What the card step and confirmation email say about the 100% cancellation charge | R09 |
| P7 | Package and voucher sales by month (counts) | `package_click` / `gift_card_click` validation |

**Data handling:** exports are produced inside The HVN by authorised staff. Analysts receive **aggregated tables only**: no names, contact details, dates of birth, clinical notes or free text. Store them in the HVN's own drive.

## 8. Enquiry log (template: `04-research-kit/templates/enquiry-log.csv`)
- **Fields:**
  - pseudonymous enquiry ID;
  - date and time received;
  - channel;
  - source page (if a form);
  - service line;
  - reason tags (price/total, fee credit, practitioner, CQC/safety, availability, evidence or suitability, other);
  - time of first response;
  - outcome (booked / pending / lost + reason);
  - date booked.
- **No names, phone numbers, emails or clinical details** in the analytic copy.

## 9. Verification and QA before go-live (after approval)

| # | Check | Pass criterion |
|---|---|---|
| V1 | GTM container access confirmed; current tags documented | Tag list exported |
| V2 | GA4 property identified (or created) and access granted | Property ID recorded here |
| V3 | Consent banner present; Consent Mode v2 states correct | No GA4 hit before "accept" (GTM preview + browser network panel) |
| V4 | Each event in `event-dictionary.csv` fires once per action in GTM preview | 100% of events pass |
| V5 | No PII in any hit | Network inspection of 20 sample hits: no email, phone, name or free text |
| V6 | DebugView shows custom dimensions populated | page_type and service_line on ≥ 95% of page_views |
| V7 | Key events marked in GA4 | 4–5 key events listed |
| V8 | Search Console access and sitemap confirmed | Screenshot |
| V9 | Pabau P1–P7 answered | Responses filed |
