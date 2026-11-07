# Lab 2 – Percepts, PEAS and a stateful climate agent

Course: CAI601400 Artificial Intelligence Lab · Student: Rasikh Ali (42365)

## What is here

| File | Purpose |
|---|---|
| `lab2_percepts.py` | `Percept` type (temperature, occupied) with input validation; loads scenarios |
| `lab2_model.py` | Reflex agent and `StatefulAgent` (remembers previous target mode) |
| `lab2_check.py` | Runs all scenarios, asserts expected results, writes captured outputs |
| `lab2_inputs.json` | Input data: core sequence, expected values, edge-case sequence |
| `lab2_output.txt` / `lab2_trace.csv` / `lab2_results.json` | Captured outputs from a real run |
| `Lab2_Report.docx` | Report: PEAS, classifications, trace, comparison, edge case, reflection |

## Setup and run

Requires Python 3.9+ and nothing else (standard library only; no virtual environment is committed).

```bash
cd lab2
python lab2_check.py
```

The script prints the trace, rewrites the three output files, and exits with code 0 only if every expected result matched.

## Assumptions

- All thresholds are **synthetic lab assumptions**: COOL if temperature > 26.0, HEAT if < 18.0, otherwise IDLE; an empty room always gives OFF (occupancy has priority). Exactly 26.0 and 18.0 are therefore IDLE.
- The original lab code was not supplied, so the baseline reflex rule was reconstructed from the lab description.
- A sent command is assumed to be delivered; the agent does not receive acknowledgements.

## Sources and borrowed material

No third-party code is used. Concepts (PEAS, environment properties, reflex vs. model-based agents) follow Russell & Norvig, *Artificial Intelligence: A Modern Approach*; full citation is in the report. No credentials or personal data are included.
