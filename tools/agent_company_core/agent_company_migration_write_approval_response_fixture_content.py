"""Pure fixture builders for parser-write approval responses."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

NEGATIVE_APPROVAL_RESPONSE_FIXTURE_SPECS = [
    ("missing_decision_id", {"decision_id": None}, "guard_required_fields_present"),
    ("unknown_response_type", {"response_type": "approve_write_import_and_live_parse"}, "guard_known_response_type"),
    ("target_path_changed", {"target_path": r"E:\agent-company-lab\tools\unexpected_parser.py"}, "guard_target_path_matches_request"),
    ("source_artifact_path_changed", {"source_artifact_path": r"E:\agent-company-lab\reports\unexpected-parser-draft.json"}, "guard_source_artifact_matches_request"),
    ("source_request_path_changed", {"source_request_path": r"E:\agent-company-lab\reports\unexpected-approval-request.json"}, "guard_source_request_matches_packet"),
    ("approval_scope_too_broad", {"approval_scope": "write_import_and_live_parse"}, "guard_approval_scope_one_file_only"),
    ("expired_response", {"expires_at": "2026-06-15T00:00:00Z"}, "guard_not_expired"),
    ("unsigned_response", {"signed_utc": None}, "guard_signed_timestamp_present"),
    ("bundled_import_or_live_parse_permission", {"risk_acknowledgement": "also_allows_import_and_live_parse"}, "guard_no_import_or_live_parse_permission"),
]


def build_approval_response_fixture_suite(
    *,
    positive_fixture_specs: list[dict[str, Any]],
    expected_target_path: object,
    expected_source_artifact_path: object,
    expected_source_request_path: object,
) -> dict[str, Any]:
    positive_fixtures = [
        {
            "fixture_id": item["fixture"],
            "kind": "positive",
            "response": {
                "decision_id": f"fixture-{item['response_type']}-20260616",
                "operator_name": "fixture_operator",
                "response_type": item["response_type"],
                "target_path": expected_target_path,
                "source_artifact_path": expected_source_artifact_path,
                "source_request_path": expected_source_request_path,
                "approval_scope": "one_local_file_write_only",
                "risk_acknowledgement": "report_only_fixture_no_approval_applied",
                "expires_at": "2026-06-17T00:00:00Z",
                "signed_utc": "2026-06-16T00:00:00Z",
            },
            "expected_valid": True,
            "expected_state": item["expected_state"],
            "assertion": "accepted approval response type maps to the declared report-only output state",
        }
        for item in positive_fixture_specs
    ]
    base_negative_response = {
        "decision_id": "fixture-approval-response-negative-base-20260616",
        "operator_name": "fixture_operator",
        "response_type": "approve_one_parser_file_write_only",
        "target_path": expected_target_path,
        "source_artifact_path": expected_source_artifact_path,
        "source_request_path": expected_source_request_path,
        "approval_scope": "one_local_file_write_only",
        "risk_acknowledgement": "report_only_fixture_no_approval_applied",
        "expires_at": "2026-06-17T00:00:00Z",
        "signed_utc": "2026-06-16T00:00:00Z",
    }
    negative_fixtures = []
    for fixture_id, overrides, expected_guard in NEGATIVE_APPROVAL_RESPONSE_FIXTURE_SPECS:
        response = dict(base_negative_response)
        response.update(overrides)
        negative_fixtures.append(
            {
                "fixture_id": fixture_id,
                "kind": "negative",
                "response": response,
                "expected_valid": False,
                "expected_state": "rejected_fixture_input",
                "expected_guard": expected_guard,
                "assertion": f"{fixture_id} is rejected by {expected_guard}",
            }
        )
    fixtures = positive_fixtures + negative_fixtures
    return {
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
        "fixtures": fixtures,
        "parser_write_approval_response_fixture_suite_count": len(fixtures),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "fixture_assertion_count": sum(1 for item in fixtures if item.get("assertion")),
    }




def build_approval_response_fixture_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    fixture_task_id: str,
    fixture_evidence_id: str,
    source_intake_task_id: str,
    source_intake_evidence_id: str,
    expected_target_path: object,
    expected_source_artifact_path: object,
    expected_source_request_path: object,
    parser_write_approval_response_fixture_suite_count: int,
    positive_fixture_count: int,
    negative_fixture_count: int,
    required_field_count: int,
    response_guard_count: int,
    output_state_count: int,
    fixture_assertion_count: int,
    fixtures: Sequence[dict[str, Any]],
    required_fields: Sequence[Any],
    response_guards: Sequence[Any],
    output_states: Sequence[Any],
) -> dict[str, Any]:
    fixture_list = [dict(item) for item in fixtures]
    required_field_list = list(required_fields)
    response_guard_list = list(response_guards)
    output_state_list = list(output_states)
    local_decision = "agent_company_migration_decision_parser_write_approval_response_fixture_suite_ready_for_report_only_runner"
    recommended_default = "build_report_only_parser_write_approval_response_runner_next_without_applying_approval"
    summary = "Materialized the report-only parser-write approval response fixture suite from the intake contract, covering accepted responses, rejection cases, and response guards."
    next_action = "Build a report-only parser-write approval response runner next; do not apply approval or write the parser."
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
    payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_fixture_suite.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_intake_task_id": source_intake_task_id,
        "source_intake_evidence_id": source_intake_evidence_id,
        "expected_target_path": expected_target_path,
        "expected_source_artifact_path": expected_source_artifact_path,
        "expected_source_request_path": expected_source_request_path,
        "parser_write_approval_response_fixture_suite_count": parser_write_approval_response_fixture_suite_count,
        "positive_fixture_count": positive_fixture_count,
        "negative_fixture_count": negative_fixture_count,
        "required_field_count": required_field_count,
        "response_guard_count": response_guard_count,
        "output_state_count": output_state_count,
        "fixture_assertion_count": fixture_assertion_count,
        "fixtures": fixture_list,
        "required_fields": required_field_list,
        "response_guards": response_guard_list,
        "output_states": output_state_list,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Write Approval Response Fixture Suite",
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
        f"- Positive fixtures: {positive_fixture_count}",
        f"- Negative fixtures: {negative_fixture_count}",
        f"- Assertions: {fixture_assertion_count}",
        "",
        "## Fixtures",
        "",
    ]
    for item in fixture_list:
        expected = item["expected_state"] if item["expected_valid"] else item["expected_guard"]
        md_lines.append(f"- `{item['fixture_id']}` ({item['kind']}): {expected}")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only approval response fixture suite. It does not execute fixtures, apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}

__all__ = [
    "NEGATIVE_APPROVAL_RESPONSE_FIXTURE_SPECS",
    "build_approval_response_fixture_artifacts",
    "build_approval_response_fixture_suite",
]
