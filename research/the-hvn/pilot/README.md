# MiroFish Pilot Runbook (budget-capped, Haiku-only)

**S1 pilot executed once on 15 Oct 2026** ($0.084; results in `../results/s1-pilot-2026-10-15/`).
**Fixed parameters:** Reddit only · `claude-haiku-5-5` only · 10–12 agents · `max_rounds=8` · graph memory updates **off** · hard cap **$1.00**.

## Files
| File | Purpose |
|---|---|
| `budget_proxy.py` | Local proxy. **Holds the real API key** (injected per request; the backend only gets a placeholder). Reserves each request's worst-case cost before forwarding and refuses anything that could breach the cap. Converts upstream 408/409/429/5xx and network errors into non-retryable 400s. Allows Haiku only; refuses streaming. Writes `ledger.jsonl` (tokens and cost only). |
| `start_proxy.sh` | Starts the proxy with the pilot settings (`BUDGET_USD`, default 1.00). |
| `start_backend_via_proxy.sh` | Starts MiroFish with a **placeholder key**, `LLM_BASE_URL` set to the proxy, model pinned to Haiku, and client timeouts above the proxy's upstream timeout. |
| `run_pilot.py` | Staged driver: `--confirm-paid` / `--confirm-zep` gates, English locale header, routing check after the first paid call, agent count must be 10–12, guard stops (proxy down, spend ≥ $0.70, >30% upstream errors; report skipped at ≥ $0.80). |

## Procedure (from the repository root)
```bash
bash research/the-hvn/pilot/start_proxy.sh &                 # real key stays in this process
bash research/the-hvn/pilot/start_backend_via_proxy.sh &     # placeholder key only
cd research/the-hvn/pilot
python3 run_pilot.py --stage preflight
python3 run_pilot.py --stage ontology --confirm-paid         # verifies routing (~$0.003)
python3 run_pilot.py --stage build --confirm-zep
python3 run_pilot.py --stage entities                         # pick types totalling 10-12 invented participants
python3 run_pilot.py --stage entities --entity-types TypeA,TypeB
python3 run_pilot.py --stage prepare --confirm-paid
python3 run_pilot.py --stage start --confirm-paid
python3 run_pilot.py --stage report --confirm-paid
curl -s --noproxy 127.0.0.1 http://127.0.0.1:8787/__budget
```

## Lessons from the 15 Oct run (apply before the next run)
1. **Run-status bug:** OASIS finishes the loop and waits for commands, but MiroFish's run-status stays at round 0 / "running". When `simulation.log` shows "模拟循环完成" (loop complete), run batch interviews first (`/api/simulation/interview/batch`), then `POST /api/simulation/close-env`, and only then `--stage report` (the report returns 409 while the run is "running").
2. **Simulated clock starts at 00:00:** 8 rounds of 60 minutes is night-time, so almost no agents are active. Use ≥ 16–24 rounds, or adjust `time_config` before `start`.
3. **Locale:** fixed. The driver now sends `Accept-Language: en` (the 15 Oct run produced Chinese profiles).
4. **Check `event_config.initial_posts` authors** before `start` (they were mis-assigned between personas).
5. **Treat the MiroFish auto-report as raw output;** verify every claim against `simulation-db-export.json`.

## Run-2 procedure additions (used on 15 Oct 2026)
- New ledger per run: `LEDGER=ledger-run2.jsonl bash start_proxy.sh` (fresh $1 cap); separate `--state` file.
- If an agent entity type contains a real person or a placeholder, delete those nodes from **that run's own graph** before `prepare`.
- After `prepare`: check profiles and opening posts for non-English text and persona/author mismatches, and log any data fixes.
- `--stage clockshift --start-hour 9`, then `--stage start --max-rounds 24`.
- `--stage activity` (gate) → `--stage interview` (environment alive) → `--stage close` → `--stage report` (only if the gate passed).

## Verified safeguards (15 Oct 2026)
- Backend process environment: placeholder key only, the real key absent (booleans checked).
- Direct calls to Anthropic with the backend's credentials: HTTP 401.
- Free `count_tokens` call through the proxy: HTTP 200 (TLS through the environment proxy works).
- 53/53 requests Haiku, all through the proxy, 0 refused, 0 upstream errors.
- Offline tests (fake upstream): key injection, auth stripping, 429/503 → non-retryable 400, worst-case reservation refusal, model and stream blocks, no secrets in ledger or banner.

## Independent backstop
Set a low monthly spend limit in the Claude Console for the workspace that holds the API key; it can't be set or verified from the container.
