"""Uniform-cost search (UCS) on the weighted graph (Task 3), plus helpers.

UCS: priority queue ordered by path cost g (ties broken by insertion order).
A node is marked explored when it is PROCESSED (popped). A successor is pushed only
if the new cost is strictly lower than the best cost known for it; stale entries
are skipped when popped. The goal test happens on PROCESSING, which is what makes
UCS return a minimum-cost path. Negative weights are rejected (UCS is not valid
with them).
"""
import heapq

from lab3_graph import fmt


def ucs(g):
    start, goal = g.start, g.goal
    heap = [(0, 0, [start])]
    counter = 1
    best = {start: 0}
    explored = set()
    order, trace = [], []
    step = 0

    def snapshot():
        items = sorted(heap)
        return [(c, fmt(p)) for c, _, p in items
                if p[-1] not in explored and c == best[p[-1]]]

    while heap:
        cost, _, path = heapq.heappop(heap)
        node = path[-1]
        if node in explored:
            continue  # stale entry
        step += 1
        explored.add(node)
        order.append((node, cost))
        if node == goal:
            trace.append({"step": step, "processed": node, "cost": cost, "path": fmt(path),
                          "goal": True, "added": [], "after": snapshot()})
            return {"status": "FOUND", "path": path, "cost": cost,
                    "order": order, "trace": trace}
        added = []
        for s in g.successors[node]:
            w = g.weight(node, s)
            if w < 0:
                raise ValueError(f"negative edge weight {w} on {node}-{s}; UCS is not valid")
            if s in explored:
                continue
            new_cost = cost + w
            if new_cost < best.get(s, float("inf")):
                best[s] = new_cost
                heapq.heappush(heap, (new_cost, counter, path + [s]))
                counter += 1
                added.append(f"{s}({new_cost})")
        trace.append({"step": step, "processed": node, "cost": cost, "path": fmt(path),
                      "goal": False, "added": added, "after": snapshot()})
    return {"status": "FAILURE", "path": None, "cost": None, "order": order, "trace": trace}


def path_cost(g, path):
    """Independent cost: sums the edge weights along the path from the weight table."""
    return sum(g.weight(path[i], path[i + 1]) for i in range(len(path) - 1))


def all_simple_paths(g):
    """Every simple (no repeated node) path from start to goal, in successor order."""
    found = []

    def rec(node, path):
        if node == g.goal:
            found.append(list(path))
            return
        for s in g.successors[node]:
            if s not in path:
                path.append(s)
                rec(s, path)
                path.pop()

    rec(g.start, [g.start])
    return found
