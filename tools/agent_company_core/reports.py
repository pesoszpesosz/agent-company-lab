from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import ARTIFACTS_REPORT, TRACE_EVENTS_REPORT
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR
from .utils import md_cell


def artifact_where(args: argparse.Namespace) -> tuple[str, list[Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if getattr(args, "artifact_id", None):
        clauses.append("artifact_id = ?")
        params.append(args.artifact_id)
    if getattr(args, "lane_id", None):
        clauses.append("lane_id = ?")
        params.append(args.lane_id)
    if getattr(args, "task_id", None):
        clauses.append("task_id = ?")
        params.append(args.task_id)
    if getattr(args, "kind", None):
        clauses.append("kind = ?")
        params.append(args.kind)
    if getattr(args, "contains", None):
        clauses.append("(path_or_url LIKE ? OR notes LIKE ?)")
        needle = f"%{args.contains}%"
        params.extend([needle, needle])
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    return where, params


def list_artifacts(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    where, params = artifact_where(args)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at
            FROM artifacts
            {where}
            ORDER BY created_at DESC
            LIMIT ?
            """,
            params,
        )
    ]
    print(json.dumps({"count": len(rows), "artifacts": rows}, indent=2))


def write_artifacts_report(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else ARTIFACTS_REPORT
    where, params = artifact_where(args)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at
            FROM artifacts
            {where}
            ORDER BY created_at DESC
            LIMIT ?
            """,
            params,
        )
    ]
    counts_by_kind: dict[str, int] = {}
    counts_by_lane: dict[str, int] = {}
    for row in rows:
        counts_by_kind[row["kind"]] = counts_by_kind.get(row["kind"], 0) + 1
        lane_key = row["lane_id"] or "unassigned"
        counts_by_lane[lane_key] = counts_by_lane.get(lane_key, 0) + 1

    lines = [
        "# Agent Company Artifacts",
        "",
        f"Generated UTC: {now_utc()}",
        f"Database: `{DB_PATH}`",
        f"Rows shown: {len(rows)}",
        "",
        "## Counts By Kind",
        "",
        "| Kind | Count |",
        "| --- | ---: |",
    ]
    for kind, count in sorted(counts_by_kind.items()):
        lines.append(f"| `{kind}` | {count} |")
    if not counts_by_kind:
        lines.append("| none | 0 |")

    lines.extend(["", "## Counts By Lane", "", "| Lane | Count |", "| --- | ---: |"])
    for lane_id, count in sorted(counts_by_lane.items()):
        lines.append(f"| `{lane_id}` | {count} |")
    if not counts_by_lane:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "| Created | Kind | Lane | Task | Artifact | Path/URL | SHA256 | Notes |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row["created_at"], 80),
                    md_cell(row["kind"], 100),
                    f"`{row['lane_id'] or ''}`",
                    f"`{row['task_id'] or ''}`",
                    f"`{row['artifact_id']}`",
                    md_cell(row["path_or_url"], 180),
                    md_cell(row["sha256"], 80),
                    md_cell(row["notes"], 220),
                ]
            )
            + " |"
        )
    if not rows:
        lines.append("| none |  |  |  |  |  |  |  |")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(output_path), "count": len(rows)}, indent=2))


def trace_event_where(args: argparse.Namespace) -> tuple[str, list[Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if getattr(args, "trace_id", None):
        clauses.append("trace_id = ?")
        params.append(args.trace_id)
    if getattr(args, "lane_id", None):
        clauses.append("lane_id = ?")
        params.append(args.lane_id)
    if getattr(args, "task_id", None):
        clauses.append("task_id = ?")
        params.append(args.task_id)
    if getattr(args, "agent_id", None):
        clauses.append("agent_id = ?")
        params.append(args.agent_id)
    if getattr(args, "event_type", None):
        clauses.append("event_type = ?")
        params.append(args.event_type)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    return where, params


def list_trace_events(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    where, params = trace_event_where(args)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
                   source, summary, metadata_json, artifact_path, created_at
            FROM trace_events
            {where}
            ORDER BY event_time DESC, created_at DESC
            LIMIT ?
            """,
            params,
        )
    ]
    for row in rows:
        try:
            row["metadata"] = json.loads(row.pop("metadata_json"))
        except json.JSONDecodeError:
            row["metadata"] = row.pop("metadata_json")
    print(json.dumps({"count": len(rows), "trace_events": rows}, indent=2))


def write_trace_report(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else TRACE_EVENTS_REPORT
    where, params = trace_event_where(args)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
                   source, summary, metadata_json, artifact_path, created_at
            FROM trace_events
            {where}
            ORDER BY event_time DESC, created_at DESC
            LIMIT ?
            """,
            params,
        )
    ]
    counts_by_type: dict[str, int] = {}
    counts_by_lane: dict[str, int] = {}
    for row in rows:
        counts_by_type[row["event_type"]] = counts_by_type.get(row["event_type"], 0) + 1
        lane_key = row["lane_id"] or "unassigned"
        counts_by_lane[lane_key] = counts_by_lane.get(lane_key, 0) + 1

    lines = [
        "# Agent Company Trace Events",
        "",
        f"Generated UTC: {now_utc()}",
        f"Database: `{DB_PATH}`",
        f"Rows shown: {len(rows)}",
        "",
        "## Boundary",
        "",
        "- Trace events are local audit records for agent/company operations.",
        "- A trace event is not approval to perform account, wallet, browser, public, legal/KYC/billing, or real-money actions.",
        "",
        "## Counts By Event Type",
        "",
        "| Event Type | Count |",
        "| --- | ---: |",
    ]
    for event_type, count in sorted(counts_by_type.items()):
        lines.append(f"| `{event_type}` | {count} |")
    if not counts_by_type:
        lines.append("| none | 0 |")

    lines.extend(["", "## Counts By Lane", "", "| Lane | Count |", "| --- | ---: |"])
    for lane_id, count in sorted(counts_by_lane.items()):
        lines.append(f"| `{lane_id}` | {count} |")
    if not counts_by_lane:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Events",
            "",
            "| Time | Type | Trace | Lane | Task | Agent | Event | Source | Artifact | Metadata |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        metadata = row["metadata_json"]
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row["event_time"], 80),
                    md_cell(row["event_type"], 100),
                    f"`{row['trace_id']}`",
                    f"`{row['lane_id'] or ''}`",
                    f"`{row['task_id'] or ''}`",
                    md_cell(row["agent_id"], 100),
                    f"`{row['event_id']}` - {md_cell(row['summary'], 220)}",
                    md_cell(row["source"], 160),
                    md_cell(row["artifact_path"], 160),
                    md_cell(metadata, 220),
                ]
            )
            + " |"
        )
    if not rows:
        lines.append("| none |  |  |  |  |  |  |  |  |  |")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(output_path), "count": len(rows)}, indent=2))
