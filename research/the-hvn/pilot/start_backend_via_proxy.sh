#!/usr/bin/env bash
# Start the MiroFish backend with all LLM traffic routed through the local
# budget proxy and pinned to Claude Haiku. API keys are inherited from the
# environment and never printed.
set -euo pipefail
cd "$(dirname "$0")/../../../backend"
export LLM_BASE_URL="http://127.0.0.1:8787/v1"
export LLM_MODEL_NAME="claude-haiku-5-5"
export NO_PROXY="127.0.0.1,localhost${NO_PROXY:+,$NO_PROXY}"
exec .venv/bin/python run.py
