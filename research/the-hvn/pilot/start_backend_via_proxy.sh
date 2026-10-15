#!/usr/bin/env bash
# Start the MiroFish backend with all LLM traffic routed through the local
# budget proxy and pinned to Claude Haiku.
#
# The backend receives only a PLACEHOLDER LLM key: the real key lives in the
# budget proxy (start_proxy.sh, --inject-key-env). Any LLM request that tried
# to bypass the proxy would therefore fail authentication instead of billing.
# Client timeouts are set above the proxy's 300 s upstream timeout so clients
# never time out and retry a request that is still running upstream.
set -euo pipefail
cd "$(dirname "$0")/../../../backend"
exec env -u LLM_API_KEY -u OPENAI_API_KEY -u ANTHROPIC_API_KEY -u LLM_BOOST_API_KEY \
  LLM_API_KEY="placeholder-real-key-is-held-by-budget-proxy" \
  LLM_BASE_URL="http://127.0.0.1:8787/v1" \
  LLM_MODEL_NAME="claude-haiku-5-5" \
  MODEL_TIMEOUT="900" \
  NO_PROXY="127.0.0.1,localhost${NO_PROXY:+,$NO_PROXY}" \
  .venv/bin/python run.py
