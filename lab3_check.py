"""Runs every Lab 3 search, compares with HAND-DERIVED expected values, saves outputs.

Usage:  python lab3_check.py
Writes: lab3_output.txt, lab3_results.json (next to this file).
Exit code 0 only if every check matched.

The expected traces below were worked out by hand on the stand-in graph
(lab3_graph.json) BEFORE the code was run; this script verifies the code against them.
"""
import dataclasses
import json
import sys
from collections import deque
from pathlib import Path

from lab3_bfs_dfs import bfs, dfs
from lab3_depth_search import dls, iddfs
from lab3_graph import fmt, load_graph
from lab3_ucs import all_simple_paths, path_cost, ucs

HERE = Path(__file__).resolve().parent
lines, failures = [], []


def out(text=""):
    print(text)
    lines.append(text)


def check(label, actual, expected):
    ok = actual == expected
    if not ok:
        failures.append(label)
        out(f"  MISMATCH {label}: actual={actual!r} expected={expected!r}")
    return ok


# ---------------- hand-derived expectations ----------------
BFS_ORDER = ["A", "B", "C", "E", "D", "F", "G"]
BFS_PATH = "A-B-D-G"
BFS_AFTER = [["A-B", "A-C"], ["A-C", "A-B-E", "A-B-D"], ["A-B-E", "A-B-D", "A-C-F"],
             ["A-B-D", "A-C-F"], ["A-C-F", "A-B-D-G"], ["A-B-D-G"], []]
DFS_ORDER = ["A", "B", "E", "F", "C", "G"]
DFS_PATH = "A-B-E-F-G"
DFS_AFTER = [["A-C", "A-B"], ["A-C", "A-B-D", "A-B-E"], ["A-C", "A-B-D", "A-B-E-F"],
             ["A-C", "A-B-D", "A-B-E-F-G", "A-B-E-F-C"], ["A-C", "A-B-D", "A-B-E-F-G"],
             ["A-C", "A-B-D"]]
DLS_EXPECT = {1: ("CUTOFF", None, 3), 2: ("CUTOFF", None, 6),
              3: ("FOUND", "A-B-D-G", 6), 4: ("FOUND", "A-B-E-F-G", 6)}
IDDFS_EXPECT = {1: ("CUTOFF", None, [0, 1], 4), 2: ("CUTOFF", None, [0, 1, 2], 10),
                3: ("FOUND", "A-B-D-G", [0, 1, 2, 3], 16),
                4: ("FOUND", "A-B-D-G", [0, 1, 2, 3], 16)}
IDDFS3_VISITS = {"A": 4, "B": 3, "C": 2, "D": 2, "E": 2, "F": 2, "G": 1}
UCS_ORDER = [("A", 0), ("B", 1), ("E", 2), ("F", 3), ("G", 4)]
UCS_PATH, UCS_COST = "A-B-E-F-G", 4
UCS_AFTER = [[(1, "A-B"), (5, "A-C")], [(2, "A-B-E"), (5, "A-C"), (7, "A-B-D")],
             [(3, "A-B-E-F"), (5, "A-C"), (7, "A-B-D")], [(4, "A-B-E-F-G"), (5, "A-C"), (7, "A-B-D")],
             [(5, "A-C"), (7, "A-B-D")]]
SIMPLE_EXPECT = {"A-B-D-G": 11, "A-C-F-G": 8, "A-B-E-F-G": 4, "A-C-F-E-B-D-G": 19}


def hop_distance(g):
    """Independent shortest hop count start->goal (plain BFS distances)."""
    dist = {g.start: 0}
    q = deque([g.start])
    while q:
        u = q.popleft()
        for v in g.successors[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist.get(g.goal)


def show_rows(rows, cols):
    for r in rows:
        out("  " + " | ".join(str(r[c]) for c in cols))


def main():
    g = load_graph()
    res = {}
    out("Lab 3 check (STAND-IN A-G graph; start A, goal G; root at depth 0)")
    out("Successor order: " + "; ".join(f"{k}: {','.join(v)}" for k, v in g.successors.items()))
    out()

    # ---- Task 1
    out("TASK 1 - BFS (queue = paths, front first)")
    b = bfs(g)
    for r in b["trace"]:
        out(f"  step {r['step']}: queue {r['before']} | process {r['processed']} | add {r['added']} | queue after {r['after']}"
            + ("  <- GOAL, stop" if r["goal"] else ""))
    out(f"  Final path: {fmt(b['path'])}    Visit (processing) order: {' '.join(b['visit_order'])}")
    check("BFS order", b["visit_order"], BFS_ORDER)
    check("BFS path", fmt(b["path"]), BFS_PATH)
    check("BFS frontier states", [r["after"] for r in b["trace"]], BFS_AFTER)
    out()
    out("TASK 1 - DFS (stack shown bottom -> top; top is processed next)")
    d = dfs(g)
    for r in d["trace"]:
        out(f"  step {r['step']}: stack {r['before']} | process {r['processed']} | push {r['added']} | stack after {r['after']}"
            + ("  <- GOAL, stop" if r["goal"] else ""))
    out(f"  Final path: {fmt(d['path'])}    Visit (processing) order: {' '.join(d['visit_order'])}")
    check("DFS order", d["visit_order"], DFS_ORDER)
    check("DFS path", fmt(d["path"]), DFS_PATH)
    check("DFS stack states", [r["after"] for r in d["trace"]], DFS_AFTER)
    res["bfs"] = {**b, "path": fmt(b["path"])}
    res["dfs"] = {**d, "path": fmt(d["path"])}

    # ---- Task 2
    out()
    hd = hop_distance(g)
    out(f"TASK 2 - shortest hop distance A->G (independent BFS distances): {hd}")
    check("hop distance", hd, 3)
    res["hop_distance_goal"] = hd
    out("DLS at limits 1-4")
    res["dls"] = []
    for lim in (1, 2, 3, 4):
        r = dls(g, lim)
        p = fmt(r["path"]) if r["path"] else None
        out(f"  limit {lim}: status={r['status']:<7} path={p}  nodes visited={r['nodes']}  call order={' '.join(r['visited'])}")
        check(f"DLS limit {lim}", (r["status"], p, r["nodes"]), DLS_EXPECT[lim])
        res["dls"].append({"limit": lim, "status": r["status"], "path": p, "nodes": r["nodes"],
                           "visited": r["visited"]})
    out("IDDFS with maximum depths 1-4 (limits start at 0)")
    res["iddfs"] = []
    for md in (1, 2, 3, 4):
        r = iddfs(g, md)
        p = fmt(r["path"]) if r["path"] else None
        per = ", ".join(f"L{it['limit']}:{it['status']}({it['nodes']})" for it in r["iterations"])
        out(f"  max depth {md}: status={r['status']:<7} path={p}  limits attempted={r['limits_attempted']}  total nodes={r['total_nodes']}  [{per}]")
        check(f"IDDFS max {md}", (r["status"], p, r["limits_attempted"], r["total_nodes"]), IDDFS_EXPECT[md])
        res["iddfs"].append({"max_depth": md, "status": r["status"], "path": p,
                             "limits_attempted": r["limits_attempted"],
                             "iterations": [{"limit": it["limit"], "status": it["status"], "nodes": it["nodes"]} for it in r["iterations"]],
                             "total_nodes": r["total_nodes"], "node_visits": r["node_visits"]})
    nv = iddfs(g, 3)["node_visits"]
    out(f"  Per-node visits across IDDFS iterations (max depth 3): {nv}")
    check("IDDFS node visits", nv, IDDFS3_VISITS)
    fd = dls(g, 10, goal="H")
    out(f"  FAILURE demo: DLS limit 10, goal 'H' (not in graph): status={fd['status']}, nodes visited={fd['nodes']}")
    check("FAILURE demo", fd["status"], "FAILURE")
    res["failure_demo"] = {"limit": 10, "goal": "H", "status": fd["status"], "nodes": fd["nodes"]}

    # ---- Task 3
    out()
    out("TASK 3 - weights: " + ", ".join(f"{'-'.join(sorted(k))}={v}" for k, v in sorted(g.weights.items(), key=lambda kv: sorted(kv[0]))))
    out("  added corridors: none (weights only; topology unchanged)")
    u = ucs(g)
    out("UCS processing order (node, cost g):")
    for r in u["trace"]:
        out(f"  step {r['step']}: process {r['processed']} (g={r['cost']}) path {r['path']} | add {r['added']} | frontier after {r['after']}"
            + ("  <- GOAL, stop" if r["goal"] else ""))
    check("UCS order", u["order"], UCS_ORDER)
    check("UCS path", fmt(u["path"]), UCS_PATH)
    check("UCS returned cost", u["cost"], UCS_COST)
    check("UCS frontier states", [r["after"] for r in u["trace"]], UCS_AFTER)
    indep = path_cost(g, u["path"])
    out(f"  UCS path {fmt(u['path'])}: returned cost={u['cost']}, independent edge-weight sum={indep}")
    check("independent cost = returned cost", indep, u["cost"])
    sp = [{"path": fmt(p), "hops": len(p) - 1, "cost": path_cost(g, p)} for p in all_simple_paths(g)]
    out("  All simple A->G paths:")
    for s in sp:
        out(f"    {s['path']}: {s['hops']} hops, cost {s['cost']}")
    check("simple path costs", {s["path"]: s["cost"] for s in sp}, SIMPLE_EXPECT)
    check("UCS cost = brute-force minimum", u["cost"], min(s["cost"] for s in sp))
    bw = bfs(g)
    bcost = path_cost(g, bw["path"])
    out(f"  BFS route on the same topology: {fmt(bw['path'])}, {len(bw['path'])-1} hops, weighted cost {bcost}")
    check("BFS weighted cost", bcost, 11)
    res["ucs"] = {"status": u["status"], "path": fmt(u["path"]), "cost": u["cost"],
                  "order": u["order"], "trace": u["trace"], "independent_cost": indep}
    res["simple_paths"] = sp
    res["bfs_weighted"] = {"path": fmt(bw["path"]), "hops": len(bw["path"]) - 1, "cost": bcost}

    # negative-weight guard
    bad_weights = dict(g.weights)
    bad_weights[frozenset(("A", "B"))] = -1
    try:
        ucs(dataclasses.replace(g, weights=bad_weights))
        guard = False
    except ValueError as e:
        guard = True
        out(f"  Negative weight rejected: {e}")
    check("negative-weight guard", guard, True)
    res["negative_weight_guard"] = guard

    out()
    ok = not failures
    out("RESULT: " + ("all checks matched the hand-derived expectations" if ok else "MISMATCH in: " + ", ".join(failures)))
    res["all_match"] = ok
    res["graph"] = {"successors": g.successors,
                    "weights": [[*sorted(k), v] for k, v in sorted(g.weights.items(), key=lambda kv: sorted(kv[0]))]}
    (HERE / "lab3_output.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (HERE / "lab3_results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
