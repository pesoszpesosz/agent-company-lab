#!/usr/bin/env python3
"""Write a report-only service-worker signed-decision apply preflight blocker."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "service-worker-signed-decision-apply-preflight-blocker-v1.schema.json"
GUARD_REPORT = REPORTS / "service-worker-signed-decision-guard-v1-20260617.json"
GUARD_VALIDATION = REPORTS / "service-worker-signed-decision-guard-v1-validation-20260617.json"
INTAKE_VALIDATION = REPORTS / "service-worker-signed-decision-intake-contract-v1-validation-20260617.json"
AUTHORITY_VALIDATION = REPORTS / "service-worker-approval-authority-coverage-v1-validation-20260617.json"
REPORT_JSON = REPORTS / "service-worker-signed-decision-apply-preflight-blocker-v1-20260617.json"
VALIDATION_JSON = REPORTS / "service-worker-signed-decision-apply-preflight-blocker-v1-validation-20260617.json"
REPORT_MD = REPORTS / "service-worker-signed-decision-apply-preflight-blocker-v1-20260617.md"

ZERO_BOUNDARY = {
    "report_only": True,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "approval_rows_written": 0,
    "decisions_applied": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "service_requests_mutated": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "runtime_processes_started": 0,
    "mcp_servers_started": 0,
    "mcp_tool_calls": False,
    "api_calls": False,
    "model_api_calls": False,
    "credentials_accessed": False,
    "credentials_created": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "security_testing_actions": False,
    "form_submit_actions": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return value.startswith(str(ROOT)) and ".." not in value


def accepted_guard_fixture_paths(guard: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    for item in guard.get("results", []):
        result = item.get("result", {})
        if result.get("accepted_for_later_apply_preflight"):
            paths.add(str(item.get("path", "")))
    return paths


def build_report(real_signed_decision_path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    schema = load_json(SCHEMA_PATH)
    guard = load_json(GUARD_REPORT)
    guard_validation = load_json(GUARD_VALIDATION)
    intake_validation = load_json(INTAKE_VALIDATION)
    authority_validation = load_json(AUTHORITY_VALIDATION)
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    if schema.get("properties", {}).get("apply_preflight_status", {}).get("enum", [None])[0] != "blocked_no_real_signed_decision":
        failures.append("schema_apply_preflight_status_must_start_blocked_no_real_signed_decision")

    checks.append({
        "check_id": "signed_decision_guard_passes",
        "passed": guard_validation.get("all_checks_passed") is True,
        "detail": str(GUARD_VALIDATION),
    })
    checks.append({
        "check_id": "guard_is_not_apply_authority",
        "passed": (
            guard_validation.get("apply_allowed") is False
            and guard_validation.get("approval_rows_written") == 0
            and guard_validation.get("decisions_applied") == 0
            and guard_validation.get("service_requests_assigned") == 0
            and guard_validation.get("service_requests_updated") == 0
            and guard_validation.get("worker_starts") == 0
        ),
        "detail": "The signed-decision guard may accept fixtures only for a later apply preflight.",
    })
    checks.append({
        "check_id": "intake_contract_passes_without_authority",
        "passed": (
            intake_validation.get("all_checks_passed") is True
            and intake_validation.get("approval_granted_by_contract") is False
            and intake_validation.get("apply_allowed") is False
            and intake_validation.get("decisions_applied") == 0
        ),
        "detail": str(INTAKE_VALIDATION),
    })
    checks.append({
        "check_id": "authority_coverage_passes_without_grant",
        "passed": (
            authority_validation.get("all_checks_passed") is True
            and authority_validation.get("approval_granted_by_coverage") is False
            and authority_validation.get("decision_authority_granted_by_coverage") is False
        ),
        "detail": str(AUTHORITY_VALIDATION),
    })
    checks.append({
        "check_id": "real_signed_decision_absent",
        "passed": not real_signed_decision_path,
        "detail": "No real signed operator service-worker decision artifact was supplied.",
    })

    real_present = bool(real_signed_decision_path)
    accepted_fixture_paths = accepted_guard_fixture_paths(guard)
    if real_signed_decision_path and not path_inside_root(real_signed_decision_path):
        failures.append("real_signed_decision_path_must_stay_inside_lab")
    if real_signed_decision_path in accepted_fixture_paths:
        failures.append("accepted_guard_fixture_is_not_real_signed_decision")
    if real_signed_decision_path and not Path(real_signed_decision_path).exists():
        failures.append("real_signed_decision_path_not_found")

    for check in checks:
        if not check["passed"]:
            failures.append(f"check_failed:{check['check_id']}")

    status = "blocked_no_real_signed_decision"
    blocker_reason = "no_real_signed_operator_decision_artifact"
    if real_signed_decision_path in accepted_fixture_paths:
        status = "blocked_fixture_decision_not_real"
        blocker_reason = "accepted_guard_fixture_is_not_real_signed_decision"
    elif not guard_validation.get("all_checks_passed"):
        status = "blocked_guard_not_passing"
        blocker_reason = "service_worker_signed_decision_guard_not_passing"

    generated = utc_now()
    report = {
        "schema_version": "agent_company.service_worker_signed_decision_apply_preflight_blocker.v1",
        "generated_utc": generated,
        "guard_report_path": str(GUARD_REPORT),
        "guard_report_sha256": sha256_path(GUARD_REPORT),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_validation_sha256": sha256_path(GUARD_VALIDATION),
        "intake_validation_path": str(INTAKE_VALIDATION),
        "intake_validation_sha256": sha256_path(INTAKE_VALIDATION),
        "authority_validation_path": str(AUTHORITY_VALIDATION),
        "authority_validation_sha256": sha256_path(AUTHORITY_VALIDATION),
        "schema_path": str(SCHEMA_PATH),
        "real_signed_decision_path": real_signed_decision_path,
        "real_signed_decision_present": real_present,
        "apply_preflight_status": status,
        "blocker_reason": blocker_reason,
        "accepted_guard_decision_count": guard_validation.get("accepted_count"),
        "service_template_count": guard_validation.get("service_template_count"),
        "current_request_count": guard_validation.get("current_request_count"),
        "checks": checks,
        "apply_allowed": False,
        "decision_apply_allowed": False,
        "assignment_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": "Provide a real signed operator service-worker decision artifact, run it through the signed-decision guard, then build an apply-command preflight before queue mutation, assignment, worker start, browser start, API call, public action, payment, wallet, or security submission.",
    }
    validation = {
        "schema_version": "agent_company.service_worker_signed_decision_apply_preflight_blocker_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "apply_preflight_status": status,
        "blocker_reason": blocker_reason,
        "real_signed_decision_path": real_signed_decision_path,
        "real_signed_decision_present": real_present,
        "accepted_guard_decision_count": guard_validation.get("accepted_count"),
        "service_template_count": guard_validation.get("service_template_count"),
        "current_request_count": guard_validation.get("current_request_count"),
        "apply_allowed": False,
        "decision_apply_allowed": False,
        "assignment_allowed": False,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Service Worker Signed Decision Apply Preflight Blocker v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Guard validation: `{GUARD_VALIDATION}`",
        f"Intake validation: `{INTAKE_VALIDATION}`",
        f"Authority validation: `{AUTHORITY_VALIDATION}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Apply preflight status: `{validation['apply_preflight_status']}`",
        f"- Blocker reason: `{validation['blocker_reason']}`",
        f"- Real signed decision present: `{validation['real_signed_decision_present']}`",
        f"- Apply allowed: `{validation['apply_allowed']}`",
        f"- Decision apply allowed: `{validation['decision_apply_allowed']}`",
        f"- Assignment allowed: `{validation['assignment_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- Service templates: `{validation['service_template_count']}`",
        f"- Current service requests: `{validation['current_request_count']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Checks",
        "",
        "| Check | Passed | Detail |",
        "| --- | --- | --- |",
    ]
    for check in report["checks"]:
        lines.append(f"| `{check['check_id']}` | `{check['passed']}` | {check['detail']} |")
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This blocker writes reports only.",
        "- It writes no apply command and executes no command.",
        "- It assigns or updates no service requests.",
        "- It starts no workers, browsers, MCP servers, runtimes, model calls, API calls, wallet actions, payments, public actions, or security submissions.",
        "- Accepted guard fixtures are not real signed operator decisions.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--real-signed-decision-path", default="")
    args = parser.parse_args()

    report, validation = build_report(args.real_signed_decision_path)
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
