# S1 Brand Perception Pilot: Launch Runbook

**Status:** prepared, **not run**. Requires explicit approval.
**Fixed parameters:** Reddit only · `claude-haiku-5-5` only · 10–12 agents · `max_rounds=8` · graph memory updates **off** · hard budget cap **$1.00** · expected cost **≈ $0.10–0.40** (see `../simulation-plan.md` §4).

## Files
| File | Purpose |
|---|---|
| `budget_proxy.py` | Local proxy that meters every LLM response and refuses requests after the cap or for any model other than Haiku. Writes `ledger.jsonl` (tokens and cost only; no prompts, no keys). |
| `start_backend_via_proxy.sh` | Starts the MiroFish backend with `LLM_BASE_URL` pointed at the proxy and `LLM_MODEL_NAME=claude-haiku-5-5`. |
| `run_pilot.py` | Staged driver with a gate on every paid or Zep stage; aborts if traffic bypasses the proxy or if the agent count is outside 10–12. |

## Commands (three terminals, from the repository root)

**Terminal 1: budget proxy (free)**
```bash
cd research/the-hvn/pilot
python3 budget_proxy.py --budget-usd 1.00 --allow-model claude-haiku-5-5 \
  --input-per-mtok 0.10 --output-per-mtok 0.50 \
  --long-context-threshold 100000 --long-input-per-mtok 0.50 --long-output-per-mtok 2.50 \
  --ledger ledger.jsonl
```

**Terminal 2: backend routed through the proxy (free to start)**
```bash
bash research/the-hvn/pilot/start_backend_via_proxy.sh
```

**Terminal 3: the pilot, stage by stage**
```bash
cd research/the-hvn/pilot
python3 run_pilot.py --stage preflight                    # free
python3 run_pilot.py --stage ontology --confirm-paid      # ~$0.002, verifies proxy routing
python3 run_pilot.py --stage build    --confirm-zep       # uploads S1 seed (~9 KB) to Zep
python3 run_pilot.py --stage entities                     # free; must show 10–12 agents
#   if not 10–12, re-run with:  --entity-types TypeA,TypeB
python3 run_pilot.py --stage prepare  --confirm-paid      # profiles + config (~$0.02–0.05)
python3 run_pilot.py --stage start    --confirm-paid      # 8 Reddit rounds (~$0.05–0.20)
python3 run_pilot.py --stage report   --confirm-paid      # report agent (~$0.03–0.12)
curl -s http://127.0.0.1:8787/__budget                     # actual spend so far
python3 run_pilot.py --stage cleanup  --confirm-zep       # optional: delete the Zep graph
```

**Single command after approval** (stops at the entities check if the agent count is wrong):
```bash
python3 run_pilot.py --stage all --confirm-paid --confirm-zep
```

## Safety behaviour (verified offline on 15 Oct 2026, no API calls)
- Without `--confirm-paid` the driver stops before `ontology` (dry run: preflight passed, ledger $0.00).
- The proxy refused a request once spend reached the cap, refused `claude-sonnet-5-5`, refused streaming, forwarded the auth header unchanged, and wrote no key material to the ledger.
- The long-context tier is applied to prompts over 100K tokens.

## Independent backstop (recommended)
Set a low monthly spend limit on the Anthropic workspace that holds this API key, in the Claude Console. This can't be checked or set from the container with a regular API key.
