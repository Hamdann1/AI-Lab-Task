"""Depth-limited search (DLS) and iterative-deepening DFS (IDDFS) (Task 2).

The root is at depth 0. Cycles are prevented with a PATH-LOCAL check: a successor
is skipped only if it is already on the current path (not if it was seen on some
other branch). Successor order follows the graph file.

Statuses:
  FOUND   - the goal was reached within the limit.
  CUTOFF  - the goal was not found, and the depth limit was reached on at least
            one branch (a deeper search might still succeed).
  FAILURE - every branch ended without reaching the limit and no goal was found
            (a deeper limit cannot help).
Simplification: any non-goal node AT the limit is reported as CUTOFF, even if it
has no unexplored successors. This is conservative (it may say CUTOFF when
FAILURE would also be true), see the report's limitations.
"""
FOUND, CUTOFF, FAILURE = "FOUND", "CUTOFF", "FAILURE"


def dls(g, limit, goal=None):
    goal = g.goal if goal is None else goal
    visited = []  # every recursive call, in order (counts nodes visited)

    def rec(node, path, depth):
        visited.append(node)
        if node == goal:
            return FOUND, path
        if depth == limit:
            return CUTOFF, None
        cutoff = False
        for s in g.successors[node]:
            if s in path:          # path-local cycle check
                continue
            status, res = rec(s, path + [s], depth + 1)
            if status == FOUND:
                return FOUND, res
            if status == CUTOFF:
                cutoff = True
        return (CUTOFF if cutoff else FAILURE), None

    status, path = rec(g.start, [g.start], 0)
    return {"limit": limit, "status": status, "path": path,
            "visited": visited, "nodes": len(visited)}


def iddfs(g, max_depth):
    """Run DLS with limits 0, 1, ..., max_depth; stop at the first FOUND (or FAILURE)."""
    iterations = []
    total_visited = []
    final = {"status": CUTOFF, "path": None}
    for limit in range(0, max_depth + 1):
        r = dls(g, limit)
        iterations.append({"limit": limit, "status": r["status"], "nodes": r["nodes"],
                           "path": r["path"]})
        total_visited.extend(r["visited"])
        if r["status"] == FOUND:
            final = {"status": FOUND, "path": r["path"]}
            break
        if r["status"] == FAILURE:
            final = {"status": FAILURE, "path": None}
            break
    node_visits = {}
    for n in total_visited:
        node_visits[n] = node_visits.get(n, 0) + 1
    return {"max_depth": max_depth, "status": final["status"], "path": final["path"],
            "limits_attempted": [it["limit"] for it in iterations],
            "iterations": iterations, "total_nodes": len(total_visited),
            "node_visits": node_visits}
