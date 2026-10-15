#!/usr/bin/env bash
# Stop the budget proxy, MiroFish backend and any OASIS simulation process.
pkill -f "budget_proxy.py" 2>/dev/null
pkill -f "\.venv/bin/python run\.py" 2>/dev/null
pkill -f "run_reddit_simulation.py" 2>/dev/null
sleep 2
if pgrep -f "budget_proxy.py|\.venv/bin/python run\.py|run_reddit_simulation.py" >/dev/null; then
  echo "WARNING: some processes still running"; exit 1
fi
echo "all services stopped"
