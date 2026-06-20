#!/usr/bin/env python3
"""Write a report-only telemetry export apply-preflight blocker."""

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

SCHEMA_PATH = ARCH / "telemetry-export-egress-apply-preflight-blocker-v1.schema.json"
GUARD_REPORT = REPORTS / "telemetry-export-egress-signed-decision-guard-v1-20260618.json"
GUARD_VALIDATION = REPORTS / "telemetry-export-egress-signed-decision-guard-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
EGRESS_LEDGER_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
SERVICE_WORKER_CHAIN_VALIDATION = REPORTS / "service-worker-chain-integrity-validation-latest.json"
TELEMETRY_EXPORT_APPLY_COMMAND_CONTRACT = REPORTS / "telemetry-export-egress-apply-command-contract-v1-validation-20260618.json"

REPORT_JSON = REPORTS / "telemetry-export-egress-apply-preflight-blocker-v1-20260618.json"
VALIDATION_JSON = REPORTS / "telemetry-export-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT_MD = REPORTS / "telemetry-export-egress-apply-preflight-blocker-v1-20260618.md"

TARGET_ROUTE_ID = "telemetry_export_gateway"
TARGET_EGRESS_TYPE = "telemetry_export"
NEXT_ACTION = (
    "Provide a real signed operator telemetry_export_gateway decision artifact, redaction policy, destination scope, "
    "retention policy, sample trace artifact, and telemetry apply-command contract before any external trace export, "
    "private prompt upload, credential export, unredacted log sync, service-request mutation, "
    "worker/browser/model/MCP start or call, live egress, or external side effect can be considered."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "gateway_registrations": 0,
    "gateway_starts": 0,
    "live_egress_events": 0,
    "telemetry_export_allowed": False,
    "telemetry_exports": 0,
    "external_trace_export_allowed": False,
    "external_trace_exports": 0,
    "private_prompt_upload_allowed": False,
    "private_prompts_uploaded": 0,
    "credential_export_allowed": False,
    "credentials_exported": 0,
    "unredacted_log_sync_allowed": False,
    "unredacted_logs_synced": 0,
    "redaction_policy_approved": False,
    "destination_scope_approved": False,
    "retention_policy_approved": False,
    "sample_trace_artifact_approved": False,
    "worker_registrations": 0,
    "worker_start_allowed": False,
    "worker_starts": 0,
    "runtime_starts": 0,
    "dependency_installs": 0,
    "browser_session_start_allowed": False,
    "browser_sessions_started": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "mcp_tool_calls": False,
    "model_api_calls": False,
    "public_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "real_money_actions": False,
    "security_testing_actions": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    try:
        return Path(value).resolve().is_relative_to(ROOT.resolve())
    except Exception:
        return False


def accepted_fixture_paths(guard: dict[str, Any]) -> set[str]:
    return {
        str(item.get("path", ""))
        for item in guard.get("results", [])
        if item.get("result", {}).get("accepted_for_apply_preflight")
    }


def add_absence_check(checks: list[dict[str, Any]], check_id: str, value: str, detail: str) -> bool:
    present = bool(value)
    checks.append({"check_id": check_id, "passed": not present, "detail": detail})
    return present


def build_report(
    real_signed_decision_path: str,
    redaction_policy_path: str,
    destination_scope_path: str,
    retention_policy_path: str,
    sample_trace_artifact_path: str,
    apply_command_contract_path: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    schema = load_json(SCHEMA_PATH)
    guard = load_json(GUARD_REPORT)
    guard_validation = load_json(GUARD_VALIDATION)
    intake_validation = load_json(INTAKE_VALIDATION)
    gateway_validation = load_json(GATEWAY_DOCKET_VALIDATION)
    egress_ledger_validation = load_json(EGRESS_LEDGER_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    service_worker_chain_validation = load_json(SERVICE_WORKER_CHAIN_VALIDATION)
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    if schema.get("properties", {}).get("apply_preflight_status", {}).get("enum", [None])[0] != "blocked_no_real_signed_decision":
        failures.append("schema_apply_preflight_status_must_start_blocked_no_real_signed_decision")
    if schema.get("properties", {}).get("target_route_id", {}).get("const") != TARGET_ROUTE_ID:
        failures.append("schema_target_route_id_must_be_telemetry_export_gateway")
    if schema.get("properties", {}).get("target_egress_type", {}).get("const") != TARGET_EGRESS_TYPE:
        failures.append("schema_target_egress_type_must_be_telemetry_export")
    for prop in [
        "apply_allowed",
        "telemetry_export_allowed",
        "external_trace_export_allowed",
        "private_prompt_upload_allowed",
        "credential_export_allowed",
        "unredacted_log_sync_allowed",
        "worker_start_allowed",
    ]:
        if schema.get("properties", {}).get(prop, {}).get("const") is not False:
            failures.append(f"schema_{prop}_must_be_false")

    checks.append({
        "check_id": "gateway_docket_validation_passes",
        "passed": gateway_validation.get("all_checks_passed") is True and gateway_validation.get("live_egress_allowed") is False,
        "detail": str(GATEWAY_DOCKET_VALIDATION),
    })
    checks.append({
        "check_id": "signed_decision_intake_validation_passes",
        "passed": (
            intake_validation.get("all_checks_passed") is True
            and intake_validation.get("live_egress_events") == 0
            and intake_validation.get("service_requests_assigned") == 0
            and intake_validation.get("service_requests_updated") == 0
        ),
        "detail": str(INTAKE_VALIDATION),
    })
    checks.append({
        "check_id": "telemetry_export_signed_decision_guard_passes_for_target_route",
        "passed": (
            guard_validation.get("all_checks_passed") is True
            and guard_validation.get("target_route_id") == TARGET_ROUTE_ID
            and guard_validation.get("target_egress_type") == TARGET_EGRESS_TYPE
            and guard_validation.get("apply_allowed") is False
            and guard_validation.get("telemetry_export_allowed") is False
            and guard_validation.get("telemetry_exports") == 0
            and guard_validation.get("external_trace_export_allowed") is False
            and guard_validation.get("external_trace_exports") == 0
            and guard_validation.get("private_prompt_upload_allowed") is False
            and guard_validation.get("private_prompts_uploaded") == 0
            and guard_validation.get("credential_export_allowed") is False
            and guard_validation.get("credentials_exported") == 0
            and guard_validation.get("unredacted_log_sync_allowed") is False
            and guard_validation.get("unredacted_logs_synced") == 0
            and guard_validation.get("redaction_policy_approved") is False
            and guard_validation.get("destination_scope_approved") is False
            and guard_validation.get("retention_policy_approved") is False
            and guard_validation.get("sample_trace_artifact_approved") is False
            and guard_validation.get("live_egress_allowed") is False
            and guard_validation.get("external_side_effects") is False
        ),
        "detail": str(GUARD_VALIDATION),
    })
    checks.append({
        "check_id": "agent_egress_event_ledger_validation_passes",
        "passed": (
            egress_ledger_validation.get("all_checks_passed") is True
            and egress_ledger_validation.get("live_egress_allowed") is False
            and egress_ledger_validation.get("model_api_calls") is False
            and egress_ledger_validation.get("mcp_tool_calls") is False
            and egress_ledger_validation.get("external_side_effects") is False
        ),
        "detail": str(EGRESS_LEDGER_VALIDATION),
    })
    checks.append({
        "check_id": "identity_envelope_validation_passes",
        "passed": (
            identity_validation.get("all_checks_passed") is True
            and identity_validation.get("worker_starts") == 0
            and identity_validation.get("worker_start_allowed") is False
            and identity_validation.get("account_actions") is False
            and identity_validation.get("wallet_actions") is False
            and identity_validation.get("payment_actions") is False
            and identity_validation.get("external_side_effects") is False
        ),
        "detail": str(IDENTITY_VALIDATION),
    })
    checks.append({
        "check_id": "service_worker_chain_integrity_passes_without_start",
        "passed": (
            service_worker_chain_validation.get("all_checks_passed") is True
            and service_worker_chain_validation.get("worker_starts") == 0
            and service_worker_chain_validation.get("service_requests_assigned_by_integrity_report") == 0
            and service_worker_chain_validation.get("service_requests_updated_by_integrity_report") == 0
            and service_worker_chain_validation.get("external_side_effects") is False
        ),
        "detail": str(SERVICE_WORKER_CHAIN_VALIDATION),
    })

    real_present = add_absence_check(
        checks,
        "real_signed_decision_absent",
        real_signed_decision_path,
        "No real signed operator telemetry-export egress-route decision artifact was supplied.",
    )
    redaction_policy_present = add_absence_check(checks, "redaction_policy_absent", redaction_policy_path, "No redaction policy was supplied.")
    destination_scope_present = add_absence_check(checks, "destination_scope_absent", destination_scope_path, "No destination scope was supplied.")
    retention_policy_present = add_absence_check(checks, "retention_policy_absent", retention_policy_path, "No retention policy was supplied.")
    sample_trace_artifact_present = add_absence_check(checks, "sample_trace_artifact_absent", sample_trace_artifact_path, "No sample trace artifact was supplied.")

    apply_contract_path = Path(apply_command_contract_path) if apply_command_contract_path else TELEMETRY_EXPORT_APPLY_COMMAND_CONTRACT
    apply_contract_present = bool(apply_command_contract_path) and apply_contract_path.exists()
    checks.append({
        "check_id": "telemetry_export_apply_command_contract_absent",
        "passed": not apply_contract_present,
        "detail": str(apply_contract_path) if apply_contract_present else "No telemetry_export_gateway apply-command contract exists yet.",
    })

    accepted_fixtures = accepted_fixture_paths(guard)
    for label, value in [
        ("real_signed_decision_path", real_signed_decision_path),
        ("redaction_policy_path", redaction_policy_path),
        ("destination_scope_path", destination_scope_path),
        ("retention_policy_path", retention_policy_path),
        ("sample_trace_artifact_path", sample_trace_artifact_path),
        ("apply_command_contract_path", apply_command_contract_path),
    ]:
        if value and not path_inside_root(value):
            failures.append(f"{label}_must_stay_inside_lab")
        if value and not Path(value).exists():
            failures.append(f"{label}_not_found")
    if real_signed_decision_path in accepted_fixtures:
        failures.append("accepted_guard_fixture_is_not_real_signed_decision")

    for check in checks:
        if not check["passed"]:
            failures.append(f"check_failed:{check['check_id']}")

    if real_signed_decision_path in accepted_fixtures:
        status = "blocked_fixture_decision_not_real"
        blocker_reason = "accepted_guard_fixture_is_not_real_signed_decision"
    elif guard_validation.get("all_checks_passed") is not True:
        status = "blocked_guard_not_passing"
        blocker_reason = "telemetry_export_egress_signed_decision_guard_not_passing"
    elif not real_present:
        status = "blocked_no_real_signed_decision"
        blocker_reason = "no_real_signed_operator_telemetry_export_egress_decision_artifact"
    elif not redaction_policy_present:
        status = "blocked_no_redaction_policy"
        blocker_reason = "no_redaction_policy"
    elif not destination_scope_present:
        status = "blocked_no_destination_scope"
        blocker_reason = "no_destination_scope"
    elif not retention_policy_present:
        status = "blocked_no_retention_policy"
        blocker_reason = "no_retention_policy"
    elif not sample_trace_artifact_present:
        status = "blocked_no_sample_trace_artifact"
        blocker_reason = "no_sample_trace_artifact"
    elif not apply_contract_present:
        status = "blocked_no_apply_command_contract"
        blocker_reason = "no_telemetry_export_egress_apply_command_contract"
    else:
        status = "blocked_no_real_signed_decision"
        blocker_reason = "no_real_signed_operator_telemetry_export_egress_decision_artifact"

    generated = utc_now()
    base = {
        "schema_version": "agent_company.telemetry_export_egress_apply_preflight_blocker.v1",
        "generated_utc": generated,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "schema_path": str(SCHEMA_PATH),
        "guard_report_path": str(GUARD_REPORT),
        "guard_report_sha256": sha256_path(GUARD_REPORT),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_validation_sha256": sha256_path(GUARD_VALIDATION),
        "intake_validation_path": str(INTAKE_VALIDATION),
        "intake_validation_sha256": sha256_path(INTAKE_VALIDATION),
        "gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "gateway_docket_validation_sha256": sha256_path(GATEWAY_DOCKET_VALIDATION),
        "egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
        "egress_ledger_validation_sha256": sha256_path(EGRESS_LEDGER_VALIDATION),
        "identity_validation_path": str(IDENTITY_VALIDATION),
        "identity_validation_sha256": sha256_path(IDENTITY_VALIDATION),
        "service_worker_chain_validation_path": str(SERVICE_WORKER_CHAIN_VALIDATION),
        "service_worker_chain_validation_sha256": sha256_path(SERVICE_WORKER_CHAIN_VALIDATION),
        "real_signed_decision_path": real_signed_decision_path,
        "real_signed_decision_present": real_present,
        "redaction_policy_path": redaction_policy_path,
        "redaction_policy_present": redaction_policy_present,
        "destination_scope_path": destination_scope_path,
        "destination_scope_present": destination_scope_present,
        "retention_policy_path": retention_policy_path,
        "retention_policy_present": retention_policy_present,
        "sample_trace_artifact_path": sample_trace_artifact_path,
        "sample_trace_artifact_present": sample_trace_artifact_present,
        "apply_command_contract_path": apply_command_contract_path or str(TELEMETRY_EXPORT_APPLY_COMMAND_CONTRACT),
        "apply_command_contract_present": apply_contract_present,
        "apply_preflight_status": status,
        "blocker_reason": blocker_reason,
        "accepted_guard_decision_count": guard_validation.get("accepted_count"),
        "rejected_guard_decision_count": guard_validation.get("rejected_count"),
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    report = {
        **base,
        "checks": checks,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "next_action": NEXT_ACTION,
    }
    validation = {
        **base,
        "schema_version": "agent_company.telemetry_export_egress_apply_preflight_blocker_validation.v1",
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Telemetry Export Egress Apply Preflight Blocker v1",
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
        f"- Redaction policy present: `{validation['redaction_policy_present']}`",
        f"- Destination scope present: `{validation['destination_scope_present']}`",
        f"- Retention policy present: `{validation['retention_policy_present']}`",
        f"- Sample trace artifact present: `{validation['sample_trace_artifact_present']}`",
        f"- Apply command contract present: `{validation['apply_command_contract_present']}`",
        f"- External trace export allowed: `{validation['external_trace_export_allowed']}`",
        f"- Private prompt upload allowed: `{validation['private_prompt_upload_allowed']}`",
        f"- Credential export allowed: `{validation['credential_export_allowed']}`",
        f"- Unredacted log sync allowed: `{validation['unredacted_log_sync_allowed']}`",
        f"- Service requests updated: `{validation['service_requests_updated']}`",
        f"- Worker starts: `{validation['worker_starts']}`",
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
            "- This blocker writes no apply command and executes no command preview.",
            "- Telemetry export egress remains blocked until a real signed decision, redaction policy, destination scope, retention policy, sample trace artifact, and apply-command contract exist.",
            "- No external trace export, private prompt upload, credential export, unredacted log sync, service-request mutation, worker start, browser start, model/MCP call, live egress, or external side effect is allowed.",
            "",
            f"Next action: {report['next_action']}",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--real-signed-decision-path", default="")
    parser.add_argument("--redaction-policy-path", default="")
    parser.add_argument("--destination-scope-path", default="")
    parser.add_argument("--retention-policy-path", default="")
    parser.add_argument("--sample-trace-artifact-path", default="")
    parser.add_argument("--apply-command-contract-path", default="")
    args = parser.parse_args()

    report, validation = build_report(
        args.real_signed_decision_path,
        args.redaction_policy_path,
        args.destination_scope_path,
        args.retention_policy_path,
        args.sample_trace_artifact_path,
        args.apply_command_contract_path,
    )
    write_json_atomic(REPORT_JSON, report)
    write_json_atomic(VALIDATION_JSON, validation)
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
