#!/usr/bin/env python3
"""
Delete named non-participant nodes (real people's roles, placeholders, fragments)
from ONE scenario's own Zep graph before agent profiles are generated.

Usage: prune_nodes.py <state-file> "<exact entity name>" ["<name>" ...]
Refuses to touch graphs listed in PROTECTED (earlier runs) and requires every
name to match exactly one entity in the state's graph. Logs to the state file.
"""
import json
import os
import sys
import urllib.request

PROTECTED = {"mirofish_e60ebfc8501b4e0c", "mirofish_912dfac77fc440b5"}  # S1 pilot, S1 run 2
state_path, names = sys.argv[1], sys.argv[2:]
st = json.load(open(state_path))
g = st["graph_id"]
if g in PROTECTED:
    sys.exit(f"refusing: {g} belongs to an earlier run")
op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
ents = json.load(op.open(f"http://127.0.0.1:5001/api/simulation/entities/{g}"))["data"]["entities"]
targets = []
for n in names:
    hits = [e for e in ents if e["name"] == n]
    if len(hits) != 1:
        sys.exit(f"refusing: '{n}' matches {len(hits)} entities")
    targets += hits
from zep_cloud.client import Zep  # imported late: needs the backend venv
z = Zep(api_key=os.environ["ZEP_API_KEY"])
for e in targets:
    z.graph.node.delete(uuid_=e["uuid"])
    print("deleted node:", e["name"])
st.setdefault("pruned_nodes", []).extend(e["name"] for e in targets)
json.dump(st, open(state_path, "w"), indent=2)
