"""Loads the Lab 3 graph (undirected, ordered successors, edge weights).

The graph is a STAND-IN for the lab's Section 3.2 / 3.7 graph (see lab3_graph.json).
"""
import json
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent


@dataclass
class Graph:
    start: str
    goal: str
    successors: dict   # node -> ordered list of neighbours (successor order matters)
    weights: dict      # frozenset({u, v}) -> edge weight (same in both directions)

    def weight(self, u, v):
        try:
            return self.weights[frozenset((u, v))]
        except KeyError:
            raise ValueError(f"no edge between {u} and {v}")


def load_graph(path=None):
    path = Path(path) if path else HERE / "lab3_graph.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    successors = {k: list(v) for k, v in data["successors"].items()}
    weights = {frozenset((a, b)): w for a, b, w in data["weights"]}
    # Validate: every successor link is two-way and has a weight.
    for u, vs in successors.items():
        for v in vs:
            if u not in successors.get(v, []):
                raise ValueError(f"edge {u}->{v} is not symmetric")
            if frozenset((u, v)) not in weights:
                raise ValueError(f"edge {u}-{v} has no weight")
    return Graph(data["start"], data["goal"], successors, weights)


def fmt(path):
    """Path as a string, e.g. ['A','B'] -> 'A-B'."""
    return "-".join(path)
