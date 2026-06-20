from __future__ import annotations

from typing import Any


def build_parser_write_approval_request_content(
    *,
    target_path: str | None,
    source_artifact_path: str | None,
    source_review_path: str,
    source_review_report_path: str,
    source_review_validation_path: str,
    source_runner_report_path: str,
    source_fixture_suite_report_path: str,
    install_preflight_report_path: str,
) -> dict[str, Any]:
    approval_fields = [
        "decision_id",
        "operator_name",
        "decision_type",
        "target_path",
        "source_artifact_path",
        "source_review_path",
        "approval_scope",
        "expires_at",
        "signed_utc",
    ]
    boundary_conditions = [
        "one local file write only",
        "target path must match parser install preflight",
        "source artifact must match parser module file draft",
        "source review must match parser-write runner review",
        "no parser import",
        "no live decision parsing",
        "post-write static review and fixture rerun required",
        "no external service request browser account wallet payment public or security action",
    ]
    refusal_triggers = [
        "missing signed decision id",
        "approval scope broader than one local file write",
        "target path differs from preflight",
        "source artifact differs from reviewed draft",
        "source review path differs from runner review",
        "approval includes import or live parsing",
        "approval includes SQL service-request worker API or browser action",
        "approval is expired or unsigned",
    ]
    evidence_links = [
        source_review_report_path,
        source_review_validation_path,
        source_runner_report_path,
        source_fixture_suite_report_path,
        install_preflight_report_path,
    ]
    operator_instructions = [
        "Default to hold until an operator signs the exact one-file approval.",
        "Do not sign if any path differs from this packet.",
        "Do not bundle parser import, live parsing, SQL, service requests, browser, account, wallet, payment, public, security, or API actions.",
        "If approving, set decision_type to approve_one_parser_file_write_only.",
        "Set approval_scope to one_local_file_write_only.",
        "Require post-write static review and fixture rerun before any import question.",
        "Reject or request rework if the evidence chain is stale or failing.",
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
    summary = "Prepared the report-only one-file parser-write approval request packet with exact fields, paths, boundaries, refusal triggers, and evidence links."
    next_action = "Hold for a signed operator approval matching this packet; do not write or import the parser without it."

    return {
        "local_decision": "agent_company_migration_decision_parser_write_approval_request_ready_for_signed_operator_decision_or_hold",
        "recommended_default": "hold_without_signed_one_file_parser_write_approval",
        "parser_write_approval_request_count": 1,
        "approval_fields": approval_fields,
        "boundary_conditions": boundary_conditions,
        "refusal_triggers": refusal_triggers,
        "evidence_links": evidence_links,
        "operator_instructions": operator_instructions,
        "approval_field_count": len(approval_fields),
        "boundary_condition_count": len(boundary_conditions),
        "refusal_trigger_count": len(refusal_triggers),
        "evidence_link_count": len(evidence_links),
        "operator_instruction_count": len(operator_instructions),
        "approval_request": {
            "target_path": target_path,
            "source_artifact_path": source_artifact_path,
            "source_review_path": source_review_path,
            "required_fields": approval_fields,
            "boundary_conditions": boundary_conditions,
            "refusal_triggers": refusal_triggers,
            "operator_instructions": operator_instructions,
        },
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_parser_write_approval_request_content"]
