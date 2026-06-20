"""Catalog-backed service-request lifecycle operations."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import SERVICE_REQUEST_REVIEW_JSON, SERVICE_REQUEST_REVIEW_REPORT
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR, ROOT
from .utils import decode_json_list, md_cell, parse_json_arg, safe_id_fragment, sha256_file


from .service_requests_core import validate_service_request_record

def service_request_where(args: argparse.Namespace) -> tuple[str, list[Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if getattr(args, "request_id", None):
        clauses.append("sr.request_id = ?")
        params.append(args.request_id)
    if getattr(args, "lane_id", None):
        clauses.append("sr.lane_id = ?")
        params.append(args.lane_id)
    if getattr(args, "service_id", None):
        clauses.append("sr.service_id = ?")
        params.append(args.service_id)
    if getattr(args, "request_type", None):
        clauses.append("sr.request_type = ?")
        params.append(args.request_type)
    if getattr(args, "status", None):
        clauses.append("sr.status = ?")
        params.append(args.status)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    return where, params


def service_request_recommendation(row: dict[str, Any], validation: dict[str, Any], approvers: list[Any]) -> str:
    status = row["status"]
    request_type = row["request_type"]
    service_id = row.get("service_id")
    if not validation["ok"]:
        missing = ", ".join(validation.get("missing", [])) or validation.get("error", "unknown")
        return f"Fill or regenerate the intake packet before review; missing: {missing}."
    if status == "needs_review":
        approver_text = ", ".join(str(item) for item in approvers) or "explicit reviewer"
        if service_id == "browser_read_only_session":
            return f"Review for exact read-only scope with {approver_text}; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions."
        if request_type == "model_api_execution":
            return "Review only after provider, model, max cost, lane scope, artifact path, and credential route are explicit; no model/API call is approved by this report."
        if "grok" in (row.get("risk_gate") or "").lower() or "x" in (row.get("risk_gate") or "").lower():
            return "Review as signed-in browser research only; no posts, likes, follows, replies, profile/account settings, or public actions."
        return f"Review with {approver_text}; if approved, record exact scope before assignment or start."
    if status == "approved":
        if not row.get("approval_scope"):
            return "Approved status is missing an approval_scope; fix the approval record before assigning."
        if not row.get("assigned_agent_id"):
            return "Assign a service worker and start only within the exact approved scope."
        return "Assigned request may start only within the exact approved scope and must write the named proof artifact."
    if status == "in_progress":
        return "Monitor the assigned worker for proof artifact, stop-gate notes, and completion status."
    if status == "complete":
        return "No action; keep as completed evidence."
    if status == "rejected":
        return "No action; keep closed unless a new request is scaffolded with a different scope."
    return "Do not act until the status is reconciled by the CEO/CRO."


def write_service_request_review(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_REQUEST_REVIEW_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_REQUEST_REVIEW_JSON
    where, params = service_request_where(args)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT sr.*, l.department, sc.name AS service_name, sc.owner_role_id,
                   sc.required_intake_json, sc.approval_required_by_json, sc.default_status,
                   sc.output_artifacts_json
            FROM service_requests sr
            LEFT JOIN lanes l ON l.lane_id = sr.lane_id
            LEFT JOIN service_catalog sc ON sc.service_id = sr.service_id
            {where}
            ORDER BY
              CASE sr.status
                WHEN 'needs_review' THEN 0
                WHEN 'approved' THEN 1
                WHEN 'in_progress' THEN 2
                WHEN 'complete' THEN 3
                WHEN 'rejected' THEN 4
                ELSE 5
              END,
              sr.created_at DESC
            LIMIT ?
            """,
            params,
        )
    ]
    counts_by_status: dict[str, int] = {}
    counts_by_lane: dict[str, int] = {}
    counts_by_service: dict[str, int] = {}
    review_rows: list[dict[str, Any]] = []
    for row in rows:
        validation = validate_service_request_record(conn, row)
        approvers = decode_json_list(row.get("approval_required_by_json"))
        required_intake = decode_json_list(row.get("required_intake_json"))
        output_artifacts = decode_json_list(row.get("output_artifacts_json"))
        recommendation = service_request_recommendation(row, validation, approvers)
        counts_by_status[row["status"]] = counts_by_status.get(row["status"], 0) + 1
        counts_by_lane[row["lane_id"]] = counts_by_lane.get(row["lane_id"], 0) + 1
        service_key = row["service_id"] or row["request_type"] or "uncataloged"
        counts_by_service[service_key] = counts_by_service.get(service_key, 0) + 1
        review_rows.append(
            {
                "request_id": row["request_id"],
                "lane_id": row["lane_id"],
                "department": row.get("department"),
                "service_id": row.get("service_id"),
                "service_name": row.get("service_name"),
                "request_type": row["request_type"],
                "status": row["status"],
                "risk_gate": row.get("risk_gate"),
                "owner_role_id": row.get("owner_role_id"),
                "requested_action": row.get("requested_action"),
                "assigned_agent_id": row.get("assigned_agent_id"),
                "artifact_path": row.get("artifact_path"),
                "decision_note": row.get("decision_note"),
                "approval_scope_present": validation["approval_scope_present"],
                "approval_scope": row.get("approval_scope"),
                "validation_ok": validation["ok"],
                "missing_fields": validation.get("missing", []),
                "required_intake": required_intake,
                "approval_required_by": approvers,
                "output_artifacts": output_artifacts,
                "recommendation": recommendation,
                "created_at": row.get("created_at"),
                "updated_at": row.get("updated_at"),
            }
        )

    json_payload = {
        "generated_utc": now_utc(),
        "db": str(DB_PATH),
        "filters": {
            "request_id": getattr(args, "request_id", None),
            "lane_id": getattr(args, "lane_id", None),
            "service_id": getattr(args, "service_id", None),
            "request_type": getattr(args, "request_type", None),
            "status": getattr(args, "status", None),
            "limit": args.limit,
        },
        "counts_by_status": counts_by_status,
        "counts_by_lane": counts_by_lane,
        "counts_by_service": counts_by_service,
        "requests": review_rows,
        "external_side_effects": False,
        "approval_granted_by_report": False,
    }
    json_output_path.write_text(json.dumps(json_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Service Request Review Queue",
        "",
        f"Generated UTC: {json_payload['generated_utc']}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        "",
        "## Operating Rule",
        "",
        "This report is read-only review infrastructure. It does not approve, assign, start, submit, browse, register, trade, spend, post, or contact anyone.",
        "",
        "A service request may move only through explicit CLI lifecycle commands with exact scope, reviewer, assignee, and proof artifact. `needs_review` means blocked.",
        "",
        "## Counts",
        "",
        f"- Requests in report: `{len(review_rows)}`",
        f"- By status: `{json.dumps(counts_by_status, sort_keys=True)}`",
        f"- By lane: `{json.dumps(counts_by_lane, sort_keys=True)}`",
        f"- By service/request type: `{json.dumps(counts_by_service, sort_keys=True)}`",
        "",
        "## Review Index",
        "",
        "| Status | Request | Lane | Service | Validation | Approval Scope | Recommended Next Action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in review_rows:
        validation_label = "ok" if row["validation_ok"] else "missing: " + ", ".join(row["missing_fields"])
        scope_label = "present" if row["approval_scope_present"] else "missing"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['status']}`",
                    f"`{row['request_id']}`",
                    f"`{row['lane_id']}`",
                    f"`{row['service_id'] or row['request_type']}`",
                    md_cell(validation_label, 120),
                    md_cell(scope_label, 80),
                    md_cell(row["recommendation"], 360),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Detail", ""])
    for row in review_rows:
        lines.extend(
            [
                f"### {row['request_id']}",
                "",
                f"- Status: `{row['status']}`",
                f"- Lane: `{row['lane_id']}`",
                f"- Department: {row['department'] or ''}",
                f"- Service: `{row['service_id'] or ''}` {row['service_name'] or ''}".rstrip(),
                f"- Request type: `{row['request_type']}`",
                f"- Owner role: `{row['owner_role_id'] or ''}`",
                f"- Risk gate: {row['risk_gate'] or ''}",
                f"- Requested action: {row['requested_action'] or ''}",
                f"- Validation: `{'ok' if row['validation_ok'] else 'missing'}`",
                f"- Missing fields: {', '.join(row['missing_fields']) or 'none'}",
                f"- Required intake: {', '.join(str(item) for item in row['required_intake']) or 'none'}",
                f"- Approval required by: {', '.join(str(item) for item in row['approval_required_by']) or 'not cataloged'}",
                f"- Approval scope present: `{row['approval_scope_present']}`",
                f"- Assigned agent: `{row['assigned_agent_id'] or ''}`",
                f"- Artifact path: `{row['artifact_path'] or ''}`",
                f"- Decision note: {row['decision_note'] or ''}",
                f"- Recommended next action: {row['recommendation']}",
                "",
            ]
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(output_path), "json_path": str(json_output_path), "count": len(review_rows)}, indent=2))
