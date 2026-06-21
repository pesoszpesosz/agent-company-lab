"""Close continuity lane-next tasks once their local proof artifacts exist."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .continuity_lane_next_task_seed import (
    AI_RESOURCES_LANE,
    AI_RESOURCES_OWNER,
    LANE_FOLLOWUP_PROFILES,
    LANE_PROFILES,
    TERMINAL_STATUSES,
)
from .io import now_utc
from .paths import REPORTS_DIR, ROOT
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "continuity_lane_next_task_closure.v1"
AR_WATCH_TASK_ID = "task-ai-resources-lane-next-evidence-watch-20260621"
AR_WATCH_DUPLICATE_KEY = "ai_resources:lane_next_evidence_watch:20260621"


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"continuity-lane-next-task-closure-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"continuity-lane-next-task-closure-v1-{day}.md")
    return json_path, md_path


def _proof_root(args: argparse.Namespace) -> Path:
    return Path(getattr(args, "proof_root", None) or ROOT)


def _lane_next_tasks(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
               evidence_required, next_action, created_at, updated_at, completed_at
        FROM tasks
        WHERE duplicate_key LIKE 'continuity:lane-next-task:%'
        ORDER BY lane_id, task_id
        """
    ).fetchall()


def _task_sequence(task: sqlite3.Row) -> str:
    duplicate_key = task["duplicate_key"] or ""
    return duplicate_key.rsplit(":", 1)[-1] if ":" in duplicate_key else "001"


def _profile_for_task(task: sqlite3.Row) -> dict[str, Any] | None:
    lane_id = task["lane_id"]
    sequence = _task_sequence(task)
    if sequence == "002" and lane_id in LANE_FOLLOWUP_PROFILES:
        return LANE_FOLLOWUP_PROFILES[lane_id]
    if sequence != "001":
        lane_fragment = safe_id_fragment(lane_id, 80)
        return {
            "expected_artifact": f"reports/{lane_fragment}/proof-derived-continuation-v1-{{day}}-{{sequence}}.md",
            "next_action": (
                "Read the evidence artifact for this task, extract exactly one concrete next local step or explicit "
                "park/revisit condition from it, and write a compact continuation packet with evidence, gate status, "
                "owner, expected next artifact, and stop conditions."
            ),
        }
    return LANE_PROFILES.get(lane_id)


def _expected_proof_path(task: sqlite3.Row, generated_utc: str, proof_root: Path) -> Path | None:
    profile = _profile_for_task(task)
    if not profile:
        return None
    day = generated_utc[:10].replace("-", "")
    raw = Path(profile["expected_artifact"].format(day=day, sequence=_task_sequence(task)))
    return raw if raw.is_absolute() else proof_root / raw


def _artifact_for_path(conn: sqlite3.Connection, task_id: str, path: Path) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at
        FROM artifacts
        WHERE task_id = ? AND path_or_url = ?
        ORDER BY created_at DESC, artifact_id DESC
        LIMIT 1
        """,
        (task_id, str(path)),
    ).fetchone()
    return dict(row) if row else None


def _upsert_closure_proof_artifact(
    conn: sqlite3.Connection,
    task: sqlite3.Row,
    path: Path,
    generated_utc: str,
) -> dict[str, Any]:
    lane_fragment = safe_id_fragment(task["lane_id"], 70)
    artifact_id = f"artifact-continuity-lane-next-task-proof-{lane_fragment}"
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES(?, ?, ?, 'continuity_lane_next_task_proof', ?, ?, ?, ?)
        ON CONFLICT(artifact_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          kind=excluded.kind,
          path_or_url=excluded.path_or_url,
          sha256=excluded.sha256,
          notes=excluded.notes,
          created_at=excluded.created_at
        """,
        (
            artifact_id,
            task["lane_id"],
            task["task_id"],
            str(path),
            sha256_file(path),
            "Registered expected proof artifact for lane-next task closure.",
            generated_utc,
        ),
    )
    return {
        "artifact_id": artifact_id,
        "lane_id": task["lane_id"],
        "task_id": task["task_id"],
        "kind": "continuity_lane_next_task_proof",
        "path_or_url": str(path),
        "sha256": sha256_file(path),
        "notes": "Registered expected proof artifact for lane-next task closure.",
        "created_at": generated_utc,
        "path_exists": True,
        "source": "expected_artifact_registered_by_closure",
    }


def _latest_non_seed_artifact(conn: sqlite3.Connection, task_id: str) -> dict[str, Any] | None:
    rows = conn.execute(
        """
        SELECT artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at
        FROM artifacts
        WHERE task_id = ?
          AND kind NOT LIKE '%seed%'
          AND kind NOT LIKE '%input%'
        ORDER BY created_at DESC, artifact_id DESC
        LIMIT 20
        """,
        (task_id,),
    ).fetchall()
    for row in rows:
        item = dict(row)
        if Path(item["path_or_url"]).exists():
            return item
    return dict(rows[0]) if rows else None


def _proof_artifact(
    conn: sqlite3.Connection,
    task: sqlite3.Row,
    generated_utc: str,
    proof_root: Path,
    no_db_record: bool,
) -> dict[str, Any] | None:
    expected = _expected_proof_path(task, generated_utc, proof_root)
    if expected and expected.exists():
        existing = _artifact_for_path(conn, task["task_id"], expected)
        if not no_db_record:
            return _upsert_closure_proof_artifact(conn, task, expected, generated_utc)
        if existing:
            existing["path_exists"] = True
            existing["source"] = "expected_artifact_registered"
            return existing
        if no_db_record:
            return {
                "artifact_id": None,
                "lane_id": task["lane_id"],
                "task_id": task["task_id"],
                "kind": "continuity_lane_next_task_proof",
                "path_or_url": str(expected),
                "sha256": sha256_file(expected),
                "notes": "Expected proof artifact exists but is not registered.",
                "created_at": generated_utc,
                "path_exists": True,
                "source": "expected_artifact_unregistered",
            }
    artifact = _latest_non_seed_artifact(conn, task["task_id"])
    if artifact:
        artifact["path_exists"] = Path(artifact["path_or_url"]).exists()
        artifact["source"] = "latest_non_seed_artifact"
        return artifact
    return None


def _close_task_if_ready(
    conn: sqlite3.Connection,
    task: sqlite3.Row,
    proof: dict[str, Any] | None,
    generated_utc: str,
    no_db_record: bool,
) -> dict[str, Any]:
    terminal = task["status"] in TERMINAL_STATUSES
    proof_exists = bool(proof and proof.get("path_exists"))
    item: dict[str, Any] = {
        "lane_id": task["lane_id"],
        "task_id": task["task_id"],
        "owner_agent_id": task["owner_agent_id"],
        "source_status": task["status"],
        "source_completed_at": task["completed_at"],
        "proof_artifact_id": proof.get("artifact_id") if proof else None,
        "proof_path": proof.get("path_or_url") if proof else None,
        "proof_source": proof.get("source") if proof else None,
        "proof_path_exists": proof_exists,
    }
    if terminal and task["completed_at"]:
        if not proof_exists:
            profile = _profile_for_task(task) or {}
            item["closure_status"] = "reopened_missing_proof_artifact"
            if not no_db_record:
                conn.execute(
                    """
                    UPDATE tasks
                    SET status = 'new',
                        completed_at = NULL,
                        updated_at = ?,
                        next_action = ?
                    WHERE task_id = ?
                    """,
                    (
                        generated_utc,
                        profile.get(
                            "next_action",
                            "Expected proof artifact is missing; continue the bounded local task and keep gates closed.",
                        ),
                        task["task_id"],
                    ),
                )
            return item
        item["closure_status"] = "already_closed"
        return item
    if terminal and proof_exists:
        completed_at = task["updated_at"] or generated_utc
        item["closure_status"] = "completed_at_repaired"
        item["completed_at"] = completed_at
        if not no_db_record:
            conn.execute(
                "UPDATE tasks SET completed_at = ?, updated_at = ? WHERE task_id = ?",
                (completed_at, generated_utc, task["task_id"]),
            )
        return item
    if proof_exists:
        item["closure_status"] = "closed"
        item["completed_at"] = generated_utc
        if not no_db_record:
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
                    f"Local proof artifact recorded at {proof['path_or_url']}; continue with the packet's next local evidence step and keep gates closed.",
                    task["task_id"],
                ),
            )
        return item
    item["closure_status"] = "missing_proof_artifact" if terminal else "waiting_for_proof_artifact"
    return item


def _open_lane_next_count(conn: sqlite3.Connection) -> int:
    terminal = tuple(TERMINAL_STATUSES)
    placeholders = ",".join("?" for _ in terminal)
    return int(
        conn.execute(
            f"""
            SELECT COUNT(*)
            FROM tasks
            WHERE duplicate_key LIKE 'continuity:lane-next-task:%'
              AND status NOT IN ({placeholders})
            """,
            terminal,
        ).fetchone()[0]
    )


def _counts(items: list[dict[str, Any]], open_after: int) -> dict[str, int]:
    return {
        "lane_next_tasks": len(items),
        "closed": sum(1 for item in items if item["closure_status"] == "closed"),
        "completed_at_repaired": sum(1 for item in items if item["closure_status"] == "completed_at_repaired"),
        "already_closed": sum(1 for item in items if item["closure_status"] == "already_closed"),
        "missing_proof_artifact": sum(1 for item in items if item["closure_status"] == "missing_proof_artifact"),
        "waiting_for_proof_artifact": sum(
            1 for item in items if item["closure_status"] == "waiting_for_proof_artifact"
        ),
        "reopened_missing_proof_artifact": sum(
            1 for item in items if item["closure_status"] == "reopened_missing_proof_artifact"
        ),
        "open_lane_next_tasks_after": open_after,
    }


def _status_from_counts(counts: dict[str, int], ar_watch_closed: bool) -> str:
    if counts["missing_proof_artifact"]:
        return "proof_missing"
    if counts["closed"] or counts["completed_at_repaired"] or counts["reopened_missing_proof_artifact"] or ar_watch_closed:
        return "closure_applied"
    if counts["waiting_for_proof_artifact"]:
        return "waiting_for_lane_next_tasks"
    return "already_closed"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Continuity Lane Next Task Closure V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
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
            "| Lane | Task | Closure | Proof |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in payload["closure_items"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['task_id']}`",
                    f"`{item['closure_status']}`",
                    md_cell(item.get("proof_path"), 180),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## AI Resources Watch",
            "",
            f"Status: `{payload['ar_watch_status']}`",
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This closure links existing local proof artifacts and updates local task state only. It does not create agents, mutate lane ownership, start workers, approve service requests, open browsers, create accounts, publish, submit, trade, spend, call external APIs, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _close_ar_watch_if_ready(
    conn: sqlite3.Connection,
    generated_utc: str,
    md_path: Path,
    no_db_record: bool,
) -> str:
    if _open_lane_next_count(conn) != 0:
        return "waiting_for_lane_next_tasks"
    row = conn.execute(
        """
        SELECT task_id, status
        FROM tasks
        WHERE task_id = ? OR duplicate_key = ?
        LIMIT 1
        """,
        (AR_WATCH_TASK_ID, AR_WATCH_DUPLICATE_KEY),
    ).fetchone()
    if not row:
        return "no_ar_watch_task"
    if row["status"] in TERMINAL_STATUSES:
        return "already_closed"
    if no_db_record:
        return "ready_to_close_report_only"
    conn.execute(
        """
        UPDATE tasks
        SET status = 'complete',
            completed_at = ?,
            updated_at = ?,
            evidence_required = ?,
            next_action = 'All continuity lane-next proof artifacts are complete; continue normal AR monitoring and keep service gates closed.'
        WHERE task_id = ?
        """,
        (generated_utc, generated_utc, str(md_path), row["task_id"]),
    )
    return "closed"


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-continuity-lane-next-task-closure-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Close completed continuity lane-next tasks', 'complete', 90, ?, ?, ?, ?, ?, ?, ?, ?)
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
            AI_RESOURCES_OWNER,
            f"continuity:lane-next-task-closure:{day}",
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
            f"artifact-continuity-lane-next-task-closure-json-{day}",
            "continuity_lane_next_task_closure_json",
            json_path,
            "Machine-readable lane-next closure report.",
        ),
        (
            f"artifact-continuity-lane-next-task-closure-md-{day}",
            "continuity_lane_next_task_closure",
            md_path,
            "Human-readable lane-next closure report.",
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
              notes=excluded.notes,
              created_at=excluded.created_at
            """,
            (artifact_id, AI_RESOURCES_LANE, task_id, kind, str(path), sha256_file(path), notes, ts),
        )


def close_continuity_lane_next_tasks(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _report_paths(generated, args)
    proof_root = _proof_root(args)
    no_db_record = bool(getattr(args, "no_db_record", False))
    closure_items: list[dict[str, Any]] = []
    for task in _lane_next_tasks(conn):
        proof = _proof_artifact(conn, task, generated, proof_root, no_db_record)
        closure_items.append(_close_task_if_ready(conn, task, proof, generated, no_db_record))
    open_after = _open_lane_next_count(conn)
    ar_watch_status = _close_ar_watch_if_ready(conn, generated, md_path, no_db_record)
    ar_watch_closed = ar_watch_status == "closed"
    counts = _counts(closure_items, open_after)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": _status_from_counts(counts, ar_watch_closed),
        "counts": counts,
        "closure_items": closure_items,
        "ar_watch_status": ar_watch_status,
        "next_action": (
            "Regenerate CEO state, manager packets, dashboard, and continuity watchdog reports."
            if counts["closed"] or counts["completed_at_repaired"] or ar_watch_closed
            else "Continue monitoring missing proof artifacts through existing lane owners."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not no_db_record:
        _record_run(conn, payload, json_path, md_path)
        conn.commit()
    return payload


def write_continuity_lane_next_task_closure_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = close_continuity_lane_next_tasks(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "ar_watch_status": payload["ar_watch_status"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
