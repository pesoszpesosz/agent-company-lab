"""Close owner acknowledgement requests after durable owner evidence exists."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "ai_resources_owner_acknowledgement_closure.v1"
DEFAULT_JSON = REPORTS_DIR / "ai-resources-owner-acknowledgement-closure-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "ai-resources-owner-acknowledgement-closure-v1-20260621.md"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
TERMINAL_STATUSES = {"complete", "cancelled", "closed"}
ACK_RESPONSE_TASK_PREFIX = "task-continuity-owner-response-task-acknowledgement_response_required-"


def _source_query(input_id: str | None) -> tuple[str, tuple[Any, ...]]:
    if input_id:
        return (
            """
            SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
                   evidence_required, next_action, created_at, updated_at, completed_at
            FROM tasks
            WHERE duplicate_key LIKE ?
            ORDER BY lane_id, task_id
            """,
            (f"{input_id}:owner-acknowledgement:%",),
        )
    return (
        """
        SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
               evidence_required, next_action, created_at, updated_at, completed_at
        FROM tasks
        WHERE duplicate_key LIKE ?
        ORDER BY lane_id, task_id
        """,
        ("%:owner-acknowledgement:%",),
    )


def _direct_evidence(conn: sqlite3.Connection, source_task_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT artifact_id, task_id, lane_id, kind, path_or_url, sha256, notes, created_at
        FROM artifacts
        WHERE task_id = ?
          AND (
            kind LIKE '%acknowledgement%'
            OR kind LIKE '%continuity%'
            OR path_or_url LIKE '%acknowledgement%'
            OR path_or_url LIKE '%continuity%'
          )
        ORDER BY created_at DESC, artifact_id DESC
        LIMIT 1
        """,
        (source_task_id,),
    ).fetchone()
    return dict(row) if row else None


def _response_evidence(conn: sqlite3.Connection, source: sqlite3.Row) -> dict[str, Any] | None:
    rows = conn.execute(
        """
        SELECT
          response.task_id AS response_task_id,
          response.status AS response_status,
          response.completed_at AS response_completed_at,
          artifact.artifact_id AS artifact_id,
          artifact.task_id AS artifact_task_id,
          artifact.lane_id AS lane_id,
          artifact.kind AS kind,
          artifact.path_or_url AS path_or_url,
          artifact.sha256 AS sha256,
          artifact.notes AS notes,
          artifact.created_at AS created_at
        FROM tasks response
        JOIN artifacts artifact ON artifact.task_id = response.task_id
        WHERE response.lane_id = ?
          AND response.owner_agent_id = ?
          AND response.status IN ('complete', 'closed')
          AND response.task_id LIKE ?
          AND (
            response.title LIKE ?
            OR response.task_id LIKE ?
            OR response.next_action LIKE ?
          )
          AND (
            artifact.kind LIKE '%acknowledgement%'
            OR artifact.kind LIKE '%continuity%'
            OR artifact.path_or_url LIKE '%acknowledgement%'
            OR artifact.path_or_url LIKE '%continuity%'
          )
        ORDER BY artifact.created_at DESC, artifact.artifact_id DESC
        """,
        (
            source["lane_id"],
            source["owner_agent_id"],
            f"{ACK_RESPONSE_TASK_PREFIX}%",
            f"%{source['task_id']}%",
            f"%{safe_id_fragment(source['lane_id'], 40)}%",
            f"%{source['lane_id']}%",
        ),
    ).fetchall()
    for row in rows:
        evidence = dict(row)
        if Path(evidence["path_or_url"]).exists():
            return evidence
    return dict(rows[0]) if rows else None


def _evidence_exists(evidence: dict[str, Any] | None) -> bool:
    return bool(evidence and Path(evidence["path_or_url"]).exists())


def _classify_source(conn: sqlite3.Connection, source: sqlite3.Row) -> dict[str, Any]:
    direct = _direct_evidence(conn, source["task_id"])
    evidence = direct if _evidence_exists(direct) else _response_evidence(conn, source)
    can_close = source["status"] not in TERMINAL_STATUSES and _evidence_exists(evidence)
    reason = "already_terminal" if source["status"] in TERMINAL_STATUSES else "closure_ready" if can_close else "missing_completed_response_evidence"
    return {
        "source_task_id": source["task_id"],
        "lane_id": source["lane_id"],
        "source_status": source["status"],
        "owner_agent_id": source["owner_agent_id"],
        "duplicate_key": source["duplicate_key"],
        "closure_status": reason,
        "can_close": can_close,
        "evidence_artifact_id": evidence.get("artifact_id") if evidence else None,
        "evidence_artifact_path": evidence.get("path_or_url") if evidence else None,
        "response_task_id": evidence.get("response_task_id") if evidence else evidence.get("artifact_task_id") if evidence else None,
    }


def _collect(conn: sqlite3.Connection, input_id: str | None) -> list[dict[str, Any]]:
    sql, params = _source_query(input_id)
    return [_classify_source(conn, row) for row in conn.execute(sql, params).fetchall()]


def _counts(items: list[dict[str, Any]], applied_count: int = 0) -> dict[str, int]:
    counts = {
        "source_acknowledgements": len(items),
        "closure_candidates": sum(1 for item in items if item["can_close"]),
        "closure_applied": applied_count,
        "already_terminal": sum(1 for item in items if item["closure_status"] == "already_terminal"),
        "missing_completed_response_evidence": sum(
            1 for item in items if item["closure_status"] == "missing_completed_response_evidence"
        ),
    }
    return counts


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# AI Resources Owner Acknowledgement Closure V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Input filter: `{payload.get('input_id') or 'all'}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Counts",
        "",
        "| Count | Value |",
        "| --- | ---: |",
    ]
    for key, value in payload["counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Closure Items",
            "",
            "| Lane | Source Task | Status | Closure | Evidence | Response Task |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["closure_items"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['source_task_id']}`",
                    md_cell(item.get("source_status"), 60),
                    md_cell(item.get("closure_status"), 80),
                    md_cell(item.get("evidence_artifact_path"), 180),
                    md_cell(item.get("response_task_id"), 160),
                ]
            )
            + " |"
        )
    if not payload["closure_items"]:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This closure reconciles local acknowledgement source tasks only after existing local evidence is present. It does not create agents, mutate lane ownership, start workers, open browsers, create accounts, publish, submit, trade, spend, call external APIs, approve service requests, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _apply_closures(conn: sqlite3.Connection, items: list[dict[str, Any]], generated_utc: str) -> int:
    applied = 0
    for item in items:
        if not item["can_close"]:
            continue
        lane_fragment = safe_id_fragment(item["lane_id"], 70)
        source_fragment = safe_id_fragment(item["source_task_id"], 70)
        artifact_id = f"artifact-ai-resources-owner-acknowledgement-closure-evidence-{lane_fragment}-{source_fragment}"
        path = Path(item["evidence_artifact_path"])
        conn.execute(
            """
            INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
            VALUES(?, ?, ?, 'owner_acknowledgement_closure_evidence', ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
              lane_id=excluded.lane_id,
              task_id=excluded.task_id,
              kind=excluded.kind,
              path_or_url=excluded.path_or_url,
              sha256=excluded.sha256,
              notes=excluded.notes
            """,
            (
                artifact_id,
                item["lane_id"],
                item["source_task_id"],
                str(path),
                sha256_file(path),
                f"Source acknowledgement closed from existing owner response evidence `{item['evidence_artifact_id']}`.",
                generated_utc,
            ),
        )
        conn.execute(
            """
            UPDATE tasks
            SET status = 'complete',
                completed_at = ?,
                updated_at = ?,
                next_action = ?
            WHERE task_id = ?
            """,
            (
                generated_utc,
                generated_utc,
                f"Owner acknowledgement evidence linked at {path}; continue the lane follow-up locally with existing owner and no duplicate worker.",
                item["source_task_id"],
            ),
        )
        item["closure_status"] = "closed"
        item["closure_artifact_id"] = artifact_id
        applied += 1
    return applied


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    input_fragment = safe_id_fragment(payload.get("input_id") or "all", 90)
    task_id = f"task-ai-resources-owner-acknowledgement-closure-v1-{input_fragment}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, ?, 'complete', 90, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          title=excluded.title,
          status=excluded.status,
          priority=excluded.priority,
          owner_agent_id=excluded.owner_agent_id,
          duplicate_key=excluded.duplicate_key,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            task_id,
            AI_RESOURCES_LANE,
            f"Close owner acknowledgement requests for {payload.get('input_id') or 'all'}",
            AI_RESOURCES_OWNER,
            f"{payload.get('input_id') or 'all'}:owner-acknowledgement-closure",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (
            f"artifact-ai-resources-owner-acknowledgement-closure-json-{input_fragment}",
            "ai_resources_owner_acknowledgement_closure_json",
            json_path,
            "Machine-readable owner acknowledgement closure report.",
        ),
        (
            f"artifact-ai-resources-owner-acknowledgement-closure-md-{input_fragment}",
            "ai_resources_owner_acknowledgement_closure",
            md_path,
            "Human-readable owner acknowledgement closure report.",
        ),
    ]:
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
            (artifact_id, AI_RESOURCES_LANE, task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "input_id": payload.get("input_id"),
        "counts": payload["counts"],
        "closed_source_task_ids": [
            item["source_task_id"] for item in payload["closure_items"] if item["closure_status"] == "closed"
        ],
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'ai_resources_owner_acknowledgement_closure_written', ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          trace_id=excluded.trace_id,
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          agent_id=excluded.agent_id,
          event_time=excluded.event_time,
          source=excluded.source,
          summary=excluded.summary,
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path
        """,
        (
            f"trace-event-ai-resources-owner-acknowledgement-closure-{input_fragment}",
            f"trace-ai-resources-owner-acknowledgement-closure-{input_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            AI_RESOURCES_OWNER,
            ts,
            "ai_resources_owner_acknowledgement_closure_v1",
            f"Closed {payload['counts']['closure_applied']} owner acknowledgement source tasks from existing evidence.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, 'ai_resources_owner_acknowledgement_closure', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-ai-resources-owner-acknowledgement-closure-{input_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            payload["status"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )


def close_ai_resources_owner_acknowledgements(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    input_id = getattr(args, "input_id", None)
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    items = _collect(conn, input_id)
    applied = 0 if getattr(args, "no_db_record", False) else _apply_closures(conn, items, generated)
    counts = _counts(items, applied)
    if counts["closure_applied"]:
        status = "closure_applied"
    elif counts["closure_candidates"]:
        status = "closure_ready"
    elif counts["missing_completed_response_evidence"]:
        status = "evidence_missing"
    else:
        status = "no_closure_needed"
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "input_id": input_id,
        "counts": counts,
        "closure_items": items,
        "next_action": (
            "Regenerate owner acknowledgement monitor, CEO state, and continuity watchdog reports."
            if counts["closure_applied"]
            else "Route missing evidence to existing lane owners; do not create duplicate workers."
            if counts["missing_completed_response_evidence"]
            else "No owner acknowledgement source closure action is needed."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
        conn.commit()
    return payload


def write_ai_resources_owner_acknowledgement_closure(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = close_ai_resources_owner_acknowledgements(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "input_id": payload.get("input_id"),
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
