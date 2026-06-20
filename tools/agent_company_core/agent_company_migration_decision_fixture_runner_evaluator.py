from __future__ import annotations


def evaluate_migration_decision_fixture(
    fixture: dict[str, object],
    *,
    accepted_decision_types: set[str],
    required_fields: set[str],
) -> dict[str, object]:
    submitted = fixture.get("submitted_intake", {}) if isinstance(fixture.get("submitted_intake"), dict) else {}
    reasons: list[str] = []
    missing = sorted(required_fields.difference(submitted))
    if missing:
        reasons.append("missing_required_fields")
    decision_type = submitted.get("decision_type")
    if decision_type not in accepted_decision_types:
        reasons.append("unknown_decision_type")
    scope = str(submitted.get("scope", "")).lower()
    if "live" in scope or "wallet" in scope or "browser" in scope or "service_request" in scope or "assign_worker" in scope:
        reasons.append("forbidden_scope")
    artifact_paths = submitted.get("artifact_paths")
    if not isinstance(artifact_paths, list) or len(artifact_paths) < 4:
        reasons.append("missing_artifact_paths")
    if str(submitted.get("expires_at", "")) <= "2026-06-16T00:00:00Z":
        reasons.append("expired_or_missing_expiration")
    if "signed_utc" not in submitted:
        reasons.append("unsigned_decision")
    actual = "reject" if reasons else "accept"
    expected = fixture.get("expected")
    return {
        "fixture_id": fixture.get("fixture_id"),
        "expected": expected,
        "actual": actual,
        "passed": actual == expected,
        "reasons": reasons,
    }
