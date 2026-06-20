#!/usr/bin/env python3
"""
Monitor lane-manager local proof tasks after CEO dispatch.

This monitor is intentionally read-only with respect to external systems. It
reads the local SQLite control plane plus the dispatch manifest and writes local
Markdown/JSON reports for CEO review.
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
REPORTS_DIR = ROOT / "reports"
DEFAULT_DISPATCH_RUN = REPORTS_DIR / "manager-local-proof-dispatch-run-20260614.json"
DEFAULT_JSON_REPORT = REPORTS_DIR / "manager-local-proof-monitor-latest.json"
DEFAULT_MD_REPORT = REPORTS_DIR / "manager-local-proof-monitor-latest.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def md_cell(value: Any, limit: int = 220) -> str:
    text = "" if value is None else " ".join(str(value).split())
    if len(text) > limit:
        text = text[: limit - 3].rstrip() + "..."
    return text.replace("|", "\\|")


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def fetch_task(conn: sqlite3.Connection, task_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT task_id, lane_id, status, priority, title, owner_agent_id,
               lease_owner_agent_id, lease_expires_at, started_at, completed_at,
               evidence_required, next_action
        FROM tasks
        WHERE task_id = ?
        """,
        (task_id,),
    ).fetchone()
    return dict(row) if row else None


def fetch_artifacts(conn: sqlite3.Connection, task_id: str) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            """
            SELECT artifact_id, lane_id, task_id, kind, path_or_url, created_at
            FROM artifacts
            WHERE task_id = ?
            ORDER BY created_at DESC
            """,
            (task_id,),
        )
    ]


def fetch_outcomes(conn: sqlite3.Connection, task_id: str) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            """
            SELECT outcome_id, lane_id, task_id, outcome_type, status,
                   realized_usd, evidence, next_action, created_at
            FROM outcomes
            WHERE task_id = ?
            ORDER BY created_at DESC
            """,
            (task_id,),
        )
    ]


def readiness(task: dict[str, Any] | None, artifacts: list[dict[str, Any]], outcomes: list[dict[str, Any]]) -> str:
    if not task:
        return "task_missing"
    if task["status"] == "complete":
        if artifacts and outcomes:
            return "proof_complete"
        if artifacts:
            return "complete_missing_outcome"
        return "complete_missing_artifact"
    if artifacts:
        return "artifact_present_task_open"
    if task["status"] == "in_progress":
        return "in_progress_no_artifact"
    if task["status"] == "new":
        return "not_started"
    return f"task_{task['status']}"


def build_monitor(dispatch_run: Path) -> dict[str, Any]:
    dispatch = load_json(dispatch_run)
    generated = now_utc()
    now_dt = datetime.now(timezone.utc)
    rows: list[dict[str, Any]] = []
    with connect() as conn:
        for item in dispatch.get("dispatches", []):
            task = fetch_task(conn, item["task_id"])
            artifacts = fetch_artifacts(conn, item["task_id"])
            outcomes = fetch_outcomes(conn, item["task_id"])
            state = readiness(task, artifacts, outcomes)
            lease_expires = parse_utc(task.get("lease_expires_at") if task else None)
            lease_expired = bool(lease_expires and lease_expires < now_dt and task and task["status"] != "complete")
            rows.append(
                {
                    "lane_id": item["lane_id"],
                    "thread_id": item["thread_id"],
                    "task_id": item["task_id"],
                    "owner_agent_id": item["owner_agent_id"],
                    "task_status": task["status"] if task else None,
                    "readiness": state,
                    "lease_owner_agent_id": task.get("lease_owner_agent_id") if task else None,
                    "lease_expires_at": task.get("lease_expires_at") if task else None,
                    "lease_expired": lease_expired,
                    "started_at": task.get("started_at") if task else None,
                    "completed_at": task.get("completed_at") if task else None,
                    "artifact_count": len(artifacts),
                    "outcome_count": len(outcomes),
                    "latest_artifact": artifacts[0]["path_or_url"] if artifacts else None,
                    "latest_outcome_status": outcomes[0]["status"] if outcomes else None,
                    "realized_usd": outcomes[0]["realized_usd"] if outcomes else 0,
                    "next_action": task.get("next_action") if task else None,
                    "scope": item.get("scope"),
                }
            )

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["readiness"]] = counts.get(row["readiness"], 0) + 1
    return {
        "generated_utc": generated,
        "db": str(DB_PATH),
        "dispatch_run": str(dispatch_run),
        "external_side_effects": False,
        "rows": rows,
        "summary": {
            "total_dispatched": len(rows),
            "counts_by_readiness": counts,
            "needs_nudge": [
                row["lane_id"]
                for row in rows
                if row["readiness"] in {"not_started", "in_progress_no_artifact"} or row["lease_expired"]
            ],
            "needs_completion_check": [
                row["lane_id"]
                for row in rows
                if row["readiness"] in {"artifact_present_task_open", "complete_missing_outcome", "complete_missing_artifact"}
            ],
            "proof_complete": [row["lane_id"] for row in rows if row["readiness"] == "proof_complete"],
        },
    }


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# Manager Local-Proof Monitor",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Database: `{payload['db']}`",
        f"Dispatch run: `{payload['dispatch_run']}`",
        "",
        "## Operating Rule",
        "",
        "This monitor is read-only with respect to external systems. It does not approve, browse, register, post, submit, trade, spend, or contact anyone.",
        "",
        "## Summary",
        "",
        f"- Total dispatched lanes: `{summary['total_dispatched']}`",
        f"- Counts by readiness: `{json.dumps(summary['counts_by_readiness'], sort_keys=True)}`",
        f"- Needs nudge: `{', '.join(summary['needs_nudge']) or 'none'}`",
        f"- Needs completion check: `{', '.join(summary['needs_completion_check']) or 'none'}`",
        f"- Proof complete: `{', '.join(summary['proof_complete']) or 'none'}`",
        "",
        "## Lane Status",
        "",
        "| Readiness | Lane | Task Status | Artifacts | Outcomes | Lease Owner | Latest Artifact | Next Action |",
        "| --- | --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in payload["rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['readiness']}`",
                    f"`{row['lane_id']}`",
                    f"`{row['task_status'] or 'missing'}`",
                    str(row["artifact_count"]),
                    str(row["outcome_count"]),
                    f"`{row['lease_owner_agent_id'] or ''}`",
                    f"`{md_cell(row['latest_artifact'], 180)}`",
                    md_cell(row["next_action"], 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Follow-Up Rule", ""])
    lines.append("Nudge only lanes that are `not_started`, `in_progress_no_artifact`, or have expired leases. For `artifact_present_task_open`, ask the owner to record outcome/trace and complete the existing task rather than redoing work.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dispatch-run", default=str(DEFAULT_DISPATCH_RUN))
    parser.add_argument("--json-path", default=str(DEFAULT_JSON_REPORT))
    parser.add_argument("--md-path", default=str(DEFAULT_MD_REPORT))
    args = parser.parse_args()

    payload = build_monitor(Path(args.dispatch_run))
    json_path = Path(args.json_path)
    md_path = Path(args.md_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(payload, md_path)
    print(json.dumps({"ok": True, "json_path": str(json_path), "md_path": str(md_path), "summary": payload["summary"]}, indent=2))


if __name__ == "__main__":
    main()
