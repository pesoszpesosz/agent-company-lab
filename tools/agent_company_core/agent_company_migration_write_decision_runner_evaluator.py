from __future__ import annotations


def evaluate_parser_write_decision_fixture(
    fixture: dict[str, object],
    *,
    required_fields: set[str],
    expected_target_path: object,
    expected_source_artifact_path: object,
    expected_source_review_path: object,
    accepted_decision_types: set[str],
) -> dict[str, object]:
    decision = fixture.get("decision", {}) if isinstance(fixture.get("decision"), dict) else {}
    reasons: list[str] = []
    missing = sorted(field for field in required_fields if decision.get(field) in (None, ""))
    if missing:
        reasons.append("guard_required_fields_present")
    if decision.get("decision_type") not in accepted_decision_types:
        reasons.append("guard_known_parser_write_decision_type")
    if decision.get("target_path") != expected_target_path:
        reasons.append("guard_target_path_matches_preflight")
    if decision.get("source_artifact_path") != expected_source_artifact_path:
        reasons.append("guard_source_artifact_matches_preflight")
    if decision.get("source_review_path") != expected_source_review_path:
        reasons.append("guard_source_review_matches_runner_review")
    if str(decision.get("expires_at", "")) <= "2026-06-16T00:00:00Z":
        reasons.append("guard_not_expired")
    if not decision.get("signed_utc"):
        reasons.append("guard_signed_timestamp_present")
    risk_ack = str(decision.get("risk_acknowledgement", "")).lower()
    if "import" in risk_ack or "live_parse" in risk_ack or "live parse" in risk_ack:
        reasons.append("guard_no_import_or_live_parse_permission")
    actual_valid = not reasons
    actual_state = fixture.get("expected_state") if actual_valid else "rejected_fixture_input"
    expected_valid = bool(fixture.get("expected_valid"))
    expected_guard = fixture.get("expected_guard")
    passed = actual_valid == expected_valid
    if expected_guard:
        passed = passed and expected_guard in reasons
    return {
        "fixture_id": fixture.get("fixture_id"),
        "kind": fixture.get("kind"),
        "expected_valid": expected_valid,
        "actual_valid": actual_valid,
        "expected_state": fixture.get("expected_state"),
        "actual_state": actual_state,
        "expected_guard": expected_guard,
        "reasons": reasons,
        "passed": passed,
    }
