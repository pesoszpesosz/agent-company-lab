from __future__ import annotations

from typing import Any


def build_parser_write_approval_response_intake_contract_content(
    *,
    source_request_payload: dict[str, Any],
    expected_source_request_path: str,
) -> dict[str, Any]:
    expected_target_path = source_request_payload.get("target_path")
    expected_source_artifact_path = source_request_payload.get("source_artifact_path")
    accepted_response_types = [
        "hold",
        "approve_one_parser_file_write_only",
        "request_approval_request_rework",
        "reject_parser_write_request",
    ]
    required_fields = [
        "decision_id",
        "operator_name",
        "response_type",
        "target_path",
        "source_artifact_path",
        "source_request_path",
        "approval_scope",
        "risk_acknowledgement",
        "expires_at",
        "signed_utc",
    ]
    positive_fixtures = [
        {"fixture": "positive_hold", "response_type": "hold", "expected_state": "accepted_hold"},
        {"fixture": "positive_approve_one_parser_file_write_only", "response_type": "approve_one_parser_file_write_only", "expected_state": "accepted_one_parser_file_write_only"},
        {"fixture": "positive_request_approval_request_rework", "response_type": "request_approval_request_rework", "expected_state": "accepted_approval_request_rework"},
        {"fixture": "positive_reject_parser_write_request", "response_type": "reject_parser_write_request", "expected_state": "accepted_parser_write_request_rejection"},
    ]
    negative_fixtures = [
        "missing_decision_id",
        "unknown_response_type",
        "target_path_changed",
        "source_artifact_path_changed",
        "source_request_path_changed",
        "approval_scope_too_broad",
        "expired_response",
        "unsigned_response",
        "bundled_import_or_live_parse_permission",
    ]
    response_guards = [
        "guard_json_object_only",
        "guard_required_fields_present",
        "guard_known_response_type",
        "guard_target_path_matches_request",
        "guard_source_artifact_matches_request",
        "guard_source_request_matches_packet",
        "guard_approval_scope_one_file_only",
        "guard_not_expired",
        "guard_signed_timestamp_present",
        "guard_no_import_or_live_parse_permission",
    ]
    output_states = [
        "accepted_hold",
        "accepted_one_parser_file_write_only",
        "accepted_approval_request_rework",
        "accepted_parser_write_request_rejection",
    ]
    summary = "Defined the report-only signed parser-write approval response intake contract, including required fields, accepted responses, guards, and fixture expectations."
    next_action = "Build a report-only parser-write approval response fixture suite next; do not apply approval or write the parser."
    runtime_boundary = {
        "operator_install_decision_applied": False,
        "parser_module_file_written": False,
        "parser_module_imported": False,
        "live_decisions_parsed": False,
        "operator_decision_applied": False,
        "migration_sql_executed": False,
        "apply_command_enabled": False,
        "tables_created": 0,
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }

    return {
        "expected_target_path": expected_target_path,
        "expected_source_artifact_path": expected_source_artifact_path,
        "expected_source_request_path": expected_source_request_path,
        "parser_write_approval_response_intake_contract_count": 1,
        "accepted_response_types": accepted_response_types,
        "required_fields": required_fields,
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
        "response_guards": response_guards,
        "output_states": output_states,
        "accepted_response_type_count": len(accepted_response_types),
        "required_field_count": len(required_fields),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "response_guard_count": len(response_guards),
        "output_state_count": len(output_states),
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_parser_write_approval_response_intake_contract_content"]
