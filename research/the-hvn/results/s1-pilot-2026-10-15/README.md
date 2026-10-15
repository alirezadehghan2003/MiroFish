# S1 Brand Perception Pilot (15 Oct 2026)

**Everything in this folder is [SIMULATED] output or its metadata. It is not customer evidence.**

| File | Content |
|---|---|
| `analysis.md` | Analyst's report: what ran, quality issues, simulated signals mapped to verified evidence, audit of the auto-report, cost |
| `run-metrics.json` | Model, agents, rounds, activity, requests, tokens, cost by stage, safeguards verified |
| `mirofish-report.md` | MiroFish's auto-generated report (**unreliable**; see analysis §5) |
| `raw/simulation-db-export.json` | All users, posts, comments, likes and traces (readable JSON) |
| `raw/reddit_simulation.db` | Original OASIS SQLite database |
| `raw/simulation_config.json`, `raw/reddit_profiles.json` | Generated config and agent profiles |
| `raw/simulation.log`, `raw/oasis-logs/` | OASIS run logs |
| `raw/proxy-ledger.jsonl` | Per-request tokens and cost from the budget proxy (no prompts, no keys) |
| `raw/report.json`, `raw/report-agent-log.jsonl`, `raw/report-console-log.txt` | Report-agent output and tool-call log |
| `raw/run_state.json`, `raw/pilot_state.json` | MiroFish run state and driver state (project, graph, simulation IDs) |

**Headline:** $0.084 total (cap $1.00), 53 requests, 10 agents, 8/8 rounds, but only 3 agent actions because the simulated clock covered 00:00–08:00. See `analysis.md` before using anything here.
