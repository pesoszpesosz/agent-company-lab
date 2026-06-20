from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def build_application_packet_runner_review_content(
    *,
    runner_report_path: str,
    runner_validation_path: str,
    fixture_suite_report_path: str,
    packet_contract_report_path: str,
) -> dict[str, Any]:
    runner_result_checks = [
        "runner_validation_clean",
        "all_application_packet_fixture_results_passed",
        "positive_fixture_accept_count_is_1",
        "negative_fixture_reject_count_is_9",
        "application_allowed_remains_false",
        "no_parser_service_or_external_side_effect",
    ]
    application_conditions = [
        "a separate signed application packet exists",
        "packet references this runner review artifact",
        "packet target path and source artifact match the approval request",
        "packet scope is one local parser file write application review only",
        "packet excludes parser import live parsing SQL service-request mutation and external actions",
        "post-application static review and fixture rerun remain required before import",
    ]
    hold_conditions = [
        "signed application packet is absent",
        "runner validation or fixture results are stale",
        "packet changes target path source artifact preflight or runner review",
        "packet scope is broader than review-only one-file application",
        "packet bundles import live parsing SQL service-request worker API or browser action",
        "packet attempts account wallet payment public security or real-money side effects",
    ]
    evidence_links = [
        runner_report_path,
        runner_validation_path,
        fixture_suite_report_path,
        packet_contract_report_path,
    ]
    operator_instructions = [
        "Default to hold unless a separate signed application packet is supplied.",
        "Do not treat this review as approval to apply anything.",
        "Do not write or import the parser from this review.",
        "Do not accept packets that alter any reviewed path or scope.",
        "Reject any bundle that includes SQL, live parsing, service requests, browser work, accounts, wallets, payments, public actions, security testing, or APIs.",
        "If a future packet passes review, prepare a separate pre-application static packet before file writes.",
        "Keep post-write static review and fixture rerun mandatory before any import question.",
    ]
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
    summary = "Reviewed the report-only approval response application packet runner results and kept application blocked pending a separate signed application packet."
    next_action = "Hold until a separate signed application packet is supplied; do not apply approval or write/import the parser from this review."

    return {
        "parser_write_approval_response_application_packet_runner_review_count": 1,
        "application_allowed": False,
        "runner_result_checks": runner_result_checks,
        "application_conditions": application_conditions,
        "hold_conditions": hold_conditions,
        "evidence_links": evidence_links,
        "operator_instructions": operator_instructions,
        "runner_result_check_count": len(runner_result_checks),
        "application_condition_count": len(application_conditions),
        "hold_condition_count": len(hold_conditions),
        "evidence_link_count": len(evidence_links),
        "operator_instruction_count": len(operator_instructions),
        "local_decision": "agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review_ready_for_signed_packet_or_hold",
        "recommended_default": "hold_without_signed_approval_response_application_packet_application",
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


def build_application_packet_runner_review_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    review_task_id: str,
    review_evidence_id: str,
    source_runner_task_id: str,
    source_runner_evidence_id: str,
    review_content: Mapping[str, Any],
    runner_result_summary: Mapping[str, Any],
) -> dict[str, Any]:
    payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_application_packet_runner_review.v1",
        "generated_utc": generated_utc,
        "review_lane_id": lane_id,
        "review_task_id": review_task_id,
        "review_evidence_id": review_evidence_id,
        "source_runner_task_id": source_runner_task_id,
        "source_runner_evidence_id": source_runner_evidence_id,
        "parser_write_approval_response_application_packet_runner_review_count": review_content["parser_write_approval_response_application_packet_runner_review_count"],
        "runner_result_check_count": review_content["runner_result_check_count"],
        "application_condition_count": review_content["application_condition_count"],
        "hold_condition_count": review_content["hold_condition_count"],
        "evidence_link_count": review_content["evidence_link_count"],
        "operator_instruction_count": review_content["operator_instruction_count"],
        "application_allowed": review_content["application_allowed"],
        "runner_result_checks": list(review_content["runner_result_checks"]),
        "application_conditions": list(review_content["application_conditions"]),
        "hold_conditions": list(review_content["hold_conditions"]),
        "evidence_links": list(review_content["evidence_links"]),
        "operator_instructions": list(review_content["operator_instructions"]),
        "runner_result_summary": dict(runner_result_summary),
        "local_decision": review_content["local_decision"],
        "recommended_default": review_content["recommended_default"],
        "summary": review_content["summary"],
        "next_action": review_content["next_action"],
        "runtime_boundary": dict(review_content["runtime_boundary"]),
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Write Approval Response Application Packet Runner Review",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{payload['local_decision']}`",
        "",
        f"Recommended default: `{payload['recommended_default']}`",
        "",
        payload["summary"],
        "",
        "## Runner Result Checks",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in payload["runner_result_checks"])
    md_lines.extend(["", "## Application Conditions", ""])
    md_lines.extend(f"- {item}" for item in payload["application_conditions"])
    md_lines.extend(["", "## Hold Conditions", ""])
    md_lines.extend(f"- {item}" for item in payload["hold_conditions"])
    md_lines.extend(["", "## Operator Instructions", ""])
    md_lines.extend(f"- {item}" for item in payload["operator_instructions"])
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only application packet runner review. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = [
    "build_application_packet_runner_review_artifacts",
    "build_application_packet_runner_review_content",
]
