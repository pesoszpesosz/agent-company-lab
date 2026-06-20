#!/usr/bin/env python3
"""Write a report-only worker capability class registry from the runtime adoption docket."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SOURCE_DOCKET = REPORTS / "agent-company-runtime-adoption-docket-v1-20260618.json"
SCHEMA_PATH = ARCH / "worker-capability-class-registry-v1.schema.json"
REPORT_JSON = REPORTS / "worker-capability-class-registry-v1-20260618.json"
VALIDATION_JSON = REPORTS / "worker-capability-class-registry-v1-validation-20260618.json"
REPORT_MD = REPORTS / "worker-capability-class-registry-v1-20260618.md"

ZERO_BOUNDARY = {
    "worker_registration_allowed": False,
    "worker_start_allowed": False,
    "runtime_start_allowed": False,
    "browser_session_start_allowed": False,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "dependency_installs": 0,
    "runtime_starts": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "mcp_tool_calls": False,
    "model_api_calls": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "security_testing_actions": False,
    "telemetry_exports": 0,
    "external_side_effects": False,
}

CLASS_DEFINITIONS = {
    "browser_worker": {
        "purpose": "Read-only or explicitly approved browser automation workers.",
        "required_gates": [
            "browser_read_only_worker_policy_v1",
            "browser_worker_adapter_contract_v1",
            "browser_read_only_signed_approval_guard_v1",
            "browser_read_only_apply_preflight_blocker_v1",
            "browser_read_only_apply_command_contract_v1",
        ],
    },
    "durable_runtime": {
        "purpose": "Long-running durable execution runtimes such as Temporal or Restate.",
        "required_gates": [
            "runtime_start_preflight_v1",
            "runtime_start_signed_decision_guard_v1",
            "runtime_start_apply_preflight_blocker_v1",
            "runtime_dependency_install_preflight_v1",
        ],
    },
    "durable_workflow": {
        "purpose": "Durable workflow libraries and transactional function runners.",
        "required_gates": [
            "runtime_start_preflight_v1",
            "runtime_dependency_install_preflight_v1",
            "queue_mutation_guard_v1",
        ],
    },
    "gateway_or_mcp": {
        "purpose": "MCP/A2A/tool/model gateway and registry workers.",
        "required_gates": [
            "mcp_tool_registry_gate_v1",
            "agent_egress_event_ledger_v1",
            "unified_agent_egress_gateway_docket_v1",
        ],
    },
    "agent_framework": {
        "purpose": "Agent orchestration frameworks used as architecture references before dependency adoption.",
        "required_gates": [
            "runtime_dependency_install_preflight_v1",
            "model_api_execution_gate",
            "runtime_start_preflight_v1",
        ],
    },
    "model_backed_agent_framework": {
        "purpose": "Agent frameworks that require model/provider/cost/secret scopes before execution.",
        "required_gates": [
            "model_api_execution_gate",
            "secrets_credentials_handling_gate",
            "runtime_dependency_install_preflight_v1",
            "runtime_start_preflight_v1",
        ],
    },
    "workflow_platform": {
        "purpose": "Workflow platforms that can mutate queues, credentials, accounts, or public actions.",
        "required_gates": [
            "runtime_start_preflight_v1",
            "runtime_dependency_install_preflight_v1",
            "service_request_queue_mutation_guard_v1",
            "secrets_credentials_handling_gate",
        ],
    },
    "platform_runtime": {
        "purpose": "Full app platforms requiring Docker/cloud/plugin/account boundaries.",
        "required_gates": [
            "runtime_start_preflight_v1",
            "legal_kyc_tax_payment_gate",
            "secrets_credentials_handling_gate",
            "public_action_execution_gate",
        ],
    },
    "observability": {
        "purpose": "Trace, eval, dashboard, and telemetry systems for CEO memory.",
        "required_gates": [
            "telemetry_privacy_export_gate_v1",
            "runtime_dependency_install_preflight_v1",
            "agent_egress_event_ledger_v1",
        ],
    },
    "unknown_or_mixed": {
        "purpose": "Mixed or unclear projects requiring manual architecture review.",
        "required_gates": [
            "manual_architecture_review_required",
            "chief_risk_officer_review",
        ],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report() -> tuple[dict[str, Any], dict[str, Any]]:
    docket_report = load_json(SOURCE_DOCKET)
    schema = load_json(SCHEMA_PATH)
    docket_items = docket_report.get("docket", [])
    by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in docket_items:
        by_class[item.get("worker_class", "unknown_or_mixed")].append(item)

    capability_classes = []
    failures: list[str] = []
    for class_id in sorted(by_class):
        definition = CLASS_DEFINITIONS.get(class_id, CLASS_DEFINITIONS["unknown_or_mixed"])
        repos = [item["repo"] for item in by_class[class_id]]
        capability_classes.append(
            {
                "capability_class_id": class_id,
                "purpose": definition["purpose"],
                "repo_count": len(repos),
                "repos": repos,
                "dispositions": sorted(set(item["disposition"] for item in by_class[class_id])),
                "required_gates": definition["required_gates"],
                "worker_registration_allowed": False,
                "worker_start_allowed": False,
                "runtime_start_allowed": False,
                "browser_session_start_allowed": False,
                "service_request_assignment_allowed": False,
                "next_action": "Create an exact operator decision packet before registration or start can be considered.",
            }
        )

    mapped_repos = {repo for cls in capability_classes for repo in cls["repos"]}
    source_repos = {item.get("repo") for item in docket_items}
    unmapped = sorted(source_repos - mapped_repos)

    if schema.get("properties", {}).get("worker_registration_allowed", {}).get("const") is not False:
        failures.append("schema_worker_registration_allowed_must_const_false")
    if len(docket_items) < 20:
        failures.append("source_docket_item_count_below_20")
    if len(capability_classes) < 8:
        failures.append("capability_class_count_below_8")
    if unmapped:
        failures.append("unmapped_docket_items:" + ",".join(unmapped))
    for item in capability_classes:
        if len(item["required_gates"]) < 2:
            failures.append(f"capability_class_missing_required_gates:{item['capability_class_id']}")
        if item["worker_registration_allowed"] or item["worker_start_allowed"] or item["runtime_start_allowed"]:
            failures.append(f"capability_class_leaks_start_authority:{item['capability_class_id']}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.worker_capability_class_registry.v1",
        "generated_utc": generated,
        "source_runtime_adoption_docket_path": str(SOURCE_DOCKET),
        "source_runtime_adoption_docket_sha256": sha256_path(SOURCE_DOCKET),
        "schema_path": str(SCHEMA_PATH),
        "source_docket_item_count": len(docket_items),
        "capability_class_count": len(capability_classes),
        "unmapped_docket_items": unmapped,
        "unmapped_docket_item_count": len(unmapped),
        "capability_classes": capability_classes,
        "next_action": "Build unified_agent_egress_gateway_docket_v1 before registering or starting any worker capability class.",
        **ZERO_BOUNDARY,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.worker_capability_class_registry_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "source_docket_item_count": len(docket_items),
        "capability_class_count": len(capability_classes),
        "unmapped_docket_item_count": len(unmapped),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Worker Capability Class Registry v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Source docket: `{SOURCE_DOCKET}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Source docket items: `{validation['source_docket_item_count']}`",
        f"- Capability classes: `{validation['capability_class_count']}`",
        f"- Unmapped docket items: `{validation['unmapped_docket_item_count']}`",
        f"- Worker registration allowed: `{validation['worker_registration_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- Runtime start allowed: `{validation['runtime_start_allowed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Capability Classes",
        "",
        "| Class | Repos | Required Gates |",
        "| --- | ---: | --- |",
    ]
    for item in report["capability_classes"]:
        lines.append(
            f"| `{item['capability_class_id']}` | `{item['repo_count']}` | {'; '.join(f'`{gate}`' for gate in item['required_gates'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This registry is report-only.",
            "- It registers no worker pool and starts no worker.",
            "- It starts no runtime, browser session, MCP server, model/API call, telemetry export, public action, wallet/payment action, or service-request assignment.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    report, validation = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
