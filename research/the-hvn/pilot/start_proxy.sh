#!/usr/bin/env bash
# Start the budget proxy for the S1 pilot: $1.00 hard cap, Claude Haiku 5.5 only,
# real key injected from LLM_API_KEY (never printed), upstream retries blocked.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 budget_proxy.py --budget-usd "${BUDGET_USD:-1.00}" --allow-model claude-haiku-5-5 \
  --input-per-mtok 0.10 --output-per-mtok 0.50 \
  --long-context-threshold 100000 --long-input-per-mtok 0.50 --long-output-per-mtok 2.50 \
  --inject-key-env LLM_API_KEY --no-upstream-retry --upstream-timeout 300 \
  --ledger "${LEDGER:-ledger.jsonl}"
