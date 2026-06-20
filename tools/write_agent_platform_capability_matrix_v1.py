#!/usr/bin/env python3
"""Write a local agent-platform capability matrix from Wave 11 radar evidence."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
SOURCE_RADAR = DATA / "agent-company-current-source-radar-wave11-20260617.json"
CHAIN_VALIDATION = REPORTS / "service-worker-chain-integrity-validation-latest.json"
GATE_MAP_VALIDATION = REPORTS / "service-worker-gate-map-validation-latest.json"
RUNTIME_PREFLIGHT_VALIDATION = REPORTS / "durable-orchestration" / "runtime-implementation-apply-preflight-blocker-v1-validation-20260617.json"
JSON_OUT = REPORTS / "agent-platform-capability-matrix-v1-20260617.json"
CSV_OUT = REPORTS / "agent-platform-capability-matrix-v1-20260617.csv"
MD_OUT = REPORTS / "agent-platform-capability-matrix-v1-20260617.md"
VALIDATION_OUT = REPORTS / "agent-platform-capability-matrix-v1-validation-20260617.json"

CAPABILITY_WEIGHTS = {
    "control_plane_fit": 5,
    "service_worker_fit": 4,
    "sandbox_fit": 4,
    "observability_fit": 3,
    "workflow_fit": 3,
    "local_pattern_value": 3,
    "credential_or_public_action_risk": -4,
    "runtime_install_pressure": -3,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def score_row(row: dict[str, Any]) -> dict[str, Any]:
    category = row["category"]
    decision = row["local_decision"]
    gate = row["risk_gate"]
    capability = {
        "control_plane_fit": 0,
        "service_worker_fit": 0,
        "sandbox_fit": 0,
        "observability_fit": 0,
        "workflow_fit": 0,
        "local_pattern_value": 2,
        "credential_or_public_action_risk": 0,
        "runtime_install_pressure": 0,
    }
    if category == "agent_platform_control_plane":
        capability.update({"control_plane_fit": 3, "observability_fit": 2, "workflow_fit": 2, "local_pattern_value": 3})
    elif category == "production_agent_harness":
        capability.update({"control_plane_fit": 2, "service_worker_fit": 2, "observability_fit": 1, "local_pattern_value": 3})
    elif category == "typescript_agent_ops_platform":
        capability.update({"control_plane_fit": 2, "observability_fit": 3, "workflow_fit": 2, "local_pattern_value": 3, "runtime_install_pressure": 1})
    elif category == "typescript_agent_app_framework":
        capability.update({"workflow_fit": 2, "observability_fit": 1, "local_pattern_value": 2, "runtime_install_pressure": 2})
    elif category == "workflow_automation":
        capability.update({"service_worker_fit": 3, "workflow_fit": 3, "local_pattern_value": 3, "credential_or_public_action_risk": 3, "runtime_install_pressure": 2})
    elif category == "agent_app_builder":
        capability.update({"service_worker_fit": 2, "workflow_fit": 2, "local_pattern_value": 3, "credential_or_public_action_risk": 2, "runtime_install_pressure": 2})
    elif category == "coding_agent_harness":
        capability.update({"service_worker_fit": 3, "sandbox_fit": 3, "observability_fit": 1, "local_pattern_value": 3, "credential_or_public_action_risk": 2, "runtime_install_pressure": 2})
    elif category == "sandbox_execution":
        capability.update({"service_worker_fit": 2, "sandbox_fit": 3, "local_pattern_value": 3, "credential_or_public_action_risk": 2, "runtime_install_pressure": 2})

    if "no_credentials" in gate or "no_api_keys" in gate:
        capability["credential_or_public_action_risk"] = max(capability["credential_or_public_action_risk"], 2)
    if "no_public" in gate or "no_pr_public_action" in gate:
        capability["credential_or_public_action_risk"] = max(capability["credential_or_public_action_risk"], 2)
    if "no_dependency_install" in gate or "no_node_install" in gate or "no_sdk_install" in gate:
        capability["runtime_install_pressure"] = max(capability["runtime_install_pressure"], 2)
    if "reference" in decision or "pattern" in decision or "study" in decision:
        capability["local_pattern_value"] = 3

    weighted_score = sum(CAPABILITY_WEIGHTS[key] * value for key, value in capability.items())
    adoption_bonus = min(int(row["stars"]) // 25000, 5)
    recency_bonus = int(row.get("recency_score", 0))
    final_score = weighted_score + adoption_bonus + recency_bonus
    if capability["control_plane_fit"] >= 3:
        recommended_posture = "promote_to_control_plane_pattern_matrix"
    elif capability["sandbox_fit"] >= 3:
        recommended_posture = "promote_to_sandbox_gate_contract"
    elif capability["credential_or_public_action_risk"] >= 3:
        recommended_posture = "pattern_only_high_side_effect_risk"
    elif capability["runtime_install_pressure"] >= 2:
        recommended_posture = "pattern_only_until_dependency_review"
    else:
        recommended_posture = "watch_as_pattern_source"

    return {
        **row,
        "capabilities": capability,
        "weighted_score": weighted_score,
        "adoption_bonus": adoption_bonus,
        "recency_bonus": recency_bonus,
        "final_score": final_score,
        "recommended_posture": recommended_posture,
    }


def local_baseline(chain: dict[str, Any], gate: dict[str, Any], preflight: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": "agent_company_sqlite_control_plane",
        "control_plane_fit": 3,
        "service_worker_fit": 3,
        "sandbox_fit": 0,
        "observability_fit": 2,
        "workflow_fit": 2,
        "local_pattern_value": 3,
        "credential_or_public_action_risk": 0,
        "runtime_install_pressure": 0,
        "chain_integrity_checked_report_count": chain.get("checked_report_count"),
        "gate_map_human_review_count": gate.get("gate_counts", {}).get("human_cro_approval_required"),
        "runtime_apply_allowed": preflight.get("apply_allowed"),
        "note": "Current local source of truth: task/evidence/artifact/trace/outcome ledger plus service-worker gate maps and runtime preflight blockers.",
    }


def build_payload() -> dict[str, Any]:
    radar = load_json(SOURCE_RADAR)
    chain = load_json(CHAIN_VALIDATION)
    gate = load_json(GATE_MAP_VALIDATION)
    preflight = load_json(RUNTIME_PREFLIGHT_VALIDATION)
    rows = sorted([score_row(row) for row in radar["rows"]], key=lambda item: item["final_score"], reverse=True)
    return {
        "schema_version": "agent_company.agent_platform_capability_matrix.v1",
        "generated_utc": utc_now(),
        "task_id": "task-agent-platform-capability-matrix-v1-20260617",
        "lane_id": "platform_engineering",
        "source_radar_path": str(SOURCE_RADAR),
        "source_repo_count": radar.get("repo_count"),
        "rate_limited_repo_count": radar.get("rate_limited_repo_count"),
        "local_baseline": local_baseline(chain, gate, preflight),
        "capability_weights": CAPABILITY_WEIGHTS,
        "rows": rows,
        "recommended_next_builds": [
            {
                "id": "sandbox_execution_gate_contract_v1",
                "reason": "OpenHands and E2B score highly for future code-worker lanes, but only after local sandbox limits for filesystem, network, secrets, cost, teardown, and proof capture exist.",
            },
            {
                "id": "workflow_automation_service_worker_manifest_v1",
                "reason": "n8n, Activepieces, Dify, Langflow, and Flowise have high adoption but require credential/public-action gates before any execution.",
            },
            {
                "id": "agent_platform_control_plane_gap_map_v1",
                "reason": "Agno/VoltAgent/Strands expose useful scheduling, RBAC, tracing, intervention, and ops-console ideas to compare against the SQLite CEO ledger.",
            },
        ],
        "hold_until_gated": [
            "dependency installs/imports",
            "runtime or server starts",
            "workflow/connector execution",
            "credentials/API keys/secrets",
            "browser sessions",
            "public actions or PR/comment/submission flows",
            "cloud sandbox start or billable execution",
            "service_request mutation",
        ],
        "runtime_boundary": {
            "browser_sessions_started": 0,
            "account_actions": False,
            "wallet_actions": False,
            "payment_actions": False,
            "public_actions": False,
            "security_testing_actions": False,
            "real_money_actions": False,
            "model_api_calls": False,
            "dependency_installs": 0,
            "dependency_imports": 0,
            "runtime_starts": 0,
            "service_requests_updated": 0,
            "service_requests_assigned": 0,
            "worker_starts": 0,
            "external_side_effects": False,
        },
    }


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if payload["source_repo_count"] != 11:
        failures.append("source_repo_count_not_11")
    if len(payload["rows"]) != 11:
        failures.append("matrix_row_count_not_11")
    if payload["local_baseline"].get("runtime_apply_allowed") is not False:
        failures.append("runtime_apply_preflight_not_blocked")
    if len(payload["recommended_next_builds"]) != 3:
        failures.append("recommended_next_build_count_not_3")
    postures = {row["recommended_posture"] for row in payload["rows"]}
    for expected in ["pattern_only_high_side_effect_risk", "promote_to_control_plane_pattern_matrix", "promote_to_sandbox_gate_contract"]:
        if expected not in postures:
            failures.append(f"missing_posture:{expected}")
    for key, value in payload["runtime_boundary"].items():
        if value not in (0, False):
            failures.append(f"runtime_boundary_nonzero:{key}")
    return {
        "schema_version": "agent_company.agent_platform_capability_matrix_validation.v1",
        "generated_utc": utc_now(),
        "matrix_path": str(JSON_OUT),
        "markdown_path": str(MD_OUT),
        "csv_path": str(CSV_OUT),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "matrix_row_count": len(payload["rows"]),
        "source_repo_count": payload["source_repo_count"],
        "rate_limited_repo_count": payload["rate_limited_repo_count"],
        "recommended_next_build_count": len(payload["recommended_next_builds"]),
        "runtime_apply_allowed": payload["local_baseline"].get("runtime_apply_allowed"),
        "dependency_installs": 0,
        "dependency_imports": 0,
        "runtime_starts": 0,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "browser_sessions_started": 0,
        "model_api_calls": False,
        "api_calls": False,
        "external_side_effects": False,
        "failures": failures,
    }


def write_csv(rows: list[dict[str, Any]]) -> None:
    fields = [
        "final_score",
        "recommended_posture",
        "category",
        "full_name",
        "stars",
        "pushed_at",
        "local_decision",
        "risk_gate",
        "html_url",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def write_markdown(payload: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Agent Platform Capability Matrix v1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Task: `{payload['task_id']}`",
        f"Source radar: `{SOURCE_RADAR}`",
        f"Matrix JSON: `{JSON_OUT}`",
        f"CSV: `{CSV_OUT}`",
        f"Validation: `{VALIDATION_OUT}`",
        "",
        "## Summary",
        "",
        f"- Source repo rows: `{payload['source_repo_count']}`",
        f"- Matrix rows: `{validation['matrix_row_count']}`",
        f"- Rate-limited follow-ups preserved: `{payload['rate_limited_repo_count']}`",
        f"- Local runtime apply allowed: `{payload['local_baseline']['runtime_apply_allowed']}`",
        f"- Validation failures: `{validation['failure_count']}`",
        "",
        "## Local Baseline",
        "",
        f"- Current company brain: `{payload['local_baseline']['name']}`",
        f"- Chain integrity layers checked: `{payload['local_baseline']['chain_integrity_checked_report_count']}`",
        f"- Human/CRO-gated service requests: `{payload['local_baseline']['gate_map_human_review_count']}`",
        f"- Note: {payload['local_baseline']['note']}",
        "",
        "## Ranked Matrix",
        "",
        "| Score | Posture | Category | Repo | Stars | Why |",
        "| ---: | --- | --- | --- | ---: | --- |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| `{row['final_score']}` | `{row['recommended_posture']}` | `{row['category']}` | [{row['full_name']}]({row['html_url']}) | `{row['stars']}` | {row['why_it_matters']} |"
        )
    lines.extend(["", "## Recommended Next Builds", "", "| Build | Reason |", "| --- | --- |"])
    for item in payload["recommended_next_builds"]:
        lines.append(f"| `{item['id']}` | {item['reason']} |")
    lines.extend(["", "## Hold Until Gated", ""])
    for item in payload["hold_until_gated"]:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This matrix is local and report-only.",
            "- It performs no dependency install/import, runtime/server start, workflow execution, credential/API-key use, browser session, public action, cloud sandbox start, service-request mutation, worker start, model/API call, payment, wallet, security-testing, real-money action, or external side effect.",
        ]
    )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    payload = build_payload()
    validation = validate_payload(payload)
    JSON_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_csv(payload["rows"])
    VALIDATION_OUT.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(payload, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "report": str(MD_OUT)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
