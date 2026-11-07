"""Draws the stand-in graph with edge weights to lab3_graph.png (needs matplotlib).

Optional helper for the report figure; the lab results do not depend on it.
Usage: python lab3_draw_graph.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lab3_graph import load_graph

POS = {"A": (0, 1.5), "B": (1.5, 2.6), "C": (1.5, 0.4), "D": (3.2, 3.0),
       "E": (3.2, 1.7), "F": (3.2, 0.4), "G": (4.7, 1.7)}


def main():
    g = load_graph()
    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=150)
    seen = set()
    for u, vs in g.successors.items():
        for v in vs:
            key = frozenset((u, v))
            if key in seen:
                continue
            seen.add(key)
            (x1, y1), (x2, y2) = POS[u], POS[v]
            ax.plot([x1, x2], [y1, y2], color="#555555", lw=1.5, zorder=1)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.12, str(g.weights[key]), fontsize=9,
                    color="#B00020", ha="center", zorder=3,
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    for n, (x, y) in POS.items():
        face = "#C6E0B4" if n == g.start else ("#F8CBAD" if n == g.goal else "#D9E2F3")
        ax.scatter([x], [y], s=650, color=face, edgecolor="#1F3864", zorder=2)
        ax.text(x, y, n, ha="center", va="center", fontsize=12, fontweight="bold", zorder=4)
    ax.set_title("Stand-in A-G graph (red numbers = edge weights; green = start A, orange = goal G)", fontsize=8)
    ax.axis("off")
    ax.set_xlim(-0.5, 5.2)
    ax.set_ylim(0, 3.5)
    fig.tight_layout()
    fig.savefig(Path(__file__).resolve().parent / "lab3_graph.png")


if __name__ == "__main__":
    main()
