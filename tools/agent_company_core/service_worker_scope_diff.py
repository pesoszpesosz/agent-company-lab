from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

"""Scope-diff, scope-template, and approval-review reporting for service workers."""

from .constants import (
    SERVICE_WORKER_APPROVAL_REVIEW_JSON,
    SERVICE_WORKER_APPROVAL_REVIEW_REPORT,
    SERVICE_WORKER_APPROVAL_REVIEW_VALIDATION_JSON,
    SERVICE_WORKER_SCOPE_DIFF_JSON,
    SERVICE_WORKER_SCOPE_DIFF_REPORT,
    SERVICE_WORKER_SCOPE_DIFF_VALIDATION_JSON,
    SERVICE_WORKER_SCOPE_TEMPLATE_JSON,
    SERVICE_WORKER_SCOPE_TEMPLATE_REPORT,
    SERVICE_WORKER_SCOPE_TEMPLATE_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import DB_PATH, REPORTS_DIR, ROOT
from .utils import compact_text, md_cell
from .service_worker_core import (
    approval_not_expired,
    latest_approval_for_request,
    service_worker_packet_path,
    synthesize_service_worker_request,
    validate_service_worker_request_object,
)


SIDE_EFFECT_SCOPE_RULES = [
    {
        "key": "credential_boundary",
        "packet_flag": None,
        "required_denial_terms": ["credential", "credentials", "otp", "private data", "private files", "secrets"],
        "conflict_terms": ["enter credentials", "use credentials", "otp", "password", "private data", "private file", "secret"],
    },
    {
        "key": "account_boundary",
        "packet_flag": "account_or_identity_action_allowed",
        "required_denial_terms": ["login", "signup", "account", "settings", "terms acceptance"],
        "conflict_terms": ["login", "log in", "sign in", "signup", "sign up", "create account", "settings", "accept terms"],
    },
    {
        "key": "money_boundary",
        "packet_flag": "real_money_allowed",
        "required_denial_terms": ["payment", "wallet", "purchase", "deposit", "withdraw", "trade", "real money"],
        "conflict_terms": ["payment", "wallet", "purchase", "deposit", "withdraw", "trade", "buy", "sell", "real money"],
    },
    {
        "key": "public_action_boundary",
        "packet_flag": "public_action_allowed",
        "required_denial_terms": ["post", "comment", "message", "submit", "publish", "listing", "upload", "public action"],
        "conflict_terms": ["post", "comment", "message", "submit", "publish", "listing", "upload", "reply", "contact"],
    },
    {
        "key": "model_or_api_cost",
        "packet_flag": "model_or_api_cost_allowed",
        "required_denial_terms": ["api", "model", "cost", "provider"],
        "conflict_terms": ["api call", "model call", "provider", "paid api", "cost"],
    },
    {
        "key": "external_side_effects",
        "packet_flag": "external_side_effects_allowed",
        "required_denial_terms": ["external action", "external side effect", "no side effect"],
        "conflict_terms": ["external action", "side effect", "start worker", "execute worker"],
    },
]


NEGATION_MARKERS = ["no", "not", "never", "without", "do not", "don't", "cannot", "may not", "must not"]


from .service_worker_scope_core import (
    SIDE_EFFECT_SCOPE_RULES,
    concrete_hosts_from_packet,
    denial_present,
    host_scope_mentions,
    normalized_scope_text,
    positive_conflicts,
)
def service_worker_scope_diff_entry(conn: sqlite3.Connection, row: dict[str, Any], generated_utc: str) -> dict[str, Any]:
    packet_path = service_worker_packet_path(row["request_id"])
    if packet_path.exists():
        packet = load_json(packet_path)
        packet_source = "existing_packet"
    else:
        packet = synthesize_service_worker_request(row, generated_utc)
        packet_source = "synthesized_from_db"
    packet_errors = validate_service_worker_request_object(packet)
    approval = latest_approval_for_request(conn, row["request_id"])
    service_scope = row.get("approval_scope") or ""
    approval_scope = approval.get("exact_scope") if approval else ""
    scope_text = normalized_scope_text(service_scope, approval_scope)
    scope_present = bool(scope_text.strip())
    boundary_checks: list[dict[str, Any]] = []
    for rule in SIDE_EFFECT_SCOPE_RULES:
        flag = rule["packet_flag"]
        packet_allows = False if flag is None else packet.get(flag) is True
        required_denial_present = True if packet_allows else denial_present(scope_text, rule["required_denial_terms"])
        conflicts = positive_conflicts(scope_text, rule["conflict_terms"])
        boundary_checks.append(
            {
                "boundary": rule["key"],
                "packet_allows": packet_allows,
                "required_denial_present": required_denial_present,
                "positive_conflicts": conflicts,
                "ok": bool(required_denial_present and not conflicts),
            }
        )
    hosts = concrete_hosts_from_packet(packet)
    host_mentions = host_scope_mentions(scope_text, hosts)
    host_scope_ok = True if not hosts else any(host_mentions.values())
    approval_matches = bool(approval and service_scope.strip() and approval_scope == service_scope)
    checks = {
        "packet_valid": not packet_errors,
        "scope_present": scope_present,
        "latest_approval_exists": approval is not None,
        "latest_approval_approved": bool(approval and approval.get("status") == "approved"),
        "latest_approval_not_expired": approval_not_expired(approval),
        "approval_scope_matches_service_scope": approval_matches,
        "side_effect_denials_present": all(item["required_denial_present"] for item in boundary_checks),
        "no_positive_side_effect_conflicts": all(not item["positive_conflicts"] for item in boundary_checks),
        "host_scope_ok": host_scope_ok,
        "report_grants_approval": False,
    }
    missing_or_failed = [key for key, value in checks.items() if key != "report_grants_approval" and not value]
    scope_compatible = not missing_or_failed
    if row["status"] in {"complete", "rejected", "cancelled"}:
        route = f"terminal_{row['status']}_scope_audit_only"
        next_action = "Do not start; keep terminal audit evidence or create a new request with a fresh scope."
    elif not scope_present:
        route = "missing_exact_scope"
        next_action = "Write an exact approval scope that names allowed actions, required denials, hosts, and output artifacts."
    elif not approval:
        route = "scope_text_without_approval_record"
        next_action = "Record an approved approval row with the exact scope before assignment or start."
    elif not scope_compatible:
        route = "scope_conflicts_or_incomplete"
        next_action = "Revise the scope until every packet boundary is explicitly preserved and no conflicting permission remains."
    else:
        route = "scope_compatible_but_report_grants_no_start"
        next_action = "Run the readiness verifier and require manual final approval before any start command."
    return {
        "source_service_request_id": row["request_id"],
        "worker_request_id": packet.get("worker_request_id"),
        "lane_id": row["lane_id"],
        "worker_type": packet.get("worker_type"),
        "service_id": row.get("service_id") or packet.get("service_id"),
        "request_type": row["request_type"],
        "service_status": row["status"],
        "packet_status": packet.get("status"),
        "risk_gate": row.get("risk_gate") or packet.get("risk_gate"),
        "packet_path": str(packet_path),
        "packet_source": packet_source,
        "packet_errors": packet_errors,
        "service_approval_scope": service_scope,
        "latest_approval_id": approval.get("approval_id") if approval else None,
        "latest_approval_status": approval.get("status") if approval else None,
        "latest_approval_exact_scope": approval_scope,
        "latest_approval_expires_at": approval.get("expires_at") if approval else None,
        "allowed_actions": packet.get("allowed_actions", []),
        "prohibited_actions": packet.get("prohibited_actions", []),
        "stop_conditions": packet.get("stop_conditions", []),
        "boundary_checks": boundary_checks,
        "host_mentions": host_mentions,
        "checks": checks,
        "missing_or_failed_checks": missing_or_failed,
        "scope_compatible_with_packet": scope_compatible,
        "route": route,
        "next_action": next_action,
        "approval_granted_by_report": False,
        "start_allowed_by_report": False,
    }


def write_service_worker_scope_diff(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_SCOPE_DIFF_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_SCOPE_DIFF_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_SCOPE_DIFF_VALIDATION_JSON
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
    entries = [service_worker_scope_diff_entry(conn, row, generated_utc) for row in rows]
    route_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    compatible_count = 0
    for entry in entries:
        route_counts[entry["route"]] = route_counts.get(entry["route"], 0) + 1
        status_counts[entry["service_status"]] = status_counts.get(entry["service_status"], 0) + 1
        if entry["scope_compatible_with_packet"]:
            compatible_count += 1
    payload = {
        "schema_version": "service_worker_approval_scope_diff.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "filters": {
            "request_id": args.request_id,
            "lane_id": args.lane_id,
            "status": args.status,
        },
        "request_count": len(entries),
        "scope_compatible_count": compatible_count,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "scope_diffs": entries,
        "execution_notice": "Read-only approval-scope diff. It grants no approval and does not assign, start, complete, enqueue, or execute service workers.",
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "service_requests_updated_by_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_approval_scope_diff_validation.v1",
        "generated_utc": generated_utc,
        "scope_diff_path": str(json_output_path),
        "validated_count": len(entries),
        "scope_compatible_count": compatible_count,
        "all_reports_no_start_authority": all(not item["start_allowed_by_report"] for item in entries),
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "service_requests_updated_by_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Approval Scope Diff",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report compares approval-scope text against `service_worker_request.v1` packet boundaries. It grants no approval and does not assign, start, complete, enqueue, browse, call APIs, post, submit, register, trade, spend, or contact anyone.",
        "",
        f"- Requests evaluated: `{len(entries)}`",
        f"- Scope-compatible rows: `{compatible_count}`",
        f"- Route counts: `{json.dumps(validation_payload['route_counts'], sort_keys=True)}`",
        f"- Status counts: `{json.dumps(validation_payload['status_counts'], sort_keys=True)}`",
        f"- Worker starts: `0`",
        f"- Service requests updated: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Scope Diff Rows",
        "",
        "| Status | Compatible | Route | Source Request | Scope Failures |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['service_status']}`",
                    f"`{entry['scope_compatible_with_packet']}`",
                    f"`{entry['route']}`",
                    f"`{entry['source_service_request_id']}`",
                    md_cell(", ".join(entry["missing_or_failed_checks"]) or "none", 260),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "Use this report before approving or starting any service-worker request. A compatible scope is still not a start command; it must be followed by the execution-readiness verifier and explicit human approval.",
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
                "scope_compatible_count": compatible_count,
            },
            indent=2,
        )
    )

