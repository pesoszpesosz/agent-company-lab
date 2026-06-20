"""Pure fixture builders for parser-write decisions."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

NEGATIVE_WRITE_DECISION_FIXTURE_SPECS = [
    ("missing_decision_id", {"decision_id": None}, "guard_required_fields_present"),
    ("unknown_decision_type", {"decision_type": "approve_write_import_and_live_parse"}, "guard_known_parser_write_decision_type"),
    ("target_path_changed", {"target_path": r"E:\agent-company-lab\tools\unexpected_parser.py"}, "guard_target_path_matches_preflight"),
    (
        "source_artifact_path_changed",
        {"source_artifact_path": r"E:\agent-company-lab\reports\unexpected-parser-draft.json"},
        "guard_source_artifact_matches_preflight",
    ),
    (
        "source_review_path_changed",
        {"source_review_path": r"E:\agent-company-lab\reports\unexpected-runner-review.json"},
        "guard_source_review_matches_runner_review",
    ),
    ("expired_decision", {"expires_at": "2026-06-15T00:00:00Z"}, "guard_not_expired"),
    ("unsigned_decision", {"signed_utc": None}, "guard_signed_timestamp_present"),
    (
        "bundled_import_or_live_parse_permission",
        {"risk_acknowledgement": "also_allows_import_and_live_parse"},
        "guard_no_import_or_live_parse_permission",
    ),
]


def build_parser_write_decision_fixture_suite(
    *,
    positive_fixture_specs: list[dict[str, Any]],
    expected_target_path: object,
    expected_source_artifact_path: object,
    expected_source_review_path: object,
) -> dict[str, Any]:
    positive_fixtures = [
        {
            "fixture_id": item["fixture"],
            "kind": "positive",
            "decision": {
                "decision_id": f"fixture-{item['decision_type']}-20260616",
                "operator_name": "fixture_operator",
                "decision_type": item["decision_type"],
                "target_path": expected_target_path,
                "source_artifact_path": expected_source_artifact_path,
                "source_review_path": expected_source_review_path,
                "expires_at": "2026-06-17T00:00:00Z",
                "risk_acknowledgement": "report_only_fixture_no_parser_write_applied",
                "signed_utc": "2026-06-16T00:00:00Z",
            },
            "expected_valid": True,
            "expected_state": item["expected_state"],
            "assertion": "accepted parser-write decision type maps to the declared report-only output state",
        }
        for item in positive_fixture_specs
    ]
    base_negative_decision = {
        "decision_id": "fixture-parser-write-negative-base-20260616",
        "operator_name": "fixture_operator",
        "decision_type": "approve_one_parser_file_write_only",
        "target_path": expected_target_path,
        "source_artifact_path": expected_source_artifact_path,
        "source_review_path": expected_source_review_path,
        "expires_at": "2026-06-17T00:00:00Z",
        "risk_acknowledgement": "report_only_fixture_no_parser_write_applied",
        "signed_utc": "2026-06-16T00:00:00Z",
    }
    negative_fixtures = []
    for fixture_id, overrides, expected_guard in NEGATIVE_WRITE_DECISION_FIXTURE_SPECS:
        decision = dict(base_negative_decision)
        decision.update(overrides)
        negative_fixtures.append(
            {
                "fixture_id": fixture_id,
                "kind": "negative",
                "decision": decision,
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
        "parser_write_decision_fixture_suite_count": len(fixtures),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "fixture_assertion_count": sum(1 for item in fixtures if item.get("assertion")),
    }




def build_parser_write_decision_fixture_artifacts(
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
    expected_source_review_path: object,
    parser_write_decision_fixture_suite_count: int,
    positive_fixture_count: int,
    negative_fixture_count: int,
    required_field_count: int,
    parser_guard_count: int,
    output_state_count: int,
    fixture_assertion_count: int,
    fixtures: Sequence[dict[str, Any]],
    required_fields: Sequence[Any],
    parser_guards: Sequence[Any],
    output_states: Sequence[Any],
) -> dict[str, Any]:
    fixture_list = [dict(item) for item in fixtures]
    required_field_list = list(required_fields)
    parser_guard_list = list(parser_guards)
    output_state_list = list(output_states)
    local_decision = "agent_company_migration_decision_parser_write_decision_fixture_suite_ready_for_report_only_runner"
    recommended_default = "build_report_only_parser_write_decision_runner_next_without_writing_parser"
    summary = "Materialized the report-only parser-write decision fixture suite from the intake contract, covering accepted write decisions, rejection cases, and parser-write guards."
    next_action = "Build a report-only parser-write decision runner next; do not execute a parser write or import the parser."
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
        "schema_version": "agent_company.migration_decision_parser_write_decision_fixture_suite.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_intake_task_id": source_intake_task_id,
        "source_intake_evidence_id": source_intake_evidence_id,
        "expected_target_path": expected_target_path,
        "expected_source_artifact_path": expected_source_artifact_path,
        "expected_source_review_path": expected_source_review_path,
        "parser_write_decision_fixture_suite_count": parser_write_decision_fixture_suite_count,
        "positive_fixture_count": positive_fixture_count,
        "negative_fixture_count": negative_fixture_count,
        "required_field_count": required_field_count,
        "parser_guard_count": parser_guard_count,
        "output_state_count": output_state_count,
        "fixture_assertion_count": fixture_assertion_count,
        "fixtures": fixture_list,
        "required_fields": required_field_list,
        "parser_guards": parser_guard_list,
        "output_states": output_state_list,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Write Decision Fixture Suite",
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
            "This is a report-only parser-write decision fixture suite. It does not execute fixtures, apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}

__all__ = [
    "NEGATIVE_WRITE_DECISION_FIXTURE_SPECS",
    "build_parser_write_decision_fixture_artifacts",
    "build_parser_write_decision_fixture_suite",
]


