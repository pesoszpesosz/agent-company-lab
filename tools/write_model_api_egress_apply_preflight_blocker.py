#!/usr/bin/env python3
"""Write a report-only model/API apply-preflight blocker for signed egress decisions."""

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

SCHEMA_PATH = ARCH / "model-api-egress-apply-preflight-blocker-v1.schema.json"
GUARD_REPORT = REPORTS / "model-api-egress-signed-decision-guard-v1-20260618.json"
GUARD_VALIDATION = REPORTS / "model-api-egress-signed-decision-guard-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
EGRESS_LEDGER_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
MODEL_API_APPLY_COMMAND_CONTRACT = REPORTS / "model-api-egress-apply-command-contract-v1-validation-20260618.json"

REPORT_JSON = REPORTS / "model-api-egress-apply-preflight-blocker-v1-20260618.json"
VALIDATION_JSON = REPORTS / "model-api-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT_MD = REPORTS / "model-api-egress-apply-preflight-blocker-v1-20260618.md"

TARGET_ROUTE_ID = "model_api_gateway"
TARGET_EGRESS_TYPE = "model_api"
NEXT_ACTION = (
    "Provide a real signed operator model/API egress-route decision artifact, then build a model/API "
    "apply-command contract before any provider key use, model/API call, data upload, worker start, "
    "service-request mutation, or live egress can be considered."
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
    "provider_key_use_allowed": False,
    "provider_keys_used": False,
    "model_api_call_allowed": False,
    "model_api_calls": False,
    "training_data_upload_allowed": False,
    "training_data_uploaded": False,
    "max_cost_usd": 0,
    "dependency_installs": 0,
    "worker_registrations": 0,
    "worker_start_allowed": False,
    "worker_starts": 0,
    "runtime_starts": 0,
    "browser_sessions_started": False,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
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


def build_report(real_signed_decision_path: str, apply_command_contract_path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    schema = load_json(SCHEMA_PATH)
    guard = load_json(GUARD_REPORT)
    guard_validation = load_json(GUARD_VALIDATION)
    intake_validation = load_json(INTAKE_VALIDATION)
    gateway_validation = load_json(GATEWAY_DOCKET_VALIDATION)
    egress_ledger_validation = load_json(EGRESS_LEDGER_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    if schema.get("properties", {}).get("apply_preflight_status", {}).get("enum", [None])[0] != "blocked_no_real_signed_decision":
        failures.append("schema_apply_preflight_status_must_start_blocked_no_real_signed_decision")
    if schema.get("properties", {}).get("target_route_id", {}).get("const") != TARGET_ROUTE_ID:
        failures.append("schema_target_route_id_must_be_model_api_gateway")
    if schema.get("properties", {}).get("target_egress_type", {}).get("const") != TARGET_EGRESS_TYPE:
        failures.append("schema_target_egress_type_must_be_model_api")
    if schema.get("properties", {}).get("apply_allowed", {}).get("const") is not False:
        failures.append("schema_apply_allowed_must_be_false")
    if schema.get("properties", {}).get("model_api_call_allowed", {}).get("const") is not False:
        failures.append("schema_model_api_call_allowed_must_be_false")

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
        "check_id": "model_api_signed_decision_guard_passes_for_target_route",
        "passed": (
            guard_validation.get("all_checks_passed") is True
            and guard_validation.get("target_route_id") == TARGET_ROUTE_ID
            and guard_validation.get("target_egress_type") == TARGET_EGRESS_TYPE
            and guard_validation.get("apply_allowed") is False
            and guard_validation.get("provider_key_use_allowed") is False
            and guard_validation.get("provider_keys_used") is False
            and guard_validation.get("model_api_call_allowed") is False
            and guard_validation.get("model_api_calls") is False
            and guard_validation.get("training_data_upload_allowed") is False
            and guard_validation.get("training_data_uploaded") is False
            and guard_validation.get("max_cost_usd") == 0
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
            and identity_validation.get("credentials_created") is False
            and identity_validation.get("external_side_effects") is False
        ),
        "detail": str(IDENTITY_VALIDATION),
    })
    checks.append({
        "check_id": "real_signed_decision_absent",
        "passed": not real_signed_decision_path,
        "detail": "No real signed operator model/API egress-route decision artifact was supplied.",
    })

    real_present = bool(real_signed_decision_path)
    apply_contract_path = Path(apply_command_contract_path) if apply_command_contract_path else MODEL_API_APPLY_COMMAND_CONTRACT
    apply_contract_present = bool(apply_command_contract_path) and apply_contract_path.exists()
    checks.append({
        "check_id": "model_api_apply_command_contract_absent",
        "passed": not apply_contract_present,
        "detail": str(apply_contract_path) if apply_contract_present else "No model/API egress apply-command contract exists yet.",
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
    elif guard_validation.get("all_checks_passed") is not True:
        status = "blocked_guard_not_passing"
        blocker_reason = "model_api_egress_signed_decision_guard_not_passing"
    elif not real_present:
        status = "blocked_no_real_signed_decision"
        blocker_reason = "no_real_signed_operator_model_api_egress_decision_artifact"
    elif not apply_contract_present:
        status = "blocked_no_apply_command_contract"
        blocker_reason = "no_model_api_egress_apply_command_contract"
    else:
        status = "blocked_no_real_signed_decision"
        blocker_reason = "no_real_signed_operator_model_api_egress_decision_artifact"

    generated = utc_now()
    report = {
        "schema_version": "agent_company.model_api_egress_apply_preflight_blocker.v1",
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
        "real_signed_decision_path": real_signed_decision_path,
        "real_signed_decision_present": real_present,
        "apply_command_contract_path": apply_command_contract_path or str(MODEL_API_APPLY_COMMAND_CONTRACT),
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
        "provider_key_use_allowed": False,
        "provider_keys_used": False,
        "model_api_call_allowed": False,
        "model_api_calls": False,
        "training_data_upload_allowed": False,
        "training_data_uploaded": False,
        "max_cost_usd": 0,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "next_action": NEXT_ACTION,
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.model_api_egress_apply_preflight_blocker_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
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
        "provider_key_use_allowed": False,
        "provider_keys_used": False,
        "model_api_call_allowed": False,
        "model_api_calls": False,
        "training_data_upload_allowed": False,
        "training_data_uploaded": False,
        "max_cost_usd": 0,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Model API Egress Apply Preflight Blocker v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Target route: `{TARGET_ROUTE_ID}`",
        f"Guard validation: `{GUARD_VALIDATION}`",
        f"Egress ledger validation: `{EGRESS_LEDGER_VALIDATION}`",
        f"Identity validation: `{IDENTITY_VALIDATION}`",
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
        f"- Provider key use allowed: `{validation['provider_key_use_allowed']}`",
        f"- Provider keys used: `{validation['provider_keys_used']}`",
        f"- Model/API call allowed: `{validation['model_api_call_allowed']}`",
        f"- Model/API calls: `{validation['model_api_calls']}`",
        f"- Training data upload allowed: `{validation['training_data_upload_allowed']}`",
        f"- Training data uploaded: `{validation['training_data_uploaded']}`",
        f"- Max cost USD: `{validation['max_cost_usd']}`",
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
            "This blocker writes reports only. It writes no apply command, executes no command, uses no provider key, calls no model/API, uploads no data, spends no money, starts no worker, mutates no service request, and performs no live egress.",
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
