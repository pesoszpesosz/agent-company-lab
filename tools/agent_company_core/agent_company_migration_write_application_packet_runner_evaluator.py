from __future__ import annotations


def evaluate_parser_write_application_packet_fixture(
    fixture: dict[str, object],
    *,
    application_fields: set[str],
    expected_paths: dict[str, object],
) -> dict[str, object]:
    packet = fixture.get("application_packet", {}) if isinstance(fixture.get("application_packet"), dict) else {}
    reasons: list[str] = []
    missing = sorted(field for field in application_fields if packet.get(field) in (None, ""))
    if missing:
        reasons.append("guard_required_fields_present")
    signed_path = str(packet.get("signed_response_artifact_path", ""))
    if not signed_path.startswith("E:\\agent-company-lab\\") or signed_path.startswith(("http://", "https://")):
        reasons.append("guard_signed_response_artifact_local")
    if packet.get("source_preflight_path") != expected_paths.get("source_preflight_path"):
        reasons.append("guard_source_preflight_matches_contract")
    if packet.get("source_runner_review_path") != expected_paths.get("source_runner_review_path"):
        reasons.append("guard_source_runner_review_matches_contract")
    if packet.get("target_path") != expected_paths.get("target_path"):
        reasons.append("guard_target_path_matches_request")
    if packet.get("source_artifact_path") != expected_paths.get("source_artifact_path"):
        reasons.append("guard_source_artifact_matches_request")
    if packet.get("application_scope") != "one_local_parser_file_write_application_review_only":
        reasons.append("guard_application_scope_review_only")
    if str(packet.get("expires_at", "")) <= "2026-06-16T00:00:00Z":
        reasons.append("guard_not_expired")
    if not packet.get("signed_utc"):
        reasons.append("guard_signed_timestamp_present")
    risk_ack = str(packet.get("risk_acknowledgement", "")).lower()
    if any(token in risk_ack for token in ["import", "live_parse", "live parse", "sql", "service_request", "service request", "external"]):
        reasons.append("guard_no_import_live_parse_sql_service_or_external_action")
    actual_valid = not reasons
    actual_state = "packet_valid_for_separate_application_review" if actual_valid else "rejected_fixture_input"
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
