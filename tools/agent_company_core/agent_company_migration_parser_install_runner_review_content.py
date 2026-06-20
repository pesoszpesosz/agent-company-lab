from __future__ import annotations

from typing import Any


def build_install_decision_runner_review_content(
    *,
    runner_report_path: str,
    runner_validation_path: str,
    fixture_suite_report_path: str,
    install_preflight_report_path: str,
) -> dict[str, Any]:
    runner_result_checks = [
        "runner_validation_clean",
        "all_fixture_results_passed",
        "positive_fixture_accept_count_is_4",
        "negative_fixture_reject_count_is_7",
        "no_parser_file_write_or_import",
        "no_service_request_or_external_side_effect",
    ]
    approval_conditions = [
        "signed operator decision id is present",
        "decision references this runner review artifact",
        "permission is limited to one parser module file write",
        "target path matches the parser install preflight path",
        "post-write static review remains required before import",
        "approval excludes live decision parsing and service-request mutation",
    ]
    hold_conditions = [
        "signed operator approval is absent",
        "approval changes target path or source artifact",
        "approval bundles parser import or live parsing",
        "approval bundles SQL migration or service request mutation",
        "runner validation or fixture results are stale",
        "approval attempts browser account wallet payment public or security side effects",
    ]
    evidence_links = [
        runner_report_path,
        runner_validation_path,
        fixture_suite_report_path,
        install_preflight_report_path,
    ]
    operator_instructions = [
        "Default to hold unless a narrow parser-write approval is explicitly signed.",
        "Do not approve parser import or live decision parsing from this review.",
        "If approving, reference the exact runner review artifact and target path.",
        "Limit approval to one local parser module file write only.",
        "Require post-write static review and fixture rerun before any import request.",
        "Reject any bundled external, service-request, payment, wallet, account, public, or security action.",
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
    summary = "Reviewed the report-only install-decision runner results and prepared an operator-facing hold-or-parser-write boundary without granting approval or changing parser state."
    next_action = "Hold for a signed one-file parser-write approval, or continue with report-only review artifacts; do not write or import the parser without approval."

    return {
        "install_decision_runner_review_count": 1,
        "runner_result_checks": runner_result_checks,
        "approval_conditions": approval_conditions,
        "hold_conditions": hold_conditions,
        "evidence_links": evidence_links,
        "operator_instructions": operator_instructions,
        "runner_result_check_count": len(runner_result_checks),
        "approval_condition_count": len(approval_conditions),
        "hold_condition_count": len(hold_conditions),
        "evidence_link_count": len(evidence_links),
        "operator_instruction_count": len(operator_instructions),
        "local_decision": "agent_company_migration_decision_parser_install_decision_runner_review_ready_for_operator_parser_write_decision_or_hold",
        "recommended_default": "hold_without_signed_operator_parser_write_approval",
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_install_decision_runner_review_content"]
