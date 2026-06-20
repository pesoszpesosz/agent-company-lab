#!/usr/bin/env python3
"""Write a report-only browser read-only apply preflight blocker."""

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
SCHEMA_PATH = ARCH / "browser-read-only-apply-preflight-blocker-v1.schema.json"
GUARD_REPORT = REPORTS / "browser-read-only-signed-approval-guard-v1-20260617.json"
GUARD_VALIDATION = REPORTS / "browser-read-only-signed-approval-guard-v1-validation-20260617.json"
ASSIGNMENT_PREFLIGHT_VALIDATION = REPORTS / "browser-read-only-assignment-preflight-v1-validation-20260617.json"
REPORT_JSON = REPORTS / "browser-read-only-apply-preflight-blocker-v1-20260617.json"
VALIDATION_JSON = REPORTS / "browser-read-only-apply-preflight-blocker-v1-validation-20260617.json"
REPORT_MD = REPORTS / "browser-read-only-apply-preflight-blocker-v1-20260617.md"

ZERO_BOUNDARY = {
    "report_only": True,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "service_requests_assigned": 0,
    "service_requests_mutated": 0,
    "browser_sessions_started": 0,
    "worker_starts": 0,
    "login_actions": False,
    "form_submit_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "security_testing_actions": False,
    "file_transfer_actions": False,
    "mcp_tool_calls": False,
    "model_api_calls": False,
    "credentials_accessed": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return str(value).startswith(str(ROOT)) and ".." not in str(value)


def guard_fixture_paths(guard: dict[str, Any]) -> set[str]:
    return {str(item.get("path", "")) for item in guard.get("results", []) if item.get("result", {}).get("accepted_for_later_preflight")}


def build_report(real_signed_decision_path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    guard = load_json(GUARD_REPORT)
    guard_validation = load_json(GUARD_VALIDATION)
    assignment_preflight = load_json(ASSIGNMENT_PREFLIGHT_VALIDATION)
    schema = load_json(SCHEMA_PATH)
    failures: list[str] = []
    checks: list[dict[str, Any]] = []
    guard_adapter_contract_gate = guard_validation.get("adapter_contract_gate")
    guard_adapter_contract_validation_path = guard_validation.get("adapter_contract_validation_path")
    guard_summary = {
        "guard_validation_path": str(GUARD_VALIDATION),
        "all_checks_passed": guard_validation.get("all_checks_passed"),
        "accepted_count": guard_validation.get("accepted_count"),
        "rejected_count": guard_validation.get("rejected_count"),
        "adapter_contract_gate": guard_adapter_contract_gate,
        "adapter_contract_validation_path": guard_adapter_contract_validation_path,
        "assignment_allowed": guard_validation.get("assignment_allowed"),
        "browser_session_start_allowed": guard_validation.get("browser_session_start_allowed"),
        "worker_start_allowed": guard_validation.get("worker_start_allowed"),
        "browser_sessions_started": guard_validation.get("browser_sessions_started"),
        "worker_starts": guard_validation.get("worker_starts"),
        "external_side_effects": guard_validation.get("external_side_effects"),
    }

    if schema.get("properties", {}).get("apply_preflight_status", {}).get("enum", [None])[0] != "blocked_no_real_signed_decision":
        failures.append("schema_apply_preflight_status_must_start_blocked_no_real_signed_decision")

    checks.append({
        "check_id": "signed_approval_guard_passes",
        "passed": guard_validation.get("all_checks_passed") is True,
        "detail": str(GUARD_VALIDATION),
    })
    checks.append({
        "check_id": "guard_does_not_allow_assignment_or_browser_start",
        "passed": (
            guard_validation.get("assignment_allowed") is False
            and guard_validation.get("browser_session_start_allowed") is False
            and guard_validation.get("worker_start_allowed") is False
        ),
        "detail": "Guard accepts authority for later preflight only.",
    })
    checks.append({
        "check_id": "signed_guard_adapter_contract_gate_present_valid_start_blocked",
        "passed": (
            guard_adapter_contract_gate == "present_valid_start_blocked"
            and bool(guard_adapter_contract_validation_path)
            and path_inside_root(str(guard_adapter_contract_validation_path))
            and Path(str(guard_adapter_contract_validation_path)).exists()
        ),
        "detail": str(guard_adapter_contract_validation_path or ""),
    })
    checks.append({
        "check_id": "assignment_preflight_still_blocks_without_signed_approval",
        "passed": (
            assignment_preflight.get("all_checks_passed") is True
            and assignment_preflight.get("preflight_verdict") == "candidates_valid_assignment_blocked_no_signed_approval"
            and assignment_preflight.get("assignment_allowed_count") == 0
        ),
        "detail": str(ASSIGNMENT_PREFLIGHT_VALIDATION),
    })
    checks.append({
        "check_id": "real_signed_decision_absent",
        "passed": not real_signed_decision_path,
        "detail": "No real signed operator browser-read-only decision artifact was supplied.",
    })

    real_present = bool(real_signed_decision_path)
    accepted_fixture_paths = guard_fixture_paths(guard)
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
    elif guard_adapter_contract_gate != "present_valid_start_blocked":
        status = "blocked_guard_adapter_contract_not_passing"
        blocker_reason = "browser_read_only_signed_approval_guard_adapter_contract_not_passing"
    elif not guard_validation.get("all_checks_passed"):
        status = "blocked_guard_not_passing"
        blocker_reason = "browser_read_only_signed_approval_guard_not_passing"

    generated = utc_now()
    report = {
        "schema_version": "agent_company.browser_read_only_apply_preflight_blocker.v1",
        "generated_utc": generated,
        "guard_report_path": str(GUARD_REPORT),
        "guard_report_sha256": sha256_path(GUARD_REPORT),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_validation_sha256": sha256_path(GUARD_VALIDATION),
        "guard_summary": guard_summary,
        "guard_adapter_contract_gate": guard_adapter_contract_gate,
        "guard_adapter_contract_validation_path": guard_adapter_contract_validation_path,
        "assignment_preflight_validation_path": str(ASSIGNMENT_PREFLIGHT_VALIDATION),
        "assignment_preflight_validation_sha256": sha256_path(ASSIGNMENT_PREFLIGHT_VALIDATION),
        "schema_path": str(SCHEMA_PATH),
        "real_signed_decision_path": real_signed_decision_path,
        "real_signed_decision_present": real_present,
        "apply_preflight_status": status,
        "blocker_reason": blocker_reason,
        "accepted_guard_decision_count": guard_validation.get("accepted_count"),
        "rejected_guard_decision_count": guard_validation.get("rejected_count"),
        "candidate_request_count": assignment_preflight.get("candidate_request_count"),
        "checks": checks,
        "apply_allowed": False,
        "assignment_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": "Provide a real signed operator browser-read-only decision artifact, run it through the signed approval guard, then build an apply-command preflight before queue mutation or browser start.",
    }
    validation = {
        "schema_version": "agent_company.browser_read_only_apply_preflight_blocker_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "apply_preflight_status": status,
        "real_signed_decision_path": real_signed_decision_path,
        "real_signed_decision_present": real_present,
        "accepted_guard_decision_count": guard_validation.get("accepted_count"),
        "rejected_guard_decision_count": guard_validation.get("rejected_count"),
        "guard_adapter_contract_gate": guard_adapter_contract_gate,
        "guard_adapter_contract_validation_path": guard_adapter_contract_validation_path,
        "candidate_request_count": assignment_preflight.get("candidate_request_count"),
        "apply_allowed": False,
        "assignment_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Browser Read-Only Apply Preflight Blocker v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Guard validation: `{GUARD_VALIDATION}`",
        f"Assignment preflight validation: `{ASSIGNMENT_PREFLIGHT_VALIDATION}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Apply preflight status: `{validation['apply_preflight_status']}`",
        f"- Blocker reason: `{report['blocker_reason']}`",
        f"- Real signed decision present: `{validation['real_signed_decision_present']}`",
        f"- Guard adapter contract gate: `{validation['guard_adapter_contract_gate']}`",
        f"- Guard adapter contract validation: `{validation['guard_adapter_contract_validation_path']}`",
        f"- Apply allowed: `{validation['apply_allowed']}`",
        f"- Assignment allowed: `{validation['assignment_allowed']}`",
        f"- Browser session start allowed: `{validation['browser_session_start_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- Candidate requests: `{validation['candidate_request_count']}`",
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
        "- It assigns no service requests and opens no browser sessions.",
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
