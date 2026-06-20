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
from .service_worker_pool_registry import service_worker_pool_registry_entries

def service_worker_pool_registration_department(pool: dict[str, Any]) -> str:
    role_id = pool["role_id"]
    if role_id == "browser_action_worker":
        return "service_worker_browser_operations"
    if role_id == "chief_risk_officer":
        return "service_worker_risk_review"
    if role_id == "reputation_review_worker":
        return "service_worker_reputation_review"
    if role_id == "observability_worker":
        return "service_worker_observability"
    if role_id == "evidence_builder":
        return "service_worker_evidence_building"
    return "service_worker_operations"


def service_worker_pool_registration_boundaries(pool: dict[str, Any]) -> list[str]:
    common = [
        "requires separate human/CRO approval before any service request assignment",
        "requires compatible exact approval scope before assignment",
        "requires execution-readiness verifier before any start",
        "must write local artifacts and trace evidence for any allowed work",
        "must stop at credentials, private data, account, public-action, payment, wallet, legal, model/API cost, or unclear scope gates",
    ]
    worker_type = pool["worker_type"]
    if worker_type.startswith("browser"):
        common.extend(
            [
                "no login or signed-in surface unless the exact approved scope names it",
                "no clicks that post, submit, message, upload, buy, sell, accept terms, or change settings",
            ]
        )
    if worker_type == "model_api_execution":
        common.append("no provider/model/API call until provider, model, max cost, data scope, and output artifact path are explicitly approved")
    if worker_type == "legal_kyc_tax_payment_review":
        common.append("no legal, KYC, tax, payment, seller, or account commitment; prepare review packets only")
    if worker_type == "public_submission":
        common.append("no public submission or contact; review route and draft quality only")
    return common


def service_worker_pool_registration_entry(pool: dict[str, Any]) -> dict[str, Any]:
    department_id_value = service_worker_pool_registration_department(pool)
    register_preview = [
        "python",
        str(ROOT / "tools" / "agent_company.py"),
        "register-agent",
        "--agent-id",
        pool["worker_pool_id"],
        "--role-id",
        pool["role_id"],
        "--department-id",
        department_id_value,
    ]
    if pool["registered_pool_available"]:
        route = "already_registered_no_action"
        register_preview = []
        next_action = "Keep the existing registered pool; rerun assignment/readiness before use."
    else:
        route = "registration_packet_ready_manual_review"
        next_action = "Review ownership and boundaries, then run register-agent manually only if the pool should exist."
    return {
        "worker_pool_id": pool["worker_pool_id"],
        "worker_type": pool["worker_type"],
        "role_id": pool["role_id"],
        "department_id": department_id_value,
        "current_request_count": pool["current_request_count"],
        "current_lanes": pool["current_lanes"],
        "capabilities": pool["capabilities"],
        "boundaries": service_worker_pool_registration_boundaries(pool),
        "registration_route": route,
        "next_action": next_action,
        "register_agent_command_preview_argv": register_preview,
        "register_command_requires_manual_review": True,
        "pool_registered_by_plan": False,
        "approval_granted_by_plan": False,
        "service_request_assigned_by_plan": False,
        "service_request_updated_by_plan": False,
        "worker_started": False,
        "api_calls": False,
        "external_side_effects": False,
    }


def write_service_worker_pool_registration_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_POOL_REGISTRATION_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_POOL_REGISTRATION_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_POOL_REGISTRATION_VALIDATION_JSON
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
    registration_entries = [service_worker_pool_registration_entry(pool) for pool in pools]
    route_counts: dict[str, int] = {}
    role_counts: dict[str, int] = {}
    department_counts: dict[str, int] = {}
    demand_count = 0
    for entry in registration_entries:
        route_counts[entry["registration_route"]] = route_counts.get(entry["registration_route"], 0) + 1
        role_counts[entry["role_id"]] = role_counts.get(entry["role_id"], 0) + 1
        department_counts[entry["department_id"]] = department_counts.get(entry["department_id"], 0) + 1
        demand_count += entry["current_request_count"]
    preview_count = sum(1 for entry in registration_entries if entry["register_agent_command_preview_argv"])
    payload = {
        "schema_version": "service_worker_pool_registration_plan.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "registration_packet_count": len(registration_entries),
        "register_command_preview_count": preview_count,
        "current_assignment_request_count": demand_count,
        "route_counts": dict(sorted(route_counts.items())),
        "role_counts": dict(sorted(role_counts.items())),
        "department_counts": dict(sorted(department_counts.items())),
        "registration_packets": registration_entries,
        "execution_notice": "Pool registration plan only. It writes manual registration packets and command previews but registers no workers, grants no approval, assigns no service request, updates no service request, and starts nothing.",
        "pools_registered_by_plan": 0,
        "approval_granted_by_plan": False,
        "service_requests_assigned_by_plan": 0,
        "service_requests_updated_by_plan": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_pool_registration_plan_validation.v1",
        "generated_utc": generated_utc,
        "pool_registration_plan_path": str(json_output_path),
        "registration_packet_count": len(registration_entries),
        "register_command_preview_count": preview_count,
        "current_assignment_request_count": demand_count,
        "all_register_previews_require_manual_review": all(entry["register_command_requires_manual_review"] for entry in registration_entries),
        "all_packets_have_boundaries": all(bool(entry["boundaries"]) for entry in registration_entries),
        "all_packets_have_capabilities": all(bool(entry["capabilities"]) for entry in registration_entries),
        "all_plans_no_registration": all(not entry["pool_registered_by_plan"] for entry in registration_entries),
        "pools_registered_by_plan": 0,
        "approval_granted_by_plan": False,
        "service_requests_assigned_by_plan": 0,
        "service_requests_updated_by_plan": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "route_counts": dict(sorted(route_counts.items())),
        "role_counts": dict(sorted(role_counts.items())),
        "department_counts": dict(sorted(department_counts.items())),
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Pool Registration Plan",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report writes manual registration packets for service-worker pools. It grants no approval and does not register, assign, start, complete, enqueue, update, browse, call APIs, post, submit, register accounts, trade, spend, or contact anyone.",
        "",
        f"- Registration packets: `{len(registration_entries)}`",
        f"- Register command previews: `{preview_count}`",
        f"- Current assignment-plan request demand: `{demand_count}`",
        f"- Route counts: `{json.dumps(validation_payload['route_counts'], sort_keys=True)}`",
        f"- Pools registered by plan: `0`",
        f"- Service requests assigned by plan: `0`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Registration Packets",
        "",
        "| Pool | Role | Department | Demand | Route | Next Action |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for entry in registration_entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['worker_pool_id']}`",
                    f"`{entry['role_id']}`",
                    f"`{entry['department_id']}`",
                    str(entry["current_request_count"]),
                    f"`{entry['registration_route']}`",
                    md_cell(entry["next_action"], 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Command Previews", ""])
    for entry in registration_entries:
        lines.extend(
            [
                f"### {entry['worker_pool_id']}",
                "",
                f"- Worker type: `{entry['worker_type']}`",
                f"- Current lanes: `{', '.join(entry['current_lanes']) or 'none'}`",
                "- Boundaries:",
            ]
        )
        lines.extend([f"  - {item}" for item in entry["boundaries"]])
        lines.append("")
        if entry["register_agent_command_preview_argv"]:
            lines.extend(["Register-agent preview argv:", "", "```json", json.dumps(entry["register_agent_command_preview_argv"], indent=2), "```", ""])
        else:
            lines.extend(["Register-agent preview argv: `[]`", ""])
    lines.extend(
        [
            "## Next Action",
            "",
            "Review ownership and boundaries before registering any pool. After manual registration, rerun the pool registry and assignment plan; real assignments still require approval, compatible exact scope, and execution readiness.",
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
                "registration_packet_count": len(registration_entries),
                "register_command_preview_count": preview_count,
            },
            indent=2,
        )
    )

