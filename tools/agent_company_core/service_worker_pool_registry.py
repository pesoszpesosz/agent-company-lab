from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

"""Assignment, pool registry, pool registration, and gate-map reporting for service workers."""

from .constants import (
    SERVICE_WORKER_ASSIGNMENT_PLAN_JSON,
    SERVICE_WORKER_ASSIGNMENT_PLAN_REPORT,
    SERVICE_WORKER_ASSIGNMENT_PLAN_VALIDATION_JSON,
    SERVICE_WORKER_GATE_MAP_JSON,
    SERVICE_WORKER_GATE_MAP_REPORT,
    SERVICE_WORKER_GATE_MAP_VALIDATION_JSON,
    SERVICE_WORKER_POOL_REGISTRATION_JSON,
    SERVICE_WORKER_POOL_REGISTRATION_REPORT,
    SERVICE_WORKER_POOL_REGISTRATION_VALIDATION_JSON,
    SERVICE_WORKER_POOL_REGISTRY_JSON,
    SERVICE_WORKER_POOL_REGISTRY_REPORT,
    SERVICE_WORKER_POOL_REGISTRY_VALIDATION_JSON,
)
from .catalog import department_id
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR, ROOT
from .utils import md_cell
from .service_worker_core import (
    service_worker_readiness_entry,
)
from .service_worker_scope import (
    service_worker_approval_review_entry,
)


WORKER_TYPE_ASSIGNMENT_ROLES = {
    "browser_read_only": {
        "role_id": "browser_action_worker",
        "worker_pool_id": "service-worker-browser-read-only-pool",
        "capabilities": [
            "public browser read-only navigation",
            "source URL and title capture",
            "short compliant excerpt capture",
            "local artifact writing",
        ],
    },
    "browser_signed_in_read_only": {
        "role_id": "browser_action_worker",
        "worker_pool_id": "service-worker-signed-in-browser-read-only-pool",
        "capabilities": [
            "approved signed-in read-only inspection",
            "no account setting changes",
            "no public X/Grok action",
            "local research note capture",
        ],
    },
    "legal_kyc_tax_payment_review": {
        "role_id": "chief_risk_officer",
        "worker_pool_id": "service-worker-legal-kyc-payment-review-pool",
        "capabilities": [
            "legal/KYC/tax/payment requirement review",
            "commitment and account-contract gate detection",
            "user/CRO question packet writing",
        ],
    },
    "public_submission": {
        "role_id": "reputation_review_worker",
        "worker_pool_id": "service-worker-public-submission-review-pool",
        "capabilities": [
            "public-facing draft review",
            "submission route risk review",
            "spam/slop and account-health check",
        ],
    },
    "model_api_execution": {
        "role_id": "observability_worker",
        "worker_pool_id": "service-worker-model-api-execution-pool",
        "capabilities": [
            "provider/model/cost scope check",
            "input/output artifact boundary check",
            "cost and trace logging before any API call",
        ],
    },
    "local_runtime_adapter": {
        "role_id": "observability_worker",
        "worker_pool_id": "service-worker-local-runtime-adapter-pool",
        "capabilities": [
            "local deterministic runtime execution",
            "artifact and trace emission",
            "no network or account side effects",
        ],
    },
    "other_gated_worker": {
        "role_id": "evidence_builder",
        "worker_pool_id": "service-worker-other-gated-work-pool",
        "capabilities": [
            "local evidence building",
            "gate-specific checklist execution",
            "artifact writing",
        ],
    },
}


from .service_worker_assignment_core import service_worker_assignment_plan_entry

def service_worker_pool_registry_entries(conn: sqlite3.Connection, assignment_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    request_count_by_pool: dict[str, int] = {}
    worker_types_by_pool: dict[str, set[str]] = {}
    lanes_by_pool: dict[str, set[str]] = {}
    for entry in assignment_entries:
        pool_id = entry["recommended_worker_pool_id"]
        request_count_by_pool[pool_id] = request_count_by_pool.get(pool_id, 0) + 1
        worker_types_by_pool.setdefault(pool_id, set()).add(entry["worker_type"])
        if entry.get("lane_id"):
            lanes_by_pool.setdefault(pool_id, set()).add(entry["lane_id"])
    role_rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT agent_id, role_id, department_id, status, thread_id
            FROM agents
            WHERE status = 'active'
            ORDER BY agent_id
            """
        )
    ]
    entries: list[dict[str, Any]] = []
    for worker_type, mapping in sorted(WORKER_TYPE_ASSIGNMENT_ROLES.items()):
        pool_id = mapping["worker_pool_id"]
        role_id = mapping["role_id"]
        active_agents = [row for row in role_rows if row["role_id"] == role_id and row["agent_id"] == pool_id]
        active_role_agents = [row for row in role_rows if row["role_id"] == role_id]
        registered = bool(active_agents)
        role_capacity_exists = bool(active_role_agents)
        if registered:
            status = "registered_pool_available"
            next_action = "Keep pool registered and require approval/readiness before assignment."
        elif role_capacity_exists:
            status = "role_capacity_exists_but_pool_not_registered"
            next_action = "Register a dedicated pool agent id or explicitly map existing role-capacity agents before assignment."
        else:
            status = "missing_service_worker_pool"
            next_action = "Register a concrete service-worker pool/agent before using assignment previews."
        entries.append(
            {
                "worker_type": worker_type,
                "worker_pool_id": pool_id,
                "role_id": role_id,
                "capabilities": mapping["capabilities"],
                "current_request_count": request_count_by_pool.get(pool_id, 0),
                "current_worker_types": sorted(worker_types_by_pool.get(pool_id, {worker_type})),
                "current_lanes": sorted(lanes_by_pool.get(pool_id, set())),
                "registered_pool_agent_ids": [row["agent_id"] for row in active_agents],
                "active_role_agent_ids": [row["agent_id"] for row in active_role_agents],
                "registered_pool_available": registered,
                "role_capacity_exists": role_capacity_exists,
                "pool_status": status,
                "next_action": next_action,
                "approval_granted_by_registry": False,
                "service_request_assigned_by_registry": False,
                "service_request_updated_by_registry": False,
                "worker_started": False,
                "api_calls": False,
                "external_side_effects": False,
            }
        )
    return entries


def write_service_worker_pool_registry(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_POOL_REGISTRY_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_POOL_REGISTRY_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_POOL_REGISTRY_VALIDATION_JSON
    generated_utc = now_utc()
    rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT sr.*, l.department
            FROM service_requests sr
            LEFT JOIN lanes l ON l.lane_id = sr.lane_id
            ORDER BY sr.request_id
            """
        )
    ]
    assignment_entries = [service_worker_assignment_plan_entry(conn, row, generated_utc) for row in rows]
    pools = service_worker_pool_registry_entries(conn, assignment_entries)
    status_counts: dict[str, int] = {}
    role_counts: dict[str, int] = {}
    current_request_count = 0
    for pool in pools:
        status_counts[pool["pool_status"]] = status_counts.get(pool["pool_status"], 0) + 1
        role_counts[pool["role_id"]] = role_counts.get(pool["role_id"], 0) + 1
        current_request_count += pool["current_request_count"]
    missing_pool_count = sum(1 for pool in pools if not pool["registered_pool_available"])
    payload = {
        "schema_version": "service_worker_pool_registry.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "pool_count": len(pools),
        "missing_pool_count": missing_pool_count,
        "current_assignment_request_count": current_request_count,
        "status_counts": dict(sorted(status_counts.items())),
        "role_counts": dict(sorted(role_counts.items())),
        "pools": pools,
        "execution_notice": "Pool registry report only. It registers no workers, grants no approval, assigns no service request, updates no service request, and starts nothing.",
        "approval_granted_by_registry": False,
        "service_requests_assigned_by_registry": 0,
        "service_requests_updated_by_registry": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_pool_registry_validation.v1",
        "generated_utc": generated_utc,
        "pool_registry_path": str(json_output_path),
        "pool_count": len(pools),
        "missing_pool_count": missing_pool_count,
        "current_assignment_request_count": current_request_count,
        "all_pools_have_role_ids": all(bool(pool["role_id"]) for pool in pools),
        "all_pools_have_capabilities": all(bool(pool["capabilities"]) for pool in pools),
        "all_registry_rows_no_assignment": all(not pool["service_request_assigned_by_registry"] for pool in pools),
        "approval_granted_by_registry": False,
        "service_requests_assigned_by_registry": 0,
        "service_requests_updated_by_registry": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "status_counts": dict(sorted(status_counts.items())),
        "role_counts": dict(sorted(role_counts.items())),
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Pool Registry",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report defines service-worker pools needed by the assignment plan. It grants no approval and does not register, assign, start, complete, enqueue, update, browse, call APIs, post, submit, register accounts, trade, spend, or contact anyone.",
        "",
        f"- Pools defined: `{len(pools)}`",
        f"- Missing dedicated pool registrations: `{missing_pool_count}`",
        f"- Current assignment-plan request demand: `{current_request_count}`",
        f"- Pool status counts: `{json.dumps(validation_payload['status_counts'], sort_keys=True)}`",
        f"- Role counts: `{json.dumps(validation_payload['role_counts'], sort_keys=True)}`",
        f"- Service requests assigned by registry: `0`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Pools",
        "",
        "| Pool | Worker Type | Role | Demand | Status | Active Role Agents | Next Action |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for pool in pools:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{pool['worker_pool_id']}`",
                    f"`{pool['worker_type']}`",
                    f"`{pool['role_id']}`",
                    str(pool["current_request_count"]),
                    f"`{pool['pool_status']}`",
                    md_cell(", ".join(pool["active_role_agent_ids"]) or "none", 220),
                    md_cell(pool["next_action"], 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Capabilities", ""])
    for pool in pools:
        lines.extend(
            [
                f"### {pool['worker_pool_id']}",
                "",
                f"- Worker type: `{pool['worker_type']}`",
                f"- Role: `{pool['role_id']}`",
                f"- Current lanes: `{', '.join(pool['current_lanes']) or 'none'}`",
                "- Capabilities:",
            ]
        )
        lines.extend([f"  - {item}" for item in pool["capabilities"]])
        lines.append("")
    lines.extend(
        [
            "## Next Action",
            "",
            "Register concrete service-worker pool agents only after deciding ownership and operating boundaries. After registration, rerun the assignment plan; real assignments still require approval, compatible exact scope, and execution readiness.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "pool_count": len(pools),
                "missing_pool_count": missing_pool_count,
            },
            indent=2,
        )
    )

