#!/usr/bin/env python3
"""
Fail-closed safety check run before every scenario (no paid calls).

Checks, printing booleans only (no key material is ever printed):
 1. budget proxy is up, has a fresh ledger (spent 0, nothing reserved), the expected cap
 2. MiroFish backend is up
 3. backend process holds only the placeholder key; the real key is absent from its environment
 4. backend LLM_BASE_URL points at the proxy and the model is pinned to claude-haiku-5-5
 5. no other LLM keys in the backend environment; no repo .env that could override settings
 6. a direct Anthropic call with the backend's credential is rejected (401)
 7. the proxy reaches Anthropic (free count_tokens call returns 200)
 8. the proxy refuses a non-Haiku model
Exit code 0 only if every check passes.
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

PLACEHOLDER = b"placeholder-real-key-is-held-by-budget-proxy"
LOCAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
results = []


def check(name, ok):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")


def get(url):
    with LOCAL.open(url, timeout=10) as r:
        return json.loads(r.read())


def post(url, body, opener=LOCAL, headers=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with opener.open(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


try:
    b = get("http://127.0.0.1:8787/__budget")
    check("1 proxy up, fresh ledger, $1.00 cap",
          b["spent_usd"] == 0 and b["reserved_usd"] == 0 and b["cap_usd"] == 1.0)
except Exception:
    check("1 proxy up, fresh ledger, $1.00 cap", False)

try:
    check("2 backend up", get("http://127.0.0.1:5001/health").get("status") == "ok")
except Exception:
    check("2 backend up", False)

pids = subprocess.run(["pgrep", "-f", r"\.venv/bin/python run\.py"], capture_output=True, text=True).stdout.split()
env = {}
if len(pids) == 1:
    raw = open(f"/proc/{pids[0]}/environ", "rb").read().split(b"\0")
    env = {k.decode(): v for k, _, v in (e.partition(b"=") for e in raw if b"=" in e)}
real = os.environ.get("LLM_API_KEY", "").encode()
check("3 backend holds placeholder only; real key absent",
      len(pids) == 1 and env.get("LLM_API_KEY") == PLACEHOLDER and bool(real) and not any(real in v for v in env.values()))
check("4 backend base URL -> proxy; model pinned to Haiku",
      env.get("LLM_BASE_URL") == b"http://127.0.0.1:8787/v1" and env.get("LLM_MODEL_NAME") == b"claude-haiku-5-5")
check("5 no other LLM keys; no repo .env",
      not any(k in env for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "LLM_BOOST_API_KEY"))
      and not os.path.exists(os.path.join(REPO, ".env")))

internet = urllib.request.build_opener()  # honours the environment's HTTPS proxy
st, _ = post("https://api.anthropic.com/v1/chat/completions",
             {"model": "claude-haiku-5-5", "max_tokens": 1, "messages": [{"role": "user", "content": "x"}]},
             opener=internet, headers={"Authorization": "Bearer " + PLACEHOLDER.decode()})
check("6 direct call with backend credential rejected (401)", st == 401)

st, body = post("http://127.0.0.1:8787/v1/messages/count_tokens",
                {"model": "claude-haiku-5-5", "messages": [{"role": "user", "content": "check"}]})
check("7 proxy reaches Anthropic (free count_tokens)", st == 200 and "input_tokens" in body)

st, body = post("http://127.0.0.1:8787/v1/chat/completions",
                {"model": "claude-sonnet-5-5", "max_tokens": 1, "messages": []})
check("8 proxy refuses non-Haiku model", st == 400 and (body.get("error") or {}).get("code") == "budget_guard")

ok = all(results)
print("ALL SAFETY CHECKS PASSED" if ok else "SAFETY CHECK FAILED - do not run")
sys.exit(0 if ok else 1)
