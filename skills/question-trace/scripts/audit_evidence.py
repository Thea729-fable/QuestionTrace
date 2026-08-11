#!/usr/bin/env python3
"""Audit a QuestionTrace evidence ledger before generating high-priority questions."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


VALID_SOURCE_STATES = {"candidate", "selected", "included", "excluded", "blocked"}
VALID_IMAGE_STATUSES = {"read", "unreadable", "blocked", "broken", "not_read"}
VALID_PRIORITIES = {"high", "medium", "low"}
SCORE_LIMITS = {
    "frequency": 4,
    "recency": 3,
    "jd_relevance": 3,
    "resume_trigger": 3,
    "company_role_similarity": 2,
}


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("ledger root must be a JSON object")
    return value


def audit(ledger: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    sources = ledger.get("sources", [])
    images = ledger.get("images", [])
    questions = ledger.get("question_clusters", [])
    run = ledger.get("run", {})

    if not isinstance(run, dict):
        return {"result": "FAIL", "errors": ["run must be an object"], "warnings": []}

    mode = str(run.get("mode", "")).strip()
    if mode not in {"live", "replay"}:
        errors.append("run.mode must be live or replay")

    bailian = run.get("bailian_runtime")
    if not isinstance(bailian, dict):
        errors.append("run.bailian_runtime must be an object")
        bailian = {}
    if bailian.get("required") is not True:
        errors.append("run.bailian_runtime.required must be true")
    if bailian.get("model") != "qwen3.5-omni-plus":
        errors.append("run.bailian_runtime.model must be qwen3.5-omni-plus")
    if bailian.get("jd_resume_status") != "success":
        errors.append("current JD/resume requires a successful Model Studio normalization call")
    for field in ("calls_succeeded", "calls_failed", "interview_images_processed"):
        value = bailian.get(field)
        if not isinstance(value, int) or value < 0:
            errors.append(f"run.bailian_runtime.{field} must be a non-negative integer")
    if bailian.get("raw_media_retained") is not False:
        errors.append("run.bailian_runtime.raw_media_retained must be false")

    data_handling = run.get("data_handling")
    if not isinstance(data_handling, dict):
        errors.append("run.data_handling must be an object")
        data_handling = {}
    for field in (
        "raw_post_body_retained",
        "creator_identifier_retained",
        "expiring_media_url_retained",
        "raw_question_image_retained",
    ):
        if data_handling.get(field) is not False:
            errors.append(f"run.data_handling.{field} must be false")

    if not isinstance(sources, list) or not isinstance(images, list) or not isinstance(questions, list):
        return {"result": "FAIL", "errors": ["sources, images, and question_clusters must be arrays"]}

    source_by_id: dict[str, dict] = {}
    images_by_source: dict[str, list[dict]] = defaultdict(list)

    for index, source in enumerate(sources, start=1):
        prefix = f"source[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        source_id = str(source.get("source_id", "")).strip()
        if not source_id:
            errors.append(f"{prefix}: missing source_id")
            continue
        if source_id in source_by_id:
            errors.append(f"{prefix}: duplicate source_id {source_id}")
        source_by_id[source_id] = source
        if source.get("state") not in VALID_SOURCE_STATES:
            errors.append(f"{source_id}: invalid state")
        if not str(source.get("canonical_url", "")).strip():
            errors.append(f"{source_id}: missing canonical_url")

    for index, image in enumerate(images, start=1):
        prefix = f"image[{index}]"
        if not isinstance(image, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        source_id = str(image.get("source_id", "")).strip()
        if source_id not in source_by_id:
            errors.append(f"{prefix}: unknown source_id {source_id!r}")
            continue
        images_by_source[source_id].append(image)
        if image.get("status") not in VALID_IMAGE_STATUSES:
            errors.append(f"{prefix}: invalid status")
        if image.get("status") in {"unreadable", "blocked", "broken"} and not str(
            image.get("unreadable_reason", "")
        ).strip():
            errors.append(f"{prefix}: unreadable image needs unreadable_reason")
        if image.get("status") == "read" and not str(image.get("attempted_at", "")).strip():
            errors.append(f"{prefix}: read image needs attempted_at")
        if image.get("raw_media_retained") is not False:
            errors.append(f"{prefix}: raw_media_retained must be false")

        accessible = image.get("status") == "read" and image.get("relevance") in {
            "relevant",
            "irrelevant",
        }
        if mode == "live" and accessible:
            if image.get("bailian_status") != "success":
                errors.append(f"{prefix}: live accessible image requires bailian_status=success")
            if image.get("bailian_model") != "qwen3.5-omni-plus":
                errors.append(f"{prefix}: live accessible image requires qwen3.5-omni-plus")
        if mode == "replay" and image.get("processing_path") == "legacy_replay":
            if not str(image.get("historical_tool", "")).strip():
                errors.append(f"{prefix}: legacy replay image requires historical_tool disclosure")

    included_ids: set[str] = set()
    for source_id, source in source_by_id.items():
        included = bool(source.get("included"))
        if included:
            included_ids.add(source_id)
            if source.get("state") != "included":
                errors.append(f"{source_id}: included=true requires state=included")
            if source.get("body_complete") is not True:
                errors.append(f"{source_id}: included source requires body_complete=true")
            if source.get("body_status") not in {"read", "complete"}:
                errors.append(f"{source_id}: included source requires body_status=read or complete")
            if source.get("duplicate_of"):
                errors.append(f"{source_id}: duplicate source cannot be included")
            if not source.get("read_events"):
                errors.append(f"{source_id}: included source needs at least one body read event")

            counts = []
            for field in ("media_total", "media_read", "media_irrelevant", "media_unreadable"):
                value = source.get(field)
                if not isinstance(value, int) or value < 0:
                    errors.append(f"{source_id}: {field} must be a non-negative integer")
                    value = 0
                counts.append(value)
            total, read, irrelevant, unreadable = counts
            if read + irrelevant + unreadable != total:
                errors.append(
                    f"{source_id}: media_read + media_irrelevant + media_unreadable must equal media_total"
                )
            if len(images_by_source[source_id]) != total:
                errors.append(
                    f"{source_id}: image ledger rows ({len(images_by_source[source_id])}) must equal media_total ({total})"
                )
            for image in images_by_source[source_id]:
                if image.get("status") == "not_read":
                    errors.append(f"{source_id}: included source contains an unattempted image")
        elif source.get("state") == "included":
            errors.append(f"{source_id}: state=included requires included=true")

    for index, question in enumerate(questions, start=1):
        prefix = str(question.get("question_id") or f"question[{index}]")
        if not isinstance(question, dict):
            errors.append(f"question[{index}]: must be an object")
            continue
        priority = question.get("priority")
        if priority not in VALID_PRIORITIES:
            errors.append(f"{prefix}: invalid priority")
        scores = question.get("scores", {})
        if not isinstance(scores, dict):
            errors.append(f"{prefix}: scores must be an object")
            continue
        calculated = 0
        for key, maximum in SCORE_LIMITS.items():
            value = scores.get(key)
            if not isinstance(value, int) or not 0 <= value <= maximum:
                errors.append(f"{prefix}: score {key} must be 0..{maximum}")
                value = 0
            calculated += value
        if question.get("total_score") != calculated:
            errors.append(f"{prefix}: total_score must equal component sum {calculated}")
        expected = "high" if calculated >= 12 else "medium" if calculated >= 8 else "low"
        if priority != expected:
            errors.append(f"{prefix}: priority must be {expected} for score {calculated}")

        evidence_ids = question.get("evidence_ids", [])
        if not isinstance(evidence_ids, list):
            errors.append(f"{prefix}: evidence_ids must be an array")
            evidence_ids = []
        unknown = [item for item in evidence_ids if item not in source_by_id]
        if unknown:
            errors.append(f"{prefix}: unknown evidence_ids {unknown}")

        if priority == "high":
            if not evidence_ids:
                errors.append(f"{prefix}: high priority requires interview evidence")
            if not question.get("jd_anchors"):
                errors.append(f"{prefix}: high priority requires JD anchors")
            if not str(question.get("resume_trigger", "")).strip():
                errors.append(f"{prefix}: high priority requires a resume trigger")
            for source_id in evidence_ids:
                if source_id not in included_ids:
                    errors.append(f"{prefix}: high-priority evidence {source_id} is not included")
                    continue
                unresolved = [
                    image
                    for image in images_by_source[source_id]
                    if image.get("status") in {"unreadable", "blocked", "broken"}
                    and image.get("relevance") != "irrelevant"
                ]
                if unresolved:
                    errors.append(
                        f"{prefix}: evidence {source_id} has unresolved potentially relevant images"
                    )

    included_sources = [source_by_id[item] for item in included_ids]
    media_total = sum(int(item.get("media_total", 0) or 0) for item in included_sources)
    media_read = sum(int(item.get("media_read", 0) or 0) for item in included_sources)
    media_irrelevant = sum(int(item.get("media_irrelevant", 0) or 0) for item in included_sources)
    media_unreadable = sum(int(item.get("media_unreadable", 0) or 0) for item in included_sources)
    states = Counter(str(item.get("state", "unknown")) for item in sources if isinstance(item, dict))

    if not included_sources:
        warnings.append("no included sources; a live evidence-backed high-priority bank cannot be produced")

    if mode == "live":
        live_processed = sum(
            image.get("bailian_status") == "success"
            for image in images
            if isinstance(image, dict)
        )
        if bailian.get("interview_images_processed") != live_processed:
            errors.append(
                "run.bailian_runtime.interview_images_processed must equal successful live image rows"
            )

    return {
        "result": "PASS" if not errors else "FAIL",
        "summary": {
            "sources_total": len(sources),
            "sources_included": len(included_sources),
            "source_states": dict(states),
            "body_complete_rate": (
                round(sum(item.get("body_complete") is True for item in included_sources) / len(included_sources), 4)
                if included_sources
                else 0
            ),
            "media_total": media_total,
            "media_read": media_read,
            "media_irrelevant": media_irrelevant,
            "media_unreadable": media_unreadable,
            "media_accounted_rate": (
                round((media_read + media_irrelevant + media_unreadable) / media_total, 4)
                if media_total
                else 1
            ),
            "questions_total": len(questions),
            "high_priority_questions": sum(
                isinstance(item, dict) and item.get("priority") == "high" for item in questions
            ),
            "bailian_runtime": {
                "required": bailian.get("required"),
                "model": bailian.get("model"),
                "jd_resume_status": bailian.get("jd_resume_status"),
                "calls_succeeded": bailian.get("calls_succeeded"),
                "calls_failed": bailian.get("calls_failed"),
                "interview_images_processed": bailian.get("interview_images_processed"),
                "raw_media_retained": bailian.get("raw_media_retained"),
            },
            "third_party_data_minimized": all(
                data_handling.get(field) is False
                for field in (
                    "raw_post_body_retained",
                    "creator_identifier_retained",
                    "expiring_media_url_retained",
                    "raw_question_image_retained",
                )
            ),
        },
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path, help="Path to a QuestionTrace ledger JSON file")
    parser.add_argument("--output", type=Path, help="Optional path for the audit JSON")
    args = parser.parse_args()

    try:
        result = audit(load_json(args.ledger))
    except ValueError as exc:
        result = {"result": "FAIL", "errors": [str(exc)], "warnings": []}

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result.get("result") == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
