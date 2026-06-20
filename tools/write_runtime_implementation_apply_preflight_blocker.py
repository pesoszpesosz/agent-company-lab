#!/usr/bin/env python3
"""Write a report-only apply preflight blocker for runtime implementation decisions."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
DURABLE = REPORTS / "durable-orchestration"
SCHEMA_PATH = ARCH / "runtime-implementation-apply-preflight-blocker-v1.schema.json"
GUARD_REPORT = DURABLE / "runtime-implementation-signed-decision-guard-v1-20260617.json"
GUARD_VALIDATION = DURABLE / "runtime-implementation-signed-decision-guard-v1-validation-20260617.json"
BLOCKER_JSON = DURABLE / "runtime-implementation-apply-preflight-blocker-v1-20260617.json"
VALIDATION_JSON = DURABLE / "runtime-implementation-apply-preflight-blocker-v1-validation-20260617.json"
BLOCKER_MD = DURABLE / "runtime-implementation-apply-preflight-blocker-v1-20260617.md"

ZERO_BOUNDARY = {
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "dependency_installs": 0,
    "dependency_imports": 0,
    "runtime_starts": 0,
    "server_starts": 0,
    "database_provisioning": False,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "service_requests_started": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "public_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "security_testing_actions": False,
    "real_money_actions": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_kind(path: str) -> str:
    normalized = path.replace("/", "\\").lower()
    if "\\runtime-implementation-signed-decision-guard-v1-fixtures\\" in normalized:
        return "fixture"
    if normalized.endswith(".json") and "\\reports\\durable-orchestration\\" in normalized:
        return "generated_report"
    if normalized.startswith(str(ROOT).lower()):
        return "local_file"
    return "unknown"


def build_checks(guard: dict[str, Any], guard_validation: dict[str, Any], real_signed_decision_path: str) -> list[dict[str, Any]]:
    accepted_results = [
        item for item in guard.get("results", [])
        if item.get("result", {}).get("accepted_for_later_preflight") is True
    ]
    fixture_apply_blockers = []
    for item in accepted_results:
        kind = source_kind(str(item.get("path", "")))
        fixture_apply_blockers.append(
            {
                "decision_id": item.get("result", {}).get("decision_id"),
                "path": item.get("path"),
                "source_kind": kind,
                "apply_blocked": kind == "fixture",
                "reason": "accepted guard fixture is not a real human operator decision",
            }
        )

    return [
        {
            "check_id": "guard_validation_clean",
            "passed": guard_validation.get("all_checks_passed") is True and guard_validation.get("failure_count") == 0,
            "detail": "Signed-decision guard validation must be clean before apply preflight can even inspect decisions.",
        },
        {
            "check_id": "guard_report_clean",
            "passed": guard.get("all_checks_passed") is True and guard.get("failure_count") == 0,
            "detail": "Signed-decision guard report must have no fixture expectation failures.",
        },
        {
            "check_id": "guard_applied_no_decisions",
            "passed": guard.get("decisions_applied") == 0 and guard_validation.get("decisions_applied") == 0,
            "detail": "The upstream guard must not have applied any decision.",
        },
        {
            "check_id": "accepted_guard_decisions_are_fixtures_only",
            "passed": bool(accepted_results) and all(item["apply_blocked"] for item in fixture_apply_blockers),
            "detail": "Current accepted decisions are fixture decisions only and must not be applied.",
            "fixture_apply_blockers": fixture_apply_blockers,
        },
        {
            "check_id": "real_signed_decision_absent",
            "passed": not real_signed_decision_path,
            "detail": "No real signed human runtime decision artifact was supplied to this report-only preflight.",
        },
        {
            "check_id": "apply_must_remain_blocked",
            "passed": True,
            "detail": "Apply readiness remains false until a real signed decision artifact passes the guard and a later apply preflight.",
        },
    ]


def build_report(real_signed_decision_path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    guard = load_json(GUARD_REPORT)
    guard_validation = load_json(GUARD_VALIDATION)
    checks = build_checks(guard, guard_validation, real_signed_decision_path)
    failures = [
        f"preflight_check_failed:{check['check_id']}"
        for check in checks
        if not check.get("passed")
    ]
    generated = utc_now()
    blocked = not real_signed_decision_path and not failures
    report = {
        "schema_version": "agent_company.runtime_implementation_apply_preflight_blocker.v1",
        "generated_utc": generated,
        "source_guard_report_path": str(GUARD_REPORT),
        "source_guard_report_sha256": sha256_path(GUARD_REPORT),
        "source_guard_validation_path": str(GUARD_VALIDATION),
        "source_guard_validation_sha256": sha256_path(GUARD_VALIDATION),
        "schema_path": str(SCHEMA_PATH),
        "real_signed_decision_path": real_signed_decision_path,
        "apply_preflight_status": "blocked_no_real_signed_decision",
        "fixture_decisions_apply_blocked": blocked,
        "real_decision_required": True,
        "preflight_checks": checks,
        "accepted_guard_decision_count": guard.get("accepted_count"),
        "rejected_guard_decision_count": guard.get("rejected_count"),
        "apply_allowed": False,
        "runtime_implementation_allowed": False,
        "runtime_code_write_allowed": False,
        "runtime_boundary": ZERO_BOUNDARY.copy(),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": "Provide a real signed human runtime decision artifact, then run the signed-decision guard and a separate apply preflight before any runtime code, dependency install, worker/server start, service_request mutation, browser/API/public/account/wallet/payment/security/real-money action, or external side effect.",
    }
    validation = {
        "schema_version": "agent_company.runtime_implementation_apply_preflight_blocker_validation.v1",
        "generated_utc": generated,
        "blocker_report_path": str(BLOCKER_JSON),
        "markdown_path": str(BLOCKER_MD),
        "schema_path": str(SCHEMA_PATH),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "preflight_check_count": len(checks),
        "accepted_guard_decision_count": guard.get("accepted_count"),
        "rejected_guard_decision_count": guard.get("rejected_count"),
        "fixture_decisions_apply_blocked": blocked,
        "real_decision_required": True,
        "real_signed_decision_present": bool(real_signed_decision_path),
        "apply_allowed": False,
        "runtime_implementation_allowed": False,
        "runtime_code_write_allowed": False,
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Runtime Implementation Apply Preflight Blocker v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Guard report: `{GUARD_REPORT}`",
        f"Guard validation: `{GUARD_VALIDATION}`",
        f"Blocker JSON: `{BLOCKER_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Schema: `{SCHEMA_PATH}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Apply preflight status: `{report['apply_preflight_status']}`",
        f"- Real signed decision present: `{validation['real_signed_decision_present']}`",
        f"- Fixture decisions apply blocked: `{validation['fixture_decisions_apply_blocked']}`",
        f"- Apply allowed: `{validation['apply_allowed']}`",
        f"- Runtime implementation allowed: `{validation['runtime_implementation_allowed']}`",
        f"- Runtime code write allowed: `{validation['runtime_code_write_allowed']}`",
        f"- Decisions applied: `{validation['decisions_applied']}`",
        f"- Service requests updated: `{validation['service_requests_updated']}`",
        f"- Worker starts: `{validation['worker_starts']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Checks",
        "",
        "| Check | Passed | Detail |",
        "| --- | --- | --- |",
    ]
    for check in report["preflight_checks"]:
        lines.append(f"| `{check['check_id']}` | `{check['passed']}` | {check['detail']} |")
    fixture_check = next(
        (check for check in report["preflight_checks"] if check["check_id"] == "accepted_guard_decisions_are_fixtures_only"),
        None,
    )
    if fixture_check:
        lines.extend(["", "## Blocked Fixture Decisions", "", "| Decision | Source Kind | Apply Blocked | Reason |", "| --- | --- | --- | --- |"])
        for item in fixture_check.get("fixture_apply_blockers", []):
            lines.append(f"| `{item['decision_id']}` | `{item['source_kind']}` | `{item['apply_blocked']}` | {item['reason']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This report writes no apply command and executes no apply command.",
            "- It applies no approval, writes no approval rows, installs no dependencies, imports no runtime dependency, starts no server/worker/workflow, mutates no service request, opens no browser, calls no API/model, and performs no public/account/wallet/payment/security/real-money action.",
        ]
    )
    BLOCKER_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--real-signed-decision-path", default="")
    args = parser.parse_args()
    report, validation = build_report(args.real_signed_decision_path)
    BLOCKER_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
