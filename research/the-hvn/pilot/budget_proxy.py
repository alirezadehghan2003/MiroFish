#!/usr/bin/env python3
"""
Local spend-capping proxy for MiroFish LLM traffic (research tooling, not app code).

MiroFish and its OASIS simulation subprocess send every LLM request to
LLM_BASE_URL. Point LLM_BASE_URL at this proxy and it will:

  * forward each request unchanged to the real upstream (default
    https://api.anthropic.com/v1), passing the caller's auth header through;
  * read `usage` from every JSON response and price it with the per-token
    rates given on the command line;
  * refuse every further request (HTTP 400, which the OpenAI SDK does not
    retry) once cumulative spend reaches --budget-usd;
  * refuse any request whose `model` is not in --allow-model, so a config
    mistake cannot silently use a pricier model;
  * append one line per request to --ledger: time, model, status, tokens,
    cost, running total. No prompt text, no response text and no headers
    are ever written, so API keys never reach disk.

Overshoot is bounded by the requests already in flight when the cap is hit
(each is capped by its own max_tokens).

Streaming responses (`"stream": true`) are refused, because their usage
cannot be metered reliably here; MiroFish's Claude path does not stream.

Usage:
  python3 budget_proxy.py --budget-usd 1.00 --allow-model claude-haiku-5-5 \
      --input-per-mtok 0.10 --output-per-mtok 0.50 \
      --long-context-threshold 100000 --long-input-per-mtok 0.50 --long-output-per-mtok 2.50 \
      --ledger ledger.jsonl
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
        self.requests = 0
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

    def exhausted(self):
        with self.lock:
            return self.spent >= self.cap

    def record(self, model, status, usage):
        tin = int(usage.get("prompt_tokens") or usage.get("input_tokens") or 0)
        tout = int(usage.get("completion_tokens") or usage.get("output_tokens") or 0)
        long = self.long_threshold is not None and tin > self.long_threshold
        rin, rout = (self.long_in_rate, self.long_out_rate) if long else (self.in_rate, self.out_rate)
        cost = tin * rin / 1e6 + tout * rout / 1e6
        with self.lock:
            self.spent += cost
            self.requests += 1
            self.tokens_in += tin
            self.tokens_out += tout
            row = {"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "model": model,
                   "status": status, "input_tokens": tin, "output_tokens": tout,
                   "cost_usd": round(cost, 6), "total_usd": round(self.spent, 6)}
            with open(self.ledger, "a") as f:
                f.write(json.dumps(row) + "\n")
        return cost


def make_handler(budget, upstream, allowed_models, ssl_ctx):
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

        def _refuse(self, message):
            # 400 + invalid_request_error: the OpenAI SDK treats this as final
            # and does not retry, so a hit cap stops traffic immediately.
            self._reply(400, {"error": {"type": "invalid_request_error",
                                        "code": "budget_guard",
                                        "message": message}})

        def do_GET(self):
            if self.path.rstrip("/") == "/__budget":
                with budget.lock:
                    self._reply(200, {"spent_usd": round(budget.spent, 6),
                                      "cap_usd": budget.cap,
                                      "requests": budget.requests,
                                      "input_tokens": budget.tokens_in,
                                      "output_tokens": budget.tokens_out})
                return
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
            if budget.exhausted():
                return self._refuse(f"budget cap of ${budget.cap:.2f} reached; request refused")

            path = self.path if self.path.startswith("/") else "/" + self.path
            if path.startswith("/v1/"):
                path = path[3:]
            req = urllib.request.Request(upstream.rstrip("/") + path, data=raw, method="POST")
            for k, v in self.headers.items():
                if k.lower() in FORWARD_HEADERS:
                    req.add_header(k, v)
            try:
                resp = urllib.request.urlopen(req, timeout=600, context=ssl_ctx)
                status, data = resp.status, resp.read()
            except urllib.error.HTTPError as e:
                status, data = e.code, e.read()
            except Exception as e:  # network failure: report without detail leakage
                return self._reply(502, {"error": {"type": "api_error",
                                                   "message": f"upstream unreachable: {type(e).__name__}"}})
            try:
                usage = json.loads(data).get("usage") or {}
            except ValueError:
                usage = {}
            budget.record(model, status, usage)
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
    p.add_argument("--upstream", default="https://api.anthropic.com/v1")
    p.add_argument("--ledger", default="ledger.jsonl")
    p.add_argument("--port", type=int, default=8787)
    a = p.parse_args()

    cafile = os.environ.get("SSL_CERT_FILE")
    ctx = ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()
    budget = Budget(a.budget_usd, a.input_per_mtok, a.output_per_mtok, a.ledger,
                    a.long_context_threshold, a.long_input_per_mtok, a.long_output_per_mtok)
    server = ThreadingHTTPServer(("127.0.0.1", a.port),
                                 make_handler(budget, a.upstream, set(a.allow_model), ctx))
    print(f"budget proxy on http://127.0.0.1:{a.port}/v1 -> {a.upstream} | cap ${a.budget_usd:.2f} "
          f"| spent so far ${budget.spent:.4f} | models {sorted(a.allow_model) or 'any'}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    sys.exit(main())
