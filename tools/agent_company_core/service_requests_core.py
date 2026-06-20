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


def resolve_service_catalog_entry(
    conn: sqlite3.Connection, service_id: str | None, request_type: str
) -> sqlite3.Row | None:
    if service_id:
        row = conn.execute("SELECT * FROM service_catalog WHERE service_id = ?", (service_id,)).fetchone()
        if not row:
            raise SystemExit(f"Unknown service_id: {service_id}. Run seed-service-catalog first.")
        if row["request_type"] != request_type:
            raise SystemExit(
                f"Service `{service_id}` has request_type `{row['request_type']}`, "
                f"but request used `{request_type}`."
            )
        return row
    matches = list(conn.execute("SELECT * FROM service_catalog WHERE request_type = ?", (request_type,)))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise SystemExit(f"Request type `{request_type}` has multiple catalog entries; pass --service-id.")
    return None


def validate_service_intake(service: sqlite3.Row | None, intake_json: str) -> dict[str, Any]:
    try:
        parsed = json.loads(intake_json or "{}")
    except json.JSONDecodeError as exc:
        return {"ok": False, "error": f"Invalid intake_json: {exc}", "missing": []}
    if not isinstance(parsed, dict):
        return {"ok": False, "error": "intake_json must be a JSON object", "missing": []}
    if not service:
        return {"ok": True, "service_id": None, "required": [], "missing": [], "intake": parsed}
    required = decode_json_list(service["required_intake_json"])
    missing = [field for field in required if parsed.get(field) in (None, "", [])]
    return {
        "ok": not missing,
        "service_id": service["service_id"],
        "request_type": service["request_type"],
        "status": service["default_status"],
        "required": required,
        "missing": missing,
        "intake": parsed,
    }


def create_service_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    service = resolve_service_catalog_entry(conn, args.service_id, args.request_type)
    intake_json = parse_json_arg(args.intake_json, args.intake_file, {})
    validation = validate_service_intake(service, intake_json)
    if not validation["ok"]:
        missing = ", ".join(validation.get("missing", []))
        raise SystemExit(
            f"Service request intake is incomplete for `{validation.get('service_id')}`. "
            f"Missing required field(s): {missing or validation.get('error', 'unknown')}"
        )
    service_id = service["service_id"] if service else None
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO service_requests(
          request_id, service_id, request_type, lane_id, requester_agent_id, risk_gate,
          requested_action, intake_json, approval_scope, artifact_path, created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            args.request_id,
            service_id,
            args.request_type,
            args.lane_id,
            args.requester_agent_id,
            args.risk_gate,
            args.requested_action,
            intake_json,
            args.approval_scope,
            args.artifact_path,
            ts,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "request_id": args.request_id, "service_id": service_id, "status": "needs_review"}, indent=2))


def get_service_request(conn: sqlite3.Connection, request_id: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM service_requests WHERE request_id = ?", (request_id,)).fetchone()
    if not row:
        raise SystemExit(f"Unknown service request: {request_id}")
    return row


def validate_service_request_record(conn: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
    service = resolve_service_catalog_entry(conn, row["service_id"], row["request_type"])
    result = validate_service_intake(service, row["intake_json"])
    result["request_id"] = row["request_id"]
    result["request_status"] = row["status"]
    result["approval_scope_present"] = bool(row["approval_scope"])
    return result


def validate_service_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = get_service_request(conn, args.request_id)
    result = validate_service_request_record(conn, row)
    print(json.dumps(result, indent=2))
