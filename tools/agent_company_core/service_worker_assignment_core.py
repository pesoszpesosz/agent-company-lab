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


def lane_manager_for_row(conn: sqlite3.Connection, row: dict[str, Any]) -> dict[str, Any] | None:
    dep = row.get("department")
    if not dep:
        return None
    dep_id = department_id(dep)
    agent = conn.execute(
        """
        SELECT agent_id, role_id, department_id, status, thread_id
        FROM agents
        WHERE department_id = ? AND role_id = 'department_manager' AND status = 'active'
        ORDER BY agent_id
        LIMIT 1
        """,
        (dep_id,),
    ).fetchone()
    return dict(agent) if agent else None


def service_worker_assignment_plan_entry(conn: sqlite3.Connection, row: dict[str, Any], generated_utc: str) -> dict[str, Any]:
    review = service_worker_approval_review_entry(conn, row, generated_utc)
    readiness = service_worker_readiness_entry(conn, row, None, generated_utc)
    worker_type = review.get("worker_type") or "other_gated_worker"
    worker_mapping = WORKER_TYPE_ASSIGNMENT_ROLES.get(worker_type, WORKER_TYPE_ASSIGNMENT_ROLES["other_gated_worker"])
    manager = lane_manager_for_row(conn, row)
    terminal = row["status"] in {"complete", "rejected", "cancelled"}
    checks = {
        "service_status_approved_or_assigned": row["status"] in {"approved", "assigned"},
        "not_terminal": not terminal,
        "packet_valid": not review.get("packet_errors"),
        "human_cro_review_candidate": review["recommended_decision"] == "human_cro_review_required",
        "exact_scope_compatible": bool(review["scope_compatible_with_packet"]),
        "execution_readiness_ready": bool(readiness["ready_to_start"]),
        "lane_manager_known": manager is not None,
        "service_worker_role_known": bool(worker_mapping.get("role_id")),
    }
    missing = [key for key, value in checks.items() if not value]
    can_assign_now = not missing
    if terminal:
        route = f"terminal_{row['status']}_no_assignment"
        next_action = "Do not assign terminal requests; keep audit evidence or create a fresh request."
    elif row["status"] == "needs_review":
        route = "blocked_until_human_cro_approval"
        next_action = "Use the CRO approval review queue first; only assign after separate approval and readiness verification."
    elif row["status"] == "approved":
        route = "approved_but_readiness_or_scope_missing" if not can_assign_now else "assignable_after_final_manual_check"
        next_action = "Run scope diff and execution-readiness verifier before assignment."
    elif row["status"] == "assigned":
        route = "already_assigned_reverify_before_start"
        next_action = "Re-run execution-readiness verifier before start."
    else:
        route = f"status_{row['status']}_manual_audit"
        next_action = "Audit status before assignment."
    assign_preview = []
    if not terminal:
        assign_preview = [
            "python",
            str(ROOT / "tools" / "agent_company.py"),
            "assign-service-request",
            "--request-id",
            row["request_id"],
            "--agent-id",
            worker_mapping["worker_pool_id"],
            "--decision-note",
            "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification.",
        ]
    return {
        "source_service_request_id": row["request_id"],
        "worker_request_id": review.get("worker_request_id"),
        "lane_id": row.get("lane_id"),
        "lane_department": row.get("department"),
        "lane_manager_agent_id": manager.get("agent_id") if manager else None,
        "lane_manager_thread_id": manager.get("thread_id") if manager else None,
        "worker_type": worker_type,
        "service_id": review.get("service_id"),
        "request_type": review.get("request_type"),
        "service_status": row["status"],
        "risk_gate": review.get("risk_gate"),
        "recommended_worker_role_id": worker_mapping["role_id"],
        "recommended_worker_pool_id": worker_mapping["worker_pool_id"],
        "required_capabilities": worker_mapping["capabilities"],
        "assignment_route": route,
        "assignment_checks": checks,
        "missing_assignment_checks": missing,
        "can_assign_now": can_assign_now,
        "assign_command_preview_argv": assign_preview,
        "assign_command_requires_manual_review": True,
        "next_action": next_action,
        "approval_review_route": review["review_route"],
        "execution_readiness_route": readiness["route"],
        "approval_granted_by_plan": False,
        "service_request_assigned_by_plan": False,
        "service_request_updated_by_plan": False,
        "worker_started": False,
        "api_calls": False,
        "external_side_effects": False,
    }

