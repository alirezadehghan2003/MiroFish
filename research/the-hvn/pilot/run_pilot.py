#!/usr/bin/env python3
"""
Staged driver for the S1 Brand Perception pilot (Reddit only, Claude Haiku only).

Every stage that costs money or sends data off this machine needs its own
explicit flag, and the driver stops at each gate so a human can look first.

Stages (run in order; each reads/writes pilot state in --state):
  preflight  free     checks backend health, model, budget proxy, seed size
  ontology   PAID     1 LLM call (~$0.002): seed -> entity types
  build      ZEP      uploads the seed text to Zep Cloud and builds the graph
  entities   free*    reads the graph's entities from Zep (read-only) and
                      proposes the persona entity types for 10-12 agents
  prepare    PAID     creates the Reddit-only simulation and generates the
                      agent profiles + config (1 call per agent + ~4)
  start      PAID     runs the simulation: max 8 rounds, graph memory OFF
  report     PAID     generates the MiroFish report (~15-45 calls)
  cleanup    ZEP      deletes the pilot graph from Zep Cloud

Flags: --confirm-paid is required for PAID stages, --confirm-zep for ZEP
stages. --stage all runs preflight..report and stops at the first gate
whose flag is missing. Agent count outside 10-12 aborts before `prepare`.

The backend must be started with LLM_BASE_URL pointing at the budget proxy;
preflight refuses to continue otherwise. API keys are never read or printed
by this script.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = os.environ.get("MIROFISH_API", "http://127.0.0.1:5001")
PROXY = os.environ.get("BUDGET_PROXY", "http://127.0.0.1:8787")
MODEL = "claude-haiku-5-5"
MAX_ROUNDS = 8
AGENT_MIN, AGENT_MAX = 10, 12
SEED = os.path.join(HERE, "..", "seeds", "s1-brand-perception.md")
REQUIREMENT = os.path.join(HERE, "..", "seeds", "s1-simulation-requirement.txt")

PAID = {"ontology", "prepare", "start", "report"}
ZEP = {"build", "cleanup"}
ORDER = ["preflight", "ontology", "build", "entities", "prepare", "start", "report"]

# Opener that ignores HTTP(S)_PROXY: all traffic here is to local services.
LOCAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call(method, path, payload=None, base=API, timeout=120):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(base + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with LOCAL.open(req, timeout=timeout) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")[:500]
        sys.exit(f"HTTP {e.code} from {path}: {body}")


def multipart(path, fields, files):
    boundary = "----hvnpilot%d" % int(time.time())
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, fp in files:
        with open(fp, "rb") as f:
            content = f.read()
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; '
                     f'filename="{os.path.basename(fp)}"\r\nContent-Type: text/markdown\r\n\r\n'.encode()
                     + content + b"\r\n")
    body = b"".join(parts) + f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(API + path, data=body, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with LOCAL.open(req, timeout=600) as r:
        return json.loads(r.read())


def load(state):
    return json.load(open(state)) if os.path.exists(state) else {}


def save(state, st):
    json.dump(st, open(state, "w"), indent=2)


def spend():
    try:
        return call("GET", "/__budget", base=PROXY, timeout=5)
    except SystemExit:
        return None


def wait_task(path, payload, label, done=("completed", "ready"), every=10):
    while True:
        r = call("POST" if payload else "GET", path, payload)
        d = r.get("data", r)
        status = d.get("status")
        b = spend() or {}
        print(f"  {label}: {status} {d.get('progress', '')}% | spent ${b.get('spent_usd', '?')}", flush=True)
        if status in done:
            return d
        if status == "failed":
            sys.exit(f"{label} failed: {d.get('error') or d.get('message')}")
        time.sleep(every)


def stage_preflight(st, a):
    print("[preflight] free checks")
    h = call("GET", "/health")
    print("  backend:", h)
    b = spend()
    if not b:
        sys.exit("  budget proxy not reachable at %s - start it first (see README)" % PROXY)
    print(f"  budget proxy: spent ${b['spent_usd']} of ${b['cap_usd']} cap")
    # backend/app/config.py loads <repo>/.env with override=True, which would
    # silently replace the proxy URL or model. Check variable names only.
    dotenv = os.path.join(HERE, "..", "..", "..", ".env")
    if os.path.exists(dotenv):
        names = {l.split("=", 1)[0].strip() for l in open(dotenv) if "=" in l and not l.lstrip().startswith("#")}
        clash = names & {"LLM_BASE_URL", "LLM_MODEL_NAME"}
        if clash:
            sys.exit(f"  ABORT: {sorted(clash)} set in .env would override the budget proxy; remove them first")
    print("  routing: verified after the first paid call (ontology); the run aborts if the "
          "backend is not sending LLM traffic through the proxy")
    size = os.path.getsize(SEED)
    print(f"  seed: {os.path.basename(SEED)} {size/1024:.1f} KB (~{size // 450} Zep chunks)")
    st["preflight"] = time.strftime("%Y-%m-%dT%H:%M:%S")


def stage_ontology(st, a):
    print("[ontology] PAID: 1 LLM call")
    before = (spend() or {}).get("requests", 0)
    r = multipart("/api/graph/ontology/generate",
                  {"simulation_requirement": open(REQUIREMENT).read().strip(),
                   "project_name": "HVN S1 Brand Perception Pilot"},
                  [("files", SEED)])
    d = r["data"]
    st["project_id"] = d["project_id"]
    st["entity_types"] = [e.get("name") for e in d["ontology"].get("entity_types", [])]
    print("  project:", st["project_id"])
    print("  entity types:", ", ".join(st["entity_types"]))
    after = (spend() or {}).get("requests", 0)
    if after <= before:
        sys.exit("  ABORT: the ontology call did not pass through the budget proxy, so spend is "
                 "NOT capped. Restart the backend with start_backend_via_proxy.sh before continuing.")
    print(f"  routing verified: proxy saw {after - before} request(s)")


def stage_build(st, a):
    print("[build] ZEP: uploading seed chunks and building the graph")
    r = call("POST", "/api/graph/build", {"project_id": st["project_id"],
                                          "graph_name": "hvn-s1-pilot"})
    wait_task(f"/api/graph/task/{r['data']['task_id']}", None, "graph build")
    proj = call("GET", f"/api/graph/project/{st['project_id']}")["data"]
    st["graph_id"] = proj["graph_id"]
    print("  graph:", st["graph_id"])


def stage_entities(st, a):
    print("[entities] reading graph entities (Zep read-only)")
    d = call("GET", f"/api/simulation/entities/{st['graph_id']}")["data"]
    by_type = {}
    for e in d["entities"]:
        t = next((l for l in e["labels"] if l not in ("Entity", "Node")), "?")
        by_type.setdefault(t, []).append(e["name"])
    for t, names in sorted(by_type.items()):
        print(f"  {t:28s} {len(names):3d}  e.g. {', '.join(names[:4])}")
    chosen = a.entity_types.split(",") if a.entity_types else [
        t for t in by_type if t not in ("Organization", "Competitor", "Company", "Brand", "Regulator",
                                        "Treatment", "Service", "Location", "Product", "Programme")]
    n = sum(len(by_type.get(t, [])) for t in chosen)
    st["chosen_types"], st["agent_count"] = chosen, n
    print(f"  -> agent types {chosen}: {n} agents")
    if not AGENT_MIN <= n <= AGENT_MAX:
        sys.exit(f"  agent count {n} is outside {AGENT_MIN}-{AGENT_MAX}. Re-run with "
                 f"--entity-types Type1,Type2 to pick a set that totals {AGENT_MIN}-{AGENT_MAX}.")


def stage_prepare(st, a):
    print(f"[prepare] PAID: Reddit-only simulation, {st['agent_count']} agent profiles")
    r = call("POST", "/api/simulation/create", {"project_id": st["project_id"], "graph_id": st["graph_id"],
                                                "enable_twitter": False, "enable_reddit": True})
    st["simulation_id"] = r["data"]["simulation_id"]
    r = call("POST", "/api/simulation/prepare", {"simulation_id": st["simulation_id"],
                                                 "entity_types": st["chosen_types"],
                                                 "use_llm_for_profiles": True,
                                                 "parallel_profile_count": 3})
    if r["data"].get("status") != "ready":
        wait_task("/api/simulation/prepare/status", {"simulation_id": st["simulation_id"],
                                                     "task_id": r["data"].get("task_id")}, "prepare")
    print("  simulation:", st["simulation_id"])


def stage_start(st, a):
    print(f"[start] PAID: Reddit, max_rounds={MAX_ROUNDS}, graph memory updates OFF")
    call("POST", "/api/simulation/start", {"simulation_id": st["simulation_id"], "platform": "reddit",
                                           "max_rounds": MAX_ROUNDS, "enable_graph_memory_update": False})
    while True:
        d = call("GET", f"/api/simulation/{st['simulation_id']}/run-status")["data"]
        b = spend() or {}
        print(f"  round {d.get('reddit_current_round', d.get('current_round'))}/{d.get('total_rounds')} "
              f"{d.get('runner_status')} | spent ${b.get('spent_usd', '?')}", flush=True)
        if d.get("runner_status") in ("completed", "stopped", "failed"):
            st["run_status"] = d.get("runner_status")
            break
        time.sleep(15)


def stage_report(st, a):
    print("[report] PAID: MiroFish report agent")
    r = call("POST", "/api/report/generate", {"simulation_id": st["simulation_id"]})
    d = wait_task("/api/report/generate/status", {"task_id": r["data"].get("task_id"),
                                                  "simulation_id": st["simulation_id"]}, "report", every=15)
    st["report_id"] = d.get("report_id") or (d.get("result") or {}).get("report_id")
    print("  report:", st.get("report_id"))


def stage_cleanup(st, a):
    print("[cleanup] ZEP: deleting pilot graph", st.get("graph_id"))
    call("DELETE", f"/api/graph/delete/{st['graph_id']}")
    st["graph_deleted"] = True


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--stage", required=True, choices=ORDER + ["cleanup", "all"])
    p.add_argument("--confirm-paid", action="store_true", help="allow stages that make paid LLM calls")
    p.add_argument("--confirm-zep", action="store_true", help="allow stages that send/delete data in Zep")
    p.add_argument("--entity-types", help="comma-separated entity types to turn into agents")
    p.add_argument("--state", default=os.path.join(HERE, "pilot_state.json"))
    a = p.parse_args()
    stages = ORDER if a.stage == "all" else [a.stage]
    st = load(a.state)
    for s in stages:
        if s in PAID and not a.confirm_paid:
            sys.exit(f"stop: stage '{s}' makes paid LLM calls - re-run with --confirm-paid")
        if s in ZEP and not a.confirm_zep:
            sys.exit(f"stop: stage '{s}' sends data to Zep Cloud - re-run with --confirm-zep")
        globals()["stage_" + s](st, a)
        st.setdefault("log", []).append({"stage": s, "t": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                         "spent_usd": (spend() or {}).get("spent_usd")})
        save(a.state, st)
    b = spend() or {}
    print(f"done. total spent ${b.get('spent_usd', '?')} over {b.get('requests', '?')} requests")


if __name__ == "__main__":
    main()
