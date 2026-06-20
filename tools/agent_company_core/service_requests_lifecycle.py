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


from .service_requests_core import get_service_request, validate_service_request_record

def approve_service_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    get_service_request(conn, args.request_id)
    approval_id = args.approval_id or f"approval-{safe_id_fragment(args.request_id, 72)}"
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO approvals(approval_id, request_id, status, approved_by, exact_scope, expires_at, created_at)
        VALUES(?, ?, 'approved', ?, ?, ?, ?)
        ON CONFLICT(approval_id) DO UPDATE SET
          status=excluded.status,
          approved_by=excluded.approved_by,
          exact_scope=excluded.exact_scope,
          expires_at=excluded.expires_at
        """,
        (approval_id, args.request_id, args.approved_by, args.exact_scope, args.expires_at, ts),
    )
    conn.execute(
        """
        UPDATE service_requests
        SET status = 'approved',
            approval_scope = ?,
            decision_note = ?,
            updated_at = ?
        WHERE request_id = ?
        """,
        (args.exact_scope, args.decision_note, ts, args.request_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "request_id": args.request_id, "status": "approved", "approval_id": approval_id}, indent=2))


def reject_service_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    get_service_request(conn, args.request_id)
    approval_id = args.approval_id or f"rejection-{safe_id_fragment(args.request_id, 72)}"
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO approvals(approval_id, request_id, status, approved_by, exact_scope, expires_at, created_at)
        VALUES(?, ?, 'rejected', ?, ?, NULL, ?)
        ON CONFLICT(approval_id) DO UPDATE SET
          status=excluded.status,
          approved_by=excluded.approved_by,
          exact_scope=excluded.exact_scope
        """,
        (approval_id, args.request_id, args.rejected_by, args.reason, ts),
    )
    conn.execute(
        """
        UPDATE service_requests
        SET status = 'rejected',
            decision_note = ?,
            updated_at = ?
        WHERE request_id = ?
        """,
        (args.reason, ts, args.request_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "request_id": args.request_id, "status": "rejected", "approval_id": approval_id}, indent=2))


def assign_service_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = get_service_request(conn, args.request_id)
    if row["status"] in {"complete", "rejected", "cancelled"} and not args.force:
        raise SystemExit(f"Service request {args.request_id} is {row['status']}")
    ts = now_utc()
    conn.execute(
        """
        UPDATE service_requests
        SET assigned_agent_id = ?,
            decision_note = COALESCE(?, decision_note),
            updated_at = ?
        WHERE request_id = ?
        """,
        (args.agent_id, args.decision_note, ts, args.request_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "request_id": args.request_id, "assigned_agent_id": args.agent_id}, indent=2))


def start_service_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = get_service_request(conn, args.request_id)
    validation = validate_service_request_record(conn, row)
    if not validation["ok"] and not args.force:
        raise SystemExit(
            f"Cannot start request `{args.request_id}`: missing catalog intake fields "
            f"{', '.join(validation.get('missing', []))}. Use --force only after explicit coordination."
        )
    if row["status"] not in {"approved", "in_progress"} and not args.force:
        raise SystemExit(
            f"Service request {args.request_id} is {row['status']}; approve it before start, or use --force after explicit coordination."
        )
    if row["assigned_agent_id"] and row["assigned_agent_id"] != args.agent_id and not args.force:
        raise SystemExit(
            f"Service request is assigned to {row['assigned_agent_id']}; {args.agent_id} cannot start it without --force."
        )
    ts = now_utc()
    conn.execute(
        """
        UPDATE service_requests
        SET status = 'in_progress',
            assigned_agent_id = COALESCE(assigned_agent_id, ?),
            artifact_path = COALESCE(?, artifact_path),
            decision_note = COALESCE(?, decision_note),
            started_at = COALESCE(started_at, ?),
            updated_at = ?
        WHERE request_id = ?
        """,
        (args.agent_id, args.artifact_path, args.decision_note, ts, ts, args.request_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "request_id": args.request_id, "status": "in_progress"}, indent=2))


def complete_service_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = get_service_request(conn, args.request_id)
    if row["assigned_agent_id"] and row["assigned_agent_id"] != args.agent_id and not args.force:
        raise SystemExit(
            f"Service request is assigned to {row['assigned_agent_id']}; {args.agent_id} cannot complete it without --force."
        )
    if row["status"] in {"rejected", "cancelled"} and not args.force:
        raise SystemExit(f"Service request {args.request_id} is {row['status']}")
    ts = now_utc()
    conn.execute(
        """
        UPDATE service_requests
        SET status = 'complete',
            assigned_agent_id = COALESCE(assigned_agent_id, ?),
            artifact_path = COALESCE(?, artifact_path),
            decision_note = COALESCE(?, decision_note),
            completed_at = ?,
            updated_at = ?
        WHERE request_id = ?
        """,
        (args.agent_id, args.artifact_path, args.decision_note, ts, ts, args.request_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "request_id": args.request_id, "status": "complete"}, indent=2))
