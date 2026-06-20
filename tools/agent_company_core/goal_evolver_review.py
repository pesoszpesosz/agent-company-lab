"""Write report-only Goal Evolver review packets."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc, parse_utc
from .paths import REPORTS_DIR, ROOT
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "goal_evolver_review.v1"
GOAL_EVOLVER_AGENT_ID = "goal-evolver-agent-20260620"
AI_RESOURCES_LANE = "ai_resources_lab"
DEFAULT_GOAL_MD = ROOT / "architecture" / "ceo-operating-goal-v1.md"
DEFAULT_GOAL_JSON = ROOT / "architecture" / "ceo-operating-goal-v1.json"
DEFAULT_AGENT_CHARTER = ROOT / "architecture" / "goal-evolver-agent-v1.md"
DEFAULT_JSON = REPORTS_DIR / "goal-evolver-review-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "goal-evolver-review-v1-20260621.md"


def _review_id(generated_utc: str) -> str:
    return f"goal-evolver-review-v1-{generated_utc[:10].replace('-', '')}"


def _task_id(generated_utc: str) -> str:
    return f"task-{_review_id(generated_utc)}"


def _read_optional_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _age_minutes(updated_at: str | None, now_value: str) -> int | None:
    if not updated_at:
        return None
    updated = parse_utc(updated_at)
    current = parse_utc(now_value)
    if not updated or not current:
        return None
    return max(0, int((current - updated).total_seconds() // 60))


def _stale_owner_acknowledgements(conn: sqlite3.Connection, generated_utc: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT task_id, lane_id, status, owner_agent_id, duplicate_key, updated_at, next_action
        FROM tasks
        WHERE duplicate_key LIKE '%:owner-acknowledgement:%'
          AND status NOT IN ('complete', 'cancelled')
        ORDER BY updated_at, priority DESC
        """
    ).fetchall()
    stale: list[dict[str, Any]] = []
    for row in rows:
        age = _age_minutes(row["updated_at"], generated_utc)
        if age is not None and age >= 60:
            stale.append(
                {
                    "task_id": row["task_id"],
                    "lane_id": row["lane_id"],
                    "status": row["status"],
                    "owner_agent_id": row["owner_agent_id"],
                    "duplicate_key": row["duplicate_key"],
                    "updated_at": row["updated_at"],
                    "age_minutes": age,
                    "next_action": row["next_action"],
                }
            )
    return stale


def _recent_rows(conn: sqlite3.Connection, table: str, columns: str, order_by: str, limit: int) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            f"SELECT {columns} FROM {table} ORDER BY {order_by} DESC LIMIT ?",
            (limit,),
        ).fetchall()
    ]


def _company_signals(conn: sqlite3.Connection, generated_utc: str, evidence_limit: int) -> dict[str, Any]:
    stale_ack = _stale_owner_acknowledgements(conn, generated_utc)
    blocked_count = int(
        conn.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('blocked', 'needs_review')").fetchone()[0]
    )
    open_count = int(
        conn.execute("SELECT COUNT(*) FROM tasks WHERE status NOT IN ('complete', 'cancelled')").fetchone()[0]
    )
    totals = {
        "tasks": int(conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]),
        "artifacts": int(conn.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]),
        "outcomes": int(conn.execute("SELECT COUNT(*) FROM outcomes").fetchone()[0]),
        "traces": int(conn.execute("SELECT COUNT(*) FROM trace_events").fetchone()[0]),
        "service_requests": int(conn.execute("SELECT COUNT(*) FROM service_requests").fetchone()[0]),
    }
    realized_usd = float(conn.execute("SELECT COALESCE(SUM(realized_usd), 0) FROM outcomes").fetchone()[0])
    return {
        "totals": totals,
        "open_task_count": open_count,
        "blocked_task_count": blocked_count,
        "stale_owner_acknowledgement_count": len(stale_ack),
        "stale_owner_acknowledgements": stale_ack[:evidence_limit],
        "realized_usd": realized_usd,
        "recent_outcomes": _recent_rows(
            conn,
            "outcomes",
            "outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at",
            "created_at",
            evidence_limit,
        ),
        "recent_traces": _recent_rows(
            conn,
            "trace_events",
            "event_id, trace_id, lane_id, task_id, agent_id, event_type, summary, artifact_path, created_at",
            "created_at",
            evidence_limit,
        ),
    }


def _evidence_paths(goal_md: Path, goal_json: Path, agent_charter: Path) -> list[str]:
    paths = [goal_md, goal_json, agent_charter]
    for candidate in [
        REPORTS_DIR / "manager-packets" / "index.md",
        REPORTS_DIR / "ai-resources-trace-20260621.md",
        REPORTS_DIR / "ai-resources-artifacts-20260621.md",
    ]:
        if candidate.exists():
            paths.append(candidate)
    return [str(path) for path in paths if path.exists()]


def _proposal(goal_json: dict[str, Any], signals: dict[str, Any]) -> dict[str, list[str] | str]:
    proposed = [
        "Convert `create_goal_evolver_review_v1` from an immediate-backlog idea into a recurring report-only review packet.",
    ]
    additions = [
        "Add a goal-evolution cadence rule: run a Goal Evolver review after each major CEO dispatch batch, blocker triage, promoted lane, killed lane, or explicit user direction change.",
    ]
    deletions = [
        "Replace any vague instruction to create new agents on demand with an overlap review that evolves an existing owner when coverage already exists.",
    ]

    if signals["stale_owner_acknowledgement_count"]:
        proposed.append(
            "Add owner acknowledgement pressure to the CEO operating loop so routed knowledge cannot sit with lane owners unnoticed."
        )
        additions.append(
            "Metric: stale_owner_acknowledgement_count, grouped by lane and max age, reviewed before creating new workers or duplicate agents."
        )
    if signals["blocked_task_count"]:
        proposed.append(
            "Add a blocker-to-decision-batch rule so repeated blocked tasks become exact CEO decisions, human-action feed items, or parked revisit conditions."
        )
        additions.append(
            "Promotion/kill rule: a lane with repeated blockers must produce an exact gate, a local proof path, or a kill/watch recommendation before more work is assigned."
        )
    if goal_json.get("immediate_backlog"):
        proposed.append(
            "Keep the immediate backlog as a living queue whose items graduate only when a command/report, test, trace, and outcome row exist."
        )
    return {
        "proposed_diff_summary": proposed,
        "recommended_additions": additions,
        "recommended_deletions": deletions,
        "apply_recommendation": "apply_after_review",
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Goal Evolver Review V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Review id: `{payload['review_id']}`",
        f"Apply recommendation: `{payload['apply_recommendation']}`",
        f"Source goal: `{payload['source_goal_path']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Company Signals",
        "",
        f"- Open tasks: `{payload['company_signals']['open_task_count']}`",
        f"- Blocked tasks: `{payload['company_signals']['blocked_task_count']}`",
        f"- Stale owner acknowledgements: `{payload['company_signals']['stale_owner_acknowledgement_count']}`",
        f"- Realized USD: `{payload['company_signals']['realized_usd']}`",
        "",
        "## Proposed Diff Summary",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["proposed_diff_summary"])
    lines.extend(["", "## Recommended Additions", ""])
    lines.extend(f"- {item}" for item in payload["recommended_additions"])
    lines.extend(["", "## Recommended Deletions", ""])
    lines.extend(f"- {item}" for item in payload["recommended_deletions"])
    lines.extend(["", "## Stale Owner Acknowledgements", "", "| Lane | Task | Status | Age Min | Next Action |", "| --- | --- | --- | ---: | --- |"])
    for item in payload["company_signals"]["stale_owner_acknowledgements"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['task_id']}`",
                    md_cell(item["status"], 80),
                    str(item["age_minutes"]),
                    md_cell(item.get("next_action"), 220),
                ]
            )
            + " |"
        )
    if not payload["company_signals"]["stale_owner_acknowledgements"]:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Guardrails Preserved",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["guardrails_preserved"])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This review writes local reports and audit rows only. It does not apply goal changes, start workers, open browsers, create accounts, publish, submit, trade, spend, call APIs, mutate service requests, or approve side effects.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    task_id = _task_id(ts)
    review_id = payload["review_id"]
    review_fragment = review_id.removeprefix("goal-evolver-review-v1-")
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write Goal Evolver review packet v1', 'complete', 92, ?, ?, ?, ?, ?, ?, ?, ?)
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
            GOAL_EVOLVER_AGENT_ID,
            review_id,
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (f"artifact-goal-evolver-review-v1-json-{review_fragment}", "goal_evolver_review_json", json_path, "Machine-readable Goal Evolver review packet."),
        (f"artifact-goal-evolver-review-v1-md-{review_fragment}", "goal_evolver_review", md_path, "Human-readable Goal Evolver review packet."),
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
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(
          ?,
          ?,
          ?, ?, ?, 'goal_evolver_review_written', ?, 'goal_evolver_review_v1',
          ?, ?, ?, ?
        )
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
            f"trace-event-goal-evolver-review-v1-{review_fragment}",
            f"trace-goal-evolver-review-v1-{review_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            GOAL_EVOLVER_AGENT_ID,
            ts,
            f"Goal Evolver proposed {len(payload['proposed_diff_summary'])} operating-goal diffs from current company evidence.",
            json.dumps(
                {
                    "review_id": payload["review_id"],
                    "company_signals": payload["company_signals"],
                    "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
                },
                sort_keys=True,
            ),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(
          ?, ?, ?, 'goal_evolver_review', ?,
          0, ?, ?, ?
        )
        ON CONFLICT(outcome_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-goal-evolver-review-v1-{review_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            payload["apply_recommendation"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def write_goal_evolver_review_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    evidence_limit = int(getattr(args, "evidence_limit", 10))
    goal_md = Path(getattr(args, "goal_md_path", None) or DEFAULT_GOAL_MD)
    goal_json = Path(getattr(args, "goal_json_path", None) or DEFAULT_GOAL_JSON)
    agent_charter = Path(getattr(args, "agent_charter_path", None) or DEFAULT_AGENT_CHARTER)
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)

    goal_text = _read_optional_text(goal_md)
    goal_payload = _read_optional_json(goal_json)
    signals = _company_signals(conn, generated, evidence_limit)
    proposal = _proposal(goal_payload, signals)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "review_id": _review_id(generated),
        "generated_utc": generated,
        "source_goal_path": str(goal_md),
        "source_goal_json_path": str(goal_json),
        "agent_charter_path": str(agent_charter),
        "goal_text_sha256": sha256_file(goal_md) if goal_md.exists() else None,
        "goal_summary": goal_payload.get("operating_goal") or goal_text.splitlines()[0] if goal_text else "",
        "evidence_paths": _evidence_paths(goal_md, goal_json, agent_charter),
        "company_signals": signals,
        "proposed_diff_summary": proposal["proposed_diff_summary"],
        "goal_sections_to_change": [
            "CEO Operating Loop",
            "North Star Metrics",
            "Immediate Backlog",
            "Goal Evolver",
        ],
        "recommended_additions": proposal["recommended_additions"],
        "recommended_deletions": proposal["recommended_deletions"],
        "risk_boundary_changes": [],
        "metrics_added_or_removed": [
            "add: stale_owner_acknowledgement_count",
            "add: blocker_to_decision_batch_latency",
            "keep: realized_usd",
            "keep: time_to_first_local_proof_artifact",
        ],
        "agent_or_department_overlap_notes": [
            "Use the existing `goal_evolver_agent` under AI Resources; do not create a duplicate goal editor.",
            "Route recurring CEO-goal cleanup into this review packet before changing role, lane, or service boundaries.",
        ],
        "human_action_feed_impact": [
            "Only convert blockers into human-action items when the exact action is user-only and tied to evidence.",
        ],
        "expected_business_impact": [
            "Less stale routed knowledge, fewer duplicate agents, sharper promotion/kill decisions, and cleaner CEO context.",
        ],
        "guardrails_preserved": [
            "Do not apply changes automatically.",
            "Do not expand side-effect authority silently.",
            "Do not approve service requests, public actions, account actions, payments, trading, browser sessions, workers, runtime starts, model/API calls, or MCP egress.",
        ],
        "apply_recommendation": proposal["apply_recommendation"],
        "next_action": "CEO reviews this packet; approved diffs can update the goal artifact through a separate explicit edit path.",
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_goal_evolver_review(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_goal_evolver_review_packet(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "review_id": payload["review_id"],
                "apply_recommendation": payload["apply_recommendation"],
                "company_signals": {
                    "open_task_count": payload["company_signals"]["open_task_count"],
                    "blocked_task_count": payload["company_signals"]["blocked_task_count"],
                    "stale_owner_acknowledgement_count": payload["company_signals"]["stale_owner_acknowledgement_count"],
                },
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
