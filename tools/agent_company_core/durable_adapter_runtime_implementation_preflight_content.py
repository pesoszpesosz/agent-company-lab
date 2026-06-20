from __future__ import annotations

from typing import Any


def build_durable_runtime_implementation_preflight_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    upstream_validations: list[dict[str, Any]],
    preflight_checks: list[dict[str, Any]],
    runtime_implementation_allowed: bool,
    runtime_code_write_allowed: bool,
    report_only_scaffolding_allowed: bool,
    explicit_runtime_approval_present: bool,
    external_runtime_implementation_allowed_now: bool,
    local_report_only_implementation_allowed_now: bool,
    negative_validation: dict[str, Any],
    forbidden_imports: list[Any],
    model_request: dict[str, Any] | None,
    model_api_gate_remains_parked: bool,
    model_api_pool_registered: bool,
    failures: list[str],
) -> dict[str, Any]:
    runtime_boundary = {
        "dependency_installs": 0,
        "dependency_imports": 0,
        "temporal_server_started": False,
        "temporal_workflows_started": 0,
        "temporal_activities_scheduled": 0,
        "inngest_service_started": False,
        "inngest_events_emitted": 0,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    passed_preflight_check_count = sum(1 for check in preflight_checks if check["passed"])
    upstream_validation_passed_count = sum(1 for item in upstream_validations if item["passed"])
    next_action = "Create local-only adapter implementation preflight fixtures for permitted report-only scaffolding, still without Temporal/Inngest imports or runtime starts."
    payload = {
        "schema_version": "temporal_inngest_adapter_runtime_implementation_preflight.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Promote runtime interface contracts and negative fixtures into a single implementation preflight before any Temporal/Inngest runtime adapter code is written.",
        "upstream_validations": upstream_validations,
        "preflight_check_count": len(preflight_checks),
        "passed_preflight_check_count": passed_preflight_check_count,
        "preflight_checks": preflight_checks,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
        "explicit_runtime_approval_present": explicit_runtime_approval_present,
        "external_runtime_implementation_allowed_now": external_runtime_implementation_allowed_now,
        "local_report_only_implementation_allowed_now": local_report_only_implementation_allowed_now,
        "negative_fixture_summary": {
            "negative_fixture_count": negative_validation.get("negative_fixture_count"),
            "rejected_fixture_count": negative_validation.get("rejected_fixture_count"),
            "accepted_fixture_count": negative_validation.get("accepted_fixture_count"),
            "all_negative_fixtures_rejected": negative_validation.get("all_negative_fixtures_rejected"),
        },
        "forbidden_runtime_imports": forbidden_imports,
        "model_api_request": model_request,
        "model_api_pool_registered": model_api_pool_registered,
        "runtime_boundary": runtime_boundary,
        "next_action": next_action,
    }
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_runtime_implementation_preflight_validation.v1",
        "generated_utc": generated_utc,
        "preflight_path": json_output_path,
        "preflight_check_count": len(preflight_checks),
        "passed_preflight_check_count": passed_preflight_check_count,
        "upstream_validation_count": len(upstream_validations),
        "upstream_validation_passed_count": upstream_validation_passed_count,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
        "explicit_runtime_approval_present": explicit_runtime_approval_present,
        "external_runtime_implementation_allowed_now": external_runtime_implementation_allowed_now,
        "local_report_only_implementation_allowed_now": local_report_only_implementation_allowed_now,
        "negative_fixture_count": negative_validation.get("negative_fixture_count"),
        "rejected_fixture_count": negative_validation.get("rejected_fixture_count"),
        "accepted_fixture_count": negative_validation.get("accepted_fixture_count"),
        "all_negative_fixtures_rejected": negative_validation.get("all_negative_fixtures_rejected"),
        "forbidden_runtime_import_count": len(forbidden_imports),
        "no_forbidden_runtime_imports_detected": len(forbidden_imports) == 0,
        "model_api_gate_remains_parked": model_api_gate_remains_parked,
        "model_api_pool_registered": model_api_pool_registered,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    lines = [
        "# Temporal/Inngest Runtime Implementation Preflight",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        "Runtime implementation remains blocked. Report-only scaffolding is allowed, but Temporal/Inngest imports, dependency installs, workflow starts, activity schedules, event emissions, worker starts, API calls, and service-request mutations still require an explicit approval gate.",
        "",
        "## Preflight Summary",
        "",
        f"- Preflight checks: `{len(preflight_checks)}`",
        f"- Passed checks: `{passed_preflight_check_count}`",
        f"- Upstream validations: `{len(upstream_validations)}`",
        f"- Passing upstream validations: `{upstream_validation_passed_count}`",
        f"- Runtime implementation allowed: `{runtime_implementation_allowed}`",
        f"- Runtime code write allowed: `{runtime_code_write_allowed}`",
        f"- Report-only scaffolding allowed: `{report_only_scaffolding_allowed}`",
        f"- Explicit runtime approval present: `{explicit_runtime_approval_present}`",
        f"- Negative fixtures rejected: `{negative_validation.get('rejected_fixture_count')}`",
        f"- Negative fixtures accepted: `{negative_validation.get('accepted_fixture_count')}`",
        f"- Forbidden runtime imports detected: `{len(forbidden_imports)}`",
        f"- Model/API gate remains parked: `{model_api_gate_remains_parked}`",
        "",
        "## Checks",
        "",
        "| Check | Passed |",
        "| --- | --- |",
    ]
    for check in preflight_checks:
        lines.append(f"| `{check['check_id']}` | `{check['passed']}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Dependency installs: `0`",
            "- Runtime imports: `0`",
            "- Temporal workflows started: `0`",
            "- Temporal activities scheduled: `0`",
            "- Inngest events emitted: `0`",
            "- Service requests updated: `0`",
            "- Service requests assigned: `0`",
            "- Worker starts: `0`",
            "- API calls: `False`",
            "- External side effects: `False`",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    return {
        "all_checks_passed": all_checks_passed,
        "markdown": "\n".join(lines) + "\n",
        "next_action": next_action,
        "passed_preflight_check_count": passed_preflight_check_count,
        "payload": payload,
        "runtime_boundary": runtime_boundary,
        "upstream_validation_passed_count": upstream_validation_passed_count,
        "validation_payload": validation_payload,
    }


__all__ = ["build_durable_runtime_implementation_preflight_content"]
