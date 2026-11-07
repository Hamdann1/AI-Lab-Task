"""Transparent rule-based scholarship eligibility check (synthetic lab example).

All thresholds are SYNTHETIC LAB ASSUMPTIONS, not real scholarship policy.
Every rule is a named, readable condition; no learning or training is involved.
"""

# --- Synthetic lab thresholds (assumptions) ---
MIN_SCORE = 70            # original rule: score >= 70
MIN_ATTENDANCE_PCT = 80   # NEW condition 1: Attendance Condition
MIN_SERVICE_HOURS = 20    # NEW condition 2: Community Service Condition


def evaluate(applicant):
    """Return (eligible, list_of_failed_condition_names)."""
    checks = [
        ("Score Condition (score >= 70)", applicant["score"] >= MIN_SCORE),
        ("Document Completeness Condition (all documents submitted)", applicant["docs_complete"]),
        ("Attendance Condition (attendance >= 80%)", applicant["attendance_pct"] >= MIN_ATTENDANCE_PCT),
        ("Community Service Condition (service hours >= 20)", applicant["service_hours"] >= MIN_SERVICE_HOURS),
    ]
    failed = [name for name, ok in checks if not ok]
    return (len(failed) == 0, failed)


# Expected results are decided BEFORE running, by reading the rules by hand.
TEST_CASES = [
    {
        "id": "T1 - Clear pass",
        "input": {"score": 82, "docs_complete": True, "attendance_pct": 90, "service_hours": 30},
        "expected": "ELIGIBLE",
    },
    {
        "id": "T2 - Fails Attendance Condition only",
        "input": {"score": 85, "docs_complete": True, "attendance_pct": 70, "service_hours": 25},
        "expected": "NOT ELIGIBLE",
    },
    {
        "id": "T3 - Fails Community Service Condition only",
        "input": {"score": 88, "docs_complete": True, "attendance_pct": 92, "service_hours": 10},
        "expected": "NOT ELIGIBLE",
    },
    {
        "id": "T4 - Threshold boundary (score exactly 70)",
        "input": {"score": 70, "docs_complete": True, "attendance_pct": 85, "service_hours": 30},
        "expected": "ELIGIBLE",
    },
]


def main():
    print("NOTE: all thresholds are synthetic lab assumptions.\n")
    all_match = True
    for case in TEST_CASES:
        eligible, failed = evaluate(case["input"])
        actual = "ELIGIBLE" if eligible else "NOT ELIGIBLE"
        reason = ("All four conditions satisfied." if eligible
                  else "Failed: " + "; ".join(failed))
        match = actual == case["expected"]
        all_match &= match
        print(case["id"])
        print("  Input:    ", case["input"])
        print("  Expected: ", case["expected"])
        print("  Actual:   ", actual)
        print("  Reason:   ", reason)
        print("  Match:    ", "PASS" if match else "MISMATCH")
        print()
    print("Overall:", "all 4 cases match expectations" if all_match else "MISMATCH FOUND")


if __name__ == "__main__":
    main()
