"""Park delivered thread deliveries superseded by a newer dispatch."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR
from .utils import sha256_file


SCHEMA_VERSION = "lane_runtime_superseded_delivery_reconcile.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
SUPERSEDED_DELIVERY_STATUS = "superseded_parked"


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None)
        or REPORTS_DIR / f"lane-runtime-superseded-delivery-reconcile-v1-{day}.json"
    )
    md_path = Path(
        getattr(args, "path", None)
        or REPORTS_DIR / f"lane-runtime-superseded-delivery-reconcile-v1-{day}.md"
    )
    return json_path, md_path


def _delivered_time_expr(alias: str) -> str:
    return f"COALESCE({alias}.delivered_at, {alias}.updated_at, {alias}.created_at, '')"


def _superseded_delivered_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    current_time = _delivered_time_expr("d")
    newer_time = _delivered_time_expr("newer")
    return conn.execute(
        f"""
        SELECT
          d.delivery_id,
          d.task_id,
          d.lane_id,
          d.session_id,
          d.owner_agent_id,
          d.owner_thread_id,
          d.packet_path,
          d.prompt_path,
          d.status AS delivery_status,
          {current_time} AS delivered_sort_at,
          t.status AS task_status,
          t.lease_owner_agent_id,
          t.lease_expires_at,
          newer.delivery_id AS superseding_delivery_id,
          newer.task_id AS superseding_task_id,
          newer.lane_id AS superseding_lane_id,
          {newer_time} AS superseding_delivered_sort_at
        FROM lane_runtime_thread_deliveries d
        JOIN tasks t ON t.task_id = d.task_id
        JOIN lane_runtime_thread_deliveries newer
          ON newer.owner_thread_id = d.owner_thread_id
         AND newer.delivery_id != d.delivery_id
         AND newer.task_id != d.task_id
         AND newer.status = 'delivered'
         AND {newer_time} > {current_time}
        WHERE d.status = 'delivered'
          AND d.owner_thread_id IS NOT NULL
          AND d.owner_thread_id != ''
          AND t.lease_owner_agent_id IS NOT NULL
          AND t.status NOT IN ('complete', 'cancelled')
        GROUP BY d.delivery_id
        ORDER BY delivered_sort_at ASC, d.delivery_id
        """
    ).fetchall()


def _reconcile_item(row: sqlite3.Row, generated_utc: str) -> dict[str, Any]:
    return {
        "delivery_id": row["delivery_id"],
        "task_id": row["task_id"],
        "lane_id": row["lane_id"],
        "session_id": row["session_id"],
        "owner_agent_id": row["owner_agent_id"],
        "owner_thread_id": row["owner_thread_id"],
        "packet_path": row["packet_path"],
        "prompt_path": row["prompt_path"],
        "previous_delivery_status": row["delivery_status"],
        "new_delivery_status": SUPERSEDED_DELIVERY_STATUS,
        "previous_task_status": row["task_status"],
        "new_task_status": "new" if row["task_status"] == "in_progress" else row["task_status"],
        "lease_owner_agent_id": row["lease_owner_agent_id"],
        "lease_expires_at": row["lease_expires_at"],
        "superseding_delivery_id": row["superseding_delivery_id"],
        "superseding_task_id": row["superseding_task_id"],
        "superseding_lane_id": row["superseding_lane_id"],
        "superseded": row["task_status"] == "in_progress",
        "next_action": "Delivered task was superseded by a newer dispatch to the same owner thread; delivery parked and task released for normal replanning.",
        "reconciled_utc": generated_utc,
    }


def _apply_item(conn: sqlite3.Connection, item: dict[str, Any], generated_utc: str) -> None:
    conn.execute(
        """
        UPDATE lane_runtime_thread_deliveries
        SET status = ?,
            last_error = ?,
            updated_at = ?
        WHERE delivery_id = ?
        """,
        (
            SUPERSEDED_DELIVERY_STATUS,
            f"superseded by newer delivered thread delivery {item['superseding_delivery_id']}; parked for replanning",
            generated_utc,
            item["delivery_id"],
        ),
    )
    conn.execute(
        """
        UPDATE tasks
        SET status = ?,
            lease_owner_agent_id = NULL,
            lease_expires_at = NULL,
            updated_at = ?,
            next_action = ?
        WHERE task_id = ?
        """,
        (
            item["new_task_status"],
            generated_utc,
            "Previous delivered thread-dispatch lease was superseded by a newer dispatch to the same owner; task is released for normal capacity planning.",
            item["task_id"],
        ),
    )


def _counts(items: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "superseded_deliveries_seen": len(items),
        "deliveries_parked": len(items),
        "tasks_requeued": sum(1 for item in items if item["superseded"]),
        "task_leases_released": len(items),
    }


def _status(counts: dict[str, int]) -> str:
    if counts["deliveries_parked"]:
        return "superseded_deliveries_parked"
    return "no_superseded_delivered_leases"


def _next_action(status: str) -> str:
    if status == "superseded_deliveries_parked":
        return "Rerun account-capacity lease reconciliation before activation planning so released slots can drain immediately."
    return "No superseded delivered thread leases need local parking."


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Superseded Delivery Reconcile v1",
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
            "## Reconciled Deliveries",
            "",
            "| Delivery | Task | Lane | Superseding Delivery | New Delivery Status | New Task Status |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["reconciled_deliveries"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['delivery_id']}`",
                    f"`{item['task_id']}`",
                    f"`{item['lane_id']}`",
                    f"`{item['superseding_delivery_id']}`",
                    f"`{item['new_delivery_status']}`",
                    f"`{item['new_task_status']}`",
                ]
            )
            + " |"
        )
    if not payload["reconciled_deliveries"]:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This reconciler mutates only local delivery status and local task lease fields for delivered rows superseded by a newer delivery to the same owner thread. It does not send thread messages, start workers, open browsers, call APIs, approve service requests, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-lane-runtime-superseded-delivery-reconcile-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Reconcile superseded lane runtime deliveries', 'complete', 97, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"lane-runtime-superseded-delivery-reconcile:{day}",
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
            f"artifact-lane-runtime-superseded-delivery-reconcile-json-{day}",
            "lane_runtime_superseded_delivery_reconcile_json",
            json_path,
            "Machine-readable superseded thread-delivery reconciliation report.",
        ),
        (
            f"artifact-lane-runtime-superseded-delivery-reconcile-md-{day}",
            "lane_runtime_superseded_delivery_reconcile",
            md_path,
            "Human-readable superseded thread-delivery reconciliation report.",
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


def reconcile_superseded_lane_runtime_deliveries(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _report_paths(generated, args)
    no_db_record = bool(getattr(args, "no_db_record", False))
    rows = _superseded_delivered_rows(conn)
    items = [_reconcile_item(row, generated) for row in rows]
    if not no_db_record:
        for item in items:
            _apply_item(conn, item, generated)
        conn.commit()
    counts = _counts(items)
    status = _status(counts)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "reconciled_deliveries": items,
        "counts": counts,
        "next_action": _next_action(status),
        "zero_side_effect_boundary": {
            "delivery_status_mutations": 0 if no_db_record else counts["deliveries_parked"],
            "task_lease_mutations": 0 if no_db_record else counts["task_leases_released"],
            "thread_messages_sent": 0,
            "worker_starts": 0,
            "browser_sessions_started": 0,
            "external_api_calls": 0,
            "service_requests_approved_or_started": 0,
            "public_actions": 0,
            "wallet_payment_trading_actions": 0,
            "external_side_effects": False,
        },
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not no_db_record:
        _record_run(conn, payload, json_path, md_path)
    return payload


def reconcile_superseded_lane_runtime_deliveries_cli(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> None:
    payload = reconcile_superseded_lane_runtime_deliveries(conn, args)
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


__all__ = [
    "SUPERSEDED_DELIVERY_STATUS",
    "reconcile_superseded_lane_runtime_deliveries",
    "reconcile_superseded_lane_runtime_deliveries_cli",
]
