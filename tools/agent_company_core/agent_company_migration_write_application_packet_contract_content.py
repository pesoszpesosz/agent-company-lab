from __future__ import annotations

from typing import Any


def build_application_packet_contract_content(
    *,
    application_preflight_report_path: str,
    application_preflight_validation_path: str,
    runner_review_report_path: str,
    intake_contract_report_path: str,
    approval_request_report_path: str,
) -> dict[str, Any]:
    application_fields = [
        "application_packet_id",
        "operator_name",
        "signed_response_artifact_path",
        "source_preflight_path",
        "source_runner_review_path",
        "target_path",
        "source_artifact_path",
        "application_scope",
        "expires_at",
        "signed_utc",
    ]
    eligibility_rules = [
        "source preflight validation is clean",
        "source preflight keeps application_allowed false until packet review",
        "signed response artifact path is present and local",
        "source preflight path matches this contract source",
        "target path matches parser write approval request",
        "application scope equals one_local_parser_file_write_application_review_only",
        "packet excludes parser import live parsing SQL service request and external actions",
        "packet expires after current validation timestamp and has signed_utc",
    ]
    blocked_actions = [
        "apply approval response",
        "write parser module file",
        "import parser module",
        "parse live decisions",
        "execute migration SQL",
        "enable apply command",
        "create database tables",
        "start workers",
        "assign or update service requests",
        "open browser or use accounts",
        "touch wallets payments or real money",
        "post publicly or run security testing",
    ]
    hold_conditions = [
        "application packet is absent",
        "signed response artifact path is missing or non-local",
        "packet target or source artifact differs from the approval request",
        "packet scope is broader than one local parser file write application review",
        "packet bundles import live parsing SQL service-request or external action",
        "source preflight validation is stale or failing",
    ]
    evidence_links = [
        application_preflight_report_path,
        application_preflight_validation_path,
        runner_review_report_path,
        intake_contract_report_path,
        approval_request_report_path,
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
    summary = "Defined the report-only signed application packet contract for parser-write approval responses, keeping application blocked until a separate signed packet exists and validates."
    next_action = "Wait for a signed approval-response application packet; do not write or import the parser from this contract."

    return {
        "parser_write_approval_response_application_packet_contract_count": 1,
        "application_allowed": False,
        "application_fields": application_fields,
        "eligibility_rules": eligibility_rules,
        "blocked_actions": blocked_actions,
        "hold_conditions": hold_conditions,
        "evidence_links": evidence_links,
        "application_field_count": len(application_fields),
        "eligibility_rule_count": len(eligibility_rules),
        "blocked_action_count": len(blocked_actions),
        "hold_condition_count": len(hold_conditions),
        "evidence_link_count": len(evidence_links),
        "local_decision": "agent_company_migration_decision_parser_write_approval_response_application_packet_contract_ready_for_signed_packet_or_hold",
        "recommended_default": "wait_for_signed_approval_response_application_packet_without_applying",
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_application_packet_contract_content"]
