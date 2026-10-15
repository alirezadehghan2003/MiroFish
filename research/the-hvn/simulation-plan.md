# The HVN: MiroFish Simulation Plan v2

**Status (15 Oct 2026):** Phase 0 complete. **Phase 1 pilot prepared but NOT run.** Nothing has been uploaded to Zep, no agents have been created, and no paid simulation calls have been made.
**Supersedes:** `archive/simulation-plan-v1-2026-10-15.md`.

## 1. Principles
1. **Simulations generate hypotheses; they do not measure customers.** Every output is labelled [SIMULATED] and kept separate from evidence in all reports.
2. **Reddit mode only.** Twitter mode downloads a Hugging Face model, which this environment blocks.
3. **Claude Haiku only** (`claude-haiku-5-5`). No Sonnet or Opus runs in this plan.
4. **Graph memory updates off** (`enable_graph_memory_update: false`).
5. **Seeds are public-information only** (`seeds/`), with staff referred to by role and participants clearly marked [Invented].
6. **Spend is hard-capped** by a local budget proxy (§5), with a separate approval for every paid or data-sharing stage.

## 2. Phases
| Phase | Scenario | Seed | Agents | Rounds | Status |
|---|---|---|---|---|---|
| 0 | Evidence refresh: dossier v2, audit, competitors, personas, seeds | — | — | — | **Done** |
| **1 (pilot)** | **S1 Brand perception** | `seeds/s1-brand-perception.md` | **10–12** | **8** | **Prepared, awaiting approval** |
| Gate | Go/no-go: agents in character and grounded in the seed, actual cost measured | | | | |
| 2 | S2 Booking decision (current offer) | `s2-booking-decision.md` | 10–12 | 10–15 | Seed ready |
| 2 | S2b same, plus a clearly hypothetical "Starter Pathway" | `s2` + `s2b-hypothetical-pathway-addendum.md` | 10–12 | 10–15 | Seed ready |
| 2 | S3 Messaging (live copy vs 3 test messages) | `s3-messaging.md` | 10–12 | 10–15 | Seed ready |
| 2 | S4 Competitor choice | `s4-competitor-choice.md` | 10–12 | 10–15 | Seed ready |
| 3 | Repeat the most decision-relevant run twice (stochastic stability) | as chosen | 10–12 | as chosen | Planned |
| 4 | Synthesis into the executive report | — | — | — | Planned |

## 3. Agent roster
The 12 [Invented] participants are identical across S1–S4 so results can be compared:
- **Customer archetypes (9):** P1 executive, P2 longevity optimiser, P3 aesthetics, P4 women's health, P5 fertility, P6 international visitor, P7 holistic seeker, P8 bridal, P9 gatekeeper.
- **Challenger voices (3):** sceptical GP, wellness journalist, competitor members'-club member.
- **No competitor brand accounts**, and no HVN brand account.

MiroFish creates agents from the knowledge-graph entity types chosen at the `prepare` step. The pilot driver lists entity types and counts after the graph is built and **aborts unless the chosen types total 10–12 agents**.

## 4. Cost model for the S1 pilot (estimate)

**Prices:** Claude Haiku 5.5 at $0.10 per million input tokens and $0.50 per million output tokens (prompts up to 100K tokens). Above 100K: $0.50 / $2.50, which the proxy also prices in.

| Step (from MiroFish code) | Model calls | Tokens per call (in / out, est.) | Est. cost |
|---|---|---|---|
| Ontology (`/api/graph/ontology/generate`) | 1 | 6k / 3k | $0.002 |
| Graph build (Zep; no LLM calls from MiroFish) | 0 | — | $0 (Zep usage: ~19–22 chunks) |
| Agent profiles (1 per agent, up to 3 attempts) | 12–36 | 3k / 1.5k | $0.01–0.04 |
| Simulation config (3 + 1 batch of agents) | 4 | 10k / 3k | $0.01 |
| Simulation: 8 rounds × ~6–10 active agents × ~1–2 calls | 50–160 | 4–8k / 0.3–0.6k | $0.05–0.20 |
| Report (outline + 2–5 sections × up to 5 steps, plus tool calls) | 15–45 | 8–20k / 1.5k | $0.03–0.12 |
| **Total** | **~80–250** | | **≈ $0.10–0.40 expected** |

- **Uncertainty:** Haiku 5.5 bills any internal reasoning as output tokens, and feed size grows each round. The estimate is therefore wide, and the cap below sits well above it.
- **Recommended hard cap: $1.00** for the pilot. The proxy ledger gives the real figure, which will be used to re-estimate Phase 2.
- **Phase 2 projection** (to be re-estimated after the pilot): about $0.25–0.60 per run, so **about $1–3 for S2, S2b, S3 and S4**.

## 5. Spending control: what is and is not enforceable

| Control | Enforced by | Reliability |
|---|---|---|
| **Local budget proxy** (`pilot/budget_proxy.py`): meters `usage` on every response, refuses all requests once the cap is reached (HTTP 400, which the SDK does not retry), blocks any model other than `claude-haiku-5-5`, refuses streaming | Runs in this container; MiroFish and its OASIS subprocess reach Anthropic only through `LLM_BASE_URL` | **Hard** for traffic that passes through it. Overshoot is limited to requests already in flight (about $0.01). Tested offline against a fake upstream: cap, model block, stream block, auth pass-through, and no keys in the ledger. |
| Routing check | The driver aborts after the first paid call (~$0.002) if the proxy didn't see it; preflight aborts if a `.env` would override `LLM_BASE_URL` | Prevents unmetered runs |
| Staged approvals | `--confirm-paid` and `--confirm-zep` flags; `--stage` gating | Procedural |
| Round and agent limits | `max_rounds=8`; agent count must be 10–12 | Bounds work, not cost |
| **Anthropic Console spend limit** on the API key's workspace | Anthropic | **Cannot be verified or set from this container.** A regular API key can't read or change org limits (that needs the Admin API). Recommended as an independent backstop: set a low monthly limit on the workspace that holds this key, in the Claude Console. |

## 6. Limitations
- Reddit-style threads stand in for considered peer discussion; UK HNW clients rarely discuss clinics on Reddit.
- All agents run on one model and inherit its biases. Outputs vary between runs (Phase 3 checks this).
- Agents know only the seed. Competitor facts in the seeds are search-sourced and dated.
- No real demand, conversion or willingness-to-pay can be inferred.
- MiroFish's report agent can overstate; every simulated claim will be checked against the raw action logs before it reaches the executive report.

## 7. Data handling
- Seeds go to **Anthropic** (LLM) and **Zep Cloud** (knowledge graph) only when the `build` stage is approved.
- `pilot/run_pilot.py --stage cleanup --confirm-zep` deletes the pilot graph from Zep afterwards.
