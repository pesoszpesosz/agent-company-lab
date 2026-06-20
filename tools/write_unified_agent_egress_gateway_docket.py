#!/usr/bin/env python3
"""Write a report-only unified agent egress gateway docket."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "unified-agent-egress-gateway-docket-v1.schema.json"
CAPABILITY_REGISTRY = REPORTS / "worker-capability-class-registry-v1-20260618.json"
CAPABILITY_VALIDATION = REPORTS / "worker-capability-class-registry-v1-validation-20260618.json"
EGRESS_LEDGER_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
MCP_GATE_VALIDATION = REPORTS / "mcp-tool-registry-gate-v1-validation-20260617.json"
BROWSER_APPLY_COMMAND_VALIDATION = REPORTS / "browser-read-only-apply-command-contract-v1-validation-20260618.json"

REPORT_JSON = REPORTS / "unified-agent-egress-gateway-docket-v1-20260618.json"
VALIDATION_JSON = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
REPORT_MD = REPORTS / "unified-agent-egress-gateway-docket-v1-20260618.md"

ZERO_BOUNDARY = {
    "report_only": True,
    "gateway_registration_allowed": False,
    "gateway_start_allowed": False,
    "live_egress_allowed": False,
    "dependency_installs": 0,
    "worker_registration_allowed": False,
    "worker_start_allowed": False,
    "runtime_start_allowed": False,
    "browser_session_start_allowed": False,
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


def route(
    route_id: str,
    egress_type: str,
    capability_class_ids: list[str],
    required_gates: list[str],
    blocked_actions: list[str],
    required_evidence: list[str],
    allowed_phase: str = "report_only_design",
) -> dict[str, Any]:
    return {
        "route_id": route_id,
        "egress_type": egress_type,
        "capability_class_ids": capability_class_ids,
        "allowed_phase": allowed_phase,
        "required_gates": required_gates,
        "blocked_actions": blocked_actions,
        "required_evidence": required_evidence,
        "live_execution_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "next_action": "Create a signed operator decision packet and rerun all referenced gates before this route can move beyond report-only design.",
    }


def build_routes(classes: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    all_classes = sorted(classes)
    return [
        route(
            "local_agent_to_agent_report_only",
            "agent_to_agent",
            all_classes,
            ["agent_egress_event_ledger_v1", "local_runtime_adapter_pool_identity_envelope_v1"],
            ["live_gateway_start", "external_api_call", "service_request_mutation"],
            ["trace_event", "input_artifact_hash", "output_artifact_hash"],
            "local_report_only_allowed",
        ),
        route(
            "browser_read_only_gateway",
            "browser_read_only",
            ["browser_worker"],
            [
                "browser_read_only_worker_policy_v1",
                "browser_worker_adapter_contract_v1",
                "browser_read_only_signed_approval_guard_v1",
                "browser_read_only_apply_preflight_blocker_v1",
                "browser_read_only_apply_command_contract_v1",
                "agent_egress_event_ledger_v1",
            ],
            ["browser_session_start", "signed_in_state_change", "form_submit", "download_private_file"],
            ["approved_service_request", "adapter_contract_report", "redacted_screenshot_or_text_capture", "post_run_trace"],
        ),
        route(
            "mcp_tool_gateway",
            "mcp_tool",
            ["gateway_or_mcp"],
            [
                "mcp_tool_registry_gate_v1",
                "agent_egress_event_ledger_v1",
                "local_runtime_adapter_pool_identity_envelope_v1",
                "signed_operator_decision_required",
            ],
            ["mcp_server_start", "mcp_tool_call", "credential_read", "network_write"],
            ["registered_tool_entry", "identity_envelope", "egress_event", "post_execution_evidence"],
        ),
        route(
            "model_api_gateway",
            "model_api",
            ["agent_framework", "model_backed_agent_framework"],
            [
                "model_api_execution_gate",
                "secrets_credentials_handling_gate",
                "agent_egress_event_ledger_v1",
                "cost_budget_signed_decision",
            ],
            ["model_api_call", "provider_key_use", "training_data_upload", "unbounded_cost"],
            ["provider_scope", "model_id", "max_cost", "data_boundary", "redaction_plan", "trace_event"],
        ),
        route(
            "runtime_process_gateway",
            "runtime_start",
            ["durable_runtime", "durable_workflow", "workflow_platform", "platform_runtime"],
            [
                "runtime_start_preflight_v1",
                "runtime_start_signed_decision_guard_v1",
                "runtime_start_apply_preflight_blocker_v1",
                "runtime_dependency_install_preflight_v1",
                "agent_egress_event_ledger_v1",
            ],
            ["dependency_install", "runtime_process_start", "queue_mutation", "worker_start"],
            ["runtime_manifest", "dependency_hashes", "signed_runtime_decision", "rollback_plan", "trace_event"],
        ),
        route(
            "public_action_gateway",
            "public_submission",
            ["browser_worker", "gateway_or_mcp", "platform_runtime"],
            [
                "public_action_execution_gate",
                "reputation_review_worker",
                "agent_egress_event_ledger_v1",
                "exact_action_body_approval",
            ],
            ["post_comment", "submit_form", "open_pr", "claim_bounty", "send_message"],
            ["exact_payload", "target_url", "account_identity", "approval_record", "post_action_receipt"],
        ),
        route(
            "account_wallet_payment_gateway",
            "account_wallet_payment",
            ["platform_runtime", "browser_worker"],
            [
                "account_registration_intake",
                "wallet_setup_packet",
                "wallet_public_address_response",
                "legal_kyc_tax_payment_gate",
                "agent_egress_event_ledger_v1",
            ],
            ["accept_terms", "create_account", "control_private_key", "send_funds", "publish_payment_address"],
            ["venue_terms_summary", "custody_boundary", "network_token_scope", "user_decision_record"],
        ),
        route(
            "telemetry_export_gateway",
            "telemetry_export",
            ["observability", "gateway_or_mcp"],
            [
                "telemetry_privacy_export_gate_v1",
                "agent_egress_event_ledger_v1",
                "secrets_credentials_handling_gate",
            ],
            ["external_trace_export", "private_prompt_upload", "credential_export", "unredacted_log_sync"],
            ["redaction_policy", "destination_scope", "retention_policy", "sample_trace_artifact"],
        ),
    ]


def build_report() -> tuple[dict[str, Any], dict[str, Any]]:
    schema = load_json(SCHEMA_PATH)
    capability = load_json(CAPABILITY_REGISTRY)
    capability_validation = load_json(CAPABILITY_VALIDATION)
    egress_validation = load_json(EGRESS_LEDGER_VALIDATION)
    mcp_validation = load_json(MCP_GATE_VALIDATION)
    browser_validation = load_json(BROWSER_APPLY_COMMAND_VALIDATION)

    classes = {item["capability_class_id"]: item for item in capability.get("capability_classes", [])}
    routes = build_routes(classes)
    failures: list[str] = []

    if schema.get("properties", {}).get("gateway_start_allowed", {}).get("const") is not False:
        failures.append("schema_gateway_start_allowed_must_const_false")
    if not capability_validation.get("all_checks_passed"):
        failures.append("source_capability_registry_validation_failed")
    if not egress_validation.get("all_checks_passed"):
        failures.append("egress_event_ledger_validation_failed")
    if not mcp_validation.get("all_checks_passed"):
        failures.append("mcp_tool_registry_gate_validation_failed")
    if not browser_validation.get("all_checks_passed"):
        failures.append("browser_apply_command_contract_validation_failed")
    if len(classes) < 8:
        failures.append("capability_class_count_below_8")
    if len(routes) < 8:
        failures.append("gateway_route_count_below_8")

    for required in ["browser_worker", "gateway_or_mcp", "model_backed_agent_framework", "durable_runtime"]:
        if required not in classes:
            failures.append(f"missing_capability_class:{required}")
    for item in routes:
        if item["live_execution_allowed"]:
            failures.append(f"live_execution_allowed:{item['route_id']}")
        if len(item["required_gates"]) < 2:
            failures.append(f"insufficient_required_gates:{item['route_id']}")
        if "agent_egress_event_ledger_v1" not in item["required_gates"]:
            failures.append(f"missing_egress_ledger_gate:{item['route_id']}")

    generated = utc_now()
    gate_index = sorted({gate for item in routes for gate in item["required_gates"]})
    report = {
        "schema_version": "agent_company.unified_agent_egress_gateway_docket.v1",
        "generated_utc": generated,
        "source_capability_registry_path": str(CAPABILITY_REGISTRY),
        "source_capability_registry_sha256": sha256_path(CAPABILITY_REGISTRY),
        "source_capability_validation_path": str(CAPABILITY_VALIDATION),
        "source_capability_class_count": len(classes),
        "route_count": len(routes),
        "gate_index": gate_index,
        "gateway_routes": routes,
        "gateway_decisions": [
            "all_live_egress_routes_remain_report_only",
            "agent_egress_event_ledger_is_required_for_every_route",
            "route_specific_gates_must_pass_before_signed_operator_decision_intake",
            "gateway_start_is_not_registration_and_neither_is_allowed_here",
            "public_account_wallet_payment_model_mcp_browser_and_runtime_paths_are_separate_routes",
        ],
        "next_action": "Build signed operator decision intake for one exact egress route before any gateway registration, gateway start, or live egress.",
        **ZERO_BOUNDARY,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.unified_agent_egress_gateway_docket_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "source_capability_registry_path": str(CAPABILITY_REGISTRY),
        "source_capability_class_count": len(classes),
        "route_count": len(routes),
        "required_gate_count": len(gate_index),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Unified Agent Egress Gateway Docket v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Source capability registry: `{CAPABILITY_REGISTRY}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Capability classes: `{validation['source_capability_class_count']}`",
        f"- Gateway routes: `{validation['route_count']}`",
        f"- Required gates indexed: `{validation['required_gate_count']}`",
        f"- Gateway registration allowed: `{validation['gateway_registration_allowed']}`",
        f"- Gateway start allowed: `{validation['gateway_start_allowed']}`",
        f"- Live egress allowed: `{validation['live_egress_allowed']}`",
        f"- Worker starts: `{validation['worker_start_allowed']}`",
        f"- Runtime starts: `{validation['runtime_start_allowed']}`",
        f"- Browser session starts: `{validation['browser_session_start_allowed']}`",
        f"- Model/API calls: `{validation['model_api_calls']}`",
        f"- MCP tool calls: `{validation['mcp_tool_calls']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Route Table",
        "",
        "| Route | Egress Type | Capability Classes | Required Gates | Blocked Actions |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["gateway_routes"]:
        lines.append(
            f"| `{item['route_id']}` | `{item['egress_type']}` | {', '.join(f'`{x}`' for x in item['capability_class_ids'])} | {', '.join(f'`{x}`' for x in item['required_gates'])} | {', '.join(f'`{x}`' for x in item['blocked_actions'])} |"
        )
    lines.extend(
        [
            "",
            "## Gateway Decisions",
            "",
        ]
    )
    for decision in report["gateway_decisions"]:
        lines.append(f"- `{decision}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This docket does not register, start, or configure an egress gateway. It is a route map and gate index for future signed operator decisions.",
            "",
            f"Next action: {report['next_action']}",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    report, validation = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(
        json.dumps(
            {
                "ok": validation["all_checks_passed"],
                "report_path": str(REPORT_JSON),
                "validation_path": str(VALIDATION_JSON),
                "route_count": validation["route_count"],
                "failure_count": validation["failure_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
