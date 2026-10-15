# The HVN: Business & Marketing Intelligence Study

| | |
|---|---|
| **Subject** | The HVN, 57–63 Knightsbridge, London ([the-hvn.com](https://the-hvn.com)) |
| **Status** | Research, 6 simulation runs (total API cost **$0.713**) and the management strategy (v2.0, 15 Oct 2026) are complete. Phase 4 readiness pack prepared (`phase-4/`); real-world validation and all website changes await approval. |
| **Start here** | [`strategic-intelligence-report.md`](strategic-intelligence-report.md) (v2.0) · [`executive-presentation.pptx`](executive-presentation.pptx) / [PDF](executive-presentation.pdf) · [`recommendations-register.md`](recommendations-register.md) |
| **Simulated results** | `results/` (one folder per run, each with `analysis.md`) · totals in `results/summary-metrics.json` |

## Contents
| File | What it is |
|---|---|
| [`strategic-intelligence-report.md`](strategic-intelligence-report.md) | Strategic report v2.0: verified situation, priority problems, positioning, journey, pricing, competitors, SWOT, recommendations, roadmap, validation; confidence levels and charts |
| [`executive-presentation.pptx`](executive-presentation.pptx) · [`.pdf`](executive-presentation.pdf) | 24-slide management deck with speaker notes |
| [`recommendations-register.md`](recommendations-register.md) · [`.csv`](recommendations-register.csv) | 24 recommendations: evidence, confidence, solution, impact hypothesis, effort, owner, priority, KPI, approval gate |
| [`implementation-roadmap.md`](implementation-roadmap.md) | 30/60/90-day plan with owners, dependencies, checkpoints and risks |
| [`customer-journey-map.md`](customer-journey-map.md) | Awareness → booking → consultation → treatment → retention; funnel KPIs |
| [`competitor-benchmark.md`](competitor-benchmark.md) | Benchmark with verification status per fact (`evidence/competitor-benchmark-2026-10-15.csv`) |
| [`validation-plan.md`](validation-plan.md) | Hypotheses from simulation and a low-cost real-world test plan with approval gates |
| [`report-audit.md`](report-audit.md) | Audit of report v1: confirmed, corrected, downgraded and unknown statements |
| [`charts/`](charts/) | Charts plus `build_assets.py` / `build_deck.py` (regenerate offline) |
| [`executive-presentation-outline.md`](executive-presentation-outline.md) | v1 outline (superseded) |
| [`phase-4/`](phase-4/) | **Phase 4 (15 Oct 2026):** 30-day priorities, booking-journey audit, measurement spec, real-customer research kit, implementation tickets, draft women's-health copy, CQC checklist, approval register, execution dashboard |
| [`dossier.md`](dossier.md) | Integrated evidence dossier v2: brand, offer and prices, trust, market, regulation, open questions |
| [`website-audit.md`](website-audit.md) | Live website audit: 12 prioritised findings (P1–P3) with evidence and fixes |
| [`competitors.md`](competitors.md) | Tiered competitor matrix (direct / longevity substitutes / specialists / substitutes / partner) |
| [`personas.md`](personas.md) | 9 segments and personas (incl. women's health, fertility, bridal); targeting evidence vs hypotheses |
| [`simulation-plan.md`](simulation-plan.md) | Phased MiroFish plan, cost model, spend controls, limitations |
| [`seeds/`](seeds/) | Public-only simulation seeds S1–S4 (+ hypothetical S2b) and their simulation requirements |
| [`pilot/`](pilot/) | S1 pilot runbook, budget-capping proxy, staged driver |
| [`results/`](results/) | Simulation runs: raw logs, metrics, cost ledger, analysis ([SIMULATED]) |
| [`evidence/`](evidence/) | Crawl table, price register, broken-link list, source log |
| [`archive/`](archive/) | Superseded v1 files and the list of retired claims |

## Evidence rules
- **[LIVE]** = loaded from the-hvn.com on 15 Oct 2026. **[OFFICIAL-PR] / [TRADE/PRESS] / [DIRECTORY] / [REGULATOR]** = third-party sources via search.
- **[HYPOTHESIS]** = analyst inference. **[SIMULATED]** = MiroFish output, never presented as customer evidence.
- No customer or patient data was used. Persona participants in seeds are marked **[Invented]**.
- Competitor websites, CQC, ASA and the booking platform could not be loaded from this environment; competitor facts are search-sourced and dated.
