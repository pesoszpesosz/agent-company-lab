"""Core contract logic for account/wallet/payment apply-command validation."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from egress_apply_command_contract_shared_core import collect_common_contract_errors

ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "account-wallet-payment-egress-apply-command-contract-v1.schema.json"
APPLY_PREFLIGHT_VALIDATION = (
    REPORTS / "account-wallet-payment-egress-apply-preflight-blocker-v1-validation-20260618.json"
)
GUARD_VALIDATION = REPORTS / "account-wallet-payment-egress-signed-decision-guard-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
EGRESS_LEDGER_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
SERVICE_WORKER_CHAIN_VALIDATION = REPORTS / "service-worker-chain-integrity-validation-latest.json"
FIXTURE_DIR = REPORTS / "account-wallet-payment-egress-apply-command-contract-v1-fixtures"
REPORT_JSON = REPORTS / "account-wallet-payment-egress-apply-command-contract-v1-20260618.json"
VALIDATION_JSON = REPORTS / "account-wallet-payment-egress-apply-command-contract-v1-validation-20260618.json"
REPORT_MD = REPORTS / "account-wallet-payment-egress-apply-command-contract-v1-20260618.md"

TARGET_ROUTE_ID = "account_wallet_payment_gateway"
TARGET_EGRESS_TYPE = "account_wallet_payment"
TRACE_ID = "trace-account-wallet-payment-egress-apply-command-contract-v1-20260618"
NEXT_ACTION = (
    "Build account_wallet_payment_gateway apply-command guard only after a real signed operator decision, "
    "exact account/wallet/payment approval, and immutable command preview exist; until then, keep "
    "account/wallet/payment egress blocked."
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
    "account_creation_allowed": False,
    "accounts_created": 0,
    "terms_acceptance_allowed": False,
    "terms_accepted": 0,
    "wallet_creation_allowed": False,
    "wallets_created": 0,
    "private_key_custody_allowed": False,
    "private_keys_stored": 0,
    "seed_phrases_stored": 0,
    "funds_transfer_allowed": False,
    "funds_transferred": 0,
    "payment_action_allowed": False,
    "payment_actions": False,
    "payment_methods_changed": 0,
    "legal_kyc_tax_action_allowed": False,
    "legal_kyc_tax_actions": False,
    "kyc_submissions": 0,
    "tax_forms_submitted": 0,
    "public_payment_address_allowed": False,
    "payment_addresses_published": 0,
    "real_money_action_allowed": False,
    "real_money_actions": False,
    "account_actions": False,
    "wallet_actions": False,
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
    "security_testing_actions": False,
    "telemetry_exports": 0,
    "external_side_effects": False,
}

REQUIRED_FIELDS = [
    "schema_version",
    "command_id",
    "command_type",
    "target_route_id",
    "target_egress_type",
    "source_apply_preflight_blocker_path",
    "source_guard_validation_path",
    "source_intake_validation_path",
    "source_gateway_docket_validation_path",
    "source_egress_ledger_validation_path",
    "source_identity_validation_path",
    "expected_source_apply_preflight_status",
    "real_signed_decision_path",
    "real_signed_decision_present",
    "exact_account_wallet_payment_approval_path",
    "exact_account_wallet_payment_approval_present",
    "allowed_scope",
    "target_request_ids",
    "immutable_command_preview_sha256",
    "apply_command_allowed",
    "apply_allowed",
    "gateway_registration_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "account_creation_allowed",
    "terms_acceptance_allowed",
    "wallet_creation_allowed",
    "private_key_custody_allowed",
    "funds_transfer_allowed",
    "payment_action_allowed",
    "legal_kyc_tax_action_allowed",
    "public_payment_address_allowed",
    "real_money_action_allowed",
    "service_requests_assigned",
    "service_requests_updated",
    "rollback_plan",
    "runtime_boundary",
]

EXPECTED_SOURCE_PATHS = {
    "source_apply_preflight_blocker_path": str(APPLY_PREFLIGHT_VALIDATION),
    "source_guard_validation_path": str(GUARD_VALIDATION),
    "source_intake_validation_path": str(INTAKE_VALIDATION),
    "source_gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
    "source_egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
    "source_identity_validation_path": str(IDENTITY_VALIDATION),
}
SCHEMA_FALSE_PROPS = [
    "account_creation_allowed",
    "wallet_creation_allowed",
    "payment_action_allowed",
    "real_money_action_allowed",
    "live_egress_allowed",
]
SOURCE_FALSE_FIELDS = [
    "apply_allowed",
    "account_creation_allowed",
    "terms_acceptance_allowed",
    "wallet_creation_allowed",
    "private_key_custody_allowed",
    "funds_transfer_allowed",
    "payment_action_allowed",
    "legal_kyc_tax_action_allowed",
    "public_payment_address_allowed",
    "real_money_action_allowed",
    "account_actions",
    "wallet_actions",
    "payment_actions",
    "real_money_actions",
    "browser_session_start_allowed",
    "mcp_tool_calls",
    "model_api_calls",
    "public_actions",
    "external_side_effects",
]
SOURCE_ZERO_FIELDS = [
    "accounts_created",
    "terms_accepted",
    "wallets_created",
    "private_keys_stored",
    "seed_phrases_stored",
    "funds_transferred",
    "payment_methods_changed",
    "kyc_submissions",
    "tax_forms_submitted",
    "payment_addresses_published",
    "browser_sessions_started",
    "service_requests_assigned",
    "service_requests_updated",
    "worker_starts",
    "runtime_starts",
]
COMMAND_FALSE_FIELDS = [
    "apply_command_allowed",
    "apply_allowed",
    "gateway_registration_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "account_creation_allowed",
    "terms_acceptance_allowed",
    "wallet_creation_allowed",
    "private_key_custody_allowed",
    "funds_transfer_allowed",
    "payment_action_allowed",
    "legal_kyc_tax_action_allowed",
    "public_payment_address_allowed",
    "real_money_action_allowed",
    "browser_session_start_allowed",
    "account_actions",
    "wallet_actions",
    "payment_actions",
    "real_money_actions",
    "mcp_tool_calls",
    "model_api_calls",
    "public_actions",
    "external_side_effects",
]
COMMAND_ZERO_FIELDS = ["service_requests_assigned", "service_requests_updated"]


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


def source_summary() -> dict[str, Any]:
    preflight = load_json(APPLY_PREFLIGHT_VALIDATION)
    guard = load_json(GUARD_VALIDATION)
    intake = load_json(INTAKE_VALIDATION)
    gateway = load_json(GATEWAY_DOCKET_VALIDATION)
    egress = load_json(EGRESS_LEDGER_VALIDATION)
    identity = load_json(IDENTITY_VALIDATION)
    service_chain = load_json(SERVICE_WORKER_CHAIN_VALIDATION)
    keys = [
        "apply_allowed",
        "account_creation_allowed",
        "terms_acceptance_allowed",
        "wallet_creation_allowed",
        "private_key_custody_allowed",
        "funds_transfer_allowed",
        "payment_action_allowed",
        "legal_kyc_tax_action_allowed",
        "public_payment_address_allowed",
        "real_money_action_allowed",
        "account_actions",
        "wallet_actions",
        "payment_actions",
        "real_money_actions",
        "browser_session_start_allowed",
        "mcp_tool_calls",
        "model_api_calls",
        "public_actions",
        "external_side_effects",
    ]
    counts = [
        "accounts_created",
        "terms_accepted",
        "wallets_created",
        "private_keys_stored",
        "seed_phrases_stored",
        "funds_transferred",
        "payment_methods_changed",
        "kyc_submissions",
        "tax_forms_submitted",
        "payment_addresses_published",
        "browser_sessions_started",
        "service_requests_assigned",
        "service_requests_updated",
        "worker_starts",
        "runtime_starts",
    ]
    summary = {
        "apply_preflight_validation_path": str(APPLY_PREFLIGHT_VALIDATION),
        "apply_preflight_all_checks_passed": preflight.get("all_checks_passed"),
        "apply_preflight_status": preflight.get("apply_preflight_status"),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_all_checks_passed": guard.get("all_checks_passed"),
        "guard_target_route_id": guard.get("target_route_id"),
        "guard_target_egress_type": guard.get("target_egress_type"),
        "intake_validation_path": str(INTAKE_VALIDATION),
        "intake_all_checks_passed": intake.get("all_checks_passed"),
        "gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "gateway_all_checks_passed": gateway.get("all_checks_passed"),
        "egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
        "egress_ledger_all_checks_passed": egress.get("all_checks_passed"),
        "identity_validation_path": str(IDENTITY_VALIDATION),
        "identity_all_checks_passed": identity.get("all_checks_passed"),
        "service_worker_chain_validation_path": str(SERVICE_WORKER_CHAIN_VALIDATION),
        "service_worker_chain_all_checks_passed": service_chain.get("all_checks_passed"),
        "service_worker_chain_worker_starts": service_chain.get("worker_starts"),
        "service_worker_chain_external_side_effects": service_chain.get("external_side_effects"),
    }
    summary.update({key: preflight.get(key) for key in keys + counts})
    return summary


def base_command(command_id: str, command_type: str = "report_only_apply_command_contract") -> dict[str, Any]:
    return {
        "schema_version": "agent_company.account_wallet_payment_egress_apply_command_contract.v1",
        "command_id": command_id,
        "command_type": command_type,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "source_apply_preflight_blocker_path": str(APPLY_PREFLIGHT_VALIDATION),
        "source_guard_validation_path": str(GUARD_VALIDATION),
        "source_intake_validation_path": str(INTAKE_VALIDATION),
        "source_gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "source_egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
        "source_identity_validation_path": str(IDENTITY_VALIDATION),
        "source_service_worker_chain_validation_path": str(SERVICE_WORKER_CHAIN_VALIDATION),
        "expected_source_apply_preflight_status": "blocked_no_real_signed_decision",
        "real_signed_decision_path": "",
        "real_signed_decision_present": False,
        "exact_account_wallet_payment_approval_path": "",
        "exact_account_wallet_payment_approval_present": False,
        "allowed_scope": "none" if command_type == "deny_noop" else "report_only_apply_command_contract",
        "target_request_ids": [],
        "immutable_command_preview_sha256": "",
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "account_creation_allowed": False,
        "terms_acceptance_allowed": False,
        "wallet_creation_allowed": False,
        "private_key_custody_allowed": False,
        "funds_transfer_allowed": False,
        "payment_action_allowed": False,
        "legal_kyc_tax_action_allowed": False,
        "public_payment_address_allowed": False,
        "real_money_action_allowed": False,
        "browser_session_start_allowed": False,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "real_money_actions": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "mcp_tool_calls": False,
        "model_api_calls": False,
        "public_actions": False,
        "external_side_effects": False,
        "rollback_plan": (
            "No account/wallet/payment egress apply command exists; discard report-only contract artifacts."
        ),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_noop",
            "expected": "accepted",
            "command": base_command("account-wallet-payment-apply-command-positive-deny", "deny_noop"),
        },
        {
            "name": "positive_report_only_contract",
            "expected": "accepted",
            "command": base_command("account-wallet-payment-apply-command-positive-contract"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        command = base_command(f"account-wallet-payment-apply-command-negative-{name}")
        mutate(command)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "command": command})

    for field, value in [
        ("target_route_id", "public_action_gateway"),
        ("target_egress_type", "public_submission"),
        ("source_apply_preflight_blocker_path", ""),
        ("source_guard_validation_path", str(REPORTS / "stale-account-guard.json")),
        ("source_intake_validation_path", str(REPORTS / "stale-intake.json")),
        ("source_gateway_docket_validation_path", str(REPORTS / "stale-gateway.json")),
        ("source_egress_ledger_validation_path", str(REPORTS / "stale-egress.json")),
        ("source_identity_validation_path", str(REPORTS / "stale-identity.json")),
        ("expected_source_apply_preflight_status", "ready_for_live_apply"),
        ("real_signed_decision_present", True),
        ("exact_account_wallet_payment_approval_present", True),
        ("command_type", "execute_account_wallet_payment_apply"),
        ("allowed_scope", "account_wallet_payment_live_apply"),
        ("immutable_command_preview_sha256", "a" * 64),
        ("apply_command_allowed", True),
        ("apply_allowed", True),
        ("gateway_registration_allowed", True),
        ("gateway_start_allowed", True),
        ("live_egress_allowed", True),
        ("account_creation_allowed", True),
        ("terms_acceptance_allowed", True),
        ("wallet_creation_allowed", True),
        ("private_key_custody_allowed", True),
        ("funds_transfer_allowed", True),
        ("payment_action_allowed", True),
        ("legal_kyc_tax_action_allowed", True),
        ("public_payment_address_allowed", True),
        ("real_money_action_allowed", True),
        ("browser_session_start_allowed", True),
        ("account_actions", True),
        ("wallet_actions", True),
        ("payment_actions", True),
        ("real_money_actions", True),
        ("service_requests_assigned", 1),
        ("service_requests_updated", 1),
        ("mcp_tool_calls", True),
        ("model_api_calls", True),
        ("public_actions", True),
        ("external_side_effects", True),
    ]:
        negative(field, lambda c, f=field, v=value: c.update({f: v}))
    negative(
        "outside_source_preflight",
        lambda c: c.update({"source_apply_preflight_blocker_path": r"C:\Temp\preflight.json"}),
    )
    negative("target_request_id", lambda c: c.update({"target_request_ids": ["req-account-wallet-payment-20260618"]}))
    negative("short_rollback", lambda c: c.update({"rollback_plan": "none"}))
    negative(
        "real_decision_path",
        lambda c: c.update({"real_signed_decision_path": str(REPORTS / "real-account-payment-decision.json")}),
    )
    negative(
        "exact_approval_path",
        lambda c: c.update(
            {"exact_account_wallet_payment_approval_path": str(REPORTS / "exact-account-payment-approval.json")}
        ),
    )
    for key, value in [
        ("apply_commands_written", 1),
        ("apply_commands_executed", 1),
        ("decisions_applied", 1),
        ("approval_rows_written", 1),
        ("gateway_registrations", 1),
        ("gateway_starts", 1),
        ("live_egress_events", 1),
        ("accounts_created", 1),
        ("terms_accepted", 1),
        ("wallets_created", 1),
        ("private_keys_stored", 1),
        ("seed_phrases_stored", 1),
        ("funds_transferred", 1),
        ("payment_methods_changed", 1),
        ("kyc_submissions", 1),
        ("tax_forms_submitted", 1),
        ("payment_addresses_published", 1),
        ("worker_starts", 1),
        ("runtime_starts", 1),
        ("browser_sessions_started", 1),
        ("service_requests_updated", 1),
        ("payment_actions", True),
        ("wallet_actions", True),
        ("real_money_actions", True),
        ("external_side_effects", True),
    ]:
        negative(f"boundary_{key}", lambda c, k=key, v=value: c["runtime_boundary"].update({k: v}))
    return fixtures


def validate_command(command: dict[str, Any], schema: dict[str, Any], sources: dict[str, Any]) -> dict[str, Any]:
    errors = collect_common_contract_errors(
        schema=schema,
        command=command,
        sources=sources,
        required_fields=REQUIRED_FIELDS,
        schema_version="agent_company.account_wallet_payment_egress_apply_command_contract.v1",
        target_route_id=TARGET_ROUTE_ID,
        target_egress_type=TARGET_EGRESS_TYPE,
        schema_false_props=SCHEMA_FALSE_PROPS,
        schema_route_error="schema_target_route_id_must_be_account_wallet_payment_gateway",
        schema_type_error="schema_target_egress_type_must_be_account_wallet_payment",
        route_error="target_route_id_must_match_account_wallet_payment_gateway",
        type_error="target_egress_type_must_be_account_wallet_payment",
        expected_paths=EXPECTED_SOURCE_PATHS,
        path_inside_root=path_inside_root,
        source_false_fields=SOURCE_FALSE_FIELDS,
        source_zero_fields=SOURCE_ZERO_FIELDS,
        command_false_fields=COMMAND_FALSE_FIELDS,
        command_zero_fields=COMMAND_ZERO_FIELDS,
        zero_boundary=ZERO_BOUNDARY,
    )

    if sources["apply_preflight_all_checks_passed"] is not True:
        errors.append("source_apply_preflight_not_passing")
    if sources["apply_preflight_status"] != "blocked_no_real_signed_decision":
        errors.append("source_apply_preflight_status_must_be_blocked_no_real_signed_decision")
    if command.get("expected_source_apply_preflight_status") != "blocked_no_real_signed_decision":
        errors.append("expected_source_apply_preflight_status_must_match")
    if sources["guard_all_checks_passed"] is not True:
        errors.append("source_guard_not_passing")
    if sources["guard_target_route_id"] != TARGET_ROUTE_ID or sources["guard_target_egress_type"] != TARGET_EGRESS_TYPE:
        errors.append("source_guard_target_mismatch")
    for key in [
        "intake_all_checks_passed",
        "gateway_all_checks_passed",
        "egress_ledger_all_checks_passed",
        "identity_all_checks_passed",
        "service_worker_chain_all_checks_passed",
    ]:
        if sources[key] is not True:
            errors.append(f"source_{key}_not_passing")
    if (
        sources["service_worker_chain_worker_starts"] != 0
        or sources["service_worker_chain_external_side_effects"] is not False
    ):
        errors.append("service_worker_chain_must_have_zero_execution")

    if (
        command.get("real_signed_decision_present") is not False
        or command.get("real_signed_decision_path") not in {"", None}
    ):
        errors.append("real_signed_decision_must_be_absent")
    if (
        command.get("exact_account_wallet_payment_approval_present") is not False
        or command.get("exact_account_wallet_payment_approval_path") not in {"", None}
    ):
        errors.append("exact_account_wallet_payment_approval_must_be_absent")
    if command.get("immutable_command_preview_sha256") not in {"", None}:
        errors.append("immutable_command_preview_sha256_must_be_empty_without_approval")
    if len(str(command.get("rollback_plan", "")).strip()) < 20:
        errors.append("rollback_plan_too_short")

    accepted = not errors
    return {
        "command_id": command.get("command_id"),
        "command_type": command.get("command_type"),
        "target_route_id": command.get("target_route_id"),
        "target_egress_type": command.get("target_egress_type"),
        "accepted_for_contract_only": accepted,
        "rejected": not accepted,
        "errors": errors,
        "apply_command_allowed": False,
        "apply_allowed": False,
        "account_creation_allowed": False,
        "wallet_creation_allowed": False,
        "payment_action_allowed": False,
        "real_money_action_allowed": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }

def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    sources = source_summary()
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        command = copy.deepcopy(fixture["command"]) if "command" in fixture else load_json(Path(fixture["path"]))
        result = validate_command(command, schema, sources)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_contract_only"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_contract_only"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.account_wallet_payment_egress_apply_command_contract_report.v1",
        "generated_utc": generated,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "trace_id": TRACE_ID,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_summary": sources,
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "next_action": NEXT_ACTION,
        **copy.deepcopy(ZERO_BOUNDARY),
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.account_wallet_payment_egress_apply_command_contract_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "fixture_expectation_mismatch_count": len(failures),
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation
