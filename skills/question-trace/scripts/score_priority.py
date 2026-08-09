#!/usr/bin/env python3
"""Validate and apply QuestionTrace's deterministic 15-point priority bands."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


LIMITS = {
    "frequency": 4,
    "recency": 3,
    "jd_relevance": 3,
    "resume_trigger": 3,
    "company_role_similarity": 2,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    errors: list[str] = []
    for index, question in enumerate(ledger.get("question_clusters", []), start=1):
        question_id = question.get("question_id") or f"question[{index}]"
        scores = question.get("scores", {})
        total = 0
        for key, maximum in LIMITS.items():
            value = scores.get(key)
            if not isinstance(value, int) or not 0 <= value <= maximum:
                errors.append(f"{question_id}: {key} must be an integer from 0 to {maximum}")
                continue
            total += value
        question["total_score"] = total
        question["priority"] = "high" if total >= 12 else "medium" if total >= 8 else "low"

    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    payload = json.dumps(ledger, ensure_ascii=False, indent=2) + "\n"
    target = args.output or args.ledger
    target.write_text(payload, encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(target)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
