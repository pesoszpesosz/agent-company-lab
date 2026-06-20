#!/usr/bin/env python3
"""Write a report-only integrity audit for egress route safety chains."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from atomic_writes import write_json_atomic


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "egress-route-chain-integrity-audit-v1.schema.json"
GATEWAY_DOCKET = REPORTS / "unified-agent-egress-gateway-docket-v1-20260618.json"
GATEWAY_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
BROWSER_GUARD_VALIDATION = REPORTS / "egress-route-signed-decision-guard-v1-validation-20260618.json"
BROWSER_PREFLIGHT_VALIDATION = REPORTS / "egress-route-apply-preflight-blocker-v1-validation-20260618.json"
BROWSER_COMMAND_VALIDATION = REPORTS / "egress-route-apply-command-contract-v1-validation-20260618.json"
MCP_GUARD_VALIDATION = REPORTS / "mcp-egress-signed-decision-guard-v1-validation-20260618.json"
MCP_PREFLIGHT_VALIDATION = REPORTS / "mcp-egress-apply-preflight-blocker-v1-validation-20260618.json"
MCP_COMMAND_GUARD_VALIDATION = REPORTS / "mcp-egress-apply-command-guard-v1-validation-20260618.json"
LOCAL_A2A_GUARD_VALIDATION = REPORTS / "local-a2a-egress-signed-decision-guard-v1-validation-20260618.json"
LOCAL_A2A_PREFLIGHT_VALIDATION = REPORTS / "local-a2a-egress-apply-preflight-blocker-v1-validation-20260618.json"
LOCAL_A2A_COMMAND_CONTRACT_VALIDATION = REPORTS / "local-a2a-egress-apply-command-contract-v1-validation-20260618.json"
LOCAL_A2A_COMMAND_GUARD_VALIDATION = REPORTS / "local-a2a-egress-apply-command-guard-v1-validation-20260618.json"
MODEL_API_GUARD_VALIDATION = REPORTS / "model-api-egress-signed-decision-guard-v1-validation-20260618.json"
MODEL_API_PREFLIGHT_VALIDATION = REPORTS / "model-api-egress-apply-preflight-blocker-v1-validation-20260618.json"
MODEL_API_COMMAND_CONTRACT_VALIDATION = REPORTS / "model-api-egress-apply-command-contract-v1-validation-20260618.json"
RUNTIME_PROCESS_GUARD_VALIDATION = REPORTS / "runtime-process-egress-signed-decision-guard-v1-validation-20260618.json"
RUNTIME_PROCESS_PREFLIGHT_VALIDATION = REPORTS / "runtime-process-egress-apply-preflight-blocker-v1-validation-20260618.json"
RUNTIME_PROCESS_COMMAND_CONTRACT_VALIDATION = REPORTS / "runtime-process-egress-apply-command-contract-v1-validation-20260618.json"
PUBLIC_ACTION_GUARD_VALIDATION = REPORTS / "public-action-egress-signed-decision-guard-v1-validation-20260618.json"
PUBLIC_ACTION_PREFLIGHT_VALIDATION = REPORTS / "public-action-egress-apply-preflight-blocker-v1-validation-20260618.json"
PUBLIC_ACTION_COMMAND_CONTRACT_VALIDATION = REPORTS / "public-action-egress-apply-command-contract-v1-validation-20260618.json"
ACCOUNT_WALLET_PAYMENT_GUARD_VALIDATION = REPORTS / "account-wallet-payment-egress-signed-decision-guard-v1-validation-20260618.json"
ACCOUNT_WALLET_PAYMENT_PREFLIGHT_VALIDATION = REPORTS / "account-wallet-payment-egress-apply-preflight-blocker-v1-validation-20260618.json"
ACCOUNT_WALLET_PAYMENT_COMMAND_CONTRACT_VALIDATION = REPORTS / "account-wallet-payment-egress-apply-command-contract-v1-validation-20260618.json"
TELEMETRY_EXPORT_GUARD_VALIDATION = REPORTS / "telemetry-export-egress-signed-decision-guard-v1-validation-20260618.json"
TELEMETRY_EXPORT_PREFLIGHT_VALIDATION = REPORTS / "telemetry-export-egress-apply-preflight-blocker-v1-validation-20260618.json"
TELEMETRY_EXPORT_COMMAND_CONTRACT_VALIDATION = REPORTS / "telemetry-export-egress-apply-command-contract-v1-validation-20260618.json"

REPORT_JSON = REPORTS / "egress-route-chain-integrity-audit-v1-20260618.json"
VALIDATION_JSON = REPORTS / "egress-route-chain-integrity-audit-v1-validation-20260618.json"
REPORT_MD = REPORTS / "egress-route-chain-integrity-audit-v1-20260618.md"

FULL_CHAIN_LAYERS = [
    "unified_gateway_docket",
    "signed_decision_intake_contract",
    "signed_decision_guard",
    "apply_preflight_blocker",
    "apply_command_contract",
]
MCP_FULL_CHAIN_LAYERS = [
    "unified_gateway_docket",
    "signed_decision_intake_contract",
    "signed_decision_guard",
    "apply_preflight_blocker",
    "apply_command_guard",
]
LOCAL_A2A_FULL_CHAIN_LAYERS = [
    "unified_gateway_docket",
    "signed_decision_intake_contract",
    "signed_decision_guard",
    "apply_preflight_blocker",
    "apply_command_contract",
    "apply_command_guard",
]
SHARED_LAYERS = ["unified_gateway_docket", "signed_decision_intake_contract"]

ZERO_BOUNDARY = {
    "report_only": True,
    "gateway_registration_allowed": False,
    "gateway_start_allowed": False,
    "live_egress_allowed": False,
    "agent_message_send_allowed": False,
    "agent_messages_sent": 0,
    "browser_sessions_started": 0,
    "worker_starts": 0,
    "runtime_starts": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "model_api_calls": False,
    "mcp_tool_calls": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validation_summary(path: Path) -> dict[str, Any]:
    data = load_json(path)
    return {
        "path": str(path),
        "sha256": sha256_path(path),
        "all_checks_passed": data.get("all_checks_passed"),
        "failure_count": data.get("failure_count"),
        "live_egress_allowed": data.get("live_egress_allowed", False),
        "gateway_start_allowed": data.get("gateway_start_allowed", False),
        "browser_session_start_allowed": data.get("browser_session_start_allowed", False),
        "mcp_server_enable_allowed": data.get("mcp_server_enable_allowed", False),
        "mcp_tool_call_allowed": data.get("mcp_tool_call_allowed", False),
        "mcp_servers_started": data.get("mcp_servers_started", 0),
        "mcp_servers_enabled": data.get("mcp_servers_enabled", 0),
        "mcp_tool_calls": data.get("mcp_tool_calls", False),
        "provider_key_use_allowed": data.get("provider_key_use_allowed", False),
        "provider_keys_used": data.get("provider_keys_used", False),
        "model_api_call_allowed": data.get("model_api_call_allowed", False),
        "model_api_calls": data.get("model_api_calls", False),
        "training_data_upload_allowed": data.get("training_data_upload_allowed", False),
        "training_data_uploaded": data.get("training_data_uploaded", False),
        "max_cost_usd": data.get("max_cost_usd", 0),
        "credentials_created": data.get("credentials_created", False),
        "credential_access_allowed": data.get("credential_access_allowed", False),
        "agent_message_send_allowed": data.get("agent_message_send_allowed", False),
        "agent_messages_sent": data.get("agent_messages_sent", 0),
        "worker_start_allowed": data.get("worker_start_allowed", False),
        "runtime_start_allowed": data.get("runtime_start_allowed", False),
        "runtime_starts": data.get("runtime_starts", 0),
        "dependency_installs": data.get("dependency_installs", 0),
        "queue_mutations": data.get("queue_mutations", 0),
        "public_action_allowed": data.get("public_action_allowed", False),
        "public_actions": data.get("public_actions", False),
        "account_actions": data.get("account_actions", False),
        "wallet_actions": data.get("wallet_actions", False),
        "payment_actions": data.get("payment_actions", False),
        "real_money_actions": data.get("real_money_actions", False),
        "account_creation_allowed": data.get("account_creation_allowed", False),
        "wallet_creation_allowed": data.get("wallet_creation_allowed", False),
        "private_key_custody_allowed": data.get("private_key_custody_allowed", False),
        "funds_transfer_allowed": data.get("funds_transfer_allowed", False),
        "payment_action_allowed": data.get("payment_action_allowed", False),
        "legal_kyc_tax_action_allowed": data.get("legal_kyc_tax_action_allowed", False),
        "public_payment_address_allowed": data.get("public_payment_address_allowed", False),
        "real_money_action_allowed": data.get("real_money_action_allowed", False),
        "telemetry_export_allowed": data.get("telemetry_export_allowed", False),
        "telemetry_exports": data.get("telemetry_exports", 0),
        "external_trace_export_allowed": data.get("external_trace_export_allowed", False),
        "external_trace_exports": data.get("external_trace_exports", 0),
        "private_prompt_upload_allowed": data.get("private_prompt_upload_allowed", False),
        "private_prompts_uploaded": data.get("private_prompts_uploaded", 0),
        "credential_export_allowed": data.get("credential_export_allowed", False),
        "credentials_exported": data.get("credentials_exported", 0),
        "unredacted_log_sync_allowed": data.get("unredacted_log_sync_allowed", False),
        "unredacted_logs_synced": data.get("unredacted_logs_synced", 0),
        "external_side_effects": data.get("external_side_effects", False),
    }


def browser_chain_sources() -> dict[str, dict[str, Any]]:
    return {
        "signed_decision_guard": validation_summary(BROWSER_GUARD_VALIDATION),
        "apply_preflight_blocker": validation_summary(BROWSER_PREFLIGHT_VALIDATION),
        "apply_command_contract": validation_summary(BROWSER_COMMAND_VALIDATION),
    }


def mcp_chain_sources() -> dict[str, dict[str, Any]]:
    return {
        "signed_decision_guard": validation_summary(MCP_GUARD_VALIDATION),
        "apply_preflight_blocker": validation_summary(MCP_PREFLIGHT_VALIDATION),
        "apply_command_guard": validation_summary(MCP_COMMAND_GUARD_VALIDATION),
    }


def local_a2a_chain_sources() -> dict[str, dict[str, Any]]:
    return {
        "signed_decision_guard": validation_summary(LOCAL_A2A_GUARD_VALIDATION),
        "apply_preflight_blocker": validation_summary(LOCAL_A2A_PREFLIGHT_VALIDATION),
        "apply_command_contract": validation_summary(LOCAL_A2A_COMMAND_CONTRACT_VALIDATION),
        "apply_command_guard": validation_summary(LOCAL_A2A_COMMAND_GUARD_VALIDATION),
    }


def model_api_chain_sources() -> dict[str, dict[str, Any]]:
    return {
        "signed_decision_guard": validation_summary(MODEL_API_GUARD_VALIDATION),
        "apply_preflight_blocker": validation_summary(MODEL_API_PREFLIGHT_VALIDATION),
        "apply_command_contract": validation_summary(MODEL_API_COMMAND_CONTRACT_VALIDATION),
    }


def runtime_process_chain_sources() -> dict[str, dict[str, Any]]:
    return {
        "signed_decision_guard": validation_summary(RUNTIME_PROCESS_GUARD_VALIDATION),
        "apply_preflight_blocker": validation_summary(RUNTIME_PROCESS_PREFLIGHT_VALIDATION),
        "apply_command_contract": validation_summary(RUNTIME_PROCESS_COMMAND_CONTRACT_VALIDATION),
    }


def public_action_chain_sources() -> dict[str, dict[str, Any]]:
    return {
        "signed_decision_guard": validation_summary(PUBLIC_ACTION_GUARD_VALIDATION),
        "apply_preflight_blocker": validation_summary(PUBLIC_ACTION_PREFLIGHT_VALIDATION),
        "apply_command_contract": validation_summary(PUBLIC_ACTION_COMMAND_CONTRACT_VALIDATION),
    }


def account_wallet_payment_chain_sources() -> dict[str, dict[str, Any]]:
    return {
        "signed_decision_guard": validation_summary(ACCOUNT_WALLET_PAYMENT_GUARD_VALIDATION),
        "apply_preflight_blocker": validation_summary(ACCOUNT_WALLET_PAYMENT_PREFLIGHT_VALIDATION),
        "apply_command_contract": validation_summary(ACCOUNT_WALLET_PAYMENT_COMMAND_CONTRACT_VALIDATION),
    }


def telemetry_export_chain_sources() -> dict[str, dict[str, Any]]:
    return {
        "signed_decision_guard": validation_summary(TELEMETRY_EXPORT_GUARD_VALIDATION),
        "apply_preflight_blocker": validation_summary(TELEMETRY_EXPORT_PREFLIGHT_VALIDATION),
        "apply_command_contract": validation_summary(TELEMETRY_EXPORT_COMMAND_CONTRACT_VALIDATION),
    }


def build_report() -> tuple[dict[str, Any], dict[str, Any]]:
    generated = utc_now()
    schema = load_json(SCHEMA_PATH)
    gateway = load_json(GATEWAY_DOCKET)
    gateway_validation = validation_summary(GATEWAY_VALIDATION)
    intake_validation = validation_summary(INTAKE_VALIDATION)
    browser_sources = browser_chain_sources()
    mcp_sources = mcp_chain_sources()
    local_a2a_sources = local_a2a_chain_sources()
    model_api_sources = model_api_chain_sources()
    runtime_process_sources = runtime_process_chain_sources()
    public_action_sources = public_action_chain_sources()
    account_wallet_payment_sources = account_wallet_payment_chain_sources()
    telemetry_export_sources = telemetry_export_chain_sources()
    failures: list[str] = []

    if schema.get("properties", {}).get("live_egress_allowed", {}).get("const") is not False:
        failures.append("schema_live_egress_allowed_must_const_false")
    if gateway_validation["all_checks_passed"] is not True:
        failures.append("gateway_docket_validation_not_passing")
    if intake_validation["all_checks_passed"] is not True:
        failures.append("signed_decision_intake_validation_not_passing")

    routes = gateway.get("gateway_routes", [])
    route_audits: list[dict[str, Any]] = []
    for route in routes:
        present = list(SHARED_LAYERS)
        required_layers = list(FULL_CHAIN_LAYERS)
        layer_sources = {
            "unified_gateway_docket": gateway_validation,
            "signed_decision_intake_contract": intake_validation,
        }
        if route["route_id"] == "browser_read_only_gateway":
            present = list(FULL_CHAIN_LAYERS)
            layer_sources.update(browser_sources)
        elif route["route_id"] == "mcp_tool_gateway":
            required_layers = list(MCP_FULL_CHAIN_LAYERS)
            present = list(MCP_FULL_CHAIN_LAYERS)
            layer_sources.update(mcp_sources)
        elif route["route_id"] == "local_agent_to_agent_report_only":
            required_layers = list(LOCAL_A2A_FULL_CHAIN_LAYERS)
            present = list(SHARED_LAYERS) + ["signed_decision_guard", "apply_preflight_blocker", "apply_command_contract", "apply_command_guard"]
            layer_sources.update(local_a2a_sources)
        elif route["route_id"] == "model_api_gateway":
            present = list(FULL_CHAIN_LAYERS)
            layer_sources.update(model_api_sources)
        elif route["route_id"] == "runtime_process_gateway":
            present = list(FULL_CHAIN_LAYERS)
            layer_sources.update(runtime_process_sources)
        elif route["route_id"] == "public_action_gateway":
            present = list(FULL_CHAIN_LAYERS)
            layer_sources.update(public_action_sources)
        elif route["route_id"] == "account_wallet_payment_gateway":
            present = list(FULL_CHAIN_LAYERS)
            layer_sources.update(account_wallet_payment_sources)
        elif route["route_id"] == "telemetry_export_gateway":
            present = list(FULL_CHAIN_LAYERS)
            layer_sources.update(telemetry_export_sources)

        missing = [layer for layer in required_layers if layer not in present]
        status = "full_report_only_chain" if not missing else "partial_shared_chain"
        layer_failures = [
            layer for layer, summary in layer_sources.items()
            if summary.get("all_checks_passed") is not True
            or summary.get("live_egress_allowed") is not False
            or summary.get("gateway_start_allowed") is not False
            or summary.get("mcp_server_enable_allowed") is not False
            or summary.get("mcp_tool_call_allowed") is not False
            or summary.get("mcp_servers_started") != 0
            or summary.get("mcp_servers_enabled") != 0
            or summary.get("mcp_tool_calls") is not False
            or summary.get("provider_key_use_allowed") is not False
            or summary.get("provider_keys_used") is not False
            or summary.get("model_api_call_allowed") is not False
            or summary.get("model_api_calls") is not False
            or summary.get("training_data_upload_allowed") is not False
            or summary.get("training_data_uploaded") is not False
            or summary.get("max_cost_usd") != 0
            or summary.get("credentials_created") is not False
            or summary.get("credential_access_allowed") is not False
            or summary.get("agent_message_send_allowed") is not False
            or summary.get("agent_messages_sent") != 0
            or summary.get("runtime_start_allowed") is not False
            or summary.get("runtime_starts") != 0
            or summary.get("dependency_installs") != 0
            or summary.get("queue_mutations") != 0
            or summary.get("public_action_allowed") is not False
            or summary.get("public_actions") is not False
            or summary.get("account_actions") is not False
            or summary.get("wallet_actions") is not False
            or summary.get("payment_actions") is not False
            or summary.get("real_money_actions") is not False
            or summary.get("account_creation_allowed") is not False
            or summary.get("wallet_creation_allowed") is not False
            or summary.get("private_key_custody_allowed") is not False
            or summary.get("funds_transfer_allowed") is not False
            or summary.get("payment_action_allowed") is not False
            or summary.get("legal_kyc_tax_action_allowed") is not False
            or summary.get("public_payment_address_allowed") is not False
            or summary.get("real_money_action_allowed") is not False
            or summary.get("telemetry_export_allowed") is not False
            or summary.get("telemetry_exports") != 0
            or summary.get("external_trace_export_allowed") is not False
            or summary.get("external_trace_exports") != 0
            or summary.get("private_prompt_upload_allowed") is not False
            or summary.get("private_prompts_uploaded") != 0
            or summary.get("credential_export_allowed") is not False
            or summary.get("credentials_exported") != 0
            or summary.get("unredacted_log_sync_allowed") is not False
            or summary.get("unredacted_logs_synced") != 0
            or summary.get("external_side_effects") is not False
        ]
        if layer_failures:
            failures.append(f"route_layer_validation_failed:{route['route_id']}:{','.join(layer_failures)}")

        route_audits.append({
            "route_id": route["route_id"],
            "egress_type": route["egress_type"],
            "target_egress_type": route["egress_type"],
            "chain_status": status,
            "present_layers": present,
            "missing_layers": missing,
            "layer_sources": layer_sources,
            "required_gates": route.get("required_gates", []),
            "live_egress_allowed": False,
            "gateway_start_allowed": False,
            "browser_session_start_allowed": False,
            "browser_sessions_started": 0,
            "agent_message_send_allowed": False,
            "agent_messages_sent": 0,
            "mcp_server_enable_allowed": False,
            "mcp_tool_call_allowed": False,
            "mcp_servers_started": 0,
            "mcp_servers_enabled": 0,
            "mcp_tool_calls": False,
            "provider_key_use_allowed": False,
            "provider_keys_used": False,
            "model_api_call_allowed": False,
            "model_api_calls": False,
            "account_actions": False,
            "wallet_actions": False,
            "payment_actions": False,
            "real_money_actions": False,
            "account_creation_allowed": False,
            "wallet_creation_allowed": False,
            "private_key_custody_allowed": False,
            "funds_transfer_allowed": False,
            "payment_action_allowed": False,
            "legal_kyc_tax_action_allowed": False,
            "public_payment_address_allowed": False,
            "real_money_action_allowed": False,
            "training_data_upload_allowed": False,
            "training_data_uploaded": False,
            "max_cost_usd": 0,
            "credentials_created": False,
            "credential_access_allowed": False,
            "worker_start_allowed": False,
            "worker_starts": 0,
            "runtime_start_allowed": False,
            "runtime_starts": 0,
            "dependency_installs": 0,
            "queue_mutations": 0,
            "public_action_allowed": False,
            "public_actions": False,
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
            "external_side_effects": False,
            "next_action": (
                "Continue route only after real signed decision exists."
                if status == "full_report_only_chain"
                else (
                    f"Build {missing[0]} for {route['route_id']} while preserving zero live egress."
                    if missing
                    else f"Review {route['route_id']} route chain."
                )
            ),
        })

    full_count = sum(1 for item in route_audits if item["chain_status"] == "full_report_only_chain")
    partial_count = sum(1 for item in route_audits if item["chain_status"] == "partial_shared_chain")
    if len(routes) != 8:
        failures.append(f"route_count_expected_8_got_{len(routes)}")
    if full_count < 2:
        failures.append("expected_browser_and_mcp_full_report_only_route_chains")
    recommended_item = next((item for item in route_audits if item["chain_status"] == "partial_shared_chain"), {})
    recommended = recommended_item.get("route_id", "")
    recommended_layer = recommended_item.get("missing_layers", [""])[0] if recommended_item.get("missing_layers") else ""
    if not recommended:
        next_action = "All report-only egress route chains have their required non-live guard layers; continue only after a real signed operator decision and route-specific approval evidence exists."
    elif recommended == "local_agent_to_agent_report_only" and recommended_layer == "apply_command_contract":
        next_action = "Build local A2A egress apply command contract for local_agent_to_agent_report_only while preserving zero live egress and zero agent message sends."
    elif recommended == "local_agent_to_agent_report_only" and recommended_layer == "apply_command_guard":
        next_action = "Build local A2A egress apply command guard for local_agent_to_agent_report_only while preserving zero live egress and zero agent message sends."
    elif recommended == "local_agent_to_agent_report_only" and recommended_layer == "apply_preflight_blocker":
        next_action = "Build local A2A egress apply preflight blocker for local_agent_to_agent_report_only while preserving zero live egress and zero agent message sends."
    else:
        next_action = f"Build route-specific {recommended_layer} for {recommended} while preserving zero live egress."

    report = {
        "schema_version": "agent_company.egress_route_chain_integrity_audit.v1",
        "generated_utc": generated,
        "schema_path": str(SCHEMA_PATH),
        "gateway_docket_path": str(GATEWAY_DOCKET),
        "gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "route_count": len(routes),
        "route_audits": route_audits,
        "full_chain_route_count": full_count,
        "partial_chain_route_count": partial_count,
        "recommended_next_route_id": recommended,
        "recommended_next_layer": recommended_layer,
        "next_action": next_action,
        **ZERO_BOUNDARY,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.egress_route_chain_integrity_audit_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "route_count": len(routes),
        "full_chain_route_count": full_count,
        "partial_chain_route_count": partial_count,
        "recommended_next_route_id": recommended,
        "recommended_next_layer": recommended_layer,
        **ZERO_BOUNDARY,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Egress Route Chain Integrity Audit v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Gateway docket: `{GATEWAY_DOCKET}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Routes audited: `{validation['route_count']}`",
        f"- Full report-only chains: `{validation['full_chain_route_count']}`",
        f"- Partial shared chains: `{validation['partial_chain_route_count']}`",
        f"- Recommended next route: `{validation['recommended_next_route_id']}`",
        f"- Recommended next layer: `{validation['recommended_next_layer']}`",
        f"- Live egress allowed: `{validation['live_egress_allowed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Route Coverage",
        "",
        "| Route | Egress Type | Status | Present Layers | Missing Layers |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["route_audits"]:
        present = ", ".join(f"`{layer}`" for layer in item["present_layers"])
        missing = ", ".join(f"`{layer}`" for layer in item["missing_layers"]) or "`none`"
        lines.append(f"| `{item['route_id']}` | `{item['egress_type']}` | `{item['chain_status']}` | {present} | {missing} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This audit is report-only. It does not register gateways, start gateways, start workers, open browser sessions, mutate service requests, call MCP/model APIs, or perform live egress.",
            "",
            f"Next action: {report['next_action']}",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    report, validation = build_report()
    write_json_atomic(REPORT_JSON, report)
    write_json_atomic(VALIDATION_JSON, validation)
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
