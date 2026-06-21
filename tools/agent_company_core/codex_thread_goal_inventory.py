"""Inventory Codex app threads that carry active goal work."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "codex_thread_goal_inventory.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
GOAL_SIGNAL_MARKERS = ("/goal", "active goal", "current goal", "goal:")


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"codex-thread-goal-inventory-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"codex-thread-goal-inventory-v1-{day}.md")
    return json_path, md_path


def _load_snapshot(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [dict(item) for item in payload]
    return [dict(item) for item in payload.get("threads", [])]


def _normalize_thread_id(thread_id: str | None) -> str:
    raw = str(thread_id or "")
    return raw.removeprefix("codex-thread:")


def _registered_thread_ids(conn: sqlite3.Connection) -> set[str]:
    registered: set[str] = set()
    for row in conn.execute("SELECT thread_id FROM agents WHERE thread_id IS NOT NULL AND thread_id != ''"):
        registered.add(_normalize_thread_id(row["thread_id"]))
    for row in conn.execute(
        "SELECT owner_thread_id FROM lanes WHERE owner_thread_id IS NOT NULL AND owner_thread_id != ''"
    ):
        registered.add(_normalize_thread_id(row["owner_thread_id"]))
    return registered


def _thread_status(thread: dict[str, Any]) -> str:
    status = thread.get("status")
    if isinstance(status, dict):
        return str(status.get("type") or "")
    return str(status or "")


def _has_goal_signal(thread: dict[str, Any]) -> bool:
    text = " ".join(str(thread.get(key) or "") for key in ["title", "preview", "prompt", "input"]).lower()
    return any(marker in text for marker in GOAL_SIGNAL_MARKERS)


def _repo_backed(cwd: str | None) -> bool:
    if not cwd:
        return False
    path = Path(cwd)
    if not path.exists():
        return False
    return any((candidate / ".git").exists() for candidate in [path, *path.parents])


def _thread_item(thread: dict[str, Any], registered_thread_ids: set[str]) -> dict[str, Any]:
    thread_id = _normalize_thread_id(thread.get("id") or thread.get("threadId"))
    has_goal = _has_goal_signal(thread)
    monitored = thread_id in registered_thread_ids
    status = _thread_status(thread)
    repo_backed = _repo_backed(thread.get("cwd"))
    recommended_actions: list[str] = []
    if has_goal and not monitored:
        recommended_actions.append("register_goal_thread")
    if has_goal and status == "systemError":
        recommended_actions.append("recover_system_error_thread")
    if has_goal and not repo_backed:
        recommended_actions.append("migrate_or_recreate_as_repo_backed_thread")
    return {
        "thread_id": thread_id,
        "title": str(thread.get("title") or ""),
        "status": status,
        "cwd": str(thread.get("cwd") or ""),
        "has_goal_signal": has_goal,
        "monitor_status": "monitored" if monitored else "unmonitored_goal_thread" if has_goal else "not_goal_thread",
        "repo_backed": repo_backed,
        "recommended_actions": recommended_actions,
    }


def _counts(items: list[dict[str, Any]]) -> dict[str, int]:
    goal_items = [item for item in items if item["has_goal_signal"]]
    return {
        "threads_seen": len(items),
        "goal_threads": len(goal_items),
        "monitored_goal_threads": sum(1 for item in goal_items if item["monitor_status"] == "monitored"),
        "unmonitored_goal_threads": sum(
            1 for item in goal_items if item["monitor_status"] == "unmonitored_goal_thread"
        ),
        "system_error_goal_threads": sum(1 for item in goal_items if item["status"] == "systemError"),
        "non_repo_goal_threads": sum(1 for item in goal_items if not item["repo_backed"]),
    }


def _status_from_counts(counts: dict[str, int]) -> str:
    if counts["system_error_goal_threads"] or counts["unmonitored_goal_threads"]:
        return "restore_or_registration_required"
    if counts["non_repo_goal_threads"]:
        return "repo_backing_recommended"
    return "clear"


def _next_action_from_counts(counts: dict[str, int]) -> str:
    if counts["unmonitored_goal_threads"] or counts["system_error_goal_threads"]:
        return "Register unmonitored goal threads, recover systemError goal threads, and prefer repo-backed threads for future dispatch."
    if counts["non_repo_goal_threads"]:
        return "Migrate or recreate non-repo-backed goal threads as repo-backed threads, or route them through a bounded absolute-path recovery executor."
    return "No dynamic goal-thread registration, restore, or repo-backed migration action is currently required."


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Codex Thread Goal Inventory v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
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
            "## Threads",
            "",
            "| Thread | Status | Goal | Monitor | Repo-backed | Actions |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["threads"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(f"{item['title']} `{item['thread_id']}`", 120),
                    f"`{item['status']}`",
                    "`yes`" if item["has_goal_signal"] else "`no`",
                    f"`{item['monitor_status']}`",
                    "`yes`" if item["repo_backed"] else "`no`",
                    md_cell(", ".join(item["recommended_actions"]) or "none", 120),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This inventory reads a supplied Codex thread snapshot and local SQLite registry only. It does not create threads, mutate ownership, start workers, approve service requests, open browsers, call APIs, publish, submit, trade, spend, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-codex-thread-goal-inventory-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Inventory Codex goal threads', 'complete', 94, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          status=excluded.status,
          priority=excluded.priority,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            task_id,
            AI_RESOURCES_LANE,
            AI_RESOURCES_OWNER,
            f"codex-thread-goal-inventory:{day}",
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
            f"artifact-codex-thread-goal-inventory-json-{day}",
            "codex_thread_goal_inventory_json",
            json_path,
            "Machine-readable dynamic Codex goal-thread inventory.",
        ),
        (
            f"artifact-codex-thread-goal-inventory-md-{day}",
            "codex_thread_goal_inventory",
            md_path,
            "Human-readable dynamic Codex goal-thread inventory.",
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
    conn.commit()


def build_codex_thread_goal_inventory(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _report_paths(generated, args)
    snapshot_path = Path(getattr(args, "thread_snapshot"))
    registered = _registered_thread_ids(conn)
    items = [_thread_item(thread, registered) for thread in _load_snapshot(snapshot_path)]
    counts = _counts(items)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": _status_from_counts(counts),
        "thread_snapshot": str(snapshot_path),
        "counts": counts,
        "threads": items,
        "next_action": _next_action_from_counts(counts),
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_codex_thread_goal_inventory_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = build_codex_thread_goal_inventory(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
            },
            indent=2,
        )
    )
