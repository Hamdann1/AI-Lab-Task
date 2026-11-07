"""BFS and DFS with full frontier traces (Task 1).

These are stand-in implementations written for this lab (the supplied BFS/DFS
code was not available). Conventions, stated so the manual trace can follow them:

BFS: FIFO queue of paths. A node is marked "discovered" when it is ADDED to the
     queue; a discovered node is never added again. The goal test happens when a
     node is PROCESSED (taken off the queue), and the search stops there.
DFS: LIFO stack of paths (shown bottom -> top). A node is marked "explored" when
     it is PROCESSED. Successors that are already explored are not pushed, and a
     popped entry whose node is already explored is skipped. Successors are pushed
     in reverse order so the FIRST listed successor is processed first.
     The goal test happens when a node is PROCESSED, and the search stops there.
"""
from collections import deque

from lab3_graph import fmt


def bfs(g):
    start, goal = g.start, g.goal
    frontier = deque([[start]])
    discovered = {start}
    visit_order, trace = [], []
    step = 0
    while frontier:
        step += 1
        before = [fmt(p) for p in frontier]
        path = frontier.popleft()
        node = path[-1]
        visit_order.append(node)
        if node == goal:
            trace.append({"step": step, "before": before, "processed": node, "path": fmt(path),
                          "goal": True, "added": [], "after": [fmt(p) for p in frontier]})
            return {"status": "FOUND", "path": path, "visit_order": visit_order, "trace": trace}
        added = []
        for s in g.successors[node]:
            if s not in discovered:
                discovered.add(s)
                frontier.append(path + [s])
                added.append(s)
        trace.append({"step": step, "before": before, "processed": node, "path": fmt(path),
                      "goal": False, "added": added, "after": [fmt(p) for p in frontier]})
    return {"status": "FAILURE", "path": None, "visit_order": visit_order, "trace": trace}


def dfs(g):
    start, goal = g.start, g.goal
    stack = [[start]]
    explored = set()
    visit_order, trace = [], []
    step = 0
    while stack:
        step += 1
        before = [fmt(p) for p in stack]
        path = stack.pop()
        node = path[-1]
        if node in explored:
            trace.append({"step": step, "before": before, "processed": node + " (skipped)",
                          "path": fmt(path), "goal": False, "added": [],
                          "after": [fmt(p) for p in stack]})
            continue
        explored.add(node)
        visit_order.append(node)
        if node == goal:
            trace.append({"step": step, "before": before, "processed": node, "path": fmt(path),
                          "goal": True, "added": [], "after": [fmt(p) for p in stack]})
            return {"status": "FOUND", "path": path, "visit_order": visit_order, "trace": trace}
        new = [s for s in g.successors[node] if s not in explored]
        for s in reversed(new):
            stack.append(path + [s])
        trace.append({"step": step, "before": before, "processed": node, "path": fmt(path),
                      "goal": False, "added": new, "after": [fmt(p) for p in stack]})
    return {"status": "FAILURE", "path": None, "visit_order": visit_order, "trace": trace}
