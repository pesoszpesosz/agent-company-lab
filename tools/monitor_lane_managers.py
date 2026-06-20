#!/usr/bin/env python3
"""
Generate a CEO monitor report for launched lane-manager threads.

This reads local control-plane state only. It does not inspect private thread
transcripts or do lane-specific research.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "state" / "agent_company.sqlite"
DEFAULT_LAUNCH_RUN = ROOT / "reports" / "lane-manager-thread-launch-run-20260614.json"
DEFAULT_WAVE4_LAUNCH_RUN = ROOT / "reports" / "wave4-manager-thread-launch-run-20260614.json"
DEFAULT_MD = ROOT / "reports" / "lane-manager-monitor-latest.md"
DEFAULT_JSON = ROOT / "reports" / "lane-manager-monitor-latest.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def md_cell(value: Any, limit: int = 220) -> str:
    if value is None:
        return ""
    cleaned = " ".join(str(value).replace("\r", "\n").split())
    return cleaned[:limit].rstrip().replace("|", "\\|")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_one(conn: sqlite3.Connection, query: str, params: tuple[Any, ...]) -> dict[str, Any] | None:
    row = conn.execute(query, params).fetchone()
    return dict(row) if row else None


def fetch_all(conn: sqlite3.Connection, query: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(query, params)]


def lane_status(conn: sqlite3.Connection, launch_item: dict[str, Any]) -> dict[str, Any]:
    lane_id = launch_item["lane_id"]
    lane = fetch_one(conn, "SELECT * FROM lanes WHERE lane_id = ?", (lane_id,))
    startup_artifacts = fetch_all(
        conn,
        """
        SELECT artifact_id, task_id, kind, path_or_url, created_at
        FROM artifacts
        WHERE lane_id = ? AND kind = 'lane_startup_memo'
        ORDER BY created_at DESC
        """,
        (lane_id,),
    )
    active_tasks = fetch_all(
        conn,
        """
        SELECT task_id, status, owner_agent_id, lease_owner_agent_id, lease_expires_at, next_action
        FROM tasks
        WHERE lane_id = ? AND status NOT IN ('complete', 'cancelled')
        ORDER BY priority DESC, created_at DESC
        """,
        (lane_id,),
    )
    completed_startup_tasks = fetch_all(
        conn,
        """
        SELECT task_id, status, owner_agent_id, completed_at, next_action
        FROM tasks
        WHERE lane_id = ? AND status = 'complete' AND task_id LIKE ?
        ORDER BY completed_at DESC
        """,
        (lane_id, f"task-{lane_id}-startup-%"),
    )
    outcomes = fetch_all(
        conn,
        """
        SELECT outcome_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at
        FROM outcomes
        WHERE lane_id = ?
        ORDER BY created_at DESC
        LIMIT 5
        """,
        (lane_id,),
    )
    traces = fetch_all(
        conn,
        """
        SELECT event_id, trace_id, task_id, event_type, event_time, summary, artifact_path
        FROM trace_events
        WHERE lane_id = ?
        ORDER BY event_time DESC, created_at DESC
        LIMIT 5
        """,
        (lane_id,),
    )

    startup_paths = [Path(item["path_or_url"]) for item in startup_artifacts if item.get("path_or_url")]
    existing_startup_paths = [str(path) for path in startup_paths if path.exists()]
    owner_agent = lane["owner_agent_id"] if lane else None
    owner_thread = lane["owner_thread_id"] if lane else None

    if startup_artifacts and completed_startup_tasks:
        readiness = "startup_complete"
        next_action = "Review startup memo for first proof task; do not duplicate lane work."
    elif startup_artifacts and active_tasks:
        readiness = "startup_artifact_task_open"
        next_action = "Ask lane manager to record/complete startup task if artifact/outcome/trace are ready."
    elif startup_artifacts:
        readiness = "startup_artifact_recorded"
        next_action = "Check for missing outcome/trace/task completion."
    elif owner_agent or active_tasks:
        readiness = "startup_in_progress"
        next_action = "Wait briefly or send a lane-specific startup nudge; no platform duplication."
    else:
        readiness = "not_started_or_not_recorded"
        next_action = "Send startup nudge to the lane-manager thread."

    return {
        "lane_id": lane_id,
        "thread_id": launch_item["thread_id"],
        "title": launch_item["title"],
        "projectless_output_directory": launch_item.get("projectless_output_directory"),
        "owner_agent_id": owner_agent,
        "owner_thread_id": owner_thread,
        "readiness": readiness,
        "startup_artifact_count": len(startup_artifacts),
        "existing_startup_paths": existing_startup_paths,
        "active_task_count": len(active_tasks),
        "active_tasks": active_tasks,
        "completed_startup_task_count": len(completed_startup_tasks),
        "recent_outcomes": outcomes,
        "recent_traces": traces,
        "next_action": next_action,
    }


def summarize(statuses: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for item in statuses:
        counts[item["readiness"]] = counts.get(item["readiness"], 0) + 1
    return {
        "total_lanes": len(statuses),
        "counts_by_readiness": counts,
        "needs_nudge": [item["lane_id"] for item in statuses if item["readiness"] == "not_started_or_not_recorded"],
        "needs_completion_check": [
            item["lane_id"]
            for item in statuses
            if item["readiness"] in {"startup_artifact_task_open", "startup_artifact_recorded"}
        ],
        "in_progress": [item["lane_id"] for item in statuses if item["readiness"] == "startup_in_progress"],
    }


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    lines = [
        "# Lane Manager CEO Monitor",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Database: `{DB_PATH}`",
        f"Launch run: `{payload['launch_run_path']}`",
        "",
        "## Summary",
        "",
        f"- Launched lanes: {summary['total_lanes']}",
        f"- Needs startup nudge: {', '.join(summary['needs_nudge']) or 'none'}",
        f"- Needs completion check: {', '.join(summary['needs_completion_check']) or 'none'}",
        f"- Startup in progress: {', '.join(summary['in_progress']) or 'none'}",
        "",
        "## Counts By Readiness",
        "",
        "| Readiness | Count |",
        "| --- | ---: |",
    ]
    for readiness, count in sorted(summary["counts_by_readiness"].items()):
        lines.append(f"| `{readiness}` | {count} |")
    if not summary["counts_by_readiness"]:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Lane Status",
            "",
            "| Lane | Thread | Owner | Readiness | Startup Artifacts | Active Tasks | Completed Startup Tasks | Next Action |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for item in payload["lanes"]:
        owner = item["owner_agent_id"] or item["owner_thread_id"] or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['thread_id']}`",
                    md_cell(owner, 150),
                    f"`{item['readiness']}`",
                    str(item["startup_artifact_count"]),
                    str(item["active_task_count"]),
                    str(item["completed_startup_task_count"]),
                    md_cell(item["next_action"], 240),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Startup Artifacts", "", "| Lane | Paths |", "| --- | --- |"])
    for item in payload["lanes"]:
        paths = "<br>".join(f"`{path}`" for path in item["existing_startup_paths"]) or ""
        lines.append(f"| `{item['lane_id']}` | {paths} |")

    lines.extend(["", "## Coordinator Rule", ""])
    lines.append(
        "The platform coordinator should monitor readiness, service gates, and artifacts only. Do not perform lane-specific research unless a lane manager explicitly asks for platform/service support."
    )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def default_launch_runs() -> list[Path]:
    paths = [DEFAULT_LAUNCH_RUN]
    if DEFAULT_WAVE4_LAUNCH_RUN.exists():
        paths.append(DEFAULT_WAVE4_LAUNCH_RUN)
    return paths


def load_launch_threads(paths: list[Path]) -> list[dict[str, Any]]:
    threads: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for path in paths:
        launch_run = load_json(path)
        for item in launch_run.get("threads", []):
            key = (item.get("lane_id", ""), item.get("thread_id", ""))
            if key in seen:
                continue
            seen.add(key)
            enriched = dict(item)
            enriched["launch_run_path"] = str(path)
            threads.append(enriched)
    return threads


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate lane-manager startup monitor report.")
    parser.add_argument("--launch-run", action="append", help="Launch-run JSON path. Can be passed more than once.")
    parser.add_argument("--md-path", default=str(DEFAULT_MD))
    parser.add_argument("--json-path", default=str(DEFAULT_JSON))
    args = parser.parse_args()

    launch_paths = [Path(item) for item in args.launch_run] if args.launch_run else default_launch_runs()
    launch_threads = load_launch_threads(launch_paths)
    with connect() as conn:
        statuses = [lane_status(conn, item) for item in launch_threads]

    payload = {
        "generated_utc": now_utc(),
        "launch_run_path": ", ".join(str(path) for path in launch_paths),
        "launch_run_paths": [str(path) for path in launch_paths],
        "database": str(DB_PATH),
        "summary": summarize(statuses),
        "lanes": statuses,
    }
    json_path = Path(args.json_path)
    md_path = Path(args.md_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(md_path, payload)
    print(json.dumps({"ok": True, "json_path": str(json_path), "md_path": str(md_path), "summary": payload["summary"]}, indent=2))


if __name__ == "__main__":
    main()
