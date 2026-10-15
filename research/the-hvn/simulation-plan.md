# The HVN — MiroFish Simulation Plan (for approval)

**Status:** Proposal only. Nothing has been uploaded, simulated or charged.
**Seed source:** [`dossier.md`](./dossier.md)
**Branch:** `claude/focused-franklin-nfz9cx` (security-hardened)

---

## 1. What MiroFish can and cannot tell us

**What MiroFish does:**
1. Builds a knowledge graph from a seed document.
2. Generates LLM "agents" from the entities in that graph.
3. Lets them post, comment and react on a simulated Reddit- or Twitter-style platform.
4. Writes a report.

**What that gives us:** a structured way to stress-test **how plausible personas might react to narratives, prices and claims**, and to surface objections we haven't thought of.

**Limits:**
- It does **not** measure real demand, conversion or market share.
- Agents inherit the biases of the seed text and the model.
- Every output is labelled **[SIMULATED]** and treated as hypotheses to validate, never as customer data.

**Platform choice:** **Reddit mode only.**
- OASIS's Twitter mode downloads an AI model from Hugging Face, which is blocked here and adds supply-chain surface.
- Reddit-style threads also suit considered, high-ticket purchase discussion better.

---

## 2. Proposed simulations

Each simulation uses the **same base seed** (dossier §§1–4, with individual names replaced by roles; see §4) plus a short **scenario brief**. MiroFish turns the scenario brief into its "simulation requirement".

### A. Brand perception

- **Question:** *How do prospective luxury-wellness clients in London interpret what The HVN is (spa, medical clinic, longevity clinic, or aesthetics clinic), and which elements build or erode their sense of luxury and credibility?*
- **Scenario brief:** A thread starts with "Has anyone tried The HVN in Knightsbridge? Is it a spa or a clinic?" Agents draw on the positioning statements, founder pedigree, CQC status and service breadth in the seed.
- **What we'll look for:** category confusion; which proof points get cited (CQC, Medical Director, Levitas, Hydrobed); luxury cues vs scepticism.

### B. Pricing and trust

- **Question:** *How do different personas react to The HVN's published pricing (consultations £100–£400, single treatments £200–£500, programmes £999–£14,500, annual price unpublished) and its booking terms (card on file, 100% late-cancellation charge)? Where is the main drop-off risk?*
- **Scenario brief:** A thread comparing the 360° Programme (£14,500, 16 weeks) and the Sleep Programme (£8,000) against single treatments and competitor memberships.
- **Variants:** two runs on one seed:
  - B1: current state.
  - B2: hypothetical mid-tier option (e.g. a £1,500–£2,500 "introductory pathway"). Clearly marked as a **hypothetical test**, not a real offer.

### C. Marketing messaging

- **Question:** *Which framing resonates most with each persona: "conscious wellbeing / conscious luxury", "evidence-based longevity", or "root-cause functional medicine"? And how do evidence-literate personas respond to IV-drip benefit claims?*
- **Scenario brief:** Three alternative campaign messages (drafted from The HVN's own published language) posted as if from the brand. Agents react, compare and challenge.
- **What we'll look for:** resonance per persona; backlash triggers; credibility of claims (links to the ASA context in dossier §2.4).

### D. Competitive positioning

- **Question:** *When choosing between The HVN, Lanserhof at The Arts Club, HUM2N, the Harrods Wellness Clinic and The Lanesborough Club & Spa, which personas choose which, and why?*
- **Scenario brief:** "Best longevity/wellness clinic in London?" thread with competitor positioning and published prices from dossier §4.2, each with its caveats.
- **What we'll look for:** switching reasons; membership vs programme preference; where The HVN wins or loses.
- **Care point:** competitor information is limited to publicly published facts, and agents are told prices may be outdated.

### Run parameters (each simulation)

| Parameter | Value | Why |
|---|---|---|
| Platform | Reddit only | No model download; suits considered purchases |
| Agents | ~15–25 (generated from persona entities) | Enough diversity, low cost |
| Rounds | 10 (max 15) | README advises starting below 40 |
| Graph memory updates | **Off** | Fewer Zep calls and less data sent |
| Report agent | On (default settings) | Produces the summary |

Total: **5 runs** (A, B1, B2, C, D).

---

## 3. Estimated costs

> **These are estimates, not measurements.** The first run will be metered and costs re-estimated before continuing. Claude 5-series models also bill internal reasoning as output tokens, which can push costs up.

**Assumed volume per run:** about 0.75–1.5 M input tokens and 0.1–0.2 M output tokens. This covers ontology, profiles, config, ~10 rounds × ~20 agents, and the report.

| Model (Anthropic API) | Price per M tokens (in / out) | Per run | 5 runs |
|---|---|---|---|
| **Claude Haiku 5.5** (recommended start) | $0.10 / $0.50 | ~$0.15–0.50 | **~$1–3** |
| Claude Sonnet 5.5 | $2 / $10 | ~$2.50–5 | ~$12–25 |
| Claude Opus 5.5 | $4 / $20 | ~$5–10 | ~$25–50 |

- **Zep Cloud:** free tier assumed. The seed is about 30 KB, so roughly 60–80 text chunks become graph episodes per run. Confirm limits in your Zep dashboard.
- **Recommendation:**
  1. Run everything on **Haiku 5.5** first, with a hard spend limit on the API key (e.g. $10).
  2. Re-run only the most decision-relevant simulation on Sonnet 5.5 if Haiku's reasoning looks shallow.

---

## 4. Data handling

- The seed is sent to **Anthropic** (LLM processing) and **Zep Cloud** (stores the knowledge graph). Both are external services; please confirm you're comfortable with that.
- The seed contains **only public information**. For the seed version I will:
  - replace named individuals with roles (e.g. "the Medical Director"), as names aren't needed for the simulations;
  - include **no** patient or customer data;
  - keep evidence labels, so agents can see which facts are verified versus hypothetical.
- After the runs, I can delete the Zep graphs (MiroFish has a delete endpoint) if you prefer nothing to persist there.

---

## 5. Required environment settings and approvals

**You change (environment settings, cloud environment menu → Edit):**
1. **Network access:** add `api.getzep.com` to Allowed domains. Required.
2. **Network secrets:** add `LLM_API_KEY` (new Anthropic key with a low spend limit) and `ZEP_API_KEY`. Please don't paste keys into chat.
3. **Optional, for a live website audit:** allow `the-hvn.com` and the competitor domains in §4.2. That lets me load pages directly, check the booking flow up to (not including) payment, and run Lighthouse to turn several [NEEDS TESTING] items into verified findings. In this session even search-based page fetching failed DNS lookup, so live verification needs this.

**I do, after your approval:**
1. **Code change, needs approval:** small Claude compatibility fix in `backend/app/utils/openai_chat_compat.py`. Current Claude models reject the temperature values MiroFish sends. Includes unit tests; committed to the working branch.
2. **One test API call**, costing under $0.01, to confirm the Claude connection and JSON handling.
3. **Create the seed file** (de-identified dossier plus scenario brief).
4. **Run A** (Haiku 5.5, Reddit, ~20 agents, 10 rounds), then report the actual cost.
5. **Continue with B1, B2, C and D** only if the cost and quality look right.
6. Add the **[SIMULATED]** findings to dossier §5 and summarise them.
