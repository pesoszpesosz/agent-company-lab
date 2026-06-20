from __future__ import annotations

from typing import Any


def build_application_preflight_content(
    *,
    runner_review_report_path: str,
    runner_review_validation_path: str,
    runner_report_path: str,
    approval_request_report_path: str,
) -> dict[str, Any]:
    prerequisite_checks = [
        "source_runner_review_validation_clean",
        "source_runner_review_default_is_hold",
        "runner_review_confirms_all_13_fixtures_passed",
        "approval_response_intake_contract_exists",
        "approval_request_packet_exists",
        "no_signed_response_artifact_supplied",
        "no_parser_write_or_import_allowed_from_preflight",
    ]
    signed_response_requirements = [
        "decision_id",
        "operator_name",
        "response_type",
        "target_path",
        "source_artifact_path",
        "source_request_path",
        "approval_scope",
        "signed_utc",
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
        "signed response artifact is absent",
        "response artifact fails intake contract validation",
        "response path or source artifact differs from approval request",
        "response bundles import live parsing SQL service-request or external action",
        "runner review or fixture evidence is stale",
        "operator approval scope is broader than one local parser file write",
    ]
    evidence_links = [
        runner_review_report_path,
        runner_review_validation_path,
        runner_report_path,
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
    summary = "Prepared a report-only application preflight for parser-write approval responses and kept application blocked because no signed response artifact is present."
    next_action = "Keep hold until a signed approval response application packet exists and validates; do not write or import the parser from this preflight."

    return {
        "parser_write_approval_response_application_preflight_count": 1,
        "signed_response_present": False,
        "application_allowed": False,
        "prerequisite_checks": prerequisite_checks,
        "signed_response_requirements": signed_response_requirements,
        "blocked_actions": blocked_actions,
        "hold_conditions": hold_conditions,
        "evidence_links": evidence_links,
        "prerequisite_check_count": len(prerequisite_checks),
        "signed_response_requirement_count": len(signed_response_requirements),
        "blocked_action_count": len(blocked_actions),
        "hold_condition_count": len(hold_conditions),
        "evidence_link_count": len(evidence_links),
        "local_decision": "agent_company_migration_decision_parser_write_approval_response_application_preflight_blocked_without_signed_response",
        "recommended_default": "keep_hold_until_signed_approval_response_application_packet_exists",
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_application_preflight_content"]
