#!/usr/bin/env python3
"""Write a report-only runtime adoption docket from open-source stack radar wave 19."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

SOURCE_DATASET = DATA / "agent-company-open-source-stack-radar-wave19-20260618.json"
SCHEMA_PATH = ARCH / "agent-company-runtime-adoption-docket-v1.schema.json"
REPORT_JSON = REPORTS / "agent-company-runtime-adoption-docket-v1-20260618.json"
VALIDATION_JSON = REPORTS / "agent-company-runtime-adoption-docket-v1-validation-20260618.json"
REPORT_MD = REPORTS / "agent-company-runtime-adoption-docket-v1-20260618.md"

ZERO_BOUNDARY = {
    "adoption_allowed": False,
    "dependency_installs": 0,
    "runtime_starts": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify(row: dict[str, Any]) -> dict[str, Any]:
    category = row.get("category", "")
    repo = row.get("repo", "")
    gate = row.get("gate", "")

    if "browser" in category:
        disposition = "adapter_candidate"
        worker_class = "browser_worker"
        next_gate = "browser_worker_adapter_contract_plus_signed_approval_plus_apply_preflight"
    elif "gateway" in category or "mcp" in category:
        disposition = "reference_only"
        worker_class = "gateway_or_mcp"
        next_gate = "mcp_registry_egress_gateway_and_signed_operator_decision"
    elif "durable_execution_runtime" in category or repo in {"temporalio/temporal", "restatedev/restate"}:
        disposition = "future_runtime_candidate"
        worker_class = "durable_runtime"
        next_gate = "runtime_start_preflight_signed_decision_and_dependency_install_gate"
    elif repo in {"microsoft/agent-framework", "openai/openai-agents-python", "google/adk-python"}:
        disposition = "blocked_dependency"
        worker_class = "model_backed_agent_framework"
        next_gate = "model_api_provider_cost_dependency_install_runtime_start_and_secrets_gates"
    elif repo in {"langchain-ai/langgraph", "crewAIInc/crewAI", "microsoft/autogen", "pydantic/pydantic-ai"}:
        disposition = "reference_only"
        worker_class = "agent_framework"
        next_gate = "model_api_dependency_install_runtime_start_and_secrets_gates"
    elif repo in {"dbos-inc/dbos-transact-py"}:
        disposition = "future_runtime_candidate"
        worker_class = "durable_workflow"
        next_gate = "runtime_start_preflight_dependency_install_gate_and_queue_mutation_guard"
    elif "workflow" in category or repo in {"hatchet-dev/hatchet", "inngest/inngest", "PrefectHQ/prefect"}:
        disposition = "blocked_dependency"
        worker_class = "workflow_platform"
        next_gate = "runtime_start_preflight_dependency_install_gate_queue_mutation_guard_and_signed_operator_decision"
    elif "observability" in category or "eval" in category:
        disposition = "reference_only"
        worker_class = "observability"
        next_gate = "telemetry_privacy_dependency_install_and_export_gate"
    elif "app_platform" in category or "workflow_automation" in category:
        disposition = "blocked_dependency"
        worker_class = "platform_runtime"
        next_gate = "docker_cloud_account_credentials_plugin_and_public_action_gates"
    else:
        disposition = "blocked_dependency"
        worker_class = "unknown_or_mixed"
        next_gate = "manual_architecture_review_required"

    if "cloud" in gate or "api_key" in gate or "payment" in gate or "credential" in gate:
        risk_level = "high"
    elif "runtime" in gate or "install" in gate or "model" in gate:
        risk_level = "medium"
    else:
        risk_level = "medium"

    return {
        "rank": row.get("rank"),
        "repo": repo,
        "category": category,
        "stars": row.get("stars"),
        "pushed_at": row.get("pushed_at"),
        "evidence_score": row.get("evidence_score"),
        "disposition": disposition,
        "worker_class": worker_class,
        "risk_level": risk_level,
        "local_decision": row.get("decision"),
        "source_gate": gate,
        "next_gate": next_gate,
        "adoption_allowed": False,
        "dependency_install_allowed": False,
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        "notes": "Use as architecture evidence only until the named gate is satisfied.",
    }


def build_report() -> tuple[dict[str, Any], dict[str, Any]]:
    source = load_json(SOURCE_DATASET)
    schema = load_json(SCHEMA_PATH)
    rows = source.get("rows", [])
    docket = [classify(row) for row in rows]
    counts = Counter(item["disposition"] for item in docket)
    worker_counts = Counter(item["worker_class"] for item in docket)
    failures: list[str] = []

    if schema.get("properties", {}).get("adoption_allowed", {}).get("const") is not False:
        failures.append("schema_adoption_allowed_must_const_false")
    if len(rows) < 20:
        failures.append("source_candidate_count_below_20")
    if len(docket) != len(rows):
        failures.append("docket_item_count_mismatch")
    if counts["reference_only"] < 10:
        failures.append("reference_only_count_below_10")
    if counts["adapter_candidate"] < 3:
        failures.append("adapter_candidate_count_below_3")
    if counts["blocked_dependency"] < 2:
        failures.append("blocked_dependency_count_below_2")
    if counts["future_runtime_candidate"] < 3:
        failures.append("future_runtime_candidate_count_below_3")
    for item in docket:
        if item["adoption_allowed"] or item["dependency_install_allowed"] or item["runtime_start_allowed"] or item["worker_start_allowed"]:
            failures.append(f"adoption_authority_leaked:{item['repo']}")

    top_adapter_candidates = [item["repo"] for item in docket if item["disposition"] == "adapter_candidate"][:8]
    future_runtime_candidates = [item["repo"] for item in docket if item["disposition"] == "future_runtime_candidate"]
    gateway_candidates = [item["repo"] for item in docket if item["worker_class"] == "gateway_or_mcp"]

    generated = utc_now()
    report = {
        "schema_version": "agent_company.runtime_adoption_docket.v1",
        "generated_utc": generated,
        "source_radar_dataset_path": str(SOURCE_DATASET),
        "source_radar_dataset_sha256": sha256_path(SOURCE_DATASET),
        "schema_path": str(SCHEMA_PATH),
        "source_candidate_count": len(rows),
        "docket_item_count": len(docket),
        "disposition_counts": dict(counts),
        "worker_class_counts": dict(worker_counts),
        "reference_only_count": counts["reference_only"],
        "adapter_candidate_count": counts["adapter_candidate"],
        "blocked_dependency_count": counts["blocked_dependency"],
        "future_runtime_candidate_count": counts["future_runtime_candidate"],
        "top_adapter_candidates": top_adapter_candidates,
        "future_runtime_candidates": future_runtime_candidates,
        "gateway_candidates": gateway_candidates,
        "docket": docket,
        "architecture_decisions": [
            "sqlite_control_plane_remains_authority",
            "external_frameworks_are_reference_or_adapter_candidates_before_dependencies",
            "runtime_dependency_install_requires_signed_operator_decision",
            "worker_classes_must_split_by_capability_and_risk",
            "observability_candidates_feed_ceo_replay_not_live_telemetry_yet",
        ],
        "next_action": "Build worker_capability_class_registry_v1 before any dependency install or runtime adoption.",
        **ZERO_BOUNDARY,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.runtime_adoption_docket_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "source_candidate_count": len(rows),
        "docket_item_count": len(docket),
        "reference_only_count": counts["reference_only"],
        "adapter_candidate_count": counts["adapter_candidate"],
        "blocked_dependency_count": counts["blocked_dependency"],
        "future_runtime_candidate_count": counts["future_runtime_candidate"],
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Agent Company Runtime Adoption Docket v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Source radar dataset: `{SOURCE_DATASET}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Source candidates: `{validation['source_candidate_count']}`",
        f"- Docket items: `{validation['docket_item_count']}`",
        f"- Reference only: `{validation['reference_only_count']}`",
        f"- Adapter candidates: `{validation['adapter_candidate_count']}`",
        f"- Future runtime candidates: `{validation['future_runtime_candidate_count']}`",
        f"- Blocked dependencies: `{validation['blocked_dependency_count']}`",
        f"- Adoption allowed: `{validation['adoption_allowed']}`",
        f"- Runtime starts: `{validation['runtime_starts']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Top Adapter Candidates",
        "",
    ]
    for repo in report["top_adapter_candidates"]:
        lines.append(f"- `{repo}`")
    lines.extend(["", "## Future Runtime Candidates", ""])
    for repo in report["future_runtime_candidates"]:
        lines.append(f"- `{repo}`")
    lines.extend(
        [
            "",
            "## Docket",
            "",
            "| Rank | Repo | Disposition | Worker Class | Risk | Next Gate |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for item in report["docket"]:
        lines.append(
            f"| `{item['rank']}` | `{item['repo']}` | `{item['disposition']}` | `{item['worker_class']}` | `{item['risk_level']}` | `{item['next_gate']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This docket is report-only.",
            "- No dependency is installed or imported.",
            "- No runtime, worker, browser, MCP server, model/API call, telemetry export, service request assignment, public action, wallet/payment action, or external side effect is allowed.",
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
