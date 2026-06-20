#!/usr/bin/env python3
"""Write a report-only apply-preflight blocker for a signed egress route decision."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from atomic_writes import write_json_atomic


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "egress-route-apply-preflight-blocker-v1.schema.json"
GUARD_REPORT = REPORTS / "egress-route-signed-decision-guard-v1-20260618.json"
GUARD_VALIDATION = REPORTS / "egress-route-signed-decision-guard-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
APPLY_COMMAND_CONTRACT = REPORTS / "egress-route-apply-command-contract-v1-validation-20260618.json"

REPORT_JSON = REPORTS / "egress-route-apply-preflight-blocker-v1-20260618.json"
VALIDATION_JSON = REPORTS / "egress-route-apply-preflight-blocker-v1-validation-20260618.json"
REPORT_MD = REPORTS / "egress-route-apply-preflight-blocker-v1-20260618.md"

TARGET_ROUTE_ID = "browser_read_only_gateway"

ZERO_BOUNDARY = {
    "report_only": True,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "gateway_registrations": 0,
    "gateway_starts": 0,
    "live_egress_events": 0,
    "dependency_installs": 0,
    "worker_registrations": 0,
    "worker_starts": 0,
    "runtime_starts": 0,
    "browser_sessions_started": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "model_api_calls": False,
    "mcp_tool_calls": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "security_testing_actions": False,
    "telemetry_exports": 0,
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


def accepted_fixture_paths(guard: dict[str, Any]) -> set[str]:
    return {
        str(item.get("path", ""))
        for item in guard.get("results", [])
        if item.get("result", {}).get("accepted_for_apply_preflight")
    }


def build_report(real_signed_decision_path: str, apply_command_contract_path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    schema = load_json(SCHEMA_PATH)
    guard = load_json(GUARD_REPORT)
    guard_validation = load_json(GUARD_VALIDATION)
    intake_validation = load_json(INTAKE_VALIDATION)
    gateway_validation = load_json(GATEWAY_DOCKET_VALIDATION)
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    if schema.get("properties", {}).get("apply_preflight_status", {}).get("enum", [None])[0] != "blocked_no_real_signed_decision":
        failures.append("schema_apply_preflight_status_must_start_blocked_no_real_signed_decision")

    checks.append({
        "check_id": "gateway_docket_validation_passes",
        "passed": gateway_validation.get("all_checks_passed") is True and gateway_validation.get("live_egress_allowed") is False,
        "detail": str(GATEWAY_DOCKET_VALIDATION),
    })
    checks.append({
        "check_id": "signed_decision_intake_validation_passes",
        "passed": intake_validation.get("all_checks_passed") is True and intake_validation.get("live_egress_events") == 0,
        "detail": str(INTAKE_VALIDATION),
    })
    checks.append({
        "check_id": "signed_decision_guard_passes_for_target_route",
        "passed": (
            guard_validation.get("all_checks_passed") is True
            and guard_validation.get("target_route_id") == TARGET_ROUTE_ID
            and guard_validation.get("live_egress_events") == 0
            and guard_validation.get("browser_sessions_started") == 0
            and guard_validation.get("worker_starts") == 0
        ),
        "detail": str(GUARD_VALIDATION),
    })
    checks.append({
        "check_id": "real_signed_decision_absent",
        "passed": not real_signed_decision_path,
        "detail": "No real signed operator egress-route decision artifact was supplied.",
    })
    real_present = bool(real_signed_decision_path)
    apply_contract_present = bool(apply_command_contract_path) or APPLY_COMMAND_CONTRACT.exists()
    apply_contract_validation_path = Path(apply_command_contract_path) if apply_command_contract_path else APPLY_COMMAND_CONTRACT
    checks.append({
        "check_id": "apply_command_contract_observed_without_apply",
        "passed": (
            not apply_contract_present
            or (apply_contract_validation_path.exists() and path_inside_root(str(apply_contract_validation_path)))
        ),
        "detail": str(apply_contract_validation_path) if apply_contract_present else "No egress route apply-command contract exists yet.",
    })
    accepted_fixtures = accepted_fixture_paths(guard)
    if real_signed_decision_path and not path_inside_root(real_signed_decision_path):
        failures.append("real_signed_decision_path_must_stay_inside_lab")
    if real_signed_decision_path in accepted_fixtures:
        failures.append("accepted_guard_fixture_is_not_real_signed_decision")
    if real_signed_decision_path and not Path(real_signed_decision_path).exists():
        failures.append("real_signed_decision_path_not_found")
    if apply_command_contract_path and not path_inside_root(apply_command_contract_path):
        failures.append("apply_command_contract_path_must_stay_inside_lab")
    if apply_command_contract_path and not Path(apply_command_contract_path).exists():
        failures.append("apply_command_contract_path_not_found")

    for check in checks:
        if not check["passed"]:
            failures.append(f"check_failed:{check['check_id']}")

    if real_signed_decision_path in accepted_fixtures:
        status = "blocked_fixture_decision_not_real"
        blocker_reason = "accepted_guard_fixture_is_not_real_signed_decision"
    elif not guard_validation.get("all_checks_passed"):
        status = "blocked_guard_not_passing"
        blocker_reason = "egress_route_signed_decision_guard_not_passing"
    elif not real_present:
        status = "blocked_no_real_signed_decision"
        blocker_reason = "no_real_signed_operator_egress_route_decision_artifact"
    elif not apply_contract_present:
        status = "blocked_no_apply_command_contract"
        blocker_reason = "no_egress_route_apply_command_contract"
    else:
        status = "blocked_no_real_signed_decision"
        blocker_reason = "no_real_signed_operator_egress_route_decision_artifact"

    generated = utc_now()
    report = {
        "schema_version": "agent_company.egress_route_apply_preflight_blocker.v1",
        "generated_utc": generated,
        "target_route_id": TARGET_ROUTE_ID,
        "schema_path": str(SCHEMA_PATH),
        "guard_report_path": str(GUARD_REPORT),
        "guard_report_sha256": sha256_path(GUARD_REPORT),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_validation_sha256": sha256_path(GUARD_VALIDATION),
        "intake_validation_path": str(INTAKE_VALIDATION),
        "intake_validation_sha256": sha256_path(INTAKE_VALIDATION),
        "gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "gateway_docket_validation_sha256": sha256_path(GATEWAY_DOCKET_VALIDATION),
        "real_signed_decision_path": real_signed_decision_path,
        "real_signed_decision_present": real_present,
        "apply_command_contract_path": apply_command_contract_path or str(APPLY_COMMAND_CONTRACT),
        "apply_command_contract_present": apply_contract_present,
        "apply_preflight_status": status,
        "blocker_reason": blocker_reason,
        "accepted_guard_decision_count": guard_validation.get("accepted_count"),
        "rejected_guard_decision_count": guard_validation.get("rejected_count"),
        "checks": checks,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "next_action": "Provide a real signed operator egress-route decision artifact, then build an apply-command guard before any browser gateway registration, service request mutation, browser session, worker start, or live egress can be considered.",
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.egress_route_apply_preflight_blocker_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "target_route_id": TARGET_ROUTE_ID,
        "apply_preflight_status": status,
        "blocker_reason": blocker_reason,
        "real_signed_decision_present": real_present,
        "apply_command_contract_present": apply_contract_present,
        "accepted_guard_decision_count": guard_validation.get("accepted_count"),
        "rejected_guard_decision_count": guard_validation.get("rejected_count"),
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Egress Route Apply Preflight Blocker v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Target route: `{TARGET_ROUTE_ID}`",
        f"Guard validation: `{GUARD_VALIDATION}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Apply preflight status: `{validation['apply_preflight_status']}`",
        f"- Blocker reason: `{validation['blocker_reason']}`",
        f"- Real signed decision present: `{validation['real_signed_decision_present']}`",
        f"- Apply command contract present: `{validation['apply_command_contract_present']}`",
        f"- Apply allowed: `{validation['apply_allowed']}`",
        f"- Gateway registration allowed: `{validation['gateway_registration_allowed']}`",
        f"- Gateway start allowed: `{validation['gateway_start_allowed']}`",
        f"- Live egress allowed: `{validation['live_egress_allowed']}`",
        f"- Browser session start allowed: `{validation['browser_session_start_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Checks",
        "",
        "| Check | Passed | Detail |",
        "| --- | --- | --- |",
    ]
    for check in report["checks"]:
        lines.append(f"| `{check['check_id']}` | `{check['passed']}` | {check['detail']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This blocker writes reports only. It writes no apply command, executes no command, registers no gateway, opens no browser, starts no worker, mutates no service request, and performs no live egress.",
            "",
            f"Next action: {report['next_action']}",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--real-signed-decision-path", default="")
    parser.add_argument("--apply-command-contract-path", default="")
    args = parser.parse_args()

    report, validation = build_report(args.real_signed_decision_path, args.apply_command_contract_path)
    write_json_atomic(REPORT_JSON, report)
    write_json_atomic(VALIDATION_JSON, validation)
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
