#!/usr/bin/env bash
# Start a fresh budget proxy (new ledger => fresh $1 cap) and the MiroFish backend
# for one scenario. Usage: start_services.sh <ledger-file> <log-dir>
set -euo pipefail
LEDGER="$1"; LOGDIR="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"
if pgrep -f "budget_proxy.py" >/dev/null || pgrep -f "\.venv/bin/python run\.py" >/dev/null; then
  echo "services already running - stop them first" >&2; exit 1
fi
[ -e "$HERE/$LEDGER" ] && { echo "ledger $LEDGER already exists - use a new one" >&2; exit 1; }
cd "$HERE"
LEDGER="$LEDGER" setsid nohup bash start_proxy.sh > "$LOGDIR/proxy.log" 2>&1 < /dev/null &
sleep 2
setsid nohup bash start_backend_via_proxy.sh > "$LOGDIR/backend.log" 2>&1 < /dev/null &
for i in $(seq 1 30); do
  curl -s --noproxy 127.0.0.1 http://127.0.0.1:5001/health >/dev/null 2>&1 && break; sleep 1
done
head -1 "$LOGDIR/proxy.log"
