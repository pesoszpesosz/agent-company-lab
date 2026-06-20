from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence


def build_agent_company_migration_decision_parser_install_decision_runner_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    runner_task_id: str,
    runner_evidence_id: str,
    source_fixture_task_id: str,
    source_fixture_evidence_id: str,
    fixture_suite_count: int,
    fixtures_evaluated: int,
    accepted_result_count: int,
    rejected_result_count: int,
    passed_fixture_count: int,
    failed_fixture_count: int,
    parser_guard_count: int,
    output_state_count: int,
    fixture_results: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    fixture_result_list = [dict(item) for item in fixture_results]
    local_decision = "agent_company_migration_decision_parser_install_decision_runner_ready_for_report_only_parser_static_review"
    recommended_default = "review_report_only_runner_results_next_without_writing_or_importing_parser"
    summary = "Evaluated the saved report-only install-decision fixture data without importing a parser, writing parser files, parsing live decisions, or applying an install decision."
    next_action = "Review the report-only runner results before any parser file write or import request."
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
        "schema_version": "agent_company.migration_decision_parser_install_decision_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_fixture_task_id": source_fixture_task_id,
        "source_fixture_evidence_id": source_fixture_evidence_id,
        "install_decision_runner_count": 1,
        "fixture_suite_count": fixture_suite_count,
        "fixtures_evaluated": fixtures_evaluated,
        "accepted_result_count": accepted_result_count,
        "rejected_result_count": rejected_result_count,
        "passed_fixture_count": passed_fixture_count,
        "failed_fixture_count": failed_fixture_count,
        "parser_guard_count": parser_guard_count,
        "output_state_count": output_state_count,
        "fixture_results": fixture_result_list,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Install Decision Runner",
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
    for item in fixture_result_list:
        expected = item["expected_state"] if item["expected_valid"] else item["expected_guard"]
        actual = item["actual_state"] if item["actual_valid"] else "reject"
        reasons = ", ".join(item["reasons"]) or "none"
        md_lines.append(f"| `{item['fixture_id']}` | `{expected}` | `{actual}` | `{item['passed']}` | {reasons} |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner evaluates saved synthetic fixture data only. It does not import a parser, write a parser module, parse live decisions, apply an install decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = ["build_agent_company_migration_decision_parser_install_decision_runner_artifacts"]
