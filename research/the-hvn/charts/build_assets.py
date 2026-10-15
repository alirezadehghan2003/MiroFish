"""Build the strategy assets for The HVN study from one data source.

Outputs (all relative to research/the-hvn/):
  recommendations-register.csv / .md   the 24 recommendations
  charts/*.png                         charts used in the report and the deck

Inputs: evidence/*.csv (live crawl, 15 Oct 2026) and results/*/raw/simulation-db-export.json.
No network access and no API calls. Run with any Python that has matplotlib:
  python charts/build_assets.py
"""
import csv
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CHARTS = ROOT / "charts"

NAVY, TEAL, SAND, RED, GREY, LIGHT = "#1f3a5f", "#2a9d8f", "#e9c46a", "#c8553d", "#8d99ae", "#edf2f4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlesize": 12})

# ---------------------------------------------------------------------------
# Recommendations register (single source of truth)
# Confidence: High = verified on the-hvn.com 15 Oct 2026 (re-checked where noted);
# Medium = regulator/official source via search, or a verified gap whose effect is a hypothesis;
# Low = simulated or directory signal only; Unknown = not established.
# Impact/Effort: H/M/L. Effort L = >10 person-days or an external dependency.
# ---------------------------------------------------------------------------
RECS = [
    dict(id="R01", area="Website", title="Fix the Menopause, PCOS and PMDD pages",
         problem="All three women's-health pages list acne lasers and peels as 'our available treatments'.",
         evidence="Re-checked live 15 Oct 2026: /menopause/ shows 'Explore our specialised solutions for rosacea, acne, and acne scarring' (Fotona Active Acne £475 etc.). Audit W1; crawl CSV.",
         confidence="High",
         solution="Replace the block with the real pathway: women's-health doctor consultation, hormonal/menopause acupuncture (from £200; course from £1,620 with session count), relevant blood profiles, fertility panel (£500) where relevant. Retitle pages ('Menopause Support in Knightsbridge | The HVN'). Clinical sign-off before publishing.",
         impact_hypothesis="Visitors with menopause/PCOS/PMDD intent see a relevant next step, so more of them enquire or book; removes a visible credibility defect.",
         impact="H", effort="S", effort_detail="1-3 days content + clinical review", owner="Marketing lead (content); women's-health doctor (clinical sign-off); web developer",
         priority="P1", window="0-30", kpi="3/3 pages corrected; booking-link clicks and enquiries from the 3 pages vs 4-week baseline (GA4); consultations attributed in Pabau",
         approval="Website change: needs your approval"),
    dict(id="R02", area="Website", title="Repair broken navigation and internal links",
         problem="Two menu links on every page return 404; 19 broken internal links; 22 links via redirects; a sitemap URL redirects into a 404.",
         evidence="Re-checked 15 Oct 2026: /clinical-treatments/ and /holistic-rituals/ return 404 (linked from 212/212 pages). evidence/hvn-broken-links-2026-10-15.csv; audit W2, W6.",
         confidence="High",
         solution="Point the menu at live hub pages (or create them); 301 every broken or retired path; update in-body links to final URLs; fix /fotona-3d-peel/ chain; add 404 monitoring.",
         impact_hypothesis="Fewer dead ends in navigation, better crawl efficiency and fewer lost sessions.",
         impact="H", effort="S", effort_detail="2-3 developer days", owner="Web developer / agency",
         priority="P1", window="0-30", kpi="0 internal 404s in a re-crawl; GA4 404 page views near zero",
         approval="Website change: needs your approval"),
    dict(id="R03", area="Pricing", title="Decide the programme tier; redirect retired URLs; remove the orphan page",
         problem="The consultation-to-plan step has no visible destination: programme pages 404 and /functional-medicine/ lands on an unfinished 'Updated' page.",
         evidence="Re-checked 15 Oct 2026: /hvn-360-proactive-health-programme/ 404. 7 retired URLs 404; orphan page has no H1, meta description or prices; Discovery's £100 credit points to unpriced 'packages'. Audit W3.",
         confidence="High",
         solution="Management decides which programmes exist today. Publish them (price or range), or 301 each retired URL to the nearest live page; finish or remove the orphan page.",
         impact_hypothesis="Restores a destination for the highest-value journey; removes 404s that press and search still point to.",
         impact="H", effort="M", effort_detail="Management decision + 3-5 developer/content days", owner="CEO/Founder + Medical Director (decision); web developer",
         priority="P1", window="0-30", kpi="Decision recorded; 0 retired programme URLs returning 404; programme page views and enquiries",
         approval="Business decision + website change"),
    dict(id="R04", area="Compliance", title="Commission a CAP-code claims review before any campaign",
         problem="Health-claim wording risk on IV/IM, injectables and superlatives.",
         evidence="Immune/boost wording on 19/20 IV/IM pages; 'Fat Burner IV'; botulinum toxin named next to prices; 'London's leading' in the home page and the site-wide schema description. ASA IVNT guidance and 2023 rulings (Get A Drip, REVIV).",
         confidence="High",
         solution="Brief a qualified advertising/regulatory adviser on IV/IM, injectables and superlative wording; implement the changes before paid media or new messaging.",
         impact_hypothesis="Reduces regulatory and reputational exposure; a precondition for any paid campaign or new positioning.",
         impact="H", effort="M", effort_detail="External review 2-4 weeks; cost to be quoted", owner="CEO/Founder + external adviser; Medical Director",
         priority="P1", window="0-30", kpi="Review completed; 100% of flagged items resolved or accepted with rationale; 0 upheld ASA complaints",
         approval="Spend: needs management approval"),
    dict(id="R05", area="Trust", title="Verify CQC status and scope, then link the badge and add a plain status line",
         problem="A 'CQC Regulated' image appears on every page but links nowhere; the inspection status used in v1 is not verified.",
         evidence="Badge on 212/212 pages, register link on 0 [crawl; re-checked]. Status 'registered, not yet inspected' comes from a v1 search result only; a 15 Oct 2026 search did not surface the record. CQC does not regulate some non-surgical cosmetic procedures (shown in a peer clinic's CQC report via search).",
         confidence="Medium",
         solution="Registered manager checks the provider and location pages on cqc.org.uk, including regulated activities and rating status; link the badge to the location page; add one accurate line (e.g. 'Registered with the CQC for [activities]; [rating / not yet rated]'). Do not imply that CQC covers every service.",
         impact_hypothesis="Turns a decorative badge into verifiable proof; avoids implying wider coverage than the registration gives.",
         impact="H", effort="S", effort_detail="1 day after the check", owner="Registered manager / compliance lead; web developer",
         priority="P1", window="0-30", kpi="Badge linked on 100% of pages; wording signed off by compliance; status re-checked quarterly",
         approval="Website change: needs your approval"),
    dict(id="R06", area="Conversion", title="One phone number, click-to-call and a sticky mobile Call/Book bar",
         problem="Phone-first and concierge buyers cannot tap to call from service pages; two numbers are in use.",
         evidence="tel: link on 1/212 pages (audit W10; 15 Oct spot-check of 16 pages: home only). 020 8015 7987 and 020 7160 0003 both published. WhatsApp mentioned on 18 pages.",
         confidence="High",
         solution="Choose one number; add tel: links site-wide; add a sticky mobile bar (Call / Book / WhatsApp); add call tracking.",
         impact_hypothesis="Easier contact for time-poor and gatekeeper buyers; more calls from mobile service pages.",
         impact="M", effort="S", effort_detail="1-2 developer days", owner="Web developer; Operations/concierge lead",
         priority="P1", window="0-30", kpi="tel: on 100% of pages; click-to-call events per week; answered-call rate",
         approval="Website change: needs your approval"),
    dict(id="R07", area="Measurement", title="Set up the analytics and booking-funnel baseline",
         problem="No analytics, booking or enquiry data was available, so no recommendation can yet be measured.",
         evidence="Study had no GA4, Search Console, Pabau or CRM access (dossier §0.2). v1 KPIs had no baselines.",
         confidence="High",
         solution="Define GA4 events (book click, tel click, form, WhatsApp), UTMs, a Pabau report for consultation-to-plan conversion, and an enquiry log with reason tags (price, practitioner, CQC, availability). Capture a 4-week baseline before changes where possible.",
         impact_hypothesis="Makes every other recommendation measurable; shows which pages and segments actually produce bookings.",
         impact="H", effort="M", effort_detail="3-5 days agency/internal", owner="Marketing lead + analytics agency; Operations lead (Pabau)",
         priority="P1", window="0-30", kpi="Dashboard live; baseline recorded for the 8 funnel metrics in the journey map",
         approval="Internal; no customer contact"),
    dict(id="R08", area="Pricing", title="Publish one consultation fees and credits table",
         problem="Only the £350 Discovery Consultation states a credit (£100); the £175 and £400 consultations state none.",
         evidence="Re-checked 15 Oct 2026: credit wording on /discovery-consultation/ only, not on /aesthetic-consultation/. Raised repeatedly in S1 run 2, S2a and S2b [simulated].",
         confidence="High",
         solution="Management sets the credit policy; publish one table (fee, length, clinician, what you receive, credit rules) on the consultations page and each consultation page.",
         impact_hypothesis="Reduces 'pay to be quoted' hesitation and confusion between consultation types.",
         impact="M", effort="S", effort_detail="Policy decision + 1 content day", owner="CEO/Founder + Finance (policy); Marketing lead",
         priority="P1", window="0-30", kpi="Table live; share of enquiries tagged 'credit/fee question'; consultation booking rate",
         approval="Business decision + website change"),
    dict(id="R09", area="Pricing", title="Show the cancellation charge in pounds at booking",
         problem="Terms require a card and 24 hours' notice; what is charged, and where it is shown, is unknown.",
         evidence="Terms of service [verified]; booking screens untested (Pabau domain blocked) [NEEDS TESTING]. S2a A3, S2b B4 [simulated].",
         confidence="Medium",
         solution="Run an internal booking test (stop before payment); then state the charge in £ next to the booking button and in confirmations.",
         impact_hypothesis="Fewer abandoned bookings and fewer disputes.",
         impact="M", effort="S", effort_detail="Half-day test + Pabau settings", owner="Operations lead / Pabau administrator",
         priority="P2", window="0-30", kpi="Booking-flow completion rate (Pabau); cancellation disputes per month",
         approval="Booking-system change: needs your approval"),
    dict(id="R10", area="Pricing", title="Remove price conflicts and show sessions per course",
         problem="The same service shows different prices on different pages; course session counts are missing.",
         evidence="NAD £375/60 min (fatigue page) vs £350/90 min (NAD page); fertility acupuncture from £200 vs from £270/£300; course 'from £1,620' without session count. Price register CSV.",
         confidence="High",
         solution="Single price source; reconcile duplicates; state sessions and validity per course.",
         impact_hypothesis="Removes doubt at the decision point; protects trust in published prices (a verified strength).",
         impact="M", effort="S", effort_detail="1-2 days", owner="Marketing lead + Operations lead",
         priority="P1", window="0-30", kpi="0 conflicting prices in a re-crawl of the price register",
         approval="Website change: needs your approval"),
    dict(id="R11", area="Pricing", title="Publish indicative pathway price ranges",
         problem="After a £175-£750 entry step, no programme price is visible except 8R 'from £3,000'.",
         evidence="Programmes unpriced; old programme pages 404 [verified]. A £15,500 12-week programme anchor exists in the market (Pillar, reported). Simulated agents asked for a written range (S1 run 2, S2a, S2b), partly prompted by the seed.",
         confidence="Medium",
         solution="Compute typical 3-month spend ranges from 12 months of Pabau data for 3-4 pathways (fatigue, longevity, skin, women's health); publish with assumptions ('most clients spend £X-£Y'). Validate wording in usability tests first.",
         impact_hypothesis="Lower uncertainty raises consultation bookings and plan acceptance (to be validated).",
         impact="H", effort="M", effort_detail="Data pull + decision + 3 content days", owner="CEO/Founder + Finance + Medical Director",
         priority="P2", window="31-60", kpi="Consultation-to-plan acceptance; booking rate on pathway pages; price-question enquiries",
         approval="Business decision + website change"),
    dict(id="R12", area="Pricing", title="Add 'your first year' worked examples",
         problem="Buyers cannot see a realistic 12-month cost.",
         evidence="S2b B2 [simulated, directional]; depends on R11 data.",
         confidence="Low",
         solution="After R11, publish 2-3 dated, assumption-labelled examples.",
         impact_hypothesis="Helps planners and gatekeepers budget; may reduce sticker shock.",
         impact="M", effort="S", effort_detail="2 days after R11", owner="Marketing lead + Finance",
         priority="P3", window="61-90", kpi="Page engagement; use in consultations (staff survey)",
         approval="Website change: needs your approval"),
    dict(id="R13", area="Trust", title="Add 'Who will treat me' to every service page",
         problem="Every page shows the same four practitioner names, including the acupuncturist on IV and injectables pages.",
         evidence="Crawl check [verified]. 'Who will treat me' raised in all five full runs [simulated].",
         confidence="High",
         solution="Treatment-specific clinician block: role, qualifications, professional registration body and number where applicable.",
         impact_hypothesis="Raises trust for new clients, especially aesthetics and gatekeeper buyers.",
         impact="H", effort="M", effort_detail="5-8 days content across ~150 pages (template-driven)", owner="Medical Director + Marketing lead; web developer",
         priority="P2", window="31-60", kpi="Coverage on 100% of service pages; service-page-to-booking click rate vs baseline",
         approval="Website change: needs your approval"),
    dict(id="R14", area="Trust", title="Publish 'What happens before your IV'",
         problem="The best trust line on the site (a doctor check before every IV) is not explained.",
         evidence="IV page: 'a brief 10 minute consultation with one of our doctors' [re-checked 15 Oct 2026]. S3 M3-M4 [simulated].",
         confidence="Medium",
         solution="Explain the steps, contraindications, who prescribes and supervises, ingredients and doses, and what the evidence does and does not show. After R04.",
         impact_hypothesis="Turns an existing safeguard into visible proof.",
         impact="M", effort="S", effort_detail="2 days + clinical sign-off", owner="Medical Director",
         priority="P2", window="31-60", kpi="Page live on all IV/IM pages; IV page booking clicks vs baseline",
         approval="Website change: needs your approval"),
    dict(id="R15", area="Positioning", title="One proposition line and consistent titles; retire unsupported superlatives",
         problem="The category is unclear and the copy contradicts itself.",
         evidence="Home H1 'HOW THE HVN CAN HELP'; Contact and Booking titles say 'Skin & Hair'; 'London's leading' on the home page and in the site schema description [verified].",
         confidence="High",
         solution="Adopt a candidate line after interviews (working draft: 'Doctor-led care for skin, energy and long-term health: one Knightsbridge team, clear prices, no membership'); update H1, titles and schema description.",
         impact_hypothesis="Clearer category; lower claim risk; better search snippets.",
         impact="M", effort="S", effort_detail="2 days after the decision", owner="Marketing lead + CEO/Founder",
         priority="P2", window="31-60", kpi="Consistent titles on 100% of pages; Search Console CTR on brand and category queries; comprehension in interviews",
         approval="Business decision + website change"),
    dict(id="R16", area="Positioning", title="Test 'no membership, pay as you go' as a differentiator",
         problem="Rivals reportedly sell memberships; The HVN does not offer one. Whether buyers value that is unknown.",
         evidence="No membership on site [verified; confirmed by you]. Rival memberships reported, unverified. S4: 10/11 agents saw it as an advantage, but the seed emphasised it [simulated, primed].",
         confidence="Low",
         solution="Test in interviews and usability sessions before using it in headlines; then a hero-copy test.",
         impact_hypothesis="Could differentiate against clubs for selective users; could equally read as 'less exclusive'.",
         impact="M", effort="S", effort_detail="Included in validation work", owner="Marketing lead",
         priority="P3", window="61-90", kpi="Interview preference; A/B click-through to booking",
         approval="Customer research: needs your approval"),
    dict(id="R17", area="Segment", title="Build a women's health and fertility hub",
         problem="Women's-health demand has no coherent route; specialists are reported to be cheaper for single needs.",
         evidence="Women's-health doctor and TCM content [verified]; W1 defect [verified]; specialist prices £185-£275 and ~£90 [directory, unverified]; S4 [simulated].",
         confidence="Medium",
         solution="One hub linking doctor, acupuncture, tests and course totals; describe coordination with the client's GP or specialist.",
         impact_hypothesis="Captures single-need demand that currently goes to specialists.",
         impact="M", effort="M", effort_detail="8-12 days", owner="Women's-health doctor + Marketing lead",
         priority="P3", window="61-90", kpi="Hub sessions; consultations booked from the hub",
         approval="Website change: needs your approval"),
    dict(id="R18", area="SEO", title="Add clinic structured data and fix metadata",
         problem="No MedicalClinic/LocalBusiness schema; title errors.",
         evidence="Schema is Organization/WebSite/WebPage/Breadcrumb only; 6 titles >60 characters; Fotona '4D' vs '5D' mismatch. Audit W9, W11.",
         confidence="High",
         solution="MedicalClinic with address, geo, hours, phone; Service/Offer on service pages; Physician for clinicians; fix titles.",
         impact_hypothesis="Better local and organic visibility.",
         impact="M", effort="S", effort_detail="2-4 developer days", owner="Web developer / SEO",
         priority="P2", window="31-60", kpi="Rich Results test valid; local impressions (Search Console / Business Profile)",
         approval="Website change: needs your approval"),
    dict(id="R19", area="Conversion", title="Measure and set a speed-to-lead standard",
         problem="Response time to enquiries is unknown.",
         evidence="Concierge contact model [verified]; S2a A7 'same-day doctor call-back' [simulated, single run].",
         confidence="Low",
         solution="Log first-response times for 4 weeks; set a standard only if slow responses correlate with lost bookings.",
         impact_hypothesis="Faster responses convert more time-poor enquiries.",
         impact="M", effort="S", effort_detail="Process change", owner="Operations / concierge lead",
         priority="P2", window="0-30", kpi="Median first-response time; enquiry-to-booking rate",
         approval="Internal"),
    dict(id="R20", area="Experience", title="Give every consultation a written summary and plan",
         problem="Whether clients leave with a written plan and total is unknown.",
         evidence="S1 run 2 #10, S2b B9 [simulated]; current practice unknown.",
         confidence="Low",
         solution="Confirm current practice; if missing, adopt a template: findings, plan, total, alternatives, what is not recommended.",
         impact_hypothesis="Higher plan acceptance and trust; counters 'upsell' perceptions (one 2025 blog anecdote).",
         impact="M", effort="M", effort_detail="Template + training", owner="Medical Director + Operations lead",
         priority="P2", window="31-60", kpi="% consultations with a written plan within 48 h; plan acceptance rate",
         approval="Internal"),
    dict(id="R21", area="Trust", title="Check and surface the review rating",
         problem="A reviews widget is on 157/212 pages, but the rating is not in the HTML and is unknown to this study.",
         evidence="Crawl [verified]; Google rating and volume unknown; one negative 2025 blog anecdote [press].",
         confidence="Low",
         solution="Check Business Profile rating and volume; if strong, show it in HTML (compliant schema); add a post-visit review request.",
         impact_hypothesis="Social proof for first-time buyers.",
         impact="M", effort="S", effort_detail="1-2 days", owner="Marketing lead",
         priority="P2", window="31-60", kpi="Rating; new reviews per month",
         approval="Website change: needs your approval"),
    dict(id="R22", area="Website", title="Test and fix mobile performance",
         problem="Pages are heavy and mobile rendering is untested.",
         evidence="Median 713 KB HTML and 55 images per page [verified]; headless browser blocked (403), so mobile untested.",
         confidence="Medium",
         solution="Lighthouse / Core Web Vitals from a normal connection; trim repeated blocks and images.",
         impact_hypothesis="Faster mobile pages reduce drop-off.",
         impact="M", effort="M", effort_detail="3-6 developer days", owner="Web developer",
         priority="P2", window="31-60", kpi="Core Web Vitals pass; mobile bounce/engagement vs baseline",
         approval="Website change: needs your approval"),
    dict(id="R23", area="Offer", title="Pilot a priced first-step pathway (gated on validation)",
         problem="No priced bridge from consultation to plan.",
         evidence="S2b hypothetical £850 pathway: directional only, discussed in one sub-thread [simulated].",
         confidence="Low",
         solution="Design only if interviews and R11 data support it: credit the full fee and show follow-on costs on the same page.",
         impact_hypothesis="Could convert hesitant buyers; could also cannibalise higher-value plans.",
         impact="M", effort="L", effort_detail="Clinical, pricing and ops design", owner="CEO/Founder + Medical Director + Finance",
         priority="P3", window="after 90 (gated)", kpi="Uptake; conversion to a full plan; margin",
         approval="Business decision"),
    dict(id="R24", area="Monitoring", title="Quarterly competitor and regulatory check at primary sources",
         problem="No competitor price, membership or rating could be verified at source.",
         evidence="Competitor sites, CQC and ASA blocked from this environment; 15 Oct 2026 searches could not confirm HUM2N or Harrods 2026 prices.",
         confidence="High",
         solution="Quarterly dated check of rivals' own sites and the CQC/ASA registers by someone with normal browser access.",
         impact_hypothesis="Keeps pricing and positioning decisions grounded in current facts.",
         impact="L", effort="S", effort_detail="1 day per quarter", owner="Marketing analyst",
         priority="P3", window="61-90", kpi="Benchmark refreshed quarterly with >=80% of facts verified at source",
         approval="Internal"),
]

FIELDS = ["id", "area", "title", "problem", "evidence", "confidence", "solution", "impact_hypothesis",
          "impact", "effort", "effort_detail", "owner", "priority", "window", "kpi", "approval"]


def write_register():
    with open(ROOT / "recommendations-register.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(RECS)

    lvl = {"H": "High", "M": "Medium", "L": "Low", "S": "Small", "L-S": "Small"}
    eff = {"S": "Small", "M": "Medium", "L": "Large", "L-S": "Small"}
    out = ["# The HVN: Recommendations Register", "",
           "**Version:** 1.0, 15 October 2026 · **Generated by** `charts/build_assets.py` (also `recommendations-register.csv`).",
           "",
           "Each recommendation states the problem, its supporting evidence and confidence, the proposed solution, a business-impact **hypothesis**, effort, a suggested owner (a role, not a named person), priority and a measurable KPI.",
           "",
           "- **Confidence** applies to the *problem evidence*, not to the predicted impact: **High** = verified on the-hvn.com (crawl 15 Oct 2026, re-checked where stated); **Medium** = verified gap but uncertain effect, or a regulator/official source found by search; **Low** = simulated or directory signal only.",
           "- **Impact** is a hypothesis until measured (see `validation-plan.md`). **Effort:** Small ≤ 3 days, Medium 3–10 days, Large > 10 days or an external dependency.",
           "- **Priority:** P1 = first 30 days; P2 = days 31–60; P3 = days 61–90 or gated on validation.",
           "- **Nothing here has been deployed.** Every website, booking-system or customer-contact action needs your approval first.",
           "",
           "## Summary", "",
           "| ID | Area | Recommendation | Evidence confidence | Impact | Effort | Owner (suggested) | Priority | Window | KPI |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in RECS:
        out.append(f"| {r['id']} | {r['area']} | {r['title']} | {r['confidence']} | {lvl[r['impact']]} | {eff[r['effort']]} | {r['owner'].split(';')[0]} | **{r['priority']}** | {r['window']} | {r['kpi']} |")
    out += ["", "![Priority matrix](charts/priority-matrix.png)", "", "## Detail", ""]
    for r in RECS:
        out += [f"### {r['id']} · {r['title']}  ({r['priority']}, {r['window']} days)", "",
                "| | |", "|---|---|",
                f"| **Problem** | {r['problem']} |",
                f"| **Supporting evidence** | {r['evidence']} |",
                f"| **Evidence confidence** | {r['confidence']} |",
                f"| **Proposed solution** | {r['solution']} |",
                f"| **Business-impact hypothesis** | {r['impact_hypothesis']} (expected impact: {lvl[r['impact']]}) |",
                f"| **Effort** | {eff[r['effort']]}: {r['effort_detail']} |",
                f"| **Owner (suggested role)** | {r['owner']} |",
                f"| **KPI** | {r['kpi']} |",
                f"| **Approval gate** | {r['approval']} |", ""]
    (ROOT / "recommendations-register.md").write_text("\n".join(out), encoding="utf-8")


def save(fig, name):
    fig.savefig(CHARTS / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def chart_price_ladder():
    # Published prices, live crawl 15 Oct 2026 (evidence/hvn-price-register-2026-10-15.csv).
    layers = [
        ("Consultations", [175, 350, 350, 400]),
        ("Diagnostics", [60, 180, 220, 450, 500, 550, 750]),
        ("IV / IM", [275, 325, 350, 375, 400, 425, 500, 675, 800, 895]),
        ("Aesthetics", [260, 450, 500, 550, 850]),
        ("Acupuncture & therapies", [200, 210, 230, 250, 260, 375, 1620]),
        ("Programmes", [3000]),
    ]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    for i, (lab, vals) in enumerate(layers):
        ax.scatter(vals, [i] * len(vals), s=60, color=TEAL if lab != "Programmes" else NAVY, zorder=3)
    ax.scatter([8000, 12000, 14500], [5] * 3, s=70, facecolors="none", edgecolors=RED, linewidths=1.5, zorder=3)
    ax.annotate("Retired programme prices\n(£8k / £12k / £14.5k pages now 404)", (11000, 5), (5200, 3.7),
                color=RED, fontsize=8.5, arrowprops=dict(arrowstyle="->", color=RED))
    ax.annotate("8R from £3,000\n(only priced programme)", (3000, 5), (1050, 4.35), fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=NAVY))
    ax.axvspan(900, 2900, color=SAND, alpha=0.35, zorder=1)
    ax.text(1600, -0.75, "'Price fog': functional-medicine\npackages not published", ha="center", fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xticks([100, 250, 500, 1000, 2500, 5000, 15000])
    ax.set_xticklabels(["£100", "£250", "£500", "£1k", "£2.5k", "£5k", "£15k"])
    ax.set_yticks(range(len(layers)))
    ax.set_yticklabels([l for l, _ in layers])
    ax.set_ylim(-1.2, 5.6)
    ax.set_title("The HVN's published price ladder [Verified, live site 15 Oct 2026]")
    ax.grid(axis="x", alpha=0.3)
    save(fig, "price-ladder.png")


def chart_audit():
    items = [  # (label, numerator, denominator, good_when_high)
        ("Service pages showing a price", 148, 151, True),
        ("Pages with Pabau booking link", 212, 212, True),
        ("Pages with CQC badge", 212, 212, True),
        ("Pages where the CQC badge links to the register", 0, 212, True),
        ("Pages with a tap-to-call (tel:) link", 1, 212, True),
        ("Pages with clinic/local structured data", 0, 212, True),
        ("Pages carrying 2 broken menu links", 212, 212, False),
        ("IV/IM pages with immune/'boost' wording", 19, 20, False),
        ("Women's-health pages listing acne treatments", 3, 3, False),
    ]
    fig, ax = plt.subplots(figsize=(9, 4.4))
    for i, (lab, n, d, good) in enumerate(items):
        pct = 100 * n / d
        colour = (TEAL if pct >= 80 else RED) if good else RED
        ax.barh(i, pct, color=colour)
        ax.text(min(pct, 100) + 1.5, i, f"{n}/{d}", va="center", fontsize=9)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([x[0] for x in items])
    ax.invert_yaxis()
    ax.set_xlim(0, 115)
    ax.set_xlabel("% of pages")
    ax.set_title("Website audit: verified strengths (green) and defects (red)")
    ax.legend(handles=[Patch(color=TEAL, label="Strength"), Patch(color=RED, label="Defect / gap")],
              loc="upper center", bbox_to_anchor=(0.45, -0.13), ncol=2, frameon=False)
    save(fig, "website-audit.png")


THEMES = {
    "Total or range in writing before paying": r"(total|range|estimate|quote).{0,60}(writing|written)|(written|in writing).{0,60}(total|range|estimate|quote|plan|cost)|12[- ]month",
    "Cancellation charge / card on file": r"cancell?ation|card on file|card details",
    "Consultation fee credited?": r"credit",
    "Who will treat me / named clinician": r"who (will|would|actually|is going to) (treat|do|perform|be)|named (clinician|practitioner|doctor|injector|coordinator)|GMC",
    "CQC: registered vs inspected": r"inspect",
    "Evidence for IV / NAD claims": r"(evidence|trial|studies|study).{0,80}(IV|NAD|drip|infusion)|(IV|NAD|drip|infusion).{0,80}(evidence|trial|studies|study)",
    "Superlatives / slogans": r"leading|slogan|superlative|transformational|unparalleled",
    "Membership / lock-in": r"membership|lock-in|locked in|subscription",
    "Atmosphere / luxury cues": r"atmospher|ambien|luxur|interior|hydrobed|exclusiv|setting",
}
RUNS = {"S1 run 2": "s1-run2-2026-10-15", "S2a": "s2a-booking-decision-2026-10-15",
        "S2b": "s2b-hypothetical-pathway-2026-10-15", "S3": "s3-messaging-2026-10-15",
        "S4": "s4-competitor-choice-2026-10-15"}


def theme_matrix():
    rows = []
    for theme, pat in THEMES.items():
        row = []
        for folder in RUNS.values():
            d = json.loads((ROOT / "results" / folder / "raw" / "simulation-db-export.json").read_text())
            cs = [c["content"] for c in d["comment"]]
            row.append(round(100 * sum(bool(re.search(pat, c, re.I)) for c in cs) / len(cs)))
        rows.append(row)
    return rows


def chart_convergence():
    m = theme_matrix()
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    im = ax.imshow(m, cmap="Blues", vmin=0, vmax=70, aspect="auto")
    for i, row in enumerate(m):
        for j, v in enumerate(row):
            ax.text(j, i, f"{v}%", ha="center", va="center", fontsize=8.5, color="white" if v > 40 else "black")
    ax.set_xticks(range(len(RUNS)))
    ax.set_xticklabels(list(RUNS))
    ax.set_yticks(range(len(THEMES)))
    ax.set_yticklabels(list(THEMES))
    ax.set_title("[SIMULATED] Share of agent comments raising each theme, by run")
    fig.text(0.01, -0.04, "Keyword-based count over all agent comments in results/*/raw/simulation-db-export.json. "
             "Fictional LLM agents, not customers.\nThemes were partly prompted by each run's seed and opening posts "
             "(e.g. S2a asked 'Would you pay a consultation fee just to find out the total?').", fontsize=7.5)
    fig.colorbar(im, ax=ax, fraction=0.03, label="% of comments")
    save(fig, "simulation-convergence.png")
    return m


def chart_s4():
    labels = ["Specialist clinic", "The Lanesborough", "HUM2N", "The HVN (conditional)", "Surrenne", "Harrods clinic"]
    # One primary choice per agent (results/s4-competitor-choice-2026-10-15/analysis.md).
    valid = [5, 1, 1, 1, 0, 0]       # Claire, Priya, Isla, Margaret, Sofia | Khalid | Daniel | Helena
    other = [3, 0, 0, 0, 0, 0]       # Emma, Natalie (persona drift); James (split: specialist + Lanesborough gym)
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    ax.barh(labels, valid, color=NAVY, label="First choice")
    ax.barh(labels, other, left=valid, color=GREY, hatch="//", label="Persona drift (2) or split choice (1)")
    ax.invert_yaxis()
    ax.set_xlabel("Agents (n = 11 fictional personas)")
    ax.set_title("[SIMULATED] S4 first choice of provider: directional only")
    ax.legend(frameon=False, loc="lower right")
    save(fig, "s4-choice.png")


def chart_priority():
    imp = {"H": 3, "M": 2, "L": 1}
    eff = {"S": 1, "L-S": 1, "M": 2, "L": 3}
    col = {"P1": RED, "P2": SAND, "P3": GREY}
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    seen = {}
    for r in RECS:
        x, y = eff[r["effort"]], imp[r["impact"]]
        k = seen.get((x, y), 0)
        seen[(x, y)] = k + 1
        dx = -0.36 + (k % 6) * 0.145
        dy = -(k // 6) * 0.25
        ax.scatter(x + dx, y + dy, s=330, color=col[r["priority"]], edgecolor="white", zorder=3)
        ax.text(x + dx, y + dy, r["id"][1:], ha="center", va="center", fontsize=7.5, color="black", zorder=4)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["Small", "Medium", "Large"])
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Low", "Medium", "High"])
    ax.set_xlim(0.45, 3.55)
    ax.set_ylim(0.5, 3.6)
    ax.set_xlabel("Effort")
    ax.set_ylabel("Expected impact (hypothesis)")
    ax.axvline(1.5, color=GREY, lw=0.6, ls="--")
    ax.axhline(2.5, color=GREY, lw=0.6, ls="--")
    ax.text(0.5, 3.4, "Quick wins (high impact, small effort)", fontsize=9, color=NAVY, weight="bold")
    ax.set_title("Recommendations by impact and effort (numbers = R-IDs)")
    ax.legend(handles=[Patch(color=col[p], label=p) for p in col], frameon=False, loc="lower right")
    save(fig, "priority-matrix.png")


def chart_gantt():
    # (label, start_day, end_day, colour, recommendation ids)
    tasks = [
        ("Approval gate: website & research", 0, 3, NAVY),
        ("Measurement baseline (R07)", 0, 28, TEAL),
        ("Fix women's-health pages (R01)", 3, 14, RED),
        ("Broken links, redirects, prices (R02, R10)", 3, 21, RED),
        ("Programme decision (R03)", 0, 21, RED),
        ("Claims review commissioned & done (R04)", 3, 45, RED),
        ("CQC check, badge link, status line (R05)", 3, 14, RED),
        ("Phone, click-to-call, mobile bar (R06)", 7, 21, RED),
        ("Fees & credits table (R08)", 7, 28, RED),
        ("Booking test; cancellation £ (R09)", 7, 35, SAND),
        ("Validation: analytics, usability, interviews", 14, 56, NAVY),
        ("Who will treat me (R13)", 30, 60, SAND),
        ("IV explainer (R14); schema (R18)", 35, 60, SAND),
        ("Pathway price ranges (R11)", 35, 60, SAND),
        ("Proposition & titles (R15)", 45, 65, SAND),
        ("Reviews, mobile perf, written plans (R20-22)", 30, 60, SAND),
        ("Women's health hub (R17)", 60, 90, GREY),
        ("Messaging test: no-membership (R16)", 60, 90, GREY),
        ("First-year examples (R12); competitor check (R24)", 65, 90, GREY),
        ("Decision gate: starter pathway (R23)", 85, 90, NAVY),
    ]
    fig, ax = plt.subplots(figsize=(10, 6.2))
    for i, (lab, s, e, c) in enumerate(tasks):
        ax.barh(i, e - s, left=s, color=c, height=0.6)
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t[0] for t in tasks], fontsize=8.5)
    ax.invert_yaxis()
    for x in (30, 60, 90):
        ax.axvline(x, color=GREY, lw=0.8, ls="--")
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_xlabel("Days from approval")
    ax.set_title("30 / 60 / 90-day implementation roadmap")
    ax.legend(handles=[Patch(color=RED, label="P1 fix"), Patch(color=SAND, label="P2 prove & price"),
                       Patch(color=GREY, label="P3 position & test"), Patch(color=NAVY, label="Gate / validation"),
                       Patch(color=TEAL, label="Measurement")], frameon=False, fontsize=8, loc="lower left")
    save(fig, "roadmap-gantt.png")


def chart_journey():
    stages = ["Trigger", "Discover", "Research\non site", "Verify\ntrust", "Check\nprice", "Enquire /\nbook",
              "Pre-visit", "Consult-\nation", "Plan\ndecision", "Treat-\nment", "Follow-up", "Retain /\nrefer"]
    verified = [0, 3, 4, 3, 4, 3, 1, 1, 2, 0, 1, 0]   # verified defects per stage (customer-journey-map.md)
    simulated = [0, 0, 1, 4, 4, 2, 0, 1, 2, 0, 0, 1]  # simulated friction signals per stage
    unknown = [1, 1, 0, 1, 1, 2, 2, 3, 2, 3, 2, 3]    # key unknowns per stage
    x = range(len(stages))
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.bar([i - 0.27 for i in x], verified, width=0.27, color=RED, label="Verified defects")
    ax.bar(list(x), simulated, width=0.27, color=SAND, label="Simulated friction signals")
    ax.bar([i + 0.27 for i in x], unknown, width=0.27, color=GREY, label="Key unknowns (no data)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(stages, fontsize=8.5)
    ax.set_ylabel("Count")
    ax.set_title("Where the journey breaks, and where we have no data")
    ax.legend(frameon=False, fontsize=8.5)
    save(fig, "journey-friction.png")


def chart_competitor_commitment():
    # Reported, UNVERIFIED first-year cost to join (membership + joining) or programme price.
    rows = [  # label, low, high, colour/label kind
        ("The HVN: no membership\n(8R programme from £3,000)", 3000, 3000, "verified"),
        ("Lanesborough Club & Spa\nmembership (conflicting)", 4000, 6000, "reported"),
        ("Surrenne membership\n(£10k + £5k joining)", 15000, 15000, "reported"),
        ("Pillar at Raffles OWO\n12-week programme", 15500, 15500, "reported"),
        ("Lanserhof at The Arts Club\n(conflicting sources)", 4800, 8000, "conflict"),
        ("HUM2N programmes\n(2026 price not found)", None, None, "unknown"),
        ("Harrods Wellness Clinic\n(2026 prices not found)", None, None, "unknown"),
    ]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    for i, (lab, lo, hi, kind) in enumerate(rows):
        if lo is None:
            ax.text(600, i, "UNKNOWN", va="center", color=GREY, weight="bold")
            continue
        colour = {"verified": TEAL, "reported": SAND, "conflict": LIGHT}[kind]
        width = max(hi - lo, 250)
        ax.barh(i, width, left=lo, color=colour, edgecolor=NAVY if kind != "verified" else TEAL,
                hatch="//" if kind != "verified" else None, height=0.55)
        ax.text(hi + 400, i, f"£{lo:,}" + (f"–£{hi:,}" if hi != lo else ""), va="center", fontsize=8.5)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 21000)
    ax.set_ylim(len(rows) - 0.4, -0.6)
    ax.set_xlabel("£ (first year or programme)")
    ax.set_title("Entry commitment: The HVN [verified] vs rivals [reported, NOT verified at source]")
    ax.legend(handles=[Patch(color=TEAL, label="Verified (the-hvn.com)"),
                       Patch(facecolor=SAND, edgecolor=NAVY, hatch="//", label="Reported by press/PR; unverified"),
                       Patch(facecolor=LIGHT, edgecolor=NAVY, hatch="//", label="Sources conflict")],
              frameon=False, fontsize=8, loc="lower right")
    fig.text(0.01, -0.05, "Hooke London (up to £54,000/yr, press 2025) omitted for scale. Lanserhof range spans the conflicting "
             "reported figures. Sources: competitor-benchmark.md.", fontsize=7.5)
    save(fig, "competitor-commitment.png")


def chart_audit_outcomes():
    # From report-audit.md: outcome of each audited v1 statement.
    labels = ["Confirmed", "Corrected (wording/number)", "Downgraded (weaker evidence)", "Unverified → Unknown"]
    counts = [12, 5, 7, 5]
    fig, ax = plt.subplots(figsize=(7, 2.8))
    ax.barh(labels, counts, color=[TEAL, SAND, RED, GREY])
    for i, c in enumerate(counts):
        ax.text(c + 0.2, i, str(c), va="center")
    ax.invert_yaxis()
    ax.set_xlabel("Statements in report v1")
    ax.set_title("Audit of strategic report v1: 29 key statements")
    save(fig, "audit-outcomes.png")


def chart_run_costs():
    m = json.loads((ROOT / "results" / "summary-metrics.json").read_text())
    runs = m["runs"]
    fig, ax = plt.subplots(figsize=(7, 2.8))
    ax.bar([r["run"] for r in runs], [r["cost_usd"] for r in runs], color=NAVY)
    for i, r in enumerate(runs):
        ax.text(i, r["cost_usd"] + 0.004, f"${r['cost_usd']:.3f}", ha="center", fontsize=8.5)
    ax.set_ylabel("US$")
    ax.set_title(f"Simulation API cost per run (total ${m['totals']['cost_usd_simulations']:.3f})")
    save(fig, "run-costs.png")


if __name__ == "__main__":
    CHARTS.mkdir(exist_ok=True)
    write_register()
    chart_price_ladder()
    chart_audit()
    print("theme matrix (% of comments):", chart_convergence())
    chart_s4()
    chart_priority()
    chart_gantt()
    chart_journey()
    chart_competitor_commitment()
    chart_audit_outcomes()
    chart_run_costs()
    print("done:", sorted(p.name for p in CHARTS.glob("*.png")))
