from __future__ import annotations

from typing import Any


def build_parser_install_intake_contract_content(
    *,
    source_review_payload: dict[str, Any],
    preflight_payload: dict[str, Any],
) -> dict[str, Any]:
    target_file = (preflight_payload.get("target_files") or [{}])[0]
    expected_target_path = target_file.get("target_path")
    expected_source_artifact_path = target_file.get("source_artifact")
    accepted_install_decision_types = [item.get("option") for item in source_review_payload.get("decision_options", [])]
    required_fields = [
        "decision_id",
        "operator_name",
        "decision_type",
        "target_path",
        "source_artifact_path",
        "expires_at",
        "risk_acknowledgement",
        "signed_utc",
    ]
    positive_fixtures = [
        {
            "fixture": f"positive_{decision_type}",
            "decision_type": decision_type,
            "target_path": expected_target_path,
            "source_artifact_path": expected_source_artifact_path,
            "expected_state": output_state,
        }
        for decision_type, output_state in [
            ("hold", "accepted_hold"),
            ("approve_one_file_write_only", "accepted_one_file_write_only"),
            ("request_preflight_rework", "accepted_preflight_rework"),
            ("reject_parser_install", "accepted_install_rejection"),
        ]
    ]
    negative_fixtures = [
        "missing_decision_id",
        "unknown_decision_type",
        "target_path_changed",
        "missing_source_artifact",
        "expired_decision",
        "unsigned_decision",
        "bundled_live_parse_permission",
    ]
    parser_guards = [
        "guard_json_object_only",
        "guard_required_fields_present",
        "guard_known_install_decision_type",
        "guard_target_path_matches_preflight",
        "guard_source_artifact_matches_preflight",
        "guard_not_expired",
        "guard_signed_timestamp_present",
        "guard_no_import_or_live_parse_permission",
    ]
    output_states = [
        "accepted_hold",
        "accepted_one_file_write_only",
        "accepted_preflight_rework",
        "accepted_install_rejection",
    ]
    summary = "Defined the report-only signed install-decision intake contract for the parser install review, including required fields, fixtures, parser guards, and output states."
    next_action = "Build a report-only install-decision fixture suite next; do not apply an install decision or write/import a parser module."
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
        "install_decision_intake_contract_count": 1,
        "accepted_install_decision_types": accepted_install_decision_types,
        "required_fields": required_fields,
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
        "parser_guards": parser_guards,
        "output_states": output_states,
        "accepted_install_decision_type_count": len(accepted_install_decision_types),
        "required_field_count": len(required_fields),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "parser_guard_count": len(parser_guards),
        "output_state_count": len(output_states),
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_parser_install_intake_contract_content"]
