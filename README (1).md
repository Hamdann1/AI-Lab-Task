# Lab 3 – Uninformed search: BFS, DFS, DLS, IDDFS and UCS

Course: CAI601400 Artificial Intelligence Lab · Student: Rasikh Ali (42365)

> **Important – stand-in graph.** The lab's Section 3.2 graph, its successor order, the supplied BFS/DFS code and the Section 3.7 weights were not available when this was written. `lab3_graph.json` holds a **stand-in** A–G graph designed to match the lab's hints (start A, goal G first reachable at depth 3, cycles present, a shorter-hop route that costs more). To use the real graph, edit `lab3_graph.json`; the hand-derived expected values in `lab3_check.py` and the numbers in the report then need re-deriving. Likewise `lab3_bfs_dfs.py` is a stand-in for the supplied BFS/DFS code.

## Files

| File | Purpose |
|---|---|
| `lab3_graph.json` | Input data: successor order, edge weights, start, goal, added corridors (none) |
| `lab3_graph.py` | Loads and validates the graph |
| `lab3_bfs_dfs.py` | BFS and DFS with frontier traces (Task 1) |
| `lab3_depth_search.py` | DLS (FOUND / CUTOFF / FAILURE, path-local cycle check) and IDDFS (Task 2) |
| `lab3_ucs.py` | UCS, independent path-cost sum, simple-path enumeration (Task 3) |
| `lab3_check.py` | Runs everything and checks it against hand-derived traces |
| `lab3_draw_graph.py` | Optional: draws `lab3_graph.png` (needs matplotlib) |
| `lab3_output.txt`, `lab3_results.json` | Captured outputs from a real run |
| `Lab3_Report.docx` | Report |

## Setup and run

Python 3.9+; the search code uses only the standard library (matplotlib is needed only for the optional figure). No virtual environment is committed.

```bash
cd lab3
python lab3_check.py        # prints all traces/results, writes lab3_output.txt and lab3_results.json
python lab3_draw_graph.py   # optional: regenerates lab3_graph.png
```

`lab3_check.py` exits with code 0 only if every result matches the hand-derived expectation.

## Conventions

- Root is at depth 0. Goal test happens when a node is **processed**, and the search stops there.
- BFS marks nodes discovered when queued; DFS marks nodes explored when processed and pushes successors in reverse so the first listed successor is processed first.
- DLS/IDDFS use a path-local cycle check. UCS rejects negative weights.

## Sources

No third-party code is used. Algorithms follow Russell & Norvig, *Artificial Intelligence: A Modern Approach* (4th ed.); IDDFS follows Korf (1985); UCS is Dijkstra's idea (1959). Full citations are in the report. No credentials or personal data are included.
