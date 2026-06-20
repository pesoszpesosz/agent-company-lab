"""Agent, lane, task, artifact, outcome, and trace registry operations."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone

from .io import now_utc, parse_utc
from .utils import parse_metadata_arg, safe_id_fragment


def claim_lane(conn: sqlite3.Connection, lane_id: str, agent_id: str, thread_id: str, force: bool) -> None:
    row = conn.execute("SELECT * FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    if not row:
        raise SystemExit(f"Unknown lane: {lane_id}")
    if row["owner_agent_id"] and row["owner_agent_id"] != agent_id and not force:
        raise SystemExit(
            f"Lane already owned by {row['owner_agent_id']} in thread {row['owner_thread_id']}. "
            "Use --force only after explicit coordination."
        )
    ts = now_utc()
    conn.execute(
        "UPDATE lanes SET owner_agent_id = ?, owner_thread_id = ?, updated_at = ? WHERE lane_id = ?",
        (agent_id, thread_id, ts, lane_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "lane_id": lane_id, "owner_agent_id": agent_id, "owner_thread_id": thread_id}, indent=2))


def register_agent(conn: sqlite3.Connection, agent_id: str, role_id: str, thread_id: str | None, department_id_: str | None) -> None:
    role = conn.execute("SELECT 1 FROM roles WHERE role_id = ?", (role_id,)).fetchone()
    if not role:
        raise SystemExit(f"Unknown role: {role_id}. Run init/seed first.")
    if department_id_:
        dep = conn.execute("SELECT 1 FROM departments WHERE department_id = ?", (department_id_,)).fetchone()
        if not dep:
            raise SystemExit(f"Unknown department: {department_id_}")
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, created_at, updated_at)
        VALUES(?, ?, ?, ?, ?, ?)
        ON CONFLICT(agent_id) DO UPDATE SET
          role_id=excluded.role_id,
          thread_id=excluded.thread_id,
          department_id=excluded.department_id,
          updated_at=excluded.updated_at
        """,
        (agent_id, role_id, thread_id, department_id_, ts, ts),
    )
    conn.commit()
    print(json.dumps({"ok": True, "agent_id": agent_id, "role_id": role_id}, indent=2))


def upsert_evidence(conn: sqlite3.Connection, args: dict[str, str | None]) -> None:
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO lane_evidence(
          evidence_id, lane_id, source_path, source_url, title, status, summary,
          next_action, ownership_note, created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(evidence_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          source_path=excluded.source_path,
          source_url=excluded.source_url,
          title=excluded.title,
          status=excluded.status,
          summary=excluded.summary,
          next_action=excluded.next_action,
          ownership_note=excluded.ownership_note,
          updated_at=excluded.updated_at
        """,
        (
            args["evidence_id"],
            args["lane_id"],
            args.get("source_path"),
            args.get("source_url"),
            args["title"],
            args["status"],
            args.get("summary"),
            args.get("next_action"),
            args.get("ownership_note"),
            ts,
            ts,
        ),
    )


def create_task(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO tasks(task_id, lane_id, title, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            args.task_id,
            args.lane_id,
            args.title,
            args.priority,
            args.owner_agent_id,
            args.duplicate_key,
            args.evidence_required,
            args.next_action,
            ts,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "task_id": args.task_id, "lane_id": args.lane_id}, indent=2))


def update_task(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = conn.execute("SELECT 1 FROM tasks WHERE task_id = ?", (args.task_id,)).fetchone()
    if not row:
        raise SystemExit(f"Unknown task: {args.task_id}")
    ts = now_utc()
    conn.execute(
        """
        UPDATE tasks
        SET status = COALESCE(?, status),
            next_action = COALESCE(?, next_action),
            updated_at = ?
        WHERE task_id = ?
        """,
        (args.status, args.next_action, ts, args.task_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "task_id": args.task_id}, indent=2))


def acquire_task(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = conn.execute("SELECT * FROM tasks WHERE task_id = ?", (args.task_id,)).fetchone()
    if not row:
        raise SystemExit(f"Unknown task: {args.task_id}")
    if row["status"] in {"complete", "cancelled"}:
        raise SystemExit(f"Task {args.task_id} is {row['status']}")

    now = datetime.now(timezone.utc)
    current_lease_owner = row["lease_owner_agent_id"]
    lease_expires_at = parse_utc(row["lease_expires_at"])
    lease_active = bool(current_lease_owner and lease_expires_at and lease_expires_at > now)
    if lease_active and current_lease_owner != args.agent_id and not args.force:
        raise SystemExit(
            f"Task is leased by {current_lease_owner} until {row['lease_expires_at']}. "
            "Use --force only after explicit coordination."
        )

    ts = now_utc()
    expires = (now + timedelta(minutes=args.lease_minutes)).isoformat(timespec="seconds").replace("+00:00", "Z")
    status = "in_progress" if row["status"] == "new" else row["status"]
    conn.execute(
        """
        UPDATE tasks
        SET status = ?,
            owner_agent_id = COALESCE(owner_agent_id, ?),
            lease_owner_agent_id = ?,
            lease_expires_at = ?,
            started_at = COALESCE(started_at, ?),
            updated_at = ?
        WHERE task_id = ?
        """,
        (status, args.agent_id, args.agent_id, expires, ts, ts, args.task_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "task_id": args.task_id, "lease_owner_agent_id": args.agent_id, "lease_expires_at": expires}, indent=2))


def release_task(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = conn.execute("SELECT * FROM tasks WHERE task_id = ?", (args.task_id,)).fetchone()
    if not row:
        raise SystemExit(f"Unknown task: {args.task_id}")
    if row["lease_owner_agent_id"] and row["lease_owner_agent_id"] != args.agent_id and not args.force:
        raise SystemExit(
            f"Task is leased by {row['lease_owner_agent_id']}; {args.agent_id} cannot release it without --force."
        )
    ts = now_utc()
    conn.execute(
        """
        UPDATE tasks
        SET lease_owner_agent_id = NULL,
            lease_expires_at = NULL,
            updated_at = ?
        WHERE task_id = ?
        """,
        (ts, args.task_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "task_id": args.task_id, "released_by": args.agent_id}, indent=2))


def complete_task(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = conn.execute("SELECT * FROM tasks WHERE task_id = ?", (args.task_id,)).fetchone()
    if not row:
        raise SystemExit(f"Unknown task: {args.task_id}")
    if row["lease_owner_agent_id"] and row["lease_owner_agent_id"] != args.agent_id and not args.force:
        raise SystemExit(
            f"Task is leased by {row['lease_owner_agent_id']}; {args.agent_id} cannot complete it without --force."
        )
    ts = now_utc()
    conn.execute(
        """
        UPDATE tasks
        SET status = 'complete',
            lease_owner_agent_id = NULL,
            lease_expires_at = NULL,
            completed_at = ?,
            next_action = COALESCE(?, next_action),
            updated_at = ?
        WHERE task_id = ?
        """,
        (ts, args.next_action, ts, args.task_id),
    )
    conn.commit()
    print(json.dumps({"ok": True, "task_id": args.task_id, "status": "complete"}, indent=2))


def record_artifact(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(artifact_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          kind=excluded.kind,
          path_or_url=excluded.path_or_url,
          sha256=excluded.sha256,
          notes=excluded.notes
        """,
        (
            args.artifact_id,
            args.lane_id,
            args.task_id,
            args.kind,
            args.path_or_url,
            args.sha256,
            args.notes,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "artifact_id": args.artifact_id}, indent=2))


def record_outcome(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          realized_usd=excluded.realized_usd,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            args.outcome_id,
            args.lane_id,
            args.task_id,
            args.outcome_type,
            args.status,
            args.realized_usd,
            args.evidence,
            args.next_action,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "outcome_id": args.outcome_id}, indent=2))


def evidence_id_for_source(prefix: str, source_key: str, title: str) -> str:
    digest = hashlib.sha1(source_key.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{safe_id_fragment(title, 50)}-{digest}"


def generated_trace_event_id(event_type: str, trace_id: str, summary: str, event_time: str) -> str:
    digest = hashlib.sha1(f"{trace_id}|{event_time}|{summary}".encode("utf-8")).hexdigest()[:12]
    return f"trace-{safe_id_fragment(event_type, 40)}-{digest}"


def record_trace_event(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    event_time = args.event_time or now_utc()
    event_id = args.event_id or generated_trace_event_id(args.event_type, args.trace_id, args.summary, event_time)
    metadata_json = parse_metadata_arg(args.metadata_json, args.metadata_file)
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          trace_id=excluded.trace_id,
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          agent_id=excluded.agent_id,
          event_type=excluded.event_type,
          event_time=excluded.event_time,
          source=excluded.source,
          summary=excluded.summary,
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path
        """,
        (
            event_id,
            args.trace_id,
            args.lane_id,
            args.task_id,
            args.agent_id,
            args.event_type,
            event_time,
            args.source,
            args.summary,
            metadata_json,
            args.artifact_path,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "event_id": event_id, "trace_id": args.trace_id}, indent=2))
