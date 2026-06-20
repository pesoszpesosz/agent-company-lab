#!/usr/bin/env python3
"""Generate a report-only CEO dispatch batch from the agent task DAG."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "ceo-dispatch-batch-v1.schema.json"
SOURCE_DAG = REPORTS / "agent-task-dag-contract-v1-20260617.json"
SOURCE_DAG_VALIDATION = REPORTS / "agent-task-dag-contract-v1-validation-20260617.json"
JSON_OUT = REPORTS / "ceo-dispatch-batch-v1-20260617.json"
MD_OUT = REPORTS / "ceo-dispatch-batch-v1-20260617.md"
VALIDATION_OUT = REPORTS / "ceo-dispatch-batch-v1-validation-20260617.json"

TASK_ID = "task-ceo-dispatch-batch-v1-20260617"
OWNER_AGENT_ID = "recovered-profitable-edge-infra"
BATCH_ID = "dispatch-agent-company-scaleout-v1-20260617"


COMPLETED_FOUNDATION = {
    "node-ceo-intake",
    "node-source-radar",
    "node-dag-contract",
}

READY_LOCAL = {
    "node-digital-product-proof",
    "node-worker-pool-preflight",
}

WAITING = {
    "node-ceo-synthesis",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dependency_status(node_id: str, inbound: dict[str, list[str]], status_by_node: dict[str, str]) -> str:
    deps = inbound.get(node_id, [])
    if not deps:
        return "no_dependencies"
    complete_like = {"completed_foundation", "ready_local_dispatch"}
    unresolved = [dep for dep in deps if status_by_node.get(dep) not in complete_like]
    if not unresolved:
        return "dependencies_clear_for_report_only_dispatch"
    return "waiting_on:" + ",".join(unresolved)


def classify_node(node: dict[str, Any]) -> str:
    node_id = node["node_id"]
    if node_id in COMPLETED_FOUNDATION:
        return "completed_foundation"
    if node_id in READY_LOCAL:
        return "ready_local_dispatch"
    if node_id in WAITING:
        return "waiting_on_dependencies"
    if node["status"] == "blocked_by_gate":
        return "blocked_by_gate"
    return "waiting_on_dependencies"


def recommended_action(node: dict[str, Any], dispatch_status: str) -> str:
    node_id = node["node_id"]
    if dispatch_status == "completed_foundation":
        return "Keep as foundation evidence; do not redispatch."
    if node_id == "node-digital-product-proof":
        return "Create a local private-review task packet for the Agent Skill Starter Kit package; no marketplace listing or account action."
    if node_id == "node-worker-pool-preflight":
        return "Run local assignment/pool/readiness preflight against existing reports; do not register pools or assign workers."
    if node_id == "node-ceo-synthesis":
        return "Wait for local dispatch artifacts and gate packets, then synthesize the next DAG revision."
    if dispatch_status == "blocked_by_gate":
        return "Prepare exact-scope decision packet only; do not approve, assign, start, browse, post, submit, trade, or register."
    return "Hold until dependencies produce required evidence."


def build_batch() -> dict[str, Any]:
    dag = load_json(SOURCE_DAG)
    dag_validation = load_json(SOURCE_DAG_VALIDATION)
    if not dag_validation.get("all_checks_passed"):
        raise SystemExit("source DAG validation is not passing")
    status_by_node = {node["node_id"]: classify_node(node) for node in dag["nodes"]}
    inbound: dict[str, list[str]] = {node["node_id"]: [] for node in dag["nodes"]}
    for edge in dag["edges"]:
        inbound.setdefault(edge["to"], []).append(edge["from"])
    entries = []
    for rank, node in enumerate(dag["nodes"], start=1):
        dispatch_status = status_by_node[node["node_id"]]
        entries.append(
            {
                "dispatch_id": f"dispatch-node-{node['node_id'].removeprefix('node-')}",
                "node_id": node["node_id"],
                "lane_id": node["lane_id"],
                "agent_role": node["agent_role"],
                "dispatch_status": dispatch_status,
                "rank": rank,
                "title": node["title"],
                "dependency_status": dependency_status(node["node_id"], inbound, status_by_node),
                "required_gate": node["risk_gate"],
                "recommended_action": recommended_action(node, dispatch_status),
                "expected_artifacts": node["outputs"],
                "prohibited_actions": node["prohibited_actions"],
            }
        )
    counts = Counter(entry["dispatch_status"] for entry in entries)
    return {
        "schema_version": "agent_company.ceo_dispatch_batch.v1",
        "batch_id": BATCH_ID,
        "generated_utc": utc_now(),
        "source_dag_id": dag["dag_id"],
        "source_contract_path": str(SOURCE_DAG),
        "owner_agent_id": OWNER_AGENT_ID,
        "entries": entries,
        "summary": {
            "entry_count": len(entries),
            "completed_foundation_count": counts["completed_foundation"],
            "ready_local_dispatch_count": counts["ready_local_dispatch"],
            "blocked_by_gate_count": counts["blocked_by_gate"],
            "waiting_on_dependencies_count": counts["waiting_on_dependencies"],
            "first_local_dispatch_ids": [
                entry["dispatch_id"] for entry in entries if entry["dispatch_status"] == "ready_local_dispatch"
            ],
            "first_gate_packet_ids": [
                entry["dispatch_id"] for entry in entries if entry["dispatch_status"] == "blocked_by_gate"
            ],
        },
        "runtime_boundary": {
            "report_only": True,
            "creates_tasks": False,
            "approves_actions": False,
            "starts_workers": False,
            "updates_service_requests": False,
            "calls_apis": False,
            "external_side_effects": False,
        },
    }


def validate_batch(batch: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    entries = batch["entries"]
    entry_ids = [entry["dispatch_id"] for entry in entries]
    if len(entry_ids) != len(set(entry_ids)):
        failures.append("duplicate_dispatch_id")
    summary = batch["summary"]
    actual_counts = Counter(entry["dispatch_status"] for entry in entries)
    expected_counts = {
        "completed_foundation_count": 3,
        "ready_local_dispatch_count": 2,
        "blocked_by_gate_count": 4,
        "waiting_on_dependencies_count": 1,
    }
    if summary["entry_count"] != 10:
        failures.append(f"entry_count_expected_10_got_{summary['entry_count']}")
    for key, expected in expected_counts.items():
        status = key.removesuffix("_count")
        actual = actual_counts[status]
        if summary[key] != expected or actual != expected:
            failures.append(f"{key}_expected_{expected}_got_summary_{summary[key]}_actual_{actual}")
    if len(summary["first_local_dispatch_ids"]) != 2:
        failures.append("first_local_dispatch_count_expected_2")
    if len(summary["first_gate_packet_ids"]) != 4:
        failures.append("first_gate_packet_count_expected_4")
    for entry in entries:
        prohibited_text = " ".join(entry["prohibited_actions"])
        for required in [
            "register_accounts",
            "create_or_control_wallet",
            "submit_public_post_or_comment",
            "place_real_money_trade",
            "start_external_runtime_or_browser_worker",
        ]:
            if required not in prohibited_text:
                failures.append(f"dispatch_missing_prohibition:{entry['dispatch_id']}:{required}")
        if entry["dispatch_status"] == "blocked_by_gate" and "gate" not in entry["required_gate"]:
            failures.append(f"blocked_dispatch_gate_label_weak:{entry['dispatch_id']}")
        if entry["dispatch_status"] == "ready_local_dispatch" and "local" not in entry["required_gate"]:
            failures.append(f"ready_dispatch_not_local:{entry['dispatch_id']}")
    for key, value in batch["runtime_boundary"].items():
        if key == "report_only":
            if value is not True:
                failures.append("runtime_boundary_report_only_not_true")
        elif value is not False:
            failures.append(f"runtime_boundary_not_false:{key}")
    return {
        "schema_version": "agent_company.ceo_dispatch_batch_validation.v1",
        "generated_utc": utc_now(),
        "schema_path": str(SCHEMA_PATH),
        "source_dag_validation_path": str(SOURCE_DAG_VALIDATION),
        "json_path": str(JSON_OUT),
        "markdown_path": str(MD_OUT),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "entry_count": len(entries),
        "completed_foundation_count": summary["completed_foundation_count"],
        "ready_local_dispatch_count": summary["ready_local_dispatch_count"],
        "blocked_by_gate_count": summary["blocked_by_gate_count"],
        "waiting_on_dependencies_count": summary["waiting_on_dependencies_count"],
        "creates_tasks": False,
        "approves_actions": False,
        "starts_workers": False,
        "updates_service_requests": False,
        "calls_apis": False,
        "external_side_effects": False,
        "failures": failures,
    }


def write_markdown(batch: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# CEO Dispatch Batch v1",
        "",
        f"Generated UTC: {batch['generated_utc']}",
        f"Batch: `{batch['batch_id']}`",
        f"Task: `{TASK_ID}`",
        f"Schema: `{SCHEMA_PATH}`",
        f"Source DAG: `{SOURCE_DAG}`",
        f"JSON: `{JSON_OUT}`",
        f"Validation: `{VALIDATION_OUT}`",
        "",
        "## Summary",
        "",
        f"- Entries: `{validation['entry_count']}`",
        f"- Completed foundation: `{validation['completed_foundation_count']}`",
        f"- Ready local dispatch: `{validation['ready_local_dispatch_count']}`",
        f"- Blocked by gate: `{validation['blocked_by_gate_count']}`",
        f"- Waiting on dependencies: `{validation['waiting_on_dependencies_count']}`",
        f"- Validation failures: `{validation['failure_count']}`",
        "",
        "## Dispatch Board",
        "",
        "| Rank | Status | Node | Lane | Role | Gate | Recommended Action |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in batch["entries"]:
        lines.append(
            f"| `{entry['rank']}` | `{entry['dispatch_status']}` | `{entry['node_id']}` | `{entry['lane_id']}` | `{entry['agent_role']}` | `{entry['required_gate']}` | {entry['recommended_action']} |"
        )
    lines.extend(
        [
            "",
            "## First Local Dispatch IDs",
            "",
        ]
    )
    for dispatch_id in batch["summary"]["first_local_dispatch_ids"]:
        lines.append(f"- `{dispatch_id}`")
    lines.extend(["", "## First Gate Packet IDs", ""])
    for dispatch_id in batch["summary"]["first_gate_packet_ids"]:
        lines.append(f"- `{dispatch_id}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This batch is report-only.",
            "- It creates no tasks, approves no actions, starts no workers, updates no service requests, calls no APIs, and performs no external side effects.",
            "- Only the two `ready_local_dispatch` rows are candidates for later local task creation.",
        ]
    )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    batch = build_batch()
    validation = validate_batch(batch)
    JSON_OUT.write_text(json.dumps(batch, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_OUT.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(batch, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "report": str(MD_OUT)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
