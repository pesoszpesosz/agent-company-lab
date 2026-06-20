"""Reusable write-decision intake contract content for migration parser writes."""

from __future__ import annotations

from typing import Any

from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT,
)


def accepted_write_decision_types() -> list[str]:
    return [
        "hold",
        "approve_one_parser_file_write_only",
        "request_runner_review_rework",
        "reject_parser_write",
    ]


def required_write_decision_fields() -> list[str]:
    return [
        "decision_id",
        "operator_name",
        "decision_type",
        "target_path",
        "source_artifact_path",
        "source_review_path",
        "expires_at",
        "risk_acknowledgement",
        "signed_utc",
    ]


def positive_write_decision_fixtures(
    expected_target_path: str | None,
    expected_source_artifact_path: str | None,
    expected_source_review_path: str,
) -> list[dict[str, Any]]:
    return [
        {
            "fixture": "positive_hold",
            "decision_type": "hold",
            "expected_state": "accepted_hold",
            "target_path": expected_target_path,
            "source_artifact_path": expected_source_artifact_path,
            "source_review_path": expected_source_review_path,
        },
        {
            "fixture": "positive_approve_one_parser_file_write_only",
            "decision_type": "approve_one_parser_file_write_only",
            "expected_state": "accepted_one_parser_file_write_only",
            "target_path": expected_target_path,
            "source_artifact_path": expected_source_artifact_path,
            "source_review_path": expected_source_review_path,
        },
        {
            "fixture": "positive_request_runner_review_rework",
            "decision_type": "request_runner_review_rework",
            "expected_state": "accepted_runner_review_rework",
            "target_path": expected_target_path,
            "source_artifact_path": expected_source_artifact_path,
            "source_review_path": expected_source_review_path,
        },
        {
            "fixture": "positive_reject_parser_write",
            "decision_type": "reject_parser_write",
            "expected_state": "accepted_parser_write_rejection",
            "target_path": expected_target_path,
            "source_artifact_path": expected_source_artifact_path,
            "source_review_path": expected_source_review_path,
        },
    ]


def negative_write_decision_fixtures() -> list[str]:
    return [
        "missing_decision_id",
        "unknown_decision_type",
        "target_path_changed",
        "source_artifact_path_changed",
        "source_review_path_changed",
        "expired_decision",
        "unsigned_decision",
        "bundled_import_or_live_parse_permission",
    ]


def parser_write_decision_guards() -> list[str]:
    return [
        "guard_json_object_only",
        "guard_required_fields_present",
        "guard_known_parser_write_decision_type",
        "guard_target_path_matches_preflight",
        "guard_source_artifact_matches_preflight",
        "guard_source_review_matches_runner_review",
        "guard_not_expired",
        "guard_signed_timestamp_present",
        "guard_no_import_or_live_parse_permission",
    ]


def parser_write_decision_output_states() -> list[str]:
    return [
        "accepted_hold",
        "accepted_one_parser_file_write_only",
        "accepted_runner_review_rework",
        "accepted_parser_write_rejection",
    ]


def parser_write_decision_evidence_links() -> list[str]:
    return [
        str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_REPORT),
        str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_VALIDATION_JSON),
        str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REPORT),
        str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT),
    ]


def build_parser_write_decision_intake_contract_model(
    expected_target_path: str | None,
    expected_source_artifact_path: str | None,
    expected_source_review_path: str,
) -> dict[str, Any]:
    return {
        "accepted_write_decision_types": accepted_write_decision_types(),
        "required_fields": required_write_decision_fields(),
        "positive_fixtures": positive_write_decision_fixtures(
            expected_target_path,
            expected_source_artifact_path,
            expected_source_review_path,
        ),
        "negative_fixtures": negative_write_decision_fixtures(),
        "parser_guards": parser_write_decision_guards(),
        "output_states": parser_write_decision_output_states(),
        "evidence_links": parser_write_decision_evidence_links(),
    }



def build_parser_write_decision_intake_contract_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    lane_id: str,
    intake_task_id: str,
    intake_evidence_id: str,
    source_review_task_id: str,
    source_review_evidence_id: str,
    expected_target_path: str | None,
    expected_source_artifact_path: str | None,
    expected_source_review_path: str,
) -> dict[str, Any]:
    local_decision = "agent_company_migration_decision_parser_write_decision_intake_contract_ready_for_report_only_fixture_suite"
    recommended_default = "build_report_only_parser_write_decision_fixture_suite_next_without_writing_parser"
    contract_model = build_parser_write_decision_intake_contract_model(
        expected_target_path,
        expected_source_artifact_path,
        expected_source_review_path,
    )
    accepted_write_decision_types = contract_model["accepted_write_decision_types"]
    required_fields = contract_model["required_fields"]
    positive_fixtures = contract_model["positive_fixtures"]
    negative_fixtures = contract_model["negative_fixtures"]
    parser_guards = contract_model["parser_guards"]
    output_states = contract_model["output_states"]
    evidence_links = contract_model["evidence_links"]
    summary = "Defined the report-only parser-write decision intake contract for a future signed one-file parser write approval, with hold as the default and no parser state changes."
    next_action = "Build a report-only parser-write decision fixture suite next; do not write or import the parser."
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
    payload = {
        "schema_version": "agent_company.migration_decision_parser_write_decision_intake_contract.v1",
        "generated_utc": generated_utc,
        "intake_lane_id": lane_id,
        "intake_task_id": intake_task_id,
        "intake_evidence_id": intake_evidence_id,
        "source_review_task_id": source_review_task_id,
        "source_review_evidence_id": source_review_evidence_id,
        "expected_target_path": expected_target_path,
        "expected_source_artifact_path": expected_source_artifact_path,
        "expected_source_review_path": expected_source_review_path,
        "parser_write_decision_intake_contract_count": 1,
        "accepted_write_decision_type_count": len(accepted_write_decision_types),
        "required_field_count": len(required_fields),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "parser_guard_count": len(parser_guards),
        "output_state_count": len(output_states),
        "evidence_link_count": len(evidence_links),
        "accepted_write_decision_types": accepted_write_decision_types,
        "required_fields": required_fields,
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
        "parser_guards": parser_guards,
        "output_states": output_states,
        "evidence_links": evidence_links,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# Agent Company Migration Decision Parser Write Decision Intake Contract",
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
        "## Required Fields",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in required_fields)
    md_lines.extend(["", "## Accepted Parser Write Decisions", ""])
    md_lines.extend(f"- `{item}`" for item in accepted_write_decision_types)
    md_lines.extend(["", "## Parser Guards", ""])
    md_lines.extend(f"- `{item}`" for item in parser_guards)
    md_lines.extend(["", "## Negative Fixtures", ""])
    md_lines.extend(f"- `{item}`" for item in negative_fixtures)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only parser-write decision intake contract. It does not apply an approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {
        "accepted_write_decision_type_count": len(accepted_write_decision_types),
        "accepted_write_decision_types": accepted_write_decision_types,
        "evidence_link_count": len(evidence_links),
        "evidence_links": evidence_links,
        "local_decision": local_decision,
        "markdown": "\n".join(md_lines) + "\n",
        "negative_fixture_count": len(negative_fixtures),
        "negative_fixtures": negative_fixtures,
        "next_action": next_action,
        "output_state_count": len(output_states),
        "output_states": output_states,
        "parser_guard_count": len(parser_guards),
        "parser_guards": parser_guards,
        "parser_write_decision_intake_contract_count": 1,
        "payload": payload,
        "positive_fixture_count": len(positive_fixtures),
        "positive_fixtures": positive_fixtures,
        "recommended_default": recommended_default,
        "required_field_count": len(required_fields),
        "required_fields": required_fields,
        "runtime_boundary": runtime_boundary,
        "summary": summary,
    }

__all__ = [
    "accepted_write_decision_types",
    "build_parser_write_decision_intake_contract_content",
    "build_parser_write_decision_intake_contract_model",
    "negative_write_decision_fixtures",
    "parser_write_decision_evidence_links",
    "parser_write_decision_guards",
    "parser_write_decision_output_states",
    "positive_write_decision_fixtures",
    "required_write_decision_fields",
]


