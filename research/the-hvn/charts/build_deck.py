"""Build executive-presentation.pptx (16:9, with speaker notes) from the charts and the report.

Run after charts/build_assets.py:
  python charts/build_deck.py
No network access and no API calls.
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "charts"

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
TEAL = RGBColor(0x2A, 0x9D, 0x8F)
RED = RGBColor(0xC8, 0x55, 0x3D)
SAND = RGBColor(0xE9, 0xC4, 0x6A)
GREY = RGBColor(0x5C, 0x67, 0x7D)
LIGHT = RGBColor(0xED, 0xF2, 0xF4)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x22, 0x22, 0x22)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height
COUNT = [0]


def box(slide, x, y, w, h, fill=None, line=None):
    shp = slide.shapes.add_shape(1, x, y, w, h)
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
    shp.shadow.inherit = False
    return shp


def text(slide, x, y, w, h, paras, size=14, color=BLACK, bold=False, align=PP_ALIGN.LEFT):
    """paras: list of str or (str, dict(size, bold, color, bullet))."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, p in enumerate(paras):
        s, o = (p, {}) if isinstance(p, str) else p
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        run = para.add_run()
        run.text = ("• " if o.get("bullet") else "") + s
        run.font.size = Pt(o.get("size", size))
        run.font.bold = o.get("bold", bold)
        run.font.color.rgb = o.get("color", color)
        para.space_after = Pt(o.get("after", 6))
    return tb


def new_slide(title, kicker=None, source=None, notes=""):
    COUNT[0] += 1
    s = prs.slides.add_slide(BLANK)
    box(s, 0, 0, W, Inches(1.05), fill=NAVY)
    text(s, Inches(0.5), Inches(0.18), Inches(12.3), Inches(0.8), [title], size=26, color=WHITE, bold=True)
    if kicker:
        text(s, Inches(0.5), Inches(1.15), Inches(12.3), Inches(0.6), [kicker], size=15, color=NAVY, bold=True)
    foot = f"The HVN strategy review · 15 Oct 2026 · {COUNT[0]}"
    if source:
        foot = f"Source: {source}   |   " + foot
    text(s, Inches(0.5), Inches(7.05), Inches(12.3), Inches(0.35), [foot], size=9, color=GREY)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def image(slide, name, x, y, w=None, h=None):
    kw = {}
    if w is not None:
        kw["width"] = w
    if h is not None:
        kw["height"] = h
    return slide.shapes.add_picture(str(CH / name), x, y, **kw)


def table(slide, x, y, w, rows, col_w=None, size=11, header_fill=NAVY, row_h=Inches(0.36)):
    n_rows, n_cols = len(rows), len(rows[0])
    t = slide.shapes.add_table(n_rows, n_cols, x, y, w, Emu(row_h * n_rows)).table
    if col_w:
        for i, cw in enumerate(col_w):
            t.columns[i].width = Inches(cw)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.text = str(val)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(size)
                    run.font.bold = r == 0
                    run.font.color.rgb = WHITE if r == 0 else BLACK
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_fill if r == 0 else (LIGHT if r % 2 == 0 else WHITE)
    return t


def card(slide, x, y, w, h, heading, lines, accent=TEAL, size=13):
    box(slide, x, y, w, h, fill=LIGHT)
    box(slide, x, y, Inches(0.09), h, fill=accent)
    text(slide, x + Inches(0.2), y + Inches(0.1), w - Inches(0.3), Inches(0.5), [heading], size=15, bold=True, color=accent)
    text(slide, x + Inches(0.2), y + Inches(0.6), w - Inches(0.3), h - Inches(0.7),
         [(l, {"bullet": True, "size": size}) for l in lines])


# 1 Title -------------------------------------------------------------------
COUNT[0] += 1
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, W, H, fill=NAVY)
text(s, Inches(0.8), Inches(2.0), Inches(11.5), Inches(1.4), ["Making The HVN easy to trust and easy to buy"], size=40, color=WHITE, bold=True)
text(s, Inches(0.8), Inches(3.5), Inches(11.5), Inches(1.6),
     ["Evidence-backed strategy review for management", "15 October 2026 · Version 2.0"], size=20, color=WHITE)
text(s, Inches(0.8), Inches(5.6), Inches(11.5), Inches(1.0),
     ["Built on a live audit of the-hvn.com, a competitor review and six MiroFish simulations. "
      "Simulated agents are fictional and are used only to generate hypotheses, not as customer evidence."],
     size=13, color=SAND)
s.notes_slide.notes_text_frame.text = (
    "Purpose: agree a 90-day plan. The headline: the offer is distinctive but the website undersells and in places "
    "contradicts it. Most first actions are cheap, verified fixes; bigger bets follow a small real-world validation.")

# 2 Executive summary ----------------------------------------------------------
s = new_slide("Executive summary", "A distinctive offer, undersold by the website. Fix first, then validate, then position.",
              source="strategic-intelligence-report.md §1",
              notes="Three columns: what we know for certain (verified on the live site), what we do not know yet, "
                    "and what to do first. Stress that competitor facts and CQC status are Unknown.")
card(s, Inches(0.5), Inches(1.9), Inches(4.0), Inches(4.9), "Strongest findings (verified)",
     ["Menopause, PCOS and PMDD pages list acne treatments",
      "2 menu links return 404 on every page; 19 broken links",
      "Plan step unpriced; old programme pages 404",
      "CQC badge links nowhere; same 4 names on every page",
      "Price conflicts; credit rule only on £350 consultation",
      "IV claim wording; tap-to-call on 1 of 212 pages"], accent=TEAL, size=13)
card(s, Inches(4.7), Inches(1.9), Inches(4.0), Inches(4.9), "Still unverified",
     ["The HVN's CQC inspection status and scope",
      "Every competitor price, membership and rating",
      "All customer reactions (simulated, partly primed)",
      "Booking flow, response times, consultation output",
      "Conversion, retention and reviews (no data access)"], accent=GREY, size=13)
card(s, Inches(8.9), Inches(1.9), Inches(4.0), Inches(4.9), "Do first (30 days)",
     ["Approve the fix list (R01, R02, R06, R10)",
      "Verify CQC status; link the badge (R05)",
      "Decide the programme tier (R03)",
      "Commission the claims review (R04)",
      "Start measurement + low-cost validation (R07; ≈£1.0–1.8k)"], accent=RED, size=13)

# 3 How to read the evidence -------------------------------------------------------
s = new_slide("How to read the evidence", "Every statement carries a source label and a confidence level",
              source="strategic-intelligence-report.md §0; evidence/sources.md",
              notes="Explain why competitor data is Unknown: their sites and the CQC/ASA registers were blocked from the research "
                    "environment, so only press and directories were available. Simulations cost $0.71 in total.")
table(s, Inches(0.5), Inches(1.9), Inches(7.6), [
    ["Label", "Meaning", "Decision use"],
    ["[V] Verified", "Loaded from the-hvn.com (crawl + re-check 15 Oct)", "Yes"],
    ["[Reg] Regulator", "ASA/CQC material found via search", "Context; confirm"],
    ["[R] Reported", "Press, PR, directories (all competitor facts)", "No: treated as Unknown"],
    ["[S] Simulated", "Fictional LLM agents (MiroFish)", "No: hypothesis"],
    ["[?] Unknown", "No data available", "Must be checked"],
], col_w=[1.8, 3.9, 1.9], size=12, row_h=Inches(0.5))
card(s, Inches(8.4), Inches(1.9), Inches(4.4), Inches(4.6), "What we could and could not see",
     ["Could: all 216 website URLs; prices; links; claims",
      "Could not: competitor sites, CQC/ASA registers, Pabau booking",
      "Had no: analytics, bookings, CRM, reviews, staff input",
      "Simulations: 6 runs, 57 interviews, $0.713 total",
      "No new simulations or paid API calls for this review"], accent=NAVY, size=12)

# 4 The offer -----------------------------------------------------------------
s = new_slide("The offer is genuinely distinctive", "Verified differentiators that rivals are not reported to combine",
              source="the-hvn.com crawl 15 Oct 2026; competitor-benchmark.md",
              notes="All five points are verified on the live site. Whether buyers value them, especially 'no membership', "
                    "is a hypothesis to test (H06, H13).")
items = [("One doctor-led team", "GP-trained Medical Director; women's-health doctor; acupuncture; osteopathy; nursing"),
         ("Published prices", "Prices on ~98% of service pages; 342 price points"),
         ("No membership", "Pay per visit; no joining fee (rivals reportedly sell memberships)"),
         ("Doctor check before IV", "'a brief 10 minute consultation with one of our doctors'"),
         ("Women's-health capability", "Doctor + extensive TCM women's-health content")]
for i, (h, d) in enumerate(items):
    x = Inches(0.5 + i * 2.5)
    box(s, x, Inches(2.0), Inches(2.3), Inches(3.6), fill=LIGHT)
    box(s, x, Inches(2.0), Inches(2.3), Inches(0.12), fill=TEAL)
    text(s, x + Inches(0.12), Inches(2.25), Inches(2.1), Inches(0.9), [h], size=17, bold=True, color=NAVY)
    text(s, x + Inches(0.12), Inches(3.2), Inches(2.1), Inches(2.3), [d], size=13)
text(s, Inches(0.5), Inches(5.9), Inches(12.3), Inches(0.9),
     ["Positioning candidate [H, to test]: \"Doctor-led care for skin, energy and long-term health: one Knightsbridge team, clear prices, no membership.\""],
     size=15, color=NAVY, bold=True)

# 5 Price fog -----------------------------------------------------------------
s = new_slide("The biggest commercial gap: 'price fog' after the first step",
              "Transparent up to ~£750, then nothing priced except 8R 'from £3,000'",
              source="evidence/hvn-price-register-2026-10-15.csv; live re-check",
              notes="The £350 Discovery Consultation offers £100 credit against 'Functional Medicine Packages' that are not "
                    "published. The £8k/£12k/£14.5k programmes have been retired or unpublished; their URLs return 404. "
                    "Market anchor: Pillar's 12-week programme from £15,500 (reported, official PR Jan 2026).")
image(s, "price-ladder.png", Inches(0.4), Inches(1.8), w=Inches(8.4))
card(s, Inches(9.0), Inches(1.9), Inches(3.9), Inches(4.8), "What to do",
     ["Decide which programmes exist (R03)",
      "One fees-and-credits table (R08)",
      "Fix NAD and fertility price conflicts (R10)",
      "Publish typical ranges from real Pabau data, after testing the wording (R11)",
      "Simulated buyers asked for a written range, but the question was primed"], accent=RED, size=12)

# 6 Website audit --------------------------------------------------------------
s = new_slide("Website: strong foundations, avoidable defects", None,
              source="website-audit.md; evidence/*.csv; re-check 15 Oct 2026",
              notes="Green bars are strengths (booking link everywhere, prices nearly everywhere). Red bars are defects "
                    "verified on the live site. The 'London's leading' superlative is visible on the home page and present "
                    "in the site-wide search description.")
image(s, "website-audit.png", Inches(0.4), Inches(1.3), w=Inches(8.6))
card(s, Inches(9.2), Inches(1.4), Inches(3.7), Inches(5.3), "Also verified",
     ["H1 'HOW THE HVN CAN HELP'; Contact/Booking titles say 'Skin & Hair'",
      "Two phone numbers",
      "No clinic/local structured data",
      "Median page: 713 KB HTML, 55 images",
      "Mobile and booking flow untested (blocked)"], accent=NAVY, size=12)

# 7 Three fixes ----------------------------------------------------------------
s = new_slide("Three things to fix this month", "All verified live on 15 October 2026; all low effort",
              source="Live re-check; website-audit.md W1–W3",
              notes="These need no customer research. They need your approval to change the website (gate G4) and a "
                    "clinical sign-off for the women's-health content.")
card(s, Inches(0.5), Inches(1.9), Inches(4.0), Inches(4.9), "1 · Women's-health pages",
     ["/menopause/, /pcos/, /premenstrual-dysphoric-disorder/",
      "Block reads: 'Explore our specialised solutions for rosacea, acne, and acne scarring'",
      "Replace with the doctor + acupuncture + tests pathway (R01)"], accent=RED, size=13)
card(s, Inches(4.7), Inches(1.9), Inches(4.0), Inches(4.9), "2 · Broken navigation",
     ["'Clinical Treatments' and 'Holistic Rituals' menu links return 404 on all 212 pages",
      "19 broken internal links; a sitemap URL redirects into a 404",
      "Fix and add 301s (R02)"], accent=RED, size=13)
card(s, Inches(8.9), Inches(1.9), Inches(4.0), Inches(4.9), "3 · Dead-end plan step",
     ["Programme pages return 404",
      "'Functional medicine' lands on an unfinished 'Updated' page",
      "Decide, publish or redirect (R03)"], accent=RED, size=13)

# 8 Trust ---------------------------------------------------------------------
s = new_slide("Trust: proof exists but cannot be verified from the page",
              "Buyers can't see who treats them, what the CQC covers, or the review rating",
              source="Crawl; competitor-benchmark.md B5; report-audit.md U1",
              notes="CQC status: v1 said 'registered, not yet inspected' from a search result. It could not be re-verified and is "
                    "now Unknown. CQC does not regulate some non-surgical cosmetic work, so a badge alone can imply more than it "
                    "covers. Check at source before publishing any status line.")
table(s, Inches(0.5), Inches(1.9), Inches(8.0), [
    ["Signal", "Today [V]", "Fix"],
    ["Who will treat me", "Same 4 names on every page", "Clinician per treatment (R13)"],
    ["CQC", "Badge on 212/212, linked on 0", "Verify; link; accurate line (R05)"],
    ["CQC status", "UNKNOWN (not re-verifiable)", "Registered manager checks at source"],
    ["Reviews", "Widget on 157 pages; rating not in HTML", "Check rating; show it (R21)"],
    ["IV safeguard", "10-minute doctor check, unexplained", "'Before your IV' explainer (R14)"],
    ["Claims", "Immune/boost on 19/20 IV/IM pages", "CAP-code review (R04)"],
], col_w=[1.9, 3.3, 2.8], size=12, row_h=Inches(0.55))
card(s, Inches(8.8), Inches(1.9), Inches(4.1), Inches(4.8), "Simulated signal [S]",
     ["'Who will treat me?' raised in all five full runs",
      "'Registered is not inspected': primed by the seed",
      "Treat as hypotheses H04 and H05",
      "A nearby aesthetics rival shows a CQC 'Good' rating (2023, via search)"], accent=GREY, size=12)

# 9 Journey ---------------------------------------------------------------------
s = new_slide("Customer journey: where it breaks, and where we are blind",
              "17 verified defects before booking; almost no data after it",
              source="customer-journey-map.md",
              notes="Red = verified defects, sand = simulated friction, grey = unknowns. Consultation, treatment and retention "
                    "are unknown because we had no Pabau/CRM access. The validation plan fills that gap.")
image(s, "journey-friction.png", Inches(0.4), Inches(1.8), w=Inches(8.6))
card(s, Inches(9.2), Inches(1.9), Inches(3.7), Inches(4.8), "Moments that matter",
     ["Women's-health visitor lands on the wrong page",
      "'What will it cost overall?'",
      "'Who treats me; is it regulated?'",
      "Broken menu links",
      "Calling from a phone",
      "What a client leaves the consultation with"], accent=NAVY, size=12)

# 10 Segments ---------------------------------------------------------------------
s = new_slide("Segments: each has a verified blocker", "Segment existence is evidenced by The HVN's own pages; behaviour is hypothesis",
              source="customer-journey-map.md §4; personas.md",
              notes="Use this to brief the content owners. Each blocker is verified; what each segment values is to be validated.")
table(s, Inches(0.5), Inches(1.9), Inches(12.3), [
    ["Segment", "Entry point (verified)", "Biggest verified blocker", "Validate"],
    ["Burnt-out executive", "Fatigue page; NAD; Discovery £350", "Plan unpriced; NAD price conflict; no tap-to-call", "H01, H10"],
    ["Longevity optimiser", "8R; blood profiles £450/£550; HRU £750", "Only 8R priced; test list/lab not stated", "H02"],
    ["Aesthetics regular", "£175 consultation; injectables from £260", "Generic practitioner block; no credit rule", "H04"],
    ["Women's health", "Menopause, PCOS, PMDD; acupuncture from £200", "Acne treatments shown", "H08"],
    ["Fertility / IVF", "Fertility acupuncture; panel £500", "Conflicting start prices; sessions unstated", "H01"],
    ["International visitor", "Jet Lag IV £375; Hydrobed", "No tap-to-call; no visitor package", "H10"],
    ["Gatekeeper (PA)", "Contact; terms; CQC badge", "Unlinked badge; two numbers", "H12"],
], col_w=[2.3, 3.9, 4.6, 1.5], size=12, row_h=Inches(0.55))

# 11 Competitors -----------------------------------------------------------------
s = new_slide("Competitors: reported landscape, nothing verified at source",
              "All rival prices, memberships and ratings are UNKNOWN until checked on their own sites",
              source="competitor-benchmark.md; evidence/competitor-benchmark-2026-10-15.csv",
              notes="Hatched bars are reported figures (press, PR) shown only for context. Pillar's £15,500 12-week programme "
                    "is the most recent (official PR, Jan 2026). HUM2N and Harrods 2026 prices could not be found.")
image(s, "competitor-commitment.png", Inches(0.4), Inches(1.8), w=Inches(8.4))
card(s, Inches(9.0), Inches(1.9), Inches(3.9), Inches(4.8), "Reading [H]",
     ["Rivals reportedly sell membership and belonging",
      "The HVN's verifiable edges: price transparency + one team",
      "Its gaps: plan pricing, visible quality proof, single-need depth",
      "New 2026 supply: HUM2N at Six Senses; Four Seasons memberships"], accent=NAVY, size=12)

# 12 Positioning map ------------------------------------------------------------
s = new_slide("Where The HVN can win, and where it probably loses", "Hypotheses to test, not conclusions",
              source="competitor-benchmark.md §4–5",
              notes="Simulated S4 choices (n=11 fictional agents): specialists 5 (+3 drift or split), Lanesborough 1, HUM2N 1, "
                    "The HVN 1 (conditional). Directional only: the seed foregrounded 'no membership' and 'not inspected'.")
table(s, Inches(0.5), Inches(1.9), Inches(7.4), [
    ["Dimension", "The HVN (verified)", "Rivals (reported)"],
    ["Access model", "Pay per visit", "Membership clubs"],
    ["Price transparency", "High (single services)", "Fees / on request"],
    ["Clinical breadth, one team", "Yes", "Operators or partners"],
    ["Visible quality signal", "Badge unlinked; status ?", "Some rated (e.g. CQC Good)"],
    ["Setting and belonging", "Clinic + rituals", "Heritage hotels, clubs"],
    ["Single-need depth", "Doctor + TCM; page defect", "Specialists"],
], col_w=[2.4, 2.5, 2.5], size=12, row_h=Inches(0.55))
image(s, "s4-choice.png", Inches(8.1), Inches(2.0), w=Inches(4.9))
text(s, Inches(8.1), Inches(4.4), Inches(4.9), Inches(1.5),
     ["[SIMULATED] fictional personas; seed primed 'no membership' and 'not inspected'. Use only to choose what to test."],
     size=11, color=GREY)

# 13 SWOT -----------------------------------------------------------------------
s = new_slide("SWOT, with confidence", None, source="strategic-intelligence-report.md §8",
              notes="Each item carries its evidence label and confidence in the report. Opportunities are mostly hypotheses.")
quad = [("Strengths", TEAL, ["Doctor-led team, one address [V]", "Prices on ~98% of service pages [V]",
                              "No membership or joining fee [V]", "Doctor check before IV [V]", "Open 7 days [V]"]),
        ("Weaknesses", RED, ["Plan step unpriced; 404 programmes [V]", "Women's-health pages wrong [V]",
                             "Broken links; tap-to-call on 1 page [V]", "Unlinked CQC badge; status unknown",
                             "Claim wording; no measurement [V]"]),
        ("Opportunities", NAVY, ["Transparent alternative to clubs [Low]", "One team for multi-need clients [Low]",
                                 "Women's health and fertility [Low–Med]", "Evidence-honest positioning [Med]",
                                 "Cheap SEO wins [High]"]),
        ("Threats", GREY, ["New 2026 hotel longevity supply [R]", "£15.5k programme anchors [R]",
                           "Lower-priced specialists [R, Low]", "ASA scrutiny; licensing pending [Reg/R]",
                           "Rivals' visible ratings [Reg via search]"])]
for i, (h, c, lines) in enumerate(quad):
    x = Inches(0.5 + (i % 2) * 6.25)
    y = Inches(1.3 + (i // 2) * 2.85)
    card(s, x, y, Inches(6.05), Inches(2.7), h, lines, accent=c, size=12)

# 14 Simulation value -------------------------------------------------------------
s = new_slide("What the simulations are worth", "Useful for generating hypotheses; not evidence of customer behaviour",
              source="results/*/raw/simulation-db-export.json; report-audit.md D1–D6",
              notes="The heatmap is a keyword count over all agent comments. High numbers often reflect what the seed or "
                    "opening post asked: S2a literally asked 'Would you pay a consultation fee just to find out the total?'. "
                    "Runs share facts, personas and one model, so they are not independent.")
image(s, "simulation-convergence.png", Inches(0.4), Inches(1.75), w=Inches(8.6))
card(s, Inches(9.2), Inches(1.9), Inches(3.7), Inches(4.8), "Limits",
     ["One model plays every persona; cautious voice",
      "Seeds and opening posts primed key themes",
      "S3 never tested the alternative taglines",
      "Fabricated 'experiences' excluded",
      "No demand, conversion or WTP measured"], accent=GREY, size=12)

# 15 Audit ----------------------------------------------------------------------------
s = new_slide("We audited our own v1 report", "29 key statements re-checked: 12 confirmed, 5 corrected, 7 downgraded, 5 now Unknown",
              source="report-audit.md",
              notes="Corrections: 'London's leading' is visible on the home page and in the schema description rather than "
                    "visible on every page; priced pages are 148 (not 149); IV-evidence theme absent in S2a; luxury cues were "
                    "raised (rarely). Downgrades: several simulation counts were echoes of leading questions.")
image(s, "audit-outcomes.png", Inches(0.4), Inches(1.9), w=Inches(7.2))
card(s, Inches(7.9), Inches(1.9), Inches(5.0), Inches(4.8), "What changed in v2",
     ["CQC status and all competitor figures → Unknown",
      "Simulation counts labelled 'primed' where the question led",
      "Positioning and starter pathway: validate, then adopt",
      "Added benchmark, journey map, register, roadmap, validation plan"], accent=NAVY, size=13)

# 16 Priority matrix --------------------------------------------------------------------
s = new_slide("24 recommendations by impact and effort", "Most high-impact items are small or medium effort",
              source="recommendations-register.md",
              notes="Numbers are R-IDs. Red = P1 (days 0–30), sand = P2 (31–60), grey = P3 (61–90 or gated). Impact is a "
                    "hypothesis until measured against the baseline (R07).")
image(s, "priority-matrix.png", Inches(0.6), Inches(1.75), h=Inches(5.2))
card(s, Inches(9.0), Inches(1.5), Inches(3.9), Inches(5.2), "Quick wins",
     ["R01 Women's-health pages", "R02 Broken links", "R05 CQC check + link", "R06 Tap-to-call",
      "R08 Fees and credits", "R10 Price conflicts"], accent=RED, size=13)

# 17 P1 table ------------------------------------------------------------------------
s = new_slide("Priority 1: the first 30 days", None, source="recommendations-register.md",
              notes="Every website change needs your approval (gate G4). R04 needs budget approval for an external adviser.")
table(s, Inches(0.4), Inches(1.3), Inches(12.5), [
    ["ID", "Action", "Evidence · confidence", "Effort", "Owner (role)", "KPI"],
    ["R01", "Fix Menopause/PCOS/PMDD pages", "Live re-check · High", "Small", "Marketing + women's-health doctor", "3/3 fixed; booking clicks"],
    ["R02", "Repair menu and internal links", "Broken-links CSV · High", "Small", "Web developer", "0 internal 404s"],
    ["R03", "Decide programme tier; redirect", "Crawl · High", "Medium", "CEO + Medical Director", "Decision; 0 retired 404s"],
    ["R04", "CAP-code claims review", "Crawl + ASA · High", "Medium", "CEO + adviser", "100% items resolved"],
    ["R05", "Verify CQC; link badge; status line", "Crawl · High; status ?", "Small", "Registered manager", "100% linked; signed off"],
    ["R06", "One number; tap-to-call; mobile bar", "Crawl · High", "Small", "Developer + Ops", "tel: 100%; call clicks"],
    ["R07", "Analytics + funnel baseline", "Study gap · High", "Medium", "Marketing + agency", "Baseline captured"],
    ["R08", "Fees and credits table", "Re-check · High", "Small", "CEO + Finance", "Credit queries ↓"],
    ["R10", "Remove price conflicts; sessions", "Price register · High", "Small", "Marketing + Ops", "0 conflicts"],
], col_w=[0.6, 3.0, 2.4, 0.9, 2.9, 2.7], size=11, row_h=Inches(0.52))

# 18 Roadmap --------------------------------------------------------------------------
s = new_slide("30 / 60 / 90-day roadmap", "Fix and measure → prove and price → position and test",
              source="implementation-roadmap.md",
              notes="Checkpoints: day 30 baseline and fixes; day 60 trust proof, ranges, validation read-out; day 90 "
                    "management review against baseline and go/no-go on the starter pathway.")
image(s, "roadmap-gantt.png", Inches(0.4), Inches(1.75), w=Inches(8.6))
card(s, Inches(9.2), Inches(1.9), Inches(3.7), Inches(4.8), "Checkpoints",
     ["Day 30: baseline; 0 internal 404s; women's-health fixed; CQC line accurate",
      "Day 60: who-treats + IV explainer; ranges decided; validation read-out",
      "Day 90: positioning decided on evidence; pathway go/no-go"], accent=NAVY, size=12)

# 19 KPIs ------------------------------------------------------------------------------
s = new_slide("How we will measure progress", "Baseline first (weeks 1–4), then targets",
              source="customer-journey-map.md §5",
              notes="Targets are deliberately not set yet: without a baseline any target would be a guess.")
table(s, Inches(0.5), Inches(1.9), Inches(12.3), [
    ["Stage", "KPI", "Source"],
    ["Discover", "Organic clicks to service and concern pages", "Search Console"],
    ["Research", "404 page views; engaged sessions", "GA4"],
    ["Price check", "% enquiries tagged price / total / credit", "Enquiry log"],
    ["Book", "Booking-intent rate (book + call + WhatsApp + form) / sessions", "GA4 events"],
    ["Book", "Booking completion; median first-response time", "Pabau; enquiry log"],
    ["Consultation", "Consultation-to-plan conversion within 30 days", "Pabau"],
    ["Retain", "90-day repeat rate; reviews per month and rating", "Pabau; Business Profile"],
], col_w=[2.0, 7.0, 3.3], size=12, row_h=Inches(0.55))

# 20 Validation --------------------------------------------------------------------------
s = new_slide("Validation: small, cheap, real", "≈ 6 weeks · ≈ £1,000–£1,800 external · no simulated agents counted as respondents",
              source="validation-plan.md",
              notes="Interviews use open questions first. The simulation showed that leading questions produce echoes. "
                    "The HVN does recruitment under UK GDPR with consent; incentives are neutral (gift card or donation).")
table(s, Inches(0.5), Inches(1.9), Inches(8.2), [
    ["Workstream", "What", "Cost"],
    ["A Analytics baseline", "GA4 events, Pabau funnel, enquiry log", "Staff time"],
    ["B Booking test", "Staff test, mobile and desktop, no payment", "½ day"],
    ["C Usability", "5–6 non-clients, 5 tasks on the live site", "£400–£600"],
    ["D Interviews", "8–12 clients, lapsed enquirers, gatekeepers", "£400–£600"],
    ["E Copy tests", "After claims review and approval", "Later"],
], col_w=[2.2, 4.4, 1.6], size=12, row_h=Inches(0.55))
card(s, Inches(9.0), Inches(1.9), Inches(3.9), Inches(4.8), "Approval gates",
     ["G1 booking test + tagging", "G2 non-client panel + incentives", "G3 contacting clients/enquirers",
      "G4 any website change or A/B test", "G5 any competitor enquiry"], accent=RED, size=12)

# 21 Hypotheses ----------------------------------------------------------------------------
s = new_slide("Hypotheses the simulations raised, and how to test them", None, source="validation-plan.md §2",
              notes="Prior confidence is low for most because they come from simulation. Decision rules in validation-plan.md §5 "
                    "say what each result changes.")
table(s, Inches(0.4), Inches(1.3), Inches(12.5), [
    ["ID", "Hypothesis", "Prior", "Method", "Changes"],
    ["H01", "Unknown plan totals stop people booking a paid consultation", "M/L", "Interviews, usability, enquiry log", "R11, R12"],
    ["H02", "A published range is enough", "L", "Interviews, usability", "R11"],
    ["H04", "Naming the clinician raises trust and intent", "M", "Usability mock-up, interviews", "R13"],
    ["H05", "Prospects check CQC status (after verifying it)", "L", "R05, then interviews", "R05"],
    ["H06", "'No membership' is a positive differentiator", "L", "Interviews, later A/B", "R15, R16"],
    ["H07", "Concrete safeguards beat superlatives", "L–M", "Usability (two heroes)", "R14, R15"],
    ["H08", "Integrated route can win single-need women's health", "L", "Search Console, interviews", "R17"],
    ["H13", "Verifiability matters more than setting", "L", "Interviews", "Positioning"],
], col_w=[0.7, 5.4, 0.8, 3.4, 2.2], size=11, row_h=Inches(0.55))

# 22 Risks -----------------------------------------------------------------------------------
s = new_slide("Risks and how we manage them", None, source="implementation-roadmap.md; strategic-intelligence-report.md §13",
              notes="The main risk is acting on simulated conclusions as if they were customer evidence; the gates prevent that.")
table(s, Inches(0.5), Inches(1.4), Inches(12.3), [
    ["Risk", "Mitigation"],
    ["CQC status differs from the earlier assumption", "Verify at source before any wording is published (R05)"],
    ["Claims review takes longer than 30 days", "No new IV/longevity copy or paid media until done"],
    ["Price ranges anchor clients wrongly", "Base on 12 months of Pabau data; test wording first"],
    ["Simulation-derived messaging misleads", "Validation gates H06, H07, H13 before any proposition change"],
    ["Competitor facts are stale", "Quarterly verification at source (R24)"],
    ["Website changes break booking links", "QA checklist; re-crawl after every release"],
], col_w=[5.2, 7.1], size=13, row_h=Inches(0.62))

# 23 Decisions -----------------------------------------------------------------------------------
s = new_slide("Decisions requested today", None, source="strategic-intelligence-report.md §1.3",
              notes="Nothing has been deployed and nobody has been contacted. Each decision unlocks a specific gate.")
decisions = [
    "Approve the 30-day fix list: R01, R02, R06, R10 (website-change gate G4)",
    "Ask the registered manager to verify CQC status and scope at source (R05)",
    "Decide which programmes exist today; publish or redirect (R03)",
    "Approve an external CAP-code claims review (R04; quote needed)",
    "Set the consultation fee-credit policy (R08)",
    "Approve measurement setup and validation gates G1–G3 (≈ £1,000–£1,800)",
]
for i, d in enumerate(decisions):
    y = Inches(1.4 + i * 0.9)
    box(s, Inches(0.6), y, Inches(0.6), Inches(0.6), fill=RED)
    text(s, Inches(0.6), y + Inches(0.08), Inches(0.6), Inches(0.5), [str(i + 1)], size=20, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    text(s, Inches(1.4), y + Inches(0.1), Inches(11.3), Inches(0.7), [d], size=18)

# 24 Appendix -----------------------------------------------------------------------------------
s = new_slide("Appendix: files, sources and cost", None, source="research/the-hvn/",
              notes="All files are in the repository under research/the-hvn/. Charts regenerate with charts/build_assets.py.")
table(s, Inches(0.5), Inches(1.4), Inches(7.6), [
    ["File", "Contents"],
    ["strategic-intelligence-report.md", "Full report v2.0"],
    ["recommendations-register.md / .csv", "24 recommendations"],
    ["implementation-roadmap.md", "30/60/90 plan"],
    ["customer-journey-map.md", "Journey and KPIs"],
    ["competitor-benchmark.md / CSV", "Verification status per fact"],
    ["validation-plan.md", "Hypotheses, methods, gates"],
    ["report-audit.md", "Audit of v1"],
    ["evidence/, results/", "Crawl data; simulation raw data"],
], col_w=[3.4, 4.2], size=11, row_h=Inches(0.48))
image(s, "run-costs.png", Inches(8.3), Inches(1.5), w=Inches(4.8))
text(s, Inches(8.3), Inches(3.7), Inches(4.8), Inches(2.5),
     ["Simulation API cost: $0.713 for 6 runs (490 requests, 0 errors).",
      "This review: no new simulations, no paid API calls."], size=12, color=GREY)

out = ROOT / "executive-presentation.pptx"
prs.save(out)
print("saved", out, "slides:", len(prs.slides))
