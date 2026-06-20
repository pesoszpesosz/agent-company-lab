"""Core guard logic for account/wallet/payment signed egress decisions."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from egress_signed_decision_guard_shared_core import collect_common_signed_decision_errors

ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "account-wallet-payment-egress-signed-decision-guard-v1.schema.json"
INTAKE_REPORT = REPORTS / "egress-route-signed-decision-intake-contract-v1-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET = REPORTS / "unified-agent-egress-gateway-docket-v1-20260618.json"
EGRESS_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "account-wallet-payment-egress-signed-decision-guard-v1-fixtures"
REPORT_JSON = REPORTS / "account-wallet-payment-egress-signed-decision-guard-v1-20260618.json"
VALIDATION_JSON = REPORTS / "account-wallet-payment-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT_MD = REPORTS / "account-wallet-payment-egress-signed-decision-guard-v1-20260618.md"

TARGET_ROUTE_ID = "account_wallet_payment_gateway"
TARGET_EGRESS_TYPE = "account_wallet_payment"
EVALUATION_UTC = "2026-06-18T05:00:00Z"
ATTESTATION = (
    "I approve account/wallet/payment egress route preflight review only and understand this does not "
    "accept terms, create an account, create or control a wallet, store a private key, send funds, publish "
    "a payment address, perform KYC/tax/legal/payment action, mutate service requests, or perform live egress."
)
NEXT_ACTION = (
    "Build account_wallet_payment_gateway apply preflight blocker before any account creation, terms acceptance, "
    "wallet creation, private-key custody, fund transfer, payment method change, KYC/tax/legal action, public "
    "payment-address publication, service-request mutation, or live egress."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "decision_authority_granted_by_contract": False,
    "approval_granted_by_contract": False,
    "apply_allowed": False,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "gateway_registration_allowed": False,
    "gateway_start_allowed": False,
    "live_egress_allowed": False,
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
    "decision_id",
    "decision",
    "route_id",
    "egress_type",
    "source_gateway_docket_path",
    "source_gateway_docket_sha256",
    "operator_id",
    "operator_attestation",
    "signed_utc",
    "expires_utc",
    "allowed_scope",
    "allowed_gate_ids",
    "allowed_evidence_artifact_paths",
    "approval_is_not_apply",
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
    "worker_start_allowed",
    "service_requests_assigned",
    "service_requests_updated",
    "rollback_plan",
    "runtime_boundary",
]

SCHEMA_FALSE_PROPS = [
    "account_creation_allowed",
    "wallet_creation_allowed",
    "private_key_custody_allowed",
    "funds_transfer_allowed",
    "payment_action_allowed",
    "legal_kyc_tax_action_allowed",
    "public_payment_address_allowed",
    "real_money_action_allowed",
    "live_egress_allowed",
]
DECISION_FALSE_FIELDS = [
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
    "worker_registration_allowed",
    "worker_start_allowed",
    "runtime_start_allowed",
    "browser_session_start_allowed",
    "mcp_tool_calls",
    "model_api_calls",
    "public_actions",
    "account_actions",
    "wallet_actions",
    "payment_actions",
    "real_money_actions",
    "external_side_effects",
]
DECISION_ZERO_FIELDS = [
    "browser_sessions_started",
    "service_requests_assigned",
    "service_requests_updated",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    try:
        return Path(value).resolve().is_relative_to(ROOT.resolve())
    except Exception:
        return False


def route_summary() -> dict[str, Any]:
    gateway = load_json(GATEWAY_DOCKET)
    route = next(row for row in gateway["gateway_routes"] if row["route_id"] == TARGET_ROUTE_ID)
    intake = load_json(INTAKE_REPORT)
    template = next(row for row in intake["decision_templates"] if row["route_id"] == TARGET_ROUTE_ID)
    return {"route": route, "template": template}


def base_decision(decision_id: str, decision: str = "approve_route_preflight_only") -> dict[str, Any]:
    route = route_summary()["route"]
    deny = decision == "deny"
    return {
        "schema_version": "agent_company.egress_route_signed_decision_intake_contract.v1",
        "decision_id": decision_id,
        "decision": decision,
        "route_id": TARGET_ROUTE_ID,
        "egress_type": TARGET_EGRESS_TYPE,
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "source_gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "operator_id": "human-operator",
        "operator_attestation": "deny-all-no-egress" if deny else ATTESTATION,
        "signed_utc": "2026-06-18T04:50:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "allowed_scope": "none" if deny else f"egress_route_preflight_only:{TARGET_ROUTE_ID}",
        "allowed_gate_ids": [] if deny else copy.deepcopy(route["required_gates"]),
        "allowed_evidence_artifact_paths": [],
        "approval_is_not_apply": True,
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
        "worker_registration_allowed": False,
        "worker_start_allowed": False,
        "runtime_start_allowed": False,
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
        "external_side_effects": False,
        "rollback_plan": (
            "No egress route decision is applied."
            if deny
            else "Discard generated report-only account/wallet/payment egress route decision artifacts; no terms, "
            "account, wallet, private key, seed phrase, fund transfer, payment method, KYC/tax/legal, public payment "
            "address, service request, MCP/model, browser, public, real-money, or external action was started."
        ),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_account_wallet_payment_route",
            "expected": "accepted",
            "decision": base_decision("account-wallet-payment-guard-positive-deny", "deny"),
        },
        {
            "name": "positive_account_wallet_payment_preflight_only",
            "expected": "accepted",
            "decision": base_decision("account-wallet-payment-guard-positive-preflight-only"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        decision = base_decision(f"account-wallet-payment-guard-negative-{name}")
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    negative("missing_operator", lambda d: d.update({"operator_id": ""}))
    negative("missing_attestation", lambda d: d.update({"operator_attestation": ""}))
    negative("wrong_attestation", lambda d: d.update({"operator_attestation": "I approve wallet/payment action."}))
    negative("expired_decision", lambda d: d.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("wrong_route", lambda d: d.update({"route_id": "public_action_gateway"}))
    negative("wrong_egress_type", lambda d: d.update({"egress_type": "public_submission"}))
    negative("missing_docket_path", lambda d: d.update({"source_gateway_docket_path": ""}))
    negative("outside_docket_path", lambda d: d.update({"source_gateway_docket_path": r"C:\Temp\gateway.json"}))
    negative("docket_hash_mismatch", lambda d: d.update({"source_gateway_docket_sha256": "0" * 64}))
    negative("execute_scope", lambda d: d.update({"allowed_scope": "account_wallet_payment_execute"}))
    negative("missing_required_gate", lambda d: d.update({"allowed_gate_ids": ["agent_egress_event_ledger_v1"]}))
    negative("extra_unknown_gate", lambda d: d.update({"allowed_gate_ids": d["allowed_gate_ids"] + ["unknown_gate"]}))
    negative("approval_is_apply", lambda d: d.update({"approval_is_not_apply": False}))
    for key in [
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
        "worker_registration_allowed",
        "worker_start_allowed",
        "runtime_start_allowed",
        "browser_session_start_allowed",
        "mcp_tool_calls",
        "model_api_calls",
        "public_actions",
        "account_actions",
        "wallet_actions",
        "payment_actions",
        "real_money_actions",
        "external_side_effects",
    ]:
        negative(key, lambda d, k=key: d.update({k: True}))
    negative("browser_started", lambda d: d.update({"browser_sessions_started": 1}))
    negative("service_request_assigned", lambda d: d.update({"service_requests_assigned": 1}))
    negative("service_request_updated", lambda d: d.update({"service_requests_updated": 1}))
    negative("short_rollback", lambda d: d.update({"rollback_plan": "undo"}))
    for key, value in [
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
        ("payment_actions", True),
        ("payment_methods_changed", 1),
        ("legal_kyc_tax_actions", True),
        ("kyc_submissions", 1),
        ("tax_forms_submitted", 1),
        ("payment_addresses_published", 1),
        ("real_money_actions", True),
        ("account_actions", True),
        ("wallet_actions", True),
        ("worker_starts", 1),
        ("browser_sessions_started", 1),
        ("service_requests_updated", 1),
        ("mcp_tool_calls", True),
        ("model_api_calls", True),
        ("public_actions", True),
        ("external_side_effects", True),
    ]:
        negative(f"boundary_{key}", lambda d, k=key, v=value: d["runtime_boundary"].update({k: v}))
    return fixtures


def validate_decision(
    decision: dict[str, Any],
    schema: dict[str, Any],
    route: dict[str, Any],
    intake_validation: dict[str, Any],
    egress_validation: dict[str, Any],
    identity_validation: dict[str, Any],
) -> dict[str, Any]:
    errors = collect_common_signed_decision_errors(
        schema=schema,
        decision=decision,
        route=route,
        required_fields=REQUIRED_FIELDS,
        schema_version="agent_company.egress_route_signed_decision_intake_contract.v1",
        target_route_id=TARGET_ROUTE_ID,
        target_egress_type=TARGET_EGRESS_TYPE,
        evaluation_utc=EVALUATION_UTC,
        expected_docket_path=str(GATEWAY_DOCKET),
        expected_docket_sha256=sha256_path(GATEWAY_DOCKET),
        path_inside_root=path_inside_root,
        parse_utc=parse_utc,
        schema_false_props=SCHEMA_FALSE_PROPS,
        schema_route_error="schema_route_const_must_target_account_wallet_payment_gateway",
        schema_type_error="schema_egress_type_const_must_target_account_wallet_payment",
        route_error="route_id_must_match_account_wallet_payment_gateway",
        type_error="egress_type_must_be_account_wallet_payment",
        decision_false_fields=DECISION_FALSE_FIELDS,
        decision_zero_fields=DECISION_ZERO_FIELDS,
        zero_boundary=ZERO_BOUNDARY,
    )

    if intake_validation.get("all_checks_passed") is not True:
        errors.append("source_intake_contract_validation_not_passing")
    if intake_validation.get("route_count") < 8 or intake_validation.get("template_count") < 8:
        errors.append("source_intake_contract_must_cover_gateway_routes")
    if intake_validation.get("decisions_applied") != 0 or intake_validation.get("external_side_effects") is not False:
        errors.append("source_intake_contract_must_be_report_only")
    if egress_validation.get("all_checks_passed") is not True:
        errors.append("source_agent_egress_event_ledger_validation_not_passing")
    if egress_validation.get("live_egress_events_recorded") != 0:
        errors.append("source_agent_egress_event_ledger_must_have_zero_live_events")
    if identity_validation.get("all_checks_passed") is not True:
        errors.append("source_identity_envelope_validation_not_passing")
    if (
        identity_validation.get("account_actions") is not False
        or identity_validation.get("wallet_actions") is not False
        or identity_validation.get("payment_actions") is not False
    ):
        errors.append("source_identity_must_deny_account_wallet_payment")

    decision_value = decision.get("decision")
    required_gates = copy.deepcopy(route["required_gates"])

    if decision_value == "deny":
        pass
    else:
        if decision.get("operator_attestation") != ATTESTATION:
            errors.append("operator_attestation_must_match_exact_account_wallet_payment_text")
        for gate in [
            "account_registration_intake",
            "wallet_setup_packet",
            "wallet_public_address_response",
            "legal_kyc_tax_payment_gate",
            "agent_egress_event_ledger_v1",
        ]:
            if gate not in decision.get("allowed_gate_ids", []):
                errors.append(f"missing_required_gate:{gate}")
        if len(str(decision.get("rollback_plan", "")).strip()) < 60:
            errors.append("rollback_plan_too_short")

    accepted = not errors
    return {
        "decision_id": decision.get("decision_id"),
        "decision": decision_value,
        "route_id": decision.get("route_id"),
        "accepted_for_apply_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
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
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "real_money_actions": False,
        "worker_start_allowed": False,
        "worker_starts": 0,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "mcp_tool_calls": False,
        "model_api_calls": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    route = route_summary()["route"]
    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        decision = copy.deepcopy(fixture["decision"]) if "decision" in fixture else load_json(Path(fixture["path"]))
        result = validate_decision(decision, schema, route, intake_validation, egress_validation, identity_validation)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_apply_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_apply_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.account_wallet_payment_egress_signed_decision_guard_report.v1",
        "generated_utc": generated,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_intake_contract_path": str(INTAKE_REPORT),
        "source_intake_contract_validation_path": str(INTAKE_VALIDATION),
        "source_agent_egress_event_ledger_validation_path": str(EGRESS_VALIDATION),
        "source_identity_validation_path": str(IDENTITY_VALIDATION),
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "source_gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "target_route_required_gates": copy.deepcopy(route["required_gates"]),
        "blocked_actions": copy.deepcopy(route["blocked_actions"]),
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "positive_authority": {
            "accepted_scope": f"egress_route_preflight_only:{TARGET_ROUTE_ID}",
            "account_creation_allowed": False,
            "wallet_creation_allowed": False,
            "private_key_custody_allowed": False,
            "funds_transfer_allowed": False,
            "payment_action_allowed": False,
            "legal_kyc_tax_action_allowed": False,
            "public_payment_address_allowed": False,
            "real_money_action_allowed": False,
            "gateway_registration_allowed": False,
            "gateway_start_allowed": False,
            "live_egress_allowed": False,
            "worker_start_allowed": False,
        },
        "next_action": NEXT_ACTION,
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.account_wallet_payment_egress_signed_decision_guard_validation.v1",
        "generated_utc": generated,
        "guard_report_path": str(REPORT_JSON),
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
        "apply_allowed": False,
        "decisions_applied": 0,
        "approval_rows_written": 0,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation
