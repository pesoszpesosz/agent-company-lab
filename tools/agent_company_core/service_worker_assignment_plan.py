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

def write_service_worker_assignment_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_ASSIGNMENT_PLAN_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_ASSIGNMENT_PLAN_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_ASSIGNMENT_PLAN_VALIDATION_JSON
    generated_utc = now_utc()
    clauses: list[str] = []
    params: list[Any] = []
    if args.request_id:
        clauses.append("sr.request_id = ?")
        params.append(args.request_id)
    if args.lane_id:
        clauses.append("sr.lane_id = ?")
        params.append(args.lane_id)
    if args.status:
        clauses.append("sr.status = ?")
        params.append(args.status)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT sr.*, l.department
            FROM service_requests sr
            LEFT JOIN lanes l ON l.lane_id = sr.lane_id
            {where}
            ORDER BY sr.request_id
            """,
            params,
        )
    ]
    entries = [service_worker_assignment_plan_entry(conn, row, generated_utc) for row in rows]
    route_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    worker_type_counts: dict[str, int] = {}
    worker_role_counts: dict[str, int] = {}
    assignable_now_count = 0
    for entry in entries:
        route_counts[entry["assignment_route"]] = route_counts.get(entry["assignment_route"], 0) + 1
        status_counts[entry["service_status"]] = status_counts.get(entry["service_status"], 0) + 1
        worker_type_counts[entry["worker_type"]] = worker_type_counts.get(entry["worker_type"], 0) + 1
        worker_role_counts[entry["recommended_worker_role_id"]] = worker_role_counts.get(entry["recommended_worker_role_id"], 0) + 1
        if entry["can_assign_now"]:
            assignable_now_count += 1
    assign_preview_count = sum(1 for item in entries if item["assign_command_preview_argv"])
    payload = {
        "schema_version": "service_worker_assignment_plan.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "filters": {
            "request_id": args.request_id,
            "lane_id": args.lane_id,
            "status": args.status,
        },
        "planned_count": len(entries),
        "assignable_now_count": assignable_now_count,
        "assign_command_preview_count": assign_preview_count,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
        "worker_role_counts": dict(sorted(worker_role_counts.items())),
        "assignment_plan": entries,
        "execution_notice": "Assignment plan only. It proposes service-worker pools and command previews but grants no approval, assigns no worker, updates no service request, and starts nothing.",
        "approval_granted_by_plan": False,
        "service_requests_assigned_by_plan": 0,
        "service_requests_updated_by_plan": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_assignment_plan_validation.v1",
        "generated_utc": generated_utc,
        "assignment_plan_path": str(json_output_path),
        "planned_count": len(entries),
        "assignable_now_count": assignable_now_count,
        "assign_command_preview_count": assign_preview_count,
        "all_assign_previews_require_manual_review": all(item["assign_command_requires_manual_review"] for item in entries),
        "all_plans_no_assignment": all(not item["service_request_assigned_by_plan"] for item in entries),
        "approval_granted_by_plan": False,
        "service_requests_assigned_by_plan": 0,
        "service_requests_updated_by_plan": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
        "worker_role_counts": dict(sorted(worker_role_counts.items())),
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Assignment Plan",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report plans service-worker assignment after approval. It grants no approval and does not assign, start, complete, enqueue, update, browse, call APIs, post, submit, register, trade, spend, or contact anyone.",
        "",
        f"- Requests planned: `{len(entries)}`",
        f"- Assignable now: `{assignable_now_count}`",
        f"- Assign command previews: `{assign_preview_count}`",
        f"- Route counts: `{json.dumps(validation_payload['route_counts'], sort_keys=True)}`",
        f"- Worker role counts: `{json.dumps(validation_payload['worker_role_counts'], sort_keys=True)}`",
        f"- Service requests assigned by plan: `0`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Assignment Queue",
        "",
        "| Status | Route | Request | Lane Manager | Worker Type | Worker Role | Worker Pool | Missing Checks |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['service_status']}`",
                    f"`{entry['assignment_route']}`",
                    f"`{entry['source_service_request_id']}`",
                    f"`{entry.get('lane_manager_agent_id') or ''}`",
                    f"`{entry['worker_type']}`",
                    f"`{entry['recommended_worker_role_id']}`",
                    f"`{entry['recommended_worker_pool_id']}`",
                    md_cell(", ".join(entry["missing_assignment_checks"]) or "none", 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Assign Preview Notes", ""])
    for entry in entries:
        lines.extend(
            [
                f"### {entry['source_service_request_id']}",
                "",
                f"- Assignment route: `{entry['assignment_route']}`",
                f"- Can assign now: `{entry['can_assign_now']}`",
                f"- Required capabilities: {md_cell('; '.join(entry['required_capabilities']), 500)}",
                "",
            ]
        )
        if entry["assign_command_preview_argv"]:
            lines.extend(["Assign preview argv:", "", "```json", json.dumps(entry["assign_command_preview_argv"], indent=2), "```", ""])
        else:
            lines.extend(["Assign preview argv: `[]`", ""])
    lines.extend(
        [
            "## Next Action",
            "",
            "Register concrete service-worker agents or pools before using any assign preview. A real assignment still requires separate approval, compatible exact scope, and a passing execution-readiness report.",
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
                "count": len(entries),
                "assignable_now_count": assignable_now_count,
            },
            indent=2,
        )
    )

