# Phase 4 · Booking Journey Audit (non-transactional)

**Date:** 15 October 2026 · **Scope:** the public route from a service page to the booking platform, on desktop and mobile, as far as it was technically reachable.
**Rules followed:**
- No booking was started or submitted and no payment was made.
- No form was submitted and no personal or patient data was entered.
- Nobody was contacted.

**Evidence:**
- `evidence/site-recheck-2026-10-15.json` (30 pages: status, booking calls-to-action and their booking-link settings, `tel:` links, form IDs, tag markers);
- `evidence/broken-links-recheck.csv` (every previously broken or retired URL, re-checked today).

Raw HTML is not committed.

## 1. What could and could not be accessed

| System | Attempt (15 Oct 2026) | Result | Consequence |
|---|---|---|---|
| the-hvn.com, plain HTTP client | 30 key pages fetched, one at a time, 2.5 s apart | **Accessible (HTTP 200).** Static HTML only | Website side of the journey audited from page source |
| the-hvn.com, headless Chromium (desktop 1366×900 and an iPhone 13 profile) | `/`, `/menopause/`, `/book-now/` | **Refused** (`ERR_HTTP_RESPONSE_CODE_FAILURE`; the site's bot protection, as in the earlier 403s) | **No rendered desktop or mobile screens, no screenshots, no JavaScript behaviour.** I did not try to get round the protection |
| Pabau booking widget `partner.pabau.com/online-bookings/the-hvn` | curl, WebFetch and headless browser | **Blocked** (proxy tunnel refused / DNS failure) | **Nothing about the booking steps, service lists, deposits, card capture, cancellation wording or confirmation screens could be observed.** No results are reported for them |
| Google Tag Manager (`googletagmanager.com`) | Direct fetch | **Blocked** | The tag container's contents cannot be inspected (see the measurement spec, §2) |
| WhatsApp, phone, email | — | Not used (no contact allowed) | Response handling is untested |

**Everything below is limited to what the HTML of the-hvn.com shows.** The booking platform steps are listed in §6 as a test script for a person with normal browser access, once you approve gate G1.

## 2. Entry points to booking (verified in page source)

| Entry point | Where | Destination | Notes |
|---|---|---|---|
| "BOOKINGS" (menu) and "Bespoke Consultations" | All 30 sampled pages | Pabau, with no service pre-selected (and `?groupCategory=0`) | The visitor must find the service again inside Pabau |
| Page-specific "BOOK A CONSULTATION" / "BOOK YOUR TREATMENT" / "BOOK TREATMENT" | Service and consultation pages | Pabau links that pre-select a booking category (`category=…`, `groupCategory=…`) | Category IDs are internal Pabau codes; **what each opens could not be seen** |
| "BUY GIFT CARDS" | All pages | Pabau voucher flow (`prepaidType=voucher`) | — |
| "BOOK TREATMENT" on the practitioner-led acupuncture pages | `/womens-health-with-susan-gu/`, `/hormonal-balance-with-susan-gu/`, `/ivf-and-fertility-susan-gu/` | Pabau **prepaid package** flow (`prepaidType=package`) | Suggests packages can be bought online; unverified |
| Enquiry forms (Gravity Forms) | `/contact/` (form 5), `/book-now/` (form 2), `/book-now-acupuncture/` (form 15), "Speak to an expert" on the women's-health pages (form 4) | Form submission (not tested) | See §4 |
| Phone `020 8015 7987` | Shown as text on contact and booking pages | **Tap-to-call (`tel:`) link only on the home page** (1 of the 30 sampled pages) | On mobile the number can't be tapped on any service, contact or booking page |
| Email `concierge@the-hvn.com` | Contact and booking pages | `mailto:` link | — |

### 2.1 Where page-specific booking buttons point (selected)

| Page | Button | Booking link settings (verified) | Observation |
|---|---|---|---|
| `/aesthetic-consultation/` | BOOK A CONSULTATION | `serviceType=0&category=194249&groupCategory=15717` | Aesthetic consultation |
| `/discovery-consultation/` | BOOK A CONSULTATION | `serviceType=0&category=194250&groupCategory=15717` | Discovery consultation |
| **`/menopause/`, `/pcos/`, `/premenstrual-dysphoric-disorder/`** | BOOK A CONSULTATION / BOOK YOUR CONSULTATION | **`groupCategory=15717&category=194249&serviceType=0`** | **Same category ID as the Aesthetic Consultation button.** Combined with the acne-treatment block, this suggests women's-health visitors may be routed to an aesthetic consultation. **What category 194249 opens is unverified** (Pabau blocked) |
| `/acupuncture-for-perimenopause-menopause/`, `/acupuncture-for-female-hormonal-health/`, `/acupuncture-for-fertility-ivf/` | BOOK TREATMENT / BOOK A CONSULTATION | `category=196302` | Same category on all acupuncture pages |
| `/iv-infusions/`, `/nad-iv-infusion/` | BOOK YOUR TREATMENT | `category=196307` | **Conflicts with `/book-now/`**, which says "For treatments such as IV Infusions and IM Shots, please use our contact form below" |
| Home, `/concerns/fatigue-and-burnout/`, blood-profile pages, `/fertility-panel/` | BOOK A CONSULTATION | `category=196297` | Used widely; destination unknown |
| `/consultations/` | BOOK CONSULTATION (8R) | `category=196299` | — |

## 3. Desktop vs mobile (static evidence only)

| Check | Desktop | Mobile | Evidence |
|---|---|---|---|
| Booking links present | Yes, on every sampled page | Same HTML | Page source |
| Tap-to-call | n/a | **Missing** on 29/30 sampled pages; on 1/212 site-wide (crawl) | `tel:` count |
| Viewport meta, lazy-loading | — | Present on all pages | Crawl |
| Page weight | Median 713 KB HTML, 55 images | Same | Crawl |
| Rendered layout, sticky elements, menus, tap targets | **Not observed** | **Not observed** | Headless browser refused |
| Pabau on mobile | **Not observed** | **Not observed** | Blocked |

## 4. Enquiry forms (fields read from HTML; nothing submitted)

| Form | Page(s) | Fields | Observations |
|---|---|---|---|
| Contact (ID 5) | `/contact/` | First, Last, Email*, Phone*, "How can we help?"*, CAPTCHA | Free text may lead people to volunteer **health information**. **No consent or privacy-notice field in the form markup** |
| Book now (ID 2) | `/book-now/` | Same as above | The page tells IV/IM clients to use this form |
| Acupuncture package (ID 15) | `/book-now-acupuncture/` | Name, Email*, Phone*, Treatment* (7 options), "How many sessions…?"* (6 or 10), question | Packages are **bought through an enquiry form here**, but **through Pabau prepaid links** on the practitioner pages. Two routes |
| Speak to an expert (ID 4) | Menopause, PCOS (and PMDD) pages | Name, Email*, Phone* | No message field; no consent field in the markup |
| Newsletter (ID 1) | All pages | Email*, consent checkbox ("I agree with the storage and handling of my data… Privacy Policy") | Only form with a consent field |

## 5. Booking terms (verified on `/terms-of-service/`)

- A valid payment card must be stored before an appointment is confirmed. The card is charged only for late cancellation or a no-show.
- Less than 24 hours' notice: **100% of the reserved service amount** is charged. No-shows: **100%**.
- Appointments booked within 24 hours must be cancelled at least 4 hours before, or 100% is charged.
- Cancellations count only **by phone or via the booking platform** (not text, email or social media).
- Confirmation by email when booking, then text and email 48 hours before.
- Clients must be **18 or over**.
- The terms also contain US-specific boilerplate (DMCA notices, "U.S. federal government end user"). Flag for legal review; no legal conclusion is drawn here.

**Correction to earlier files.** `recommendations-register.md` R09 said the charge "in pounds" was unknown. The terms state it clearly as **100% of the service price**. What remains unknown is **whether the booking screen shows it** before the card is taken.

## 6. Findings

| # | Finding | Evidence | Confidence | Ticket |
|---|---|---|---|---|
| B1 | Women's-health "Book a consultation" buttons use the **same booking category as the Aesthetic Consultation** | §2.1 | High (link), Unknown (what it opens) | T01 |
| B2 | IV booking instructions **conflict**: IV pages link straight to Pabau, while `/book-now/` says IV and IM must go through the contact form | §2.1; `/book-now/` text | High | T10 |
| B3 | Acupuncture packages have **two purchase routes** (enquiry form vs Pabau prepaid package) | §2, §4 | High | T10 |
| B4 | No tap-to-call outside the home page | §3 | High | T06 |
| B5 | Generic "BOOKINGS" buttons drop visitors into Pabau with no service pre-selected | §2 | High (link); effect unknown | T10 |
| B6 | Enquiry forms invite free-text health details without a consent or privacy field in the form | §4 | High (markup) | T11 (privacy review) |
| B7 | The cancellation charge is clear in the terms (100%); its visibility at booking is unknown | §5 | High / Unknown | Test script below |
| B8 | Booking and Contact page titles still say "Skin & Hair" | Page titles | High | T10 |
| B9 | **Booking platform steps, deposits, card capture and mobile usability are unobserved** | §1 | — | Test script below (gate G1) |

## 7. Test script for the booking platform (needs approval G1; for a staff member or analyst with normal browser access)

**Rules:** use a test identity only if Pabau allows browsing without one; **stop before entering card details or confirming**; record screenshots; no patient data.

| Step | Desktop | Mobile (real phone) | Record |
|---|---|---|---|
| 1 | Open `/menopause/` → "BOOK A CONSULTATION" | Same | Which service list or category appears (does 194249 open the aesthetic consultation?) |
| 2 | Open `/discovery-consultation/` → "BOOK A CONSULTATION" | Same | Steps to reach a time slot; fields required before seeing availability |
| 3 | Open `/nad-iv-infusion/` → "BOOK YOUR TREATMENT" | Same | Is IV bookable online? (Conflicts with `/book-now/`) |
| 4 | Open `/womens-health-with-susan-gu/` → "BOOK TREATMENT" (package) | Same | Package price, sessions, terms shown? |
| 5 | Menu "BOOKINGS" | Same | Number of categories; can a first-time visitor find "menopause"? |
| 6 | Proceed to the card step **without entering a card** | Same | Is the 100% cancellation charge shown? Deposit? |
| 7 | Time each journey; count taps or clicks | Same | Steps, time, errors, dead ends |
| 8 | Check the confirmation-email template with the booking-platform admin (not by booking) | — | Content, cancellation wording |

Capture results in `04-research-kit/templates/booking-flow-test-log.csv`.
