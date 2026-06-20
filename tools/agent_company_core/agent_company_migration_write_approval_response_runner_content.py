from __future__ import annotations

from typing import Any


def build_approval_response_runner_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    lane_id: str,
    runner_task_id: str,
    runner_evidence_id: str,
    source_fixture_task_id: str,
    source_fixture_evidence_id: str,
    fixture_results: list[dict[str, Any]],
    response_guard_count: int,
    output_state_count: int,
) -> dict[str, Any]:
    local_decision = "agent_company_migration_decision_parser_write_approval_response_runner_ready_for_report_only_review"
    recommended_default = "review_report_only_parser_write_approval_response_runner_results_next_without_applying_approval"
    parser_write_approval_response_runner_count = 1
    fixture_suite_count = len(fixture_results)
    fixtures_evaluated = len(fixture_results)
    accepted_result_count = sum(1 for item in fixture_results if item["actual_valid"])
    rejected_result_count = fixtures_evaluated - accepted_result_count
    passed_fixture_count = sum(1 for item in fixture_results if item["passed"])
    failed_fixture_count = fixtures_evaluated - passed_fixture_count
    summary = "Evaluated the saved report-only parser-write approval response fixture data without applying approval, writing parser files, importing a parser, parsing live decisions, or mutating service requests."
    next_action = "Review the report-only parser-write approval response runner results before any parser write approval application request."
    runtime_boundary = {
        "report_only_fixtures_evaluated": True,
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
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_fixture_task_id": source_fixture_task_id,
        "source_fixture_evidence_id": source_fixture_evidence_id,
        "parser_write_approval_response_runner_count": parser_write_approval_response_runner_count,
        "fixture_suite_count": fixture_suite_count,
        "fixtures_evaluated": fixtures_evaluated,
        "accepted_result_count": accepted_result_count,
        "rejected_result_count": rejected_result_count,
        "passed_fixture_count": passed_fixture_count,
        "failed_fixture_count": failed_fixture_count,
        "response_guard_count": response_guard_count,
        "output_state_count": output_state_count,
        "fixture_results": fixture_results,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# Agent Company Migration Decision Parser Write Approval Response Runner",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        summary,
        "",
        "## Runner Results",
        "",
        f"- Fixtures evaluated: {fixtures_evaluated}",
        f"- Accepted results: {accepted_result_count}",
        f"- Rejected results: {rejected_result_count}",
        f"- Passed fixtures: {passed_fixture_count}",
        f"- Failed fixtures: {failed_fixture_count}",
        "",
        "| Fixture | Expected | Actual | Passed | Reasons |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in fixture_results:
        expected = item["expected_state"] if item["expected_valid"] else item["expected_guard"]
        actual = item["actual_state"] if item["actual_valid"] else "reject"
        md_lines.append(f"| `{item['fixture_id']}` | `{expected}` | `{actual}` | `{item['passed']}` | {', '.join(item['reasons']) or 'none'} |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner evaluates saved synthetic approval response fixture data only. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {
        "accepted_result_count": accepted_result_count,
        "failed_fixture_count": failed_fixture_count,
        "fixture_suite_count": fixture_suite_count,
        "fixtures_evaluated": fixtures_evaluated,
        "local_decision": local_decision,
        "markdown": "\n".join(md_lines) + "\n",
        "next_action": next_action,
        "parser_write_approval_response_runner_count": parser_write_approval_response_runner_count,
        "passed_fixture_count": passed_fixture_count,
        "payload": payload,
        "recommended_default": recommended_default,
        "rejected_result_count": rejected_result_count,
        "runtime_boundary": runtime_boundary,
        "summary": summary,
    }


__all__ = ["build_approval_response_runner_content"]
