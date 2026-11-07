"""Runs the Lab 2 scenarios, prints the trace, checks expectations, saves outputs.

Usage:  python lab2_check.py
Writes: lab2_output.txt, lab2_trace.csv, lab2_results.json (next to this file).
Exit code is 0 only if every expected value matched.
"""
import csv
import json
import sys
from pathlib import Path

from lab2_model import StatefulAgent, reflex_agent
from lab2_percepts import Percept, load_inputs, to_percept

HERE = Path(__file__).resolve().parent
lines = []


def out(text=""):
    print(text)
    lines.append(text)


def run_core(data):
    agent = StatefulAgent()
    rows = []
    all_match = True
    out("CORE SEQUENCE (one continuous run, previous mode starts as None)")
    header = f"{'#':>2} {'category':<20} {'previous':<9} {'percept':<20} {'target':<7} {'outcome':<11} {'check'}"
    out(header)
    out("-" * len(header))
    for i, step in enumerate(data["core_sequence"], start=1):
        percept = to_percept(step)
        previous = agent.previous_mode
        target, send = agent.step(percept)
        reflex_t, reflex_send = reflex_agent(percept)
        ok = (target == step["expected_target"] and send == step["expected_send"]
              and reflex_t == target)
        all_match &= ok
        outcome = "SEND" if send else "NO COMMAND"
        out(f"{i:>2} {step['category']:<20} {str(previous):<9} {str(percept):<20} {target:<7} {outcome:<11} {'match' if ok else 'MISMATCH'}")
        rows.append({
            "step": i, "category": step["category"], "previous_mode": str(previous),
            "temperature_c": percept.temperature_c, "occupied": percept.occupied,
            "target": target, "stateful_command": "SEND" if send else "NO COMMAND",
            "reflex_command": "SEND" if reflex_send else "NO COMMAND",
            "expected_target": step["expected_target"],
            "expected_command": "SEND" if step["expected_send"] else "NO COMMAND",
            "match": ok,
        })
    return rows, all_match


def run_edge_chatter(data):
    out("")
    out("EDGE CASE: temperature oscillating around the 26.0 threshold (fresh agent)")
    agent = StatefulAgent()
    sent = 0
    rows = []
    for i, step in enumerate(data["edge_chatter"], start=1):
        percept = to_percept(step)
        previous = agent.previous_mode
        target, send = agent.step(percept)
        sent += int(send)
        out(f"{i:>2} previous={str(previous):<5} percept={str(percept):<18} target={target:<5} {'SEND' if send else 'NO COMMAND'}")
        rows.append({"step": i, "previous_mode": str(previous), "temperature_c": percept.temperature_c,
                     "target": target, "command": "SEND" if send else "NO COMMAND"})
    out(f"commands sent: {sent} of {len(rows)} percepts (memory did not reduce them)")
    return rows, sent


def check_invalid_input():
    out("")
    out("INVALID INPUT CHECK")
    try:
        Percept(float("nan"), True)
    except ValueError as e:
        out(f"NaN temperature rejected: {e}")
        return True
    out("NaN temperature was NOT rejected")
    return False


def main():
    data = load_inputs(HERE / "lab2_inputs.json")
    out("Lab 2 check - thresholds: COOL if > 26.0, HEAT if < 18.0, empty room -> OFF (synthetic assumptions)")
    out()
    rows, core_ok = run_core(data)
    n = len(rows)
    stateful_sent = sum(r["stateful_command"] == "SEND" for r in rows)
    out("")
    out(f"Reflex agent commands:   {n} of {n} percepts")
    out(f"Stateful agent commands: {stateful_sent} of {n} percepts")
    out(f"Redundant commands avoided: {n - stateful_sent}")
    chatter_rows, chatter_sent = run_edge_chatter(data)
    invalid_ok = check_invalid_input()
    overall = core_ok and invalid_ok
    out("")
    out("RESULT: " + ("all expectations matched" if overall else "MISMATCH FOUND"))

    (HERE / "lab2_output.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with open(HERE / "lab2_trace.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    results = {
        "core_rows": rows, "n": n, "reflex_commands": n, "stateful_commands": stateful_sent,
        "edge_chatter_rows": chatter_rows, "edge_chatter_commands": chatter_sent,
        "all_match": overall,
    }
    (HERE / "lab2_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
