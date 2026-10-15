# Phase 4 · Implementation-Ready Tickets (quick wins)

**Date:** 15 October 2026 · **Status of every ticket:** `READY FOR APPROVAL`. **Nothing has been deployed.** Machine-readable copy: `tickets.csv`.
**Evidence:**
- `evidence/site-recheck-2026-10-15.json` (30 pages re-fetched today);
- `evidence/broken-links-recheck.csv` (27 URLs re-checked today, all 404);
- `../evidence/hvn-price-register-2026-10-15.csv`.

**Common Definition of Done (applies to every ticket):**
- Change made on **staging** first.
- Peer-reviewed and approved by the named approver.
- Deployed in a low-traffic window, with a before/after screenshot of every affected URL.
- Re-crawl run, and release date annotated in GA4 and Search Console.
- Rollback = restore the previous WordPress revision, or remove the redirect rule.

| Ticket | Title | Rec | Priority | Approver(s) before deploy | Blocked by |
|---|---|---|---|---|---|
| T01 | Replace the wrong treatment block and booking route on Menopause, PCOS and PMDD | R01, R04 | P1 | Women's-health doctor (clinical); compliance adviser (CAP); management (deploy) | Clinical + compliance sign-off; booking category answer (P1) |
| T02 | Fix the two broken site-wide menu links | R02 | P1 | Marketing lead; management (deploy) | — |
| T03 | Fix 17 broken in-body links and the 3D-peel redirect chain; update 22 redirected links | R02 | P1 | Marketing lead | Content owner confirms targets |
| T04 | Redirect the 8 retired programme/HBOT URLs; resolve the orphan functional-medicine page | R03 | P1 | CEO + Medical Director (decision) | Programme decision |
| T05 | Link the CQC badge and add an accurate status line | R05 | P1 | Registered manager / compliance | **CQC verification checklist completed** |
| T06 | One phone number; tap-to-call everywhere; sticky mobile Call/Book bar | R06 | P1 | Operations lead (number); management (deploy) | Number decision |
| T07 | Make prices consistent and explain acupuncture formats | R10 | P1 | Operations lead (prices); marketing | Price-owner confirmation |
| T08 | Publish one consultation fees-and-credits table | R08 | P1 | CEO + Finance (policy) | Credit-policy decision |
| T09 | Measurement baseline: verify GTM/GA4/consent, then tag per spec; start enquiry log | R07, R19 | P1 | Data protection officer (consent); marketing (tags) | Access to GTM, GA4, Search Console, Pabau |
| T10 | Booking-route consistency (IV, packages, generic BOOKINGS) and "Skin & Hair" titles | N1, R15 (partial) | P1 | Operations lead (booking rules); marketing | Booking-system answers P1, P5 |
| T11 | Privacy and consent hygiene review | N2 | P1 | Data protection officer | — |

---

## T01 · Women's-health pages: wrong treatments and booking route

**Affected URLs:**
- https://the-hvn.com/menopause/
- https://the-hvn.com/pcos/
- https://the-hvn.com/premenstrual-dysphoric-disorder/

**Current issue and evidence (re-checked 15 Oct 2026):**
1. Each page shows the block "OUR AVAILABLE TREATMENTS · Explore our specialised solutions for rosacea, acne, and acne scarring", listing seven treatments:
   - Fotona Active Acne £475;
   - Fotona Acne Scarring from £600;
   - ZO Brightening Peel £185;
   - microneedling £450;
   - Exosome Therapy £500;
   - HydrO2 facial from £140;
   - SkinPen from £300.
2. The "BOOK A CONSULTATION / BOOK YOUR CONSULTATION" buttons link to Pabau `groupCategory=15717&category=194249`, **the same category as the Aesthetic Consultation page's button** (`02-booking-journey-audit.md` B1). What it opens is unverified.
3. Compliance flags for the claims review:
   - PCOS names **metformin** and "hormonal therapy";
   - PMDD names **SSRIs** and "specific birth control pills";
   - all three say "evidence-based care", and PCOS says "diagnosing and managing PCOS";
   - **whether The HVN actually offers these medical services is unverified.**
4. Titles are generic ("Menopause - The HVN", "PCOS - The HVN", "Premenstrual Dysphoric Disorder - The HVN").
5. The "Speak to an expert" form (Gravity Form 4: name, email, phone) has no consent or privacy field in its markup.

**Proposed change:**
- Replace the acne block and the "Why choose…" sections with the approved version of `06-draft-copy-womens-health.md`.
- Point the booking buttons at the clinically agreed route: menopause/hormonal acupuncture (`category=196302`, already used on the acupuncture pages), a doctor-led route **if one exists**, or the enquiry form.
- New titles and meta descriptions (in the draft).
- Remove prescription-medicine names unless the compliance adviser approves them.

**Responsible:**
- Content: Marketing lead.
- Clinical accuracy: women's-health doctor (and lead TCM practitioner for acupuncture text).
- Compliance: external CAP adviser.
- Build: web developer.

**Acceptance criteria:**
- [ ] No acne, rosacea or scarring treatments appear on the three pages.
- [ ] Every service listed exists on the live site, with the same price and duration as its own page.
- [ ] Booking buttons open a booking category or contact route confirmed by Operations, never the aesthetic consultation by default.
- [ ] Clinical and compliance sign-offs are recorded (name, role, date) in `08-approval-register.csv`.
- [ ] Titles ≤ 60 characters with a single brand mention; one meta description per page.
- [ ] No prescription-only medicine named unless approved in writing.

**QA checklist:**
- [ ] Desktop and real-phone screenshots of all three pages.
- [ ] Each "Discover"/"Book" link returns 200 and opens the intended destination.
- [ ] Prices match the price register (re-crawl).
- [ ] Gravity Form 4 still submits on staging (test data only, deleted afterwards).
- [ ] No layout breakage at 375 px width.

**Success metric:** women's-health intent rate (funnel F2) and booking clicks from these three pages vs a 4-week baseline; Search Console click-through rate for menopause/PCOS/PMDD queries after 6–8 weeks.

---

## T02 · Broken site-wide menu links

**Affected:** the header/footer menu template, so all 212 pages.

| Broken target (404 re-checked today) | Menu label | Proposed target (**candidate: content owner to confirm**) |
|---|---|---|
| https://the-hvn.com/clinical-treatments/ | Clinical Treatments | https://the-hvn.com/treatments/ (live) or a new hub page |
| https://the-hvn.com/holistic-rituals/ | Holistic Rituals | https://the-hvn.com/body-rituals-massages/ (live) or a new hub page |

**Proposed change:** update both menu items. Add 301s from the two broken paths to the chosen targets, so external links also resolve.

**Responsible:** web developer; marketing lead (targets).

**Acceptance criteria:**
- [ ] Both menu items return 200 on desktop and mobile menus.
- [ ] Both old paths 301 to the chosen targets.
- [ ] Re-crawl shows 0 links to either broken path.

**QA:**
- [ ] Test on 3 page templates (home, service, blog), on desktop and phone.
- [ ] Check the 301 with a header check (single hop).

**Success metric:** `page_not_found` views fall (GA4, after T09); `nav_click` on these items leads to engaged sessions.

---

## T03 · Broken in-body links (17) and redirect hygiene

**17 broken targets (all 404 on 15 Oct 2026), with linking pages and candidate fixes.** Candidates are suggestions from live URLs. **The content owner confirms each, or chooses "remove link".**

| Broken target | Linked from | Candidate replacement (verify) |
|---|---|---|
| /reflexology-ritual-face-hands-feet/ | /cellulite-lymphatic/, /concerns/, /concerns/chronic-stress-and-anxiety/, /concerns/fatigue-and-burnout/, /concerns/insomnia-and-poor-sleep/ (+1 page, find by re-crawl) | /reflexology/ |
| /fotona-refresh-revitalise-peel/ | /concerns/, /concerns/hyperpigmentation-sun-damage/, /transformative-bio-stimulating-peel/, /zo-brightening-peel/, /zo-restorative-peel/ | /peels/ |
| /scalp-mesotherapy/ | /concerns/, /laser-hair-restoration/, /scalp-prp-platelet-rich-plasma/ | /mesotherapy/ or /scalp-hair-health/ |
| /acupuncture-for-skin-health/ | /concerns/, /concerns/rosacea-acne-and-acne-scarring/ | /facial-acupuncture/ |
| /anti-burnout-consultation/ | /treatments/ | /concerns/fatigue-and-burnout/ or /discovery-consultation/ |
| /back-and-shoulders-massage/ | /concerns/ | /upper-body-tension-release-massage/ |
| /facial-threads/ | /concerns/ | /threads/ |
| /hvn-glass-skin-microinfusion-facial/ | /lumineo-led/ | /the-glass-skin-microinfusion-facial/ |
| /hvn-kansa-wand-facial/ | /face-or-decolletage-mask/ | No obvious match: remove link |
| /nourishing-facial-ritual/ | /lumineo-led/ | No obvious match: remove link |
| /pure-detox-ritual/ | /steam-bath/ | /purification-detox-ritual/ |
| /reflexology-ritual-mothers-journey/ | /concerns/post-pregnancy-changes/ | /new-mother-ritual/ |
| /shirodhara-sleep-therapy/ | /your-gut-is-the-gateway-to-good-health/ | Remove, or /concerns/insomnia-and-poor-sleep/ |
| /smootheye-lift/ | /fotona-vectorlift/ | /fotona-smootheye-lift/ |
| /soothing-sleep-ritual/ | /holistic-relaxation-in-the-heart-of-the-city/ | Remove, or /concerns/insomnia-and-poor-sleep/ |
| /visia-skin-analysis/ | /discovery-consultation/ | No VISIA page: remove link, or link /consultations/ |
| /vitamin-iv-infusion/ | /nad-therapy-for-mind-mood-and-longevity/ | /iv-infusions/ |

**Redirect into a 404:** sitemap URL https://the-hvn.com/fotona-3d-peel/ → 301 → `/fotona-refresh-revitalise-peel` → 404. Point it at the chosen peel page, or remove it from the sitemap.

**22 links that work only through redirects:** update them to their final URLs. Full list in `../evidence/hvn-broken-links-2026-10-15.csv` (classification "redirect"). The three on every page:
- `/body-rituals/` → `/body-rituals-massages/` (212 pages);
- `/hair-tonic-iv-infusion/` → `/hair-tonic-iv-infusion-1/` (212);
- `/hru-health-performance-assesssment/` (misspelt) → `/hru-health-performance-assessment/` (210).

**Responsible:** web developer; content owner for targets.

**Acceptance criteria:**
- [ ] Re-crawl: 0 internal links return 404.
- [ ] 0 internal links go through redirects, except intentional ones.
- [ ] `/fotona-3d-peel/` resolves in one hop or is removed from the sitemap.

**QA:**
- [ ] Re-run the link checker (the method in `evidence/`).
- [ ] Spot-check 10 changed links on a phone.

**Success metric:** internal 404s = 0; Search Console "Not found (404)" count falls over 4–8 weeks.

---

## T04 · Retired programme and HBOT URLs; orphan page

**Affected (all 404 on 15 Oct 2026):**
- https://the-hvn.com/hvn-360-proactive-health-programme/
- https://the-hvn.com/hvn-sleep-rest-recover-de-stress-programme/
- https://the-hvn.com/hvn-skin-prevent-rejuvenate-restore-programme/
- https://the-hvn.com/hvn-body-rebalance-reshape-programme/
- https://the-hvn.com/anti-jetlag-programme/
- https://the-hvn.com/hyperbaric-oxygen-therapy/
- https://the-hvn.com/pages/hyperbaric-oxygen-therapy
- https://the-hvn.com/pages/360-proactive-health-programme

**Orphan:** https://the-hvn.com/functional-medicine/ → 301 → https://the-hvn.com/functional-medicine-programmes-2/ ("Functional Medicine Programmes Updated": no H1, no meta description, no prices, not in the sitemap).

**Decision required (CEO + Medical Director):** which programmes exist today, and whether hyperbaric oxygen is still offered.

**Proposed change after the decision:**

| Old URL | If retired, redirect candidate | If still offered |
|---|---|---|
| 360 Proactive Health | /discovery-consultation/ or /8r-longevity-programme-levitas/ | Republish with price or range |
| Sleep, Rest, Recover | /concerns/insomnia-and-poor-sleep/ | Republish |
| Skin Prevent/Rejuvenate | /consultations/ | Republish |
| Body Rebalance/Reshape | /body-rituals-massages/ or a relevant concern page | Republish |
| Anti-Jetlag | /jet-lag-iv-infusion/ | Republish |
| Hyperbaric oxygen (×2) | 410 Gone, or the nearest concern page | Republish |
| /functional-medicine/ | Point at a finished page, or at /discovery-consultation/ | Finish the "Updated" page (H1, meta, prices or range) |

**Acceptance criteria:**
- [ ] Decision recorded.
- [ ] Each URL returns 200 (republished) or a single-hop 301/410.
- [ ] The orphan page is either finished and in the sitemap, or no longer reachable.
- [ ] The Discovery Consultation's "£100 redeemable against future Functional Medicine Packages" wording points to something that exists, or is changed (see T08).

**Success metric:** 0 retired 404s; consultation-to-plan conversion is tracked (F6).

---

## T05 · CQC badge link and accurate status line (**blocked until verification**)

**Affected:** site-wide badge (image alt "CQC Regulated", 212/212 pages, linked on 0); footer or trust area.

**Current issue:** the badge is decorative and links nowhere. The HVN's current CQC registration details, regulated activities and rating status are **unverified**. The earlier "registered, not yet inspected" came from a search result and must not be published without checking.

**Proposed change:**
- Complete `07-cqc-verification-checklist.md`.
- Then link the badge to the **location** page on cqc.org.uk.
- Add one line using only the verified facts, for example `Registered with the Care Quality Commission (location ID …) for [regulated activities]. [Rating and date | Not yet rated]`.
- If a rating exists, consider CQC's official ratings widget.
- Do not imply CQC covers services outside the registration.

**Responsible:** registered manager / compliance lead (verification and wording); web developer.

**Acceptance criteria:**
- [ ] Checklist completed with screenshots dated within 7 days of release.
- [ ] Wording signed off by the registered manager.
- [ ] Badge links on 100% of pages, opening in a new tab.
- [ ] A quarterly re-check is scheduled.

**QA:**
- [ ] Link resolves to the correct location (address 57–63 Knightsbridge).
- [ ] Text matches the register exactly.

**Success metric:** `cqc_link_click` events (after T09); fewer CQC questions in the enquiry log; usability task 3 success (research kit).

---

## T06 · One phone number, tap-to-call, sticky mobile bar

**Affected:**
- Phone shown as plain text (not tappable) on /contact/, /book-now/, /book-now-acupuncture/ and other pages.
- `tel:` link only on the home page (1 of 30 sampled; 1 of 212 site-wide).
- Two numbers in use: 020 8015 7987 (home, contact, booking) and 020 7160 0003 (About).

**Proposed change:**
- Operations chooses one number.
- Wrap every displayed number in a `tel:+44…` link.
- Add a sticky bottom bar on mobile (≤ 768 px) with "Call", "Book" (generic Pabau link) and, if adopted, "WhatsApp".
- Add `tel_click` tracking (T09).

**Responsible:** Operations lead (number, call handling); web developer.

**Acceptance criteria:**
- [ ] Re-crawl: every page with a phone number has a working `tel:` link.
- [ ] The second number is removed or justified.
- [ ] The sticky bar appears on mobile only, doesn't cover content or the cookie banner, and passes tap-target size (≥ 44 px).

**QA:**
- [ ] Real iPhone and Android test: tapping opens the dialler with the right number.
- [ ] The bar doesn't overlap form submit buttons.

**Success metric:** `tel_click` per 100 mobile sessions; answered-call rate (Operations).

---

## T07 · Price consistency and acupuncture formats

**Verified on 15 Oct 2026:**

| # | Where | What the pages say | Issue |
|---|---|---|---|
| a | https://the-hvn.com/concerns/fatigue-and-burnout/ vs https://the-hvn.com/nad-iv-infusion/ | "NAD+ Infusion · 60 minutes · £375" vs "From £350 · 90 minutes" (tiers £350 / £500 / £800) | Same product, different price and duration |
| b | https://the-hvn.com/acupuncture-for-perimenopause-menopause/, /acupuncture-for-female-hormonal-health/, /acupuncture-for-fertility-ivf/ vs https://the-hvn.com/womens-health-with-susan-gu/, /hormonal-balance-with-susan-gu/, /ivf-and-fertility-susan-gu/ | First set: "From £200 · From 45 minutes" (15-min consultation + 30-min needling); course "From £1620 · Duration: TBA". Second set: "From £300 · 60 minutes"; 6 sessions "From £270" each (10% off); 10 sessions "From £255" each (15% off) | Two parallel page families for the same practitioner with different formats and prices. **£1,620 = 6 × £270**, consistent with the 6-session price, but the course page doesn't say so. "Duration: TBA" is unfinished. Not necessarily an error; confusing |
| c | Complete Wellness and Elite Functional Health profiles | Pages say **48** and **56** health markers | Our own earlier files said "50+" and "60+". Correct our documents, not the site |

**Proposed change:**
- (a) The price owner confirms the NAD entry product, and the fatigue page shows the same item, price and duration as the NAD page.
- (b) Add a short "Acupuncture formats and prices" table to all six pages: 45-min session from £200; 60-min session with the lead practitioner from £300; 6- and 10-session packages with per-session and total price. Replace "Duration: TBA" with the number of sessions and validity.
- Single source of prices: a reusable WordPress block or global field.

**Responsible:** Operations lead (price authority); marketing lead; web developer.

**Acceptance criteria:**
- [ ] Re-crawl of the price register shows no item with two different prices for the same duration.
- [ ] Course entries state sessions and total.
- [ ] No "TBA" remains.

**QA:**
- [ ] Prices match what Pabau charges (Operations confirms against the booking system).

**Success metric:** price-question enquiries (enquiry log); `package_click` / package enquiries.

---

## T08 · Consultation fees-and-credits table (**blocked by policy decision**)

**Affected:**
- https://the-hvn.com/consultations/
- https://the-hvn.com/discovery-consultation/
- https://the-hvn.com/aesthetic-consultation/
- and the consultation sections of other pages.

**Verified:**
- £175 aesthetic consultations (seven types, 60 min) show **no credit wording**.
- £350 Discovery: "£100 will be redeemable against future Functional Medicine Packages" (packages unpublished, see T04).
- £400 8R consultation (up to 90 min, "follow-up consultation is included in your initial fee").
- Blood profiles offer a "10-minute follow-up phone consultation with one of our doctors for £150".

**Decision required (CEO + Finance):** the credit rule for each consultation.

**Proposed table (structure; values from the decision):**

| Consultation | Fee | Length | Who | What you receive | Credited against | Valid for |
|---|---|---|---|---|---|---|
| Aesthetic (7 types) | £175 | 60 min | [role] | [e.g. written plan] | [decision] | [decision] |
| Discovery | £350 | up to 60 min | [role] | [—] | £100 against [named, priced packages] | [—] |
| Nutrition | £350 | 60 min | [role] | [—] | [decision] | [—] |
| 8R Longevity | £400 | up to 90 min | [role] | Follow-up included | [decision] | [—] |
| Results call (after a blood profile) | £150 | 10 min | Doctor | Explanation of results | — | — |

**Acceptance criteria:**
- [ ] The same table appears on every consultation page.
- [ ] Every credit rule names a priced, existing product.
- [ ] Finance confirms Pabau applies the credits.

**Success metric:** share of enquiries tagged "fee credit"; consultation booking clicks.

---

## T09 · Measurement baseline (verification first)
- **Scope:** `03-measurement-spec.md` §2, §3, §7–§9.
- **Steps:**
  1. Get read access to GTM container `GTM-N7X2W4QF`, the GA4 property (if any), Search Console and Pabau reporting.
  2. Document the existing tags.
  3. Check the consent banner in a normal browser.
  4. Answer the booking-system questions P1–P7.
  5. Only then implement the event dictionary.
  6. Start the enquiry log (template in `04-research-kit/templates/enquiry-log.csv`).
- **Responsible:**
  - marketing lead + analytics agency (tags);
  - data protection officer (consent, privacy);
  - Operations lead (Pabau, enquiry log).
- **Acceptance criteria:** QA checks V1–V9 in the spec all pass. No personal data appears in any hit.
- **Success metric:** 4-week baseline captured for every KPI in spec §5.

---

## T10 · Booking-route consistency and titles

| Issue (verified) | URLs | Proposed change |
|---|---|---|
| IV pages link "BOOK YOUR TREATMENT" to Pabau (`category=196307`), but /book-now/ says IV and IM must use the contact form | /iv-infusions/, /nad-iv-infusion/, /book-now/ | Operations decides the rule (the IV doctor check may need a call). Make both pages say the same thing |
| Acupuncture packages: an enquiry form on /book-now-acupuncture/ (6 or 10 sessions) vs Pabau prepaid package links on the practitioner pages | /book-now-acupuncture/, /womens-health-with-susan-gu/, /hormonal-balance-with-susan-gu/, /ivf-and-fertility-susan-gu/ | One purchase route, explained the same way everywhere |
| Generic "BOOKINGS" / "Bespoke Consultations" open Pabau with no service pre-selected | All pages | After the booking-system answer P1: use the right deep link per page, or add a short "what would you like to book?" chooser |
| Titles say "Skin & Hair" | /book-now/ ("Book Your Skin & Hair Treatment Appointment"), /contact/ ("Contact The HVN \| Expert Skin & Hair Clinic Support") | Neutral titles, e.g. "Book an Appointment \| The HVN Knightsbridge" and "Contact The HVN \| Knightsbridge Clinic". Final wording after positioning (R15) |

**Responsible:** Operations lead (booking rules); marketing lead; web developer.

**Acceptance criteria:**
- [ ] One documented booking rule per service family.
- [ ] Every booking button follows it (re-crawl of booking-link settings).
- [ ] Titles updated.

**Success metric:** booking-click-to-booking ratio by category (F4); fewer "how do I book X" enquiries.

---

## T11 · Privacy and consent hygiene (review only, for the data protection officer)

| Observation (verified in public HTML/text) | Ask |
|---|---|
| No consent banner or consent-management platform found in the static HTML; the policies refer to accepting cookies and to Facebook/Instagram advertising | Confirm in a normal browser whether a banner appears and blocks non-essential cookies until consent (UK PECR) |
| Privacy policy names the controller "**The HVN Wellness Limited**"; contact page and footer say "**The HVN Wellbeing Ltd**" | Confirm the correct legal entity and update |
| Privacy policy cookie link is malformed: `https://the-hvn/cookie-policy/` | Fix to `https://the-hvn.com/cookie-policy/` |
| Enquiry forms 2, 4, 5 and 15 collect contact details and free text ("How can we help?"), which may include health information, with no privacy field in the form | Add a short privacy notice under each form; decide whether consent is the right lawful basis |
| Condition pages (menopause, PCOS, PMDD, fertility) can reveal health interest if ad pixels fire | Exclude these pages from ad remarketing; document in the cookie policy |
| Terms include US-specific boilerplate (DMCA, US federal end users) | Legal review (no conclusion drawn here) |

**Acceptance:** data protection officer's decisions recorded in `08-approval-register.csv`. Copy changes only after sign-off.
