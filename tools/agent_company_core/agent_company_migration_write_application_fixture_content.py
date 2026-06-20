"""Pure content builders for approval-response application packet fixtures."""

from __future__ import annotations

from typing import Any

APPLICATION_PACKET_GUARDS = [
    "guard_required_fields_present",
    "guard_signed_response_artifact_local",
    "guard_source_preflight_matches_contract",
    "guard_source_runner_review_matches_contract",
    "guard_target_path_matches_request",
    "guard_source_artifact_matches_request",
    "guard_application_scope_review_only",
    "guard_not_expired",
    "guard_signed_timestamp_present",
    "guard_no_import_live_parse_sql_service_or_external_action",
]

NEGATIVE_APPLICATION_PACKET_FIXTURE_SPECS = [
    ("missing_application_packet_id", {"application_packet_id": None}, "guard_required_fields_present"),
    ("nonlocal_signed_response_artifact", {"signed_response_artifact_path": "https://example.invalid/response.json"}, "guard_signed_response_artifact_local"),
    ("source_preflight_changed", {"source_preflight_path": r"E:\agent-company-lab\reports\unexpected-preflight.json"}, "guard_source_preflight_matches_contract"),
    ("source_runner_review_changed", {"source_runner_review_path": r"E:\agent-company-lab\reports\unexpected-review.json"}, "guard_source_runner_review_matches_contract"),
    ("target_path_changed", {"target_path": r"E:\agent-company-lab\tools\unexpected_parser.py"}, "guard_target_path_matches_request"),
    ("source_artifact_changed", {"source_artifact_path": r"E:\agent-company-lab\reports\unexpected-artifact.json"}, "guard_source_artifact_matches_request"),
    ("application_scope_too_broad", {"application_scope": "write_import_and_live_parse"}, "guard_application_scope_review_only"),
    ("expired_packet", {"expires_at": "2026-06-15T00:00:00Z"}, "guard_not_expired"),
    ("bundled_import_sql_or_service_action", {"risk_acknowledgement": "also_allows_import_live_parse_sql_and_service_request_update"}, "guard_no_import_live_parse_sql_service_or_external_action"),
]


def build_application_packet_fixture_suite(
    *,
    expected_target_path: str | None,
    expected_source_artifact_path: str | None,
    expected_source_preflight_path: str,
    expected_source_runner_review_path: str,
    expected_signed_response_artifact_path: str,
) -> dict[str, Any]:
    base_packet = {
        "application_packet_id": "fixture-application-packet-positive-20260616",
        "operator_name": "fixture_operator",
        "signed_response_artifact_path": expected_signed_response_artifact_path,
        "source_preflight_path": expected_source_preflight_path,
        "source_runner_review_path": expected_source_runner_review_path,
        "target_path": expected_target_path,
        "source_artifact_path": expected_source_artifact_path,
        "application_scope": "one_local_parser_file_write_application_review_only",
        "expires_at": "2026-06-17T00:00:00Z",
        "signed_utc": "2026-06-16T00:00:00Z",
        "risk_acknowledgement": "report_only_fixture_no_approval_applied",
    }
    positive_fixtures = [
        {
            "fixture_id": "positive_valid_review_only_application_packet",
            "kind": "positive",
            "application_packet": dict(base_packet),
            "expected_valid": True,
            "expected_state": "packet_valid_for_separate_application_review",
            "assertion": "valid signed packet shape is accepted only for a separate report-only application review",
        }
    ]
    negative_fixtures = []
    for fixture_id, overrides, expected_guard in NEGATIVE_APPLICATION_PACKET_FIXTURE_SPECS:
        packet = dict(base_packet)
        packet["application_packet_id"] = f"fixture-{fixture_id}-20260616"
        packet.update(overrides)
        negative_fixtures.append(
            {
                "fixture_id": fixture_id,
                "kind": "negative",
                "application_packet": packet,
                "expected_valid": False,
                "expected_state": "rejected_fixture_input",
                "expected_guard": expected_guard,
                "assertion": f"{fixture_id} is rejected by {expected_guard}",
            }
        )
    fixtures = positive_fixtures + negative_fixtures
    return {
        "application_packet_guards": APPLICATION_PACKET_GUARDS,
        "base_packet": base_packet,
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
        "fixtures": fixtures,
        "fixture_assertion_count": sum(1 for item in fixtures if item.get("assertion")),
        "expected_paths": {
            "target_path": expected_target_path,
            "source_artifact_path": expected_source_artifact_path,
            "source_preflight_path": expected_source_preflight_path,
            "source_runner_review_path": expected_source_runner_review_path,
        },
    }



def build_application_packet_fixture_suite_artifacts(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    lane_id: str,
    fixture_task_id: str,
    fixture_evidence_id: str,
    source_contract_task_id: str,
    source_contract_evidence_id: str,
    application_fields: list[str],
    eligibility_rules: list[str],
    application_allowed: bool,
    fixture_content: dict[str, Any],
) -> dict[str, Any]:
    application_packet_guards = fixture_content["application_packet_guards"]
    positive_fixtures = fixture_content["positive_fixtures"]
    negative_fixtures = fixture_content["negative_fixtures"]
    fixtures = fixture_content["fixtures"]
    fixture_assertion_count = fixture_content["fixture_assertion_count"]
    expected_paths = fixture_content["expected_paths"]
    local_decision = "agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite_ready_for_report_only_runner"
    recommended_default = "build_report_only_approval_response_application_packet_runner_next_without_applying"
    summary = "Materialized report-only approval response application packet fixtures from the contract, including one valid review-only packet and nine guard rejection cases."
    next_action = "Build a report-only application packet runner next; do not apply approval or write/import the parser."
    runtime_boundary = {
        "operator_install_decision_applied": False,
        "parser_module_file_written": False,
        "parser_module_imported": False,
        "fixtures_executed": False,
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
    artifact_content = {
        "parser_write_approval_response_application_packet_fixture_suite_count": len(fixtures),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "application_field_count": len(application_fields),
        "eligibility_rule_count": len(eligibility_rules),
        "application_packet_guard_count": len(application_packet_guards),
        "fixture_assertion_count": fixture_assertion_count,
        "application_allowed": application_allowed,
        "application_fields": application_fields,
        "eligibility_rules": eligibility_rules,
        "application_packet_guards": application_packet_guards,
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
        "fixtures": fixtures,
        "expected_paths": expected_paths,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_application_packet_fixture_suite.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_contract_task_id": source_contract_task_id,
        "source_contract_evidence_id": source_contract_evidence_id,
        **artifact_content,
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Write Approval Response Application Packet Fixture Suite",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        f"Recommended default: `{recommended_default}`",
        "",
        summary,
        "",
        "## Fixture Counts",
        "",
        f"- Positive fixtures: {len(positive_fixtures)}",
        f"- Negative fixtures: {len(negative_fixtures)}",
        f"- Assertions: {fixture_assertion_count}",
        "",
        "## Fixtures",
        "",
    ]
    for item in fixtures:
        expected = item["expected_state"] if item["expected_valid"] else item["expected_guard"]
        md_lines.append(f"- `{item['fixture_id']}` ({item['kind']}): `{expected}`")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only fixture suite. It does not execute fixtures, apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {**artifact_content, "payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = [
    "APPLICATION_PACKET_GUARDS",
    "NEGATIVE_APPLICATION_PACKET_FIXTURE_SPECS",
    "build_application_packet_fixture_suite",
    "build_application_packet_fixture_suite_artifacts",
]
