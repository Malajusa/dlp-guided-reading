#!/usr/bin/env python3
"""Validate level-specific Guided Reading pitch approvals."""
from __future__ import annotations

import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any

EXPECTED_GROUPS = ("Alpha", "Beta", "Gamma", "Delta", "Epsilon")
REQUIRED_DIMENSIONS = ("decoding", "vocabulary_morphology", "syntax", "cohesion", "background_knowledge", "evidence_distance", "inference_ambiguity", "response_demand", "age_appropriateness", "visual_support", "conceptual_parity")
FORBIDDEN_REVIEW_FIELDS = {"suggested_profile", "replacement_profile", "new_group"}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_passage_hash(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("passage text must be a string")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _find_forbidden(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in FORBIDDEN_REVIEW_FIELDS:
                found.append(child_path)
            found.extend(_find_forbidden(child, child_path))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            found.extend(_find_forbidden(child, f"{path}[{i}]"))
    return found


def _require_list(value: Any, label: str, errors: list[str]) -> list[Any]:
    if isinstance(value, list):
        return value
    errors.append(f"{label} must be a list")
    return []


def validate_review_package(package: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    checks: list[str] = []
    if not isinstance(package, dict):
        return {"status": "FAIL", "errors": ["Package must be a JSON object"], "checks": []}
    if package.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    expected = set(EXPECTED_GROUPS)
    passages = package.get("passages") if isinstance(package.get("passages"), dict) else {}
    if not isinstance(package.get("passages"), dict):
        errors.append("passages must be an object")
    if set(passages) != expected:
        missing = sorted(expected - set(passages)); extra = sorted(set(passages) - expected)
        if missing: errors.append("Missing passages: " + ", ".join(missing))
        if extra: errors.append("Unexpected passages: " + ", ".join(extra))

    hashes: dict[str, str] = {}
    for group in EXPECTED_GROUPS:
        entry = passages.get(group)
        if not isinstance(entry, dict):
            errors.append(f"{group}: passage entry must be an object"); continue
        text = entry.get("text")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{group}: passage text must be a non-empty string"); continue
        hashes[group] = canonical_passage_hash(text)
        cycle = entry.get("revision_cycle")
        if not isinstance(cycle, int) or isinstance(cycle, bool) or not 0 <= cycle <= 3:
            errors.append(f"{group}: revision_cycle must be an integer from 0 to 3")
        if entry.get("current_sha256") is not None and entry.get("current_sha256") != hashes[group]:
            errors.append(f"{group}: current_sha256 does not match exact passage text")

    reviews = package.get("level_reviews") if isinstance(package.get("level_reviews"), dict) else {}
    if not isinstance(package.get("level_reviews"), dict): errors.append("level_reviews must be an object")
    if set(reviews) != expected:
        missing = sorted(expected - set(reviews)); extra = sorted(set(reviews) - expected)
        if missing: errors.append("Missing level reviews: " + ", ".join(missing))
        if extra: errors.append("Unexpected level reviews: " + ", ".join(extra))

    for group in EXPECTED_GROUPS:
        review = reviews.get(group)
        if not isinstance(review, dict):
            errors.append(f"{group}: level review must be an object"); continue
        role = f"{group.lower()}-pitch-reviewer"
        if review.get("reviewer_role") != role: errors.append(f"{group}: reviewer_role must be {role}")
        if review.get("group") != group: errors.append(f"{group}: review group must be {group}")
        review_hash = review.get("passage_sha256")
        if not isinstance(review_hash, str) or not HASH_RE.fullmatch(review_hash):
            errors.append(f"{group}: passage_sha256 must be 64-character lowercase hex")
        elif group in hashes and review_hash != hashes[group]:
            errors.append(f"{group}: review hash is stale and does not match current passage")
        verdict = review.get("verdict")
        if verdict not in {"PASS", "REVISE", "REJECT"}: errors.append(f"{group}: verdict must be PASS, REVISE, or REJECT")
        elif verdict != "PASS": errors.append(f"{group}: release package requires PASS; found {verdict}")
        if not isinstance(review.get("pitch_summary"), str) or not review.get("pitch_summary", "").strip():
            errors.append(f"{group}: pitch_summary must be non-empty")
        dims = review.get("dimension_findings")
        if not isinstance(dims, dict): errors.append(f"{group}: dimension_findings must be an object")
        else:
            required = set(REQUIRED_DIMENSIONS)
            if set(dims) != required:
                missing = sorted(required - set(dims)); extra = sorted(set(dims) - required)
                if missing: errors.append(f"{group}: missing dimensions: " + ", ".join(missing))
                if extra: errors.append(f"{group}: unexpected dimensions: " + ", ".join(extra))
            for dim in REQUIRED_DIMENSIONS:
                if dim in dims and (not isinstance(dims[dim], str) or not dims[dim].strip()): errors.append(f"{group}: dimension {dim} must be non-empty")
        blocking = _require_list(review.get("blocking_issues"), f"{group}: blocking_issues", errors)
        revisions = _require_list(review.get("required_revisions"), f"{group}: required_revisions", errors)
        _require_list(review.get("non_blocking_notes"), f"{group}: non_blocking_notes", errors)
        if verdict == "PASS" and blocking: errors.append(f"{group}: PASS cannot contain blocking_issues")
        if verdict == "PASS" and revisions: errors.append(f"{group}: PASS cannot contain required_revisions")
        for path in _find_forbidden(review): errors.append(f"{group}: reviewer attempted placement change via forbidden field {path}")

    progression = package.get("progression_review")
    if not isinstance(progression, dict): errors.append("progression_review must be an object")
    else:
        if progression.get("reviewer_role") != "progression-parity-reviewer": errors.append("progression_review reviewer_role must be progression-parity-reviewer")
        verdict = progression.get("verdict")
        if verdict not in {"PASS", "REVISE_LEVELS", "REJECT_SET"}: errors.append("progression_review verdict must be PASS, REVISE_LEVELS, or REJECT_SET")
        elif verdict != "PASS": errors.append(f"progression_review release package requires PASS; found {verdict}")
        if not isinstance(progression.get("pitch_progression_summary"), str) or not progression.get("pitch_progression_summary", "").strip(): errors.append("progression_review pitch_progression_summary must be non-empty")
        p_hashes = progression.get("passage_sha256")
        if not isinstance(p_hashes, dict): errors.append("progression_review passage_sha256 must be an object")
        else:
            if set(p_hashes) != expected: errors.append("progression_review passage_sha256 must contain exactly Alpha-Epsilon")
            for group in EXPECTED_GROUPS:
                value = p_hashes.get(group)
                if not isinstance(value, str) or not HASH_RE.fullmatch(value): errors.append(f"progression_review {group} hash must be 64-character lowercase hex")
                elif group in hashes and value != hashes[group]: errors.append(f"progression_review {group} hash is stale")
        blocking = _require_list(progression.get("blocking_issues"), "progression_review blocking_issues", errors)
        revisions = progression.get("required_revisions")
        if not isinstance(revisions, dict): errors.append("progression_review required_revisions must be an object"); revisions = {}
        _require_list(progression.get("non_blocking_notes"), "progression_review non_blocking_notes", errors)
        if verdict == "PASS" and blocking: errors.append("progression_review PASS cannot contain blocking_issues")
        if verdict == "PASS" and revisions: errors.append("progression_review PASS cannot contain required_revisions")
        for path in _find_forbidden(progression): errors.append(f"progression reviewer attempted placement change via forbidden field {path}")

    if not errors:
        checks = ["All five current passages have matching level PASS approvals", "All review dimensions are present", "Revision-cycle limits are satisfied", "Progression/parity PASS matches the exact five hashes", "No placement-change fields were used"]
    return {"status": "PASS" if not errors else "FAIL", "errors": errors, "checks": checks}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv or sys.argv[1:])
    try:
        report = validate_review_package(json.loads(args.package.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        report = {"status": "FAIL", "errors": [str(exc)], "checks": []}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
