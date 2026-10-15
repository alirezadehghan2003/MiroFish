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
import sqlite3
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = os.environ.get("MIROFISH_API", "http://127.0.0.1:5001")
PROXY = os.environ.get("BUDGET_PROXY", "http://127.0.0.1:8787")
MODEL = "claude-haiku-5-5"
MAX_ROUNDS = 8
# MiroFish picks its prompt language from Accept-Language and defaults to Chinese.
LOCALE = "en"
STOP_SIM_AT_USD = 0.70      # stop the simulation if spend reaches this
SKIP_REPORT_AT_USD = 0.80   # do not start the report agent above this
MAX_ERROR_SHARE = 0.30      # stop if >30% of (>=10) forwarded requests fail upstream
AGENT_MIN, AGENT_MAX = 10, 12
SEED = os.path.join(HERE, "..", "seeds", "s1-brand-perception.md")
REQUIREMENT = os.path.join(HERE, "..", "seeds", "s1-simulation-requirement.txt")

SIM_ROOT = os.path.join(HERE, "..", "..", "..", "backend", "uploads", "simulations")
# Activity gate before the (most expensive) report stage.
GATE_MIN_PARTICIPANTS = 5          # distinct agents with posts/comments/likes of their own
GATE_MIN_MEANINGFUL = 12           # agent-authored posts+comments with >= 80 characters
INTERVIEW_PROMPT = (
    "In English and in your own voice, in 4-6 sentences: what do you now think The HVN in Knightsbridge is "
    "(spa, medical clinic, longevity clinic or aesthetics clinic)? What, if anything, makes it feel trustworthy "
    "and premium, what worries you, and what would make you book or not book? Use only what you know from the "
    "discussion and briefing; say if you are unsure.")

PAID = {"ontology", "prepare", "start", "interview", "report"}
ZEP = {"build", "cleanup"}
ORDER = ["preflight", "ontology", "build", "entities", "prepare", "postprepare", "clockshift", "start",
         "activity", "interview", "close", "report"]

# Opener that ignores HTTP(S)_PROXY: all traffic here is to local services.
LOCAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call(method, path, payload=None, base=API, timeout=120):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(base + path, data=data, method=method,
                                 headers={"Content-Type": "application/json", "Accept-Language": LOCALE})
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
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                                          "Accept-Language": LOCALE})
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
    size = os.path.getsize(a.seed)
    print(f"  seed: {os.path.basename(a.seed)} {size/1024:.1f} KB (~{size // 450} Zep chunks)")
    st["preflight"] = time.strftime("%Y-%m-%dT%H:%M:%S")


def stage_ontology(st, a):
    print("[ontology] PAID: 1 LLM call")
    before = (spend() or {}).get("requests", 0)
    r = multipart("/api/graph/ontology/generate",
                  {"simulation_requirement": open(a.requirement).read().strip(),
                   "project_name": a.project_name},
                  [("files", a.seed)])
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


def unsafe(b):
    """Return a reason to stop, or None. b is the proxy snapshot (None = proxy down)."""
    if not b:
        return "budget proxy unreachable"
    if b["spent_usd"] >= STOP_SIM_AT_USD:
        return f"spend ${b['spent_usd']} reached the ${STOP_SIM_AT_USD} stop threshold"
    if b["requests"] >= 10 and b["upstream_errors"] / b["requests"] > MAX_ERROR_SHARE:
        return f"{b['upstream_errors']}/{b['requests']} upstream requests failed"
    return None


def sim_dir(st):
    return os.path.join(SIM_ROOT, st["simulation_id"])


def activity(st):
    """Independent agent activity from the OASIS database (read-only)."""
    db = os.path.join(sim_dir(st), "reddit_simulation.db")
    if not os.path.exists(db):
        return {}
    cfg = json.load(open(os.path.join(sim_dir(st), "simulation_config.json")))
    n_seed = len((cfg.get("event_config") or {}).get("initial_posts") or [])
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    posts = c.execute("select post_id, user_id, content from post order by post_id").fetchall()
    agent_posts = posts[n_seed:]
    comments = c.execute("select c.user_id, c.content, p.user_id from comment c "
                         "left join post p on p.post_id = c.post_id").fetchall()
    acts = c.execute("select user_id, action from trace where action not in "
                     "('sign_up','refresh','do_nothing','interview')").fetchall()
    c.close()
    seed_ids = {pid for pid, _, _ in posts[:n_seed]}
    participants = {u for u, a_ in acts} - set()
    meaningful = [x for x in agent_posts if len(x[2] or "") >= 80] + [x for x in comments if len(x[1] or "") >= 80]
    return {"seed_posts": n_seed, "agent_posts": len(agent_posts), "comments": len(comments),
            "replies_to_others": sum(1 for u, _, pu in comments if pu is not None and pu != u),
            "likes_dislikes": sum(1 for _, a_ in acts if "like" in a_),
            "participants": len({u for u, a_ in acts if a_ != "create_post"} | {u for _, u, _ in agent_posts}),
            "meaningful": len(meaningful), "actions": len(acts), "seed_post_ids": sorted(seed_ids)}


def loop_done(st):
    log = os.path.join(sim_dir(st), "simulation.log")
    return os.path.exists(log) and "模拟循环完成" in open(log, errors="ignore").read()


COUNTRY_EN = {"英国": "United Kingdom", "阿联酋": "United Arab Emirates", "美国": "United States",
              "法国": "France", "印度": "India", "沙特阿拉伯": "Saudi Arabia", "中国": "China"}


def stage_postprepare(st, a):
    """Free checks after prepare: force English data, list opening posts for an author check."""
    import re
    cjk = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")
    d = sim_dir(st)
    pp, cp = os.path.join(d, "reddit_profiles.json"), os.path.join(d, "simulation_config.json")
    for f in (pp, cp):
        if not os.path.exists(f + ".as-generated.json"):
            open(f + ".as-generated.json", "w").write(open(f).read())
    prof, cfg = json.load(open(pp)), json.load(open(cp))
    log = []
    for x in prof:
        if x.get("country") in COUNTRY_EN:
            log.append(f"{x.get('name')}: country {x['country']} -> {COUNTRY_EN[x['country']]}")
            x["country"] = COUNTRY_EN[x["country"]]
    json.dump(prof, open(pp, "w"), ensure_ascii=False, indent=2)
    with open(os.path.join(d, "data_fixes_log.txt"), "a") as f:
        f.writelines(l + "\n" for l in log)
    left = [(x.get("name"), k) for x in prof for k, v in x.items() if cjk.search(json.dumps(v, ensure_ascii=False))]
    left += [("config", "simulation_config")] if cjk.search(json.dumps(cfg, ensure_ascii=False)) else []
    print(f"[postprepare] {len(log)} country fixes; remaining non-English fields: {left or 'none'}")
    names = {ag["agent_id"]: ag["entity_name"] for ag in cfg["agent_configs"]}
    for i, ip in enumerate(cfg["event_config"].get("initial_posts", [])):
        print(f"  opening post {i}: author {names.get(ip.get('poster_agent_id'))} | {ip.get('content', '')[:150]}")
    st["agent_names"] = list(names.values())
    if left:
        sys.exit("  STOP: non-English text remains; fix it (and log it) before starting")


def stage_clockshift(st, a):
    """Free data edit: make hour index 0 behave as --start-hour by shifting every hour-based setting."""
    if not a.start_hour:
        print("[clockshift] start hour 0: nothing to do")
        return
    path = os.path.join(sim_dir(st), "simulation_config.json")
    cfg = json.load(open(path))
    json.dump(cfg, open(path + ".before-clockshift.json", "w"), ensure_ascii=False, indent=2)
    shift = lambda hs: sorted({(h - a.start_hour) % 24 for h in hs})
    tc = cfg["time_config"]
    for k in ("peak_hours", "off_peak_hours", "morning_hours", "work_hours"):
        if isinstance(tc.get(k), list):
            tc[k] = shift(tc[k])
    for ag in cfg.get("agent_configs", []):
        if isinstance(ag.get("active_hours"), list):
            ag["active_hours"] = shift(ag["active_hours"])
    tc["clock_shift_note"] = f"hour index 0 == {a.start_hour:02d}:00 (hour lists shifted by -{a.start_hour})"
    json.dump(cfg, open(path, "w"), ensure_ascii=False, indent=2)
    st["clock_shift_hours"] = a.start_hour
    print(f"[clockshift] round 1 now behaves as {a.start_hour:02d}:00; backup saved next to config")


def stage_start(st, a):
    print(f"[start] PAID: Reddit, max_rounds={a.max_rounds}, graph memory updates OFF")
    call("POST", "/api/simulation/start", {"simulation_id": st["simulation_id"], "platform": "reddit",
                                           "max_rounds": a.max_rounds, "enable_graph_memory_update": False})
    while True:
        b = spend()
        act = activity(st)
        print(f"  {time.strftime('%H:%M:%S')} spent ${(b or {}).get('spent_usd', '?')} | errors "
              f"{(b or {}).get('upstream_errors', '?')} | agent posts {act.get('agent_posts')} comments "
              f"{act.get('comments')} likes {act.get('likes_dislikes')} participants {act.get('participants')}",
              flush=True)
        reason = unsafe(b)
        if reason:
            call("POST", "/api/simulation/stop", {"simulation_id": st["simulation_id"]})
            st["run_status"] = "stopped_by_guard: " + reason
            save(a.state, st)
            sys.exit(f"  GUARD STOP: {reason}; simulation stopped")
        if loop_done(st):
            st["run_status"] = "loop_complete"
            st["rounds_completed"] = a.max_rounds
            break
        time.sleep(15)


def stage_activity(st, a):
    act = activity(st)
    act["gate_passed"] = act.get("participants", 0) >= GATE_MIN_PARTICIPANTS and \
        act.get("meaningful", 0) >= GATE_MIN_MEANINGFUL
    st["activity"] = act
    print("[activity]", json.dumps(act))
    print(f"  gate (>= {GATE_MIN_PARTICIPANTS} participants and >= {GATE_MIN_MEANINGFUL} meaningful items): "
          f"{'PASSED' if act['gate_passed'] else 'FAILED - report will be skipped'}")


def stage_interview(st, a):
    print("[interview] PAID: one English question to every agent (environment must be alive)")
    r = call("POST", "/api/simulation/interview/all", {"simulation_id": st["simulation_id"],
                                                       "prompt": a.interview_prompt or INTERVIEW_PROMPT, "platform": "reddit",
                                                       "timeout": 300}, timeout=400)
    out = os.path.join(sim_dir(st), "interviews.json")
    json.dump(r, open(out, "w"), ensure_ascii=False, indent=2)
    res = ((r.get("data") or {}).get("result") or {}).get("results") or {}
    st["interviews"] = len(res)
    print(f"  {len(res)} interview answers saved to {out}")


def stage_close(st, a):
    print("[close] closing the OASIS environment (no LLM calls)")
    call("POST", "/api/simulation/close-env", {"simulation_id": st["simulation_id"]})
    for _ in range(36):
        d = call("GET", f"/api/simulation/{st['simulation_id']}/run-status")["data"]
        if d.get("runner_status") in ("completed", "stopped", "failed"):
            print("  runner status:", d.get("runner_status"))
            return
        time.sleep(5)
    sys.exit("  environment did not reach a terminal status")


def stage_report(st, a):
    print("[report] PAID: MiroFish report agent")
    if not (st.get("activity") or {}).get("gate_passed"):
        sys.exit("  GATE STOP: too little discussion; report skipped (run --stage activity first)")
    b = spend()
    if not b or b["spent_usd"] >= SKIP_REPORT_AT_USD:
        sys.exit(f"  GUARD STOP: report skipped (proxy {'down' if not b else 'spend $%s' % b['spent_usd']})")
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
    p.add_argument("--max-rounds", type=int, default=MAX_ROUNDS)
    p.add_argument("--start-hour", type=int, default=0, help="simulated clock hour for round 1 (clockshift)")
    p.add_argument("--project-name", default="HVN S1 Brand Perception Pilot")
    p.add_argument("--seed", default=SEED)
    p.add_argument("--interview-prompt", default=None, help="scenario-specific interview question (English)")
    p.add_argument("--requirement", default=REQUIREMENT)
    a = p.parse_args()
    stages = ORDER if a.stage == "all" else [a.stage]
    st = load(a.state)
    for s in stages:
        if s in PAID and not a.confirm_paid:
            sys.exit(f"stop: stage '{s}' makes paid LLM calls - re-run with --confirm-paid")
        if s in ZEP and not a.confirm_zep:
            sys.exit(f"stop: stage '{s}' sends data to Zep Cloud - re-run with --confirm-zep")
        if s in PAID and s != "ontology" and not spend():
            sys.exit("GUARD STOP: budget proxy unreachable")
        globals()["stage_" + s](st, a)
        st.setdefault("log", []).append({"stage": s, "t": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                         "spent_usd": (spend() or {}).get("spent_usd")})
        save(a.state, st)
    b = spend() or {}
    print(f"done. total spent ${b.get('spent_usd', '?')} over {b.get('requests', '?')} requests")


if __name__ == "__main__":
    main()
