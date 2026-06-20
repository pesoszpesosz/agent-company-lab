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
    compact_sequence,
    join_scope_items,
    scope_template_allowed_data,
    scope_template_hosts,
    scope_template_output_paths,
    scope_template_required_denials,
    scope_template_starting_urls,
)
def service_worker_scope_template_entry(conn: sqlite3.Connection, row: dict[str, Any], generated_utc: str) -> dict[str, Any]:
    packet_path = service_worker_packet_path(row["request_id"])
    if packet_path.exists():
        packet = load_json(packet_path)
        packet_source = "existing_packet"
    else:
        packet = synthesize_service_worker_request(row, generated_utc)
        packet_source = "synthesized_from_db"
    packet_errors = validate_service_worker_request_object(packet)
    approval = latest_approval_for_request(conn, row["request_id"])
    allowed_actions = compact_sequence(packet.get("allowed_actions", []), "only the actions explicitly listed in the service-worker packet")
    stop_conditions = compact_sequence(packet.get("stop_conditions", []), "stop whenever the packet boundary is unclear")
    output_paths = scope_template_output_paths(packet)
    max_cost = packet.get("max_cost_usd", 0)
    base_parts = [
        f"DRAFT ONLY - NOT APPROVED. For source service request `{row['request_id']}` and worker request `{packet.get('worker_request_id') or 'unknown'}`, allow `{packet.get('worker_type') or 'unknown'}` worker activity only after separate explicit user/CRO approval.",
        f"Objective: {compact_text(str(packet.get('objective') or row.get('requested_action') or 'execute only the packet objective'), 500)}",
        join_scope_items("Allowed actions", allowed_actions),
        join_scope_items("Allowed hosts", scope_template_hosts(packet)),
        join_scope_items("Starting URLs", scope_template_starting_urls(packet)),
        join_scope_items("Allowed data", scope_template_allowed_data(packet)),
        join_scope_items("Required outputs", output_paths),
        join_scope_items("Hard denials", scope_template_required_denials(packet)),
        join_scope_items("Stop conditions", stop_conditions),
        f"Max cost USD: {max_cost}.",
        "This draft expires unless separately approved with `approve-service-request`; this report grants no approval, assignment, start authority, browser action, API call, public action, payment, trade, submission, or external side effect.",
    ]
    if row["status"] in {"complete", "rejected", "cancelled"}:
        route = f"terminal_{row['status']}_do_not_approve"
        suggested_scope = (
            f"DRAFT ONLY - NOT APPROVED. Do not approve or start terminal request `{row['request_id']}` "
            f"while its service status is `{row['status']}`. Keep this as audit text only, or create a fresh "
            "service request with a fresh exact scope if work is still needed."
        )
        next_action = "Do not approve this terminal row; retain audit evidence or create a new scoped request."
    else:
        route = "draft_scope_template_for_human_review"
        suggested_scope = " ".join(base_parts)
        next_action = "Human/CRO may copy-edit this draft into approve-service-request only after checking current scope, packet, risk gate, and stop conditions."
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
        "latest_approval_id": approval.get("approval_id") if approval else None,
        "latest_approval_status": approval.get("status") if approval else None,
        "latest_approval_expires_at": approval.get("expires_at") if approval else None,
        "allowed_actions": allowed_actions,
        "allowed_hosts": scope_template_hosts(packet),
        "starting_urls": scope_template_starting_urls(packet),
        "allowed_data_types": scope_template_allowed_data(packet),
        "required_output_paths": output_paths,
        "required_denials": scope_template_required_denials(packet),
        "stop_conditions": stop_conditions,
        "max_cost_usd": max_cost,
        "template_route": route,
        "suggested_exact_scope": suggested_scope,
        "next_action": next_action,
        "approval_command_requires_manual_review": True,
        "approval_granted_by_template": False,
        "service_request_updated": False,
        "worker_started": False,
        "api_calls": False,
        "external_side_effects": False,
    }


def write_service_worker_scope_templates(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_SCOPE_TEMPLATE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_SCOPE_TEMPLATE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_SCOPE_TEMPLATE_VALIDATION_JSON
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
    entries = [service_worker_scope_template_entry(conn, row, generated_utc) for row in rows]
    route_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    worker_type_counts: dict[str, int] = {}
    for entry in entries:
        route_counts[entry["template_route"]] = route_counts.get(entry["template_route"], 0) + 1
        status_counts[entry["service_status"]] = status_counts.get(entry["service_status"], 0) + 1
        worker_type = entry.get("worker_type") or "unknown"
        worker_type_counts[worker_type] = worker_type_counts.get(worker_type, 0) + 1
    payload = {
        "schema_version": "service_worker_exact_scope_templates.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "filters": {
            "request_id": args.request_id,
            "lane_id": args.lane_id,
            "status": args.status,
        },
        "request_count": len(entries),
        "draft_templates_written": len(entries),
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
        "scope_templates": entries,
        "execution_notice": "Draft-only exact-scope templates for human/CRO review. They grant no approval and do not assign, start, complete, enqueue, update, or execute service workers.",
        "templates_grant_approval": False,
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "service_requests_updated_by_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_exact_scope_templates_validation.v1",
        "generated_utc": generated_utc,
        "scope_templates_path": str(json_output_path),
        "validated_count": len(entries),
        "draft_templates_written": len(entries),
        "templates_grant_approval": False,
        "all_templates_require_manual_review": all(item["approval_command_requires_manual_review"] for item in entries),
        "all_templates_no_approval": all(not item["approval_granted_by_template"] for item in entries),
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "service_requests_updated_by_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Exact Scope Templates",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report writes draft exact-scope text for human/CRO review. It grants no approval and does not assign, start, complete, enqueue, update, browse, call APIs, post, submit, register, trade, spend, or contact anyone.",
        "",
        f"- Requests evaluated: `{len(entries)}`",
        f"- Draft templates written: `{len(entries)}`",
        f"- Route counts: `{json.dumps(validation_payload['route_counts'], sort_keys=True)}`",
        f"- Status counts: `{json.dumps(validation_payload['status_counts'], sort_keys=True)}`",
        f"- Templates grant approval: `False`",
        f"- Worker starts: `0`",
        f"- Service requests updated: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Template Rows",
        "",
        "| Status | Route | Source Request | Worker Type | Draft Scope Preview |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['service_status']}`",
                    f"`{entry['template_route']}`",
                    f"`{entry['source_service_request_id']}`",
                    f"`{entry.get('worker_type') or ''}`",
                    md_cell(entry["suggested_exact_scope"], 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Draft Text", ""])
    for entry in entries:
        lines.extend(
            [
                f"### {entry['source_service_request_id']}",
                "",
                "```text",
                entry["suggested_exact_scope"],
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## Next Action",
            "",
            "Use these drafts only as review starting points. Any real approval must be a separate explicit approve-service-request decision, followed by assignment and the execution-readiness verifier before any worker start.",
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
                "draft_templates_written": len(entries),
            },
            indent=2,
        )
    )

