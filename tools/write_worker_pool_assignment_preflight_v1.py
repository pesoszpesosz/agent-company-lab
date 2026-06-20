#!/usr/bin/env python3
"""Generate the local worker-pool assignment preflight for CEO dispatch."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "worker-pool-assignment-preflight-v1.schema.json"
DISPATCH_BATCH = REPORTS / "ceo-dispatch-batch-v1-20260617.json"
ASSIGNMENT_PLAN = REPORTS / "service-worker-assignment-plan-latest.json"
POOL_REGISTRY = REPORTS / "service-worker-pool-registry-latest.json"
READINESS = REPORTS / "service-worker-execution-readiness-latest.json"
GATE_MAP = REPORTS / "service-worker-gate-map-latest.json"

JSON_OUT = REPORTS / "worker-pool-assignment-preflight-v1-20260617.json"
MD_OUT = REPORTS / "worker-pool-assignment-preflight-v1-20260617.md"
VALIDATION_OUT = REPORTS / "worker-pool-assignment-preflight-v1-validation-20260617.json"

TASK_ID = "task-worker-pool-assignment-preflight-v1-20260617"
PREFLIGHT_ID = "worker-pool-preflight-agent-company-scaleout-v1-20260617"
SOURCE_DISPATCH_ID = "dispatch-node-worker-pool-preflight"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_preflight() -> dict[str, Any]:
    dispatch = load_json(DISPATCH_BATCH)
    assignment = load_json(ASSIGNMENT_PLAN)
    pool = load_json(POOL_REGISTRY)
    readiness = load_json(READINESS)
    gate_map = load_json(GATE_MAP)
    dispatch_entry = next(
        entry for entry in dispatch["entries"] if entry["dispatch_id"] == SOURCE_DISPATCH_ID
    )
    gate_counts = gate_map.get("gate_counts", {})
    summary = {
        "assignment_plan_count": int(assignment.get("planned_count", 0)),
        "assignable_now_count": int(assignment.get("assignable_now_count", 0)),
        "pool_count": int(pool.get("pool_count", 0)),
        "missing_pool_count": int(pool.get("missing_pool_count", 0)),
        "readiness_request_count": int(readiness.get("request_count", 0)),
        "ready_to_start_count": int(readiness.get("ready_to_start_count", 0)),
        "human_cro_gate_count": int(gate_counts.get("human_cro_approval_required", 0)),
        "terminal_no_execution_count": int(gate_counts.get("terminal_no_execution", 0)),
    }
    blocking_findings = [
        {
            "finding_id": "finding-no-assignable-requests",
            "severity": "blocker",
            "finding": "No service-worker request is assignable now.",
            "evidence": f"assignment_plan.assignable_now_count={summary['assignable_now_count']}",
            "required_before_worker_start": True,
        },
        {
            "finding_id": "finding-missing-worker-pools",
            "severity": "blocker",
            "finding": "All required dedicated service-worker pools are still missing.",
            "evidence": f"pool_registry.missing_pool_count={summary['missing_pool_count']} of pool_count={summary['pool_count']}",
            "required_before_worker_start": True,
        },
        {
            "finding_id": "finding-no-ready-starts",
            "severity": "blocker",
            "finding": "Execution readiness has zero requests ready to start.",
            "evidence": f"readiness.ready_to_start_count={summary['ready_to_start_count']}",
            "required_before_worker_start": True,
        },
        {
            "finding_id": "finding-human-cro-gate",
            "severity": "blocker",
            "finding": "Human/CRO approval remains the dominant gate for non-terminal service-worker requests.",
            "evidence": f"gate_map.human_cro_approval_required={summary['human_cro_gate_count']}",
            "required_before_worker_start": True,
        },
    ]
    recommended_next_actions = [
        {
            "action_id": "action-refresh-gate-chain",
            "action_type": "local_report_refresh",
            "description": "Refresh service-worker gate map, pool registry, assignment plan, readiness, and chain integrity before any human decision.",
            "allowed_now": True,
        },
        {
            "action_id": "action-draft-pool-registration-review",
            "action_type": "manual_review_packet",
            "description": "Use existing pool registration packets to decide whether to register local service-worker pool agents.",
            "allowed_now": True,
        },
        {
            "action_id": "action-assign-worker",
            "action_type": "service_request_assignment",
            "description": "Assign any service request to a worker pool.",
            "allowed_now": False,
        },
        {
            "action_id": "action-start-worker",
            "action_type": "worker_start",
            "description": "Start any browser, model/API, public-submission, wallet/payment, legal/KYC, or runtime worker.",
            "allowed_now": False,
        },
    ]
    return {
        "schema_version": "agent_company.worker_pool_assignment_preflight.v1",
        "preflight_id": PREFLIGHT_ID,
        "generated_utc": utc_now(),
        "source_dispatch_id": dispatch_entry["dispatch_id"],
        "source_reports": {
            "dispatch_batch": str(DISPATCH_BATCH),
            "assignment_plan": str(ASSIGNMENT_PLAN),
            "pool_registry": str(POOL_REGISTRY),
            "execution_readiness": str(READINESS),
            "gate_map": str(GATE_MAP),
        },
        "summary": summary,
        "blocking_findings": blocking_findings,
        "recommended_next_actions": recommended_next_actions,
        "runtime_boundary": {
            "report_only": True,
            "registers_pools": False,
            "assigns_service_requests": False,
            "starts_workers": False,
            "updates_service_requests": False,
            "calls_apis": False,
            "external_side_effects": False,
        },
    }


def validate_preflight(preflight: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    summary = preflight["summary"]
    expected = {
        "assignment_plan_count": 14,
        "assignable_now_count": 0,
        "pool_count": 7,
        "missing_pool_count": 7,
        "readiness_request_count": 14,
        "ready_to_start_count": 0,
        "human_cro_gate_count": 11,
        "terminal_no_execution_count": 3,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            failures.append(f"{key}_expected_{value}_got_{summary.get(key)}")
    blocker_count = sum(1 for item in preflight["blocking_findings"] if item["severity"] == "blocker")
    if blocker_count != 4:
        failures.append(f"blocker_count_expected_4_got_{blocker_count}")
    allowed_now_count = sum(1 for item in preflight["recommended_next_actions"] if item["allowed_now"])
    blocked_action_count = sum(1 for item in preflight["recommended_next_actions"] if not item["allowed_now"])
    if allowed_now_count != 2:
        failures.append(f"allowed_now_count_expected_2_got_{allowed_now_count}")
    if blocked_action_count != 2:
        failures.append(f"blocked_action_count_expected_2_got_{blocked_action_count}")
    for key, value in preflight["runtime_boundary"].items():
        if key == "report_only":
            if value is not True:
                failures.append("runtime_boundary_report_only_not_true")
        elif value is not False:
            failures.append(f"runtime_boundary_not_false:{key}")
    return {
        "schema_version": "agent_company.worker_pool_assignment_preflight_validation.v1",
        "generated_utc": utc_now(),
        "schema_path": str(SCHEMA_PATH),
        "json_path": str(JSON_OUT),
        "markdown_path": str(MD_OUT),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "assignment_plan_count": summary["assignment_plan_count"],
        "assignable_now_count": summary["assignable_now_count"],
        "pool_count": summary["pool_count"],
        "missing_pool_count": summary["missing_pool_count"],
        "readiness_request_count": summary["readiness_request_count"],
        "ready_to_start_count": summary["ready_to_start_count"],
        "human_cro_gate_count": summary["human_cro_gate_count"],
        "terminal_no_execution_count": summary["terminal_no_execution_count"],
        "blocker_count": blocker_count,
        "allowed_now_count": allowed_now_count,
        "blocked_action_count": blocked_action_count,
        "registers_pools": False,
        "assigns_service_requests": False,
        "starts_workers": False,
        "updates_service_requests": False,
        "calls_apis": False,
        "external_side_effects": False,
        "failures": failures,
    }


def write_markdown(preflight: dict[str, Any], validation: dict[str, Any]) -> None:
    summary = preflight["summary"]
    lines = [
        "# Worker Pool Assignment Preflight v1",
        "",
        f"Generated UTC: {preflight['generated_utc']}",
        f"Preflight: `{preflight['preflight_id']}`",
        f"Task: `{TASK_ID}`",
        f"Schema: `{SCHEMA_PATH}`",
        f"JSON: `{JSON_OUT}`",
        f"Validation: `{VALIDATION_OUT}`",
        "",
        "## Summary",
        "",
        f"- Assignment rows: `{summary['assignment_plan_count']}`",
        f"- Assignable now: `{summary['assignable_now_count']}`",
        f"- Worker pools required: `{summary['pool_count']}`",
        f"- Missing pools: `{summary['missing_pool_count']}`",
        f"- Readiness rows: `{summary['readiness_request_count']}`",
        f"- Ready to start: `{summary['ready_to_start_count']}`",
        f"- Human/CRO-gated rows: `{summary['human_cro_gate_count']}`",
        f"- Terminal no-execution rows: `{summary['terminal_no_execution_count']}`",
        f"- Validation failures: `{validation['failure_count']}`",
        "",
        "## Blocking Findings",
        "",
        "| Finding | Severity | Evidence | Required Before Start |",
        "| --- | --- | --- | --- |",
    ]
    for item in preflight["blocking_findings"]:
        lines.append(
            f"| `{item['finding_id']}` | `{item['severity']}` | {item['evidence']} | `{item['required_before_worker_start']}` |"
        )
    lines.extend(["", "## Recommended Next Actions", "", "| Action | Type | Allowed Now | Description |", "| --- | --- | --- | --- |"])
    for item in preflight["recommended_next_actions"]:
        lines.append(
            f"| `{item['action_id']}` | `{item['action_type']}` | `{item['allowed_now']}` | {item['description']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This preflight is report-only.",
            "- It registers no pools, assigns no service requests, starts no workers, updates no service requests, calls no APIs, and performs no external side effects.",
        ]
    )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    preflight = build_preflight()
    validation = validate_preflight(preflight)
    JSON_OUT.write_text(json.dumps(preflight, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_OUT.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(preflight, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "report": str(MD_OUT)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
