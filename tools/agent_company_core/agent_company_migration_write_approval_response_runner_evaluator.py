from __future__ import annotations


def evaluate_parser_write_approval_response_fixture(
    fixture: dict[str, object],
    *,
    required_fields: set[str],
    expected_target_path: object,
    expected_source_artifact_path: object,
    expected_source_request_path: object,
    accepted_response_types: set[str],
    output_state_by_response_type: dict[str, str],
) -> dict[str, object]:
    response = fixture.get("response", {}) if isinstance(fixture.get("response"), dict) else {}
    reasons: list[str] = []
    if not isinstance(response, dict):
        reasons.append("guard_json_object_only")
    missing = sorted(field for field in required_fields if response.get(field) in (None, ""))
    if missing:
        reasons.append("guard_required_fields_present")
    response_type = response.get("response_type")
    if response_type not in accepted_response_types:
        reasons.append("guard_known_response_type")
    if response.get("target_path") != expected_target_path:
        reasons.append("guard_target_path_matches_request")
    if response.get("source_artifact_path") != expected_source_artifact_path:
        reasons.append("guard_source_artifact_matches_request")
    if response.get("source_request_path") != expected_source_request_path:
        reasons.append("guard_source_request_matches_packet")
    if response.get("approval_scope") != "one_local_file_write_only":
        reasons.append("guard_approval_scope_one_file_only")
    if str(response.get("expires_at", "")) <= "2026-06-16T00:00:00Z":
        reasons.append("guard_not_expired")
    if not response.get("signed_utc"):
        reasons.append("guard_signed_timestamp_present")
    risk_ack = str(response.get("risk_acknowledgement", "")).lower()
    if "import" in risk_ack or "live_parse" in risk_ack or "live parse" in risk_ack:
        reasons.append("guard_no_import_or_live_parse_permission")
    actual_valid = not reasons
    actual_state = output_state_by_response_type.get(str(response_type), "rejected_fixture_input") if actual_valid else "rejected_fixture_input"
    expected_valid = bool(fixture.get("expected_valid"))
    expected_guard = fixture.get("expected_guard")
    passed = actual_valid == expected_valid
    if expected_valid:
        passed = passed and actual_state == fixture.get("expected_state")
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
