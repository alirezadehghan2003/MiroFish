#!/usr/bin/env python3
"""
Local spend-capping proxy for MiroFish LLM traffic (research tooling, not app code).

MiroFish and its OASIS simulation subprocess send every LLM request to
LLM_BASE_URL. Point LLM_BASE_URL at this proxy and it will:

  * forward each request to the real upstream (default
    https://api.anthropic.com/v1);
  * with --inject-key-env NAME, hold the real API key itself: incoming auth
    headers are discarded and the key from environment variable NAME is
    added. The backend can then run with a placeholder key, so nothing in it
    can authenticate to Anthropic directly (no bypass);
  * reserve each request's WORST-CASE cost before forwarding (estimated
    prompt tokens + its max_tokens as output) and refuse it if spent +
    in-flight reservations + this reservation would exceed --budget-usd.
    The cap therefore cannot be overshot, even by concurrent requests;
  * settle the reservation to the real cost from the response `usage`;
  * with --no-upstream-retry, turn upstream 408/409/429/5xx and network
    errors into HTTP 400, which OpenAI-SDK clients do not retry, so
    automatic client retries cannot re-send (and re-bill) a request;
  * refuse any model not in --allow-model, and refuse streaming requests
    (their usage cannot be metered here);
  * append one line per forwarded request to --ledger: time, model, status,
    tokens, cost, running total. No prompt text, response text or headers
    are ever written, and the injected key is never printed or logged.

Usage:
  python3 budget_proxy.py --budget-usd 1.00 --allow-model claude-haiku-5-5 \\
      --input-per-mtok 0.10 --output-per-mtok 0.50 \\
      --long-context-threshold 100000 --long-input-per-mtok 0.50 --long-output-per-mtok 2.50 \\
      --inject-key-env LLM_API_KEY --no-upstream-retry --ledger ledger.jsonl
"""

import argparse
import json
import os
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

FORWARD_HEADERS = {"authorization", "x-api-key", "anthropic-version",
                   "anthropic-beta", "content-type", "accept"}
AUTH_HEADERS = {"authorization", "x-api-key"}
RETRYABLE = {408, 409, 429}
DEFAULT_MAX_TOKENS = 8192     # what MiroFish sends for Claude when unset
CHARS_PER_TOKEN = 2.5         # deliberately pessimistic prompt-size estimate


class Budget:
    def __init__(self, cap, in_rate, out_rate, ledger, long_threshold=None,
                 long_in_rate=None, long_out_rate=None):
        self.cap, self.in_rate, self.out_rate = cap, in_rate, out_rate
        # Some models bill a higher rate once a prompt exceeds a size threshold.
        self.long_threshold = long_threshold
        self.long_in_rate = long_in_rate if long_in_rate is not None else in_rate
        self.long_out_rate = long_out_rate if long_out_rate is not None else out_rate
        self.ledger = ledger
        self.spent = 0.0
        self.reserved = 0.0
        self.requests = 0
        self.refused = 0
        self.upstream_errors = 0
        self.tokens_in = 0
        self.tokens_out = 0
        self.lock = threading.Lock()
        if os.path.exists(ledger):  # resume the running total across restarts
            with open(ledger) as f:
                for line in f:
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    self.spent = max(self.spent, float(row.get("total_usd", 0)))
                    self.requests += 1
                    self.tokens_in += int(row.get("input_tokens", 0))
                    self.tokens_out += int(row.get("output_tokens", 0))

    def price(self, tin, tout):
        long = self.long_threshold is not None and tin > self.long_threshold
        rin, rout = (self.long_in_rate, self.long_out_rate) if long else (self.in_rate, self.out_rate)
        return tin * rin / 1e6 + tout * rout / 1e6

    def reserve(self, raw_len, max_tokens):
        """Reserve the worst-case cost; return the amount, or None if it would breach the cap."""
        worst = self.price(int(raw_len / CHARS_PER_TOKEN) + 1, max_tokens)
        with self.lock:
            if self.spent + self.reserved + worst > self.cap:
                self.refused += 1
                return None
            self.reserved += worst
            return worst

    def settle(self, reservation, model, status, usage):
        tin = int(usage.get("prompt_tokens") or usage.get("input_tokens") or 0)
        tout = int(usage.get("completion_tokens") or usage.get("output_tokens") or 0)
        cost = self.price(tin, tout)
        with self.lock:
            self.reserved -= reservation
            self.spent += cost
            self.requests += 1
            self.tokens_in += tin
            self.tokens_out += tout
            if status >= 400:
                self.upstream_errors += 1
            row = {"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "model": model,
                   "status": status, "input_tokens": tin, "output_tokens": tout,
                   "cost_usd": round(cost, 6), "total_usd": round(self.spent, 6)}
            with open(self.ledger, "a") as f:
                f.write(json.dumps(row) + "\n")
        return cost

    def snapshot(self):
        with self.lock:
            return {"spent_usd": round(self.spent, 6), "reserved_usd": round(self.reserved, 6),
                    "cap_usd": self.cap, "requests": self.requests, "refused": self.refused,
                    "upstream_errors": self.upstream_errors,
                    "input_tokens": self.tokens_in, "output_tokens": self.tokens_out}


def make_handler(budget, upstream, allowed_models, ssl_ctx, injected_key, no_retry, timeout):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):  # keep stdout free of request details
            pass

        def _reply(self, code, payload):
            body = json.dumps(payload).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _refuse(self, message, code="budget_guard"):
            # 400 + invalid_request_error: OpenAI-SDK clients treat this as
            # final and do not retry.
            self._reply(400, {"error": {"type": "invalid_request_error",
                                        "code": code, "message": message}})

        def do_GET(self):
            if self.path.rstrip("/") == "/__budget":
                return self._reply(200, budget.snapshot())
            self._refuse("budget proxy only forwards POST requests")

        def do_POST(self):
            raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
            try:
                body = json.loads(raw or b"{}")
            except ValueError:
                return self._refuse("request body is not JSON")
            model = str(body.get("model", ""))
            if allowed_models and model not in allowed_models:
                return self._refuse(f"model '{model}' is not allowed by the budget proxy")
            if body.get("stream"):
                return self._refuse("streaming requests are not metered; refused")
            max_tokens = int(body.get("max_tokens") or body.get("max_completion_tokens") or DEFAULT_MAX_TOKENS)
            reservation = budget.reserve(len(raw), max_tokens)
            if reservation is None:
                return self._refuse(f"budget cap of ${budget.cap:.2f} would be exceeded; request refused")

            path = self.path if self.path.startswith("/") else "/" + self.path
            if path.startswith("/v1/"):
                path = path[3:]
            req = urllib.request.Request(upstream.rstrip("/") + path, data=raw, method="POST")
            for k, v in self.headers.items():
                if k.lower() in FORWARD_HEADERS and not (injected_key and k.lower() in AUTH_HEADERS):
                    req.add_header(k, v)
            if injected_key:
                if path.endswith("/chat/completions"):
                    req.add_header("Authorization", "Bearer " + injected_key)
                else:
                    req.add_header("x-api-key", injected_key)
                    if not self.headers.get("anthropic-version"):
                        req.add_header("anthropic-version", "2023-06-01")
            try:
                resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
                status, data = resp.status, resp.read()
            except urllib.error.HTTPError as e:
                status, data = e.code, e.read()
            except Exception as e:  # network failure or timeout; no detail leakage
                budget.settle(reservation, model, 599, {})
                msg = f"upstream unreachable: {type(e).__name__}"
                return self._refuse(msg, "upstream_error_no_retry") if no_retry else \
                    self._reply(502, {"error": {"type": "api_error", "message": msg}})
            try:
                usage = json.loads(data).get("usage") or {}
            except ValueError:
                usage = {}
            budget.settle(reservation, model, status, usage)
            if no_retry and (status in RETRYABLE or status >= 500):
                return self._refuse(f"upstream returned HTTP {status}; not retried by policy",
                                    "upstream_error_no_retry")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return Handler


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--budget-usd", type=float, required=True)
    p.add_argument("--input-per-mtok", type=float, required=True)
    p.add_argument("--output-per-mtok", type=float, required=True)
    p.add_argument("--long-context-threshold", type=int, default=None,
                   help="prompt tokens above which the long-context rates apply")
    p.add_argument("--long-input-per-mtok", type=float, default=None)
    p.add_argument("--long-output-per-mtok", type=float, default=None)
    p.add_argument("--allow-model", action="append", default=[])
    p.add_argument("--inject-key-env", default=None,
                   help="environment variable holding the real API key; incoming auth is discarded")
    p.add_argument("--no-upstream-retry", action="store_true",
                   help="return upstream 408/409/429/5xx and network errors as non-retryable 400s")
    p.add_argument("--upstream-timeout", type=float, default=300.0)
    p.add_argument("--upstream", default="https://api.anthropic.com/v1")
    p.add_argument("--ledger", default="ledger.jsonl")
    p.add_argument("--port", type=int, default=8787)
    a = p.parse_args()

    key = None
    if a.inject_key_env:
        key = os.environ.get(a.inject_key_env)
        if not key:
            sys.exit(f"--inject-key-env: environment variable {a.inject_key_env} is empty")

    cafile = os.environ.get("SSL_CERT_FILE")
    ctx = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
    budget = Budget(a.budget_usd, a.input_per_mtok, a.output_per_mtok, a.ledger,
                    a.long_context_threshold, a.long_input_per_mtok, a.long_output_per_mtok)
    handler = make_handler(budget, a.upstream, set(a.allow_model), ctx, key,
                           a.no_upstream_retry, a.upstream_timeout)
    server = ThreadingHTTPServer(("127.0.0.1", a.port), handler)
    print(f"budget proxy on http://127.0.0.1:{a.port}/v1 -> {a.upstream} | cap ${a.budget_usd:.2f} "
          f"| spent so far ${budget.spent:.4f} | models {sorted(a.allow_model) or 'any'} "
          f"| key injection {'on' if key else 'off'} | upstream retry {'blocked' if a.no_upstream_retry else 'allowed'}",
          flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    sys.exit(main())
