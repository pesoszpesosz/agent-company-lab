from __future__ import annotations

from typing import Any


def build_approval_response_runner_review_content(
    *,
    runner_report_path: str,
    runner_validation_path: str,
    fixture_suite_report_path: str,
    intake_contract_report_path: str,
    approval_request_report_path: str,
) -> dict[str, Any]:
    runner_result_checks = [
        "runner_validation_clean",
        "all_approval_response_fixture_results_passed",
        "positive_fixture_accept_count_is_4",
        "negative_fixture_reject_count_is_9",
        "no_parser_file_write_import_or_approval_application",
        "no_service_request_or_external_side_effect",
    ]
    approval_conditions = [
        "signed operator approval response id is present",
        "response references the exact parser-write approval request packet",
        "response type is one of the accepted approval response contract values",
        "target path matches the parser install preflight path",
        "permission remains limited to one local parser file write only",
        "response excludes parser import live parsing SQL service-request mutation and external actions",
    ]
    hold_conditions = [
        "signed approval response is absent",
        "response changes target path source artifact or approval request path",
        "response bundles parser import or live decision parsing",
        "response bundles SQL service-request worker API or browser action",
        "runner validation or fixture results are stale",
        "response attempts account wallet payment public security or real-money side effects",
    ]
    evidence_links = [
        runner_report_path,
        runner_validation_path,
        fixture_suite_report_path,
        intake_contract_report_path,
        approval_request_report_path,
    ]
    operator_instructions = [
        "Default to hold unless an operator supplies a signed approval response matching the intake contract.",
        "Do not treat this review as approval to write the parser.",
        "Do not apply an approval response that changes any path from the request packet.",
        "Do not bundle parser import, live parsing, SQL, service requests, browser, account, wallet, payment, public, security, or API actions.",
        "If the response asks for rework or rejection, keep the system in report-only hold.",
        "If the response approves one file write, require a separate narrow application step before touching the parser file.",
        "Require post-application static review and fixture rerun before any import question.",
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
    summary = "Reviewed the report-only parser-write approval response runner results and prepared a hold-first operator boundary without applying any approval response."
    next_action = "Hold unless a signed approval response matches the intake contract and a separate narrow application step is prepared; do not write or import the parser from this review."

    return {
        "parser_write_approval_response_runner_review_count": 1,
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
        "local_decision": "agent_company_migration_decision_parser_write_approval_response_runner_review_ready_for_signed_response_or_hold",
        "recommended_default": "hold_without_signed_parser_write_approval_response_application",
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_approval_response_runner_review_content"]
