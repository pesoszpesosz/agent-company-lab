from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Manager proof task packet, promotion preflight, and queue report writers."""

from .constants import (
    MANAGER_PROOF_TASK_PACKETS_JSON,
    MANAGER_PROOF_TASK_PACKETS_REPORT,
    MANAGER_PROOF_TASK_PACKETS_VALIDATION_JSON,
    MANAGER_PROOF_TASK_PACKET_DIR,
    MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_JSON,
    MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_REPORT,
    MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_VALIDATION_JSON,
    MANAGER_PROOF_TASK_PROMOTION_QUEUE_JSON,
    MANAGER_PROOF_TASK_PROMOTION_QUEUE_REPORT,
    MANAGER_PROOF_TASK_PROMOTION_QUEUE_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR, ROOT
from .service_workers import db_scalar
from .utils import safe_id_fragment


from .money_paths_manager_proof_core import manager_proof_task_queue_score

def write_manager_proof_task_promotion_queue(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else MANAGER_PROOF_TASK_PROMOTION_QUEUE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else MANAGER_PROOF_TASK_PROMOTION_QUEUE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else MANAGER_PROOF_TASK_PROMOTION_QUEUE_VALIDATION_JSON
    preflight_path = Path(args.preflight_path) if args.preflight_path else MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    try:
        preflight_payload = load_json(preflight_path)
    except FileNotFoundError:
        raise SystemExit(f"Manager proof-task promotion preflight not found: {preflight_path}")
    candidate_rows = preflight_payload.get("candidate_rows", [])
    queue_entries: list[dict[str, Any]] = []
    for candidate in candidate_rows:
        parked_request_count = len(candidate.get("parked_request_ids", []))
        score, rationale = manager_proof_task_queue_score(candidate.get("lane_id", ""), parked_request_count)
        ready = bool(candidate.get("ready_for_manual_promotion")) and not candidate.get("blockers")
        queue_entries.append(
            {
                "rank": 0,
                "lane_id": candidate.get("lane_id"),
                "task_id": candidate.get("task_id"),
                "owner_agent_id": candidate.get("owner_agent_id"),
                "score": score,
                "score_rationale": rationale,
                "parked_request_count": parked_request_count,
                "ready_for_manual_promotion": ready,
                "blockers": candidate.get("blockers", []),
                "command_preview": candidate.get("command_preview"),
                "report_only": True,
                "live_task_created": False,
                "next_decision": "Promote this candidate only with an explicit create-task command; do not start gated service workers from the queue.",
            }
        )
    queue_entries.sort(key=lambda row: (-int(row["score"]), row["lane_id"] or ""))
    for index, entry in enumerate(queue_entries, start=1):
        entry["rank"] = index

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_queue = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    promotion_candidate_count = len(candidate_rows)
    queue_entry_count = len(queue_entries)
    ready_queue_count = sum(1 for row in queue_entries if row["ready_for_manual_promotion"])
    blocked_queue_count = queue_entry_count - ready_queue_count
    first_entry = queue_entries[0] if queue_entries else {}
    first_recommended_lane_id = first_entry.get("lane_id")
    first_recommended_task_id = first_entry.get("task_id")
    all_queue_entries_ready = all(row["ready_for_manual_promotion"] for row in queue_entries)
    all_queue_entries_have_command_preview = all(bool(row["command_preview"]) for row in queue_entries)
    all_queue_entries_report_only = all(row["report_only"] and not row["live_task_created"] for row in queue_entries)
    live_tasks_created = sum(1 for row in queue_entries if row["live_task_created"])

    if promotion_candidate_count != 6:
        failures.append(f"expected 6 promotion candidates, got {promotion_candidate_count}")
    if queue_entry_count != 6:
        failures.append(f"expected 6 queue entries, got {queue_entry_count}")
    if ready_queue_count != 6:
        failures.append(f"expected 6 ready queue entries, got {ready_queue_count}")
    if blocked_queue_count != 0:
        failures.append(f"expected 0 blocked queue entries, got {blocked_queue_count}")
    if first_recommended_lane_id != "paid_code_bounties":
        failures.append(f"expected first recommended lane paid_code_bounties, got {first_recommended_lane_id}")
    if first_recommended_task_id != "task-paid_code_bounties-first-local-proof-20260615":
        failures.append(f"unexpected first recommended task id: {first_recommended_task_id}")
    if not all_queue_entries_ready:
        failures.append("not all queue entries are ready")
    if not all_queue_entries_have_command_preview:
        failures.append("not all queue entries have command previews")
    if not all_queue_entries_report_only:
        failures.append("not all queue entries are report-only")
    if live_tasks_created != 0:
        failures.append(f"expected 0 live tasks created, got {live_tasks_created}")
    if tasks_table_rows_before != 142:
        failures.append(f"expected 142 task rows before queue, got {tasks_table_rows_before}")
    if tasks_table_rows_after != 142:
        failures.append(f"expected 142 task rows after queue, got {tasks_table_rows_after}")
    if task_rows_inserted_by_queue != 0:
        failures.append(f"expected 0 task rows inserted by queue, got {task_rows_inserted_by_queue}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during queue generation")

    runtime_boundary = {
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    payload = {
        "schema_version": "agent_company.manager_proof_task_promotion_queue.v1",
        "generated_utc": generated_utc,
        "purpose": "Rank ready manager proof-task promotion candidates for the next explicit local task creation decision.",
        "promotion_preflight_path": str(preflight_path),
        "promotion_candidate_count": promotion_candidate_count,
        "queue_entry_count": queue_entry_count,
        "ready_queue_count": ready_queue_count,
        "blocked_queue_count": blocked_queue_count,
        "first_recommended_lane_id": first_recommended_lane_id,
        "first_recommended_task_id": first_recommended_task_id,
        "all_queue_entries_ready": all_queue_entries_ready,
        "all_queue_entries_have_command_preview": all_queue_entries_have_command_preview,
        "all_queue_entries_report_only": all_queue_entries_report_only,
        "live_tasks_created": live_tasks_created,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_queue": task_rows_inserted_by_queue,
        "queue_entries": queue_entries,
        "runtime_boundary": runtime_boundary,
        "next_action": "Create the first ranked local proof task only if the user accepts the queue recommendation; keep all browser/account/payment/security/API workers parked until separately approved.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.manager_proof_task_promotion_queue_validation.v1",
        "generated_utc": generated_utc,
        "promotion_queue_path": str(json_output_path),
        "promotion_candidate_count": promotion_candidate_count,
        "queue_entry_count": queue_entry_count,
        "ready_queue_count": ready_queue_count,
        "blocked_queue_count": blocked_queue_count,
        "first_recommended_lane_id": first_recommended_lane_id,
        "first_recommended_task_id": first_recommended_task_id,
        "all_queue_entries_ready": all_queue_entries_ready,
        "all_queue_entries_have_command_preview": all_queue_entries_have_command_preview,
        "all_queue_entries_report_only": all_queue_entries_report_only,
        "live_tasks_created": live_tasks_created,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_queue": task_rows_inserted_by_queue,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Manager Proof Task Promotion Queue",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        f"- Promotion candidates ranked: `{queue_entry_count}`",
        f"- Ready entries: `{ready_queue_count}`",
        f"- Blocked entries: `{blocked_queue_count}`",
        f"- First recommendation: `{first_recommended_lane_id}` / `{first_recommended_task_id}`",
        f"- Task rows before/after: `{tasks_table_rows_before}` / `{tasks_table_rows_after}`",
        "",
        "## Queue",
        "",
        "| Rank | Lane | Task | Score | Ready | Rationale |",
        "| ---: | --- | --- | ---: | --- | --- |",
    ]
    for row in queue_entries:
        ready = "yes" if row["ready_for_manual_promotion"] else "no"
        lines.append(
            f"| `{row['rank']}` | `{row['lane_id']}` | `{row['task_id']}` | `{row['score']}` | `{ready}` | {row['score_rationale']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This queue is report-only. It does not create live tasks, mutate service requests, browse, register accounts, accept terms, upload/download gated data, publish, submit, contact anyone, trade, touch wallets/payments, assign/start workers, call APIs, perform security testing, or create external side effects.",
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "queue_entry_count": queue_entry_count,
                "ready_queue_count": ready_queue_count,
                "first_recommended_lane_id": first_recommended_lane_id,
                "first_recommended_task_id": first_recommended_task_id,
                "task_rows_inserted_by_queue": task_rows_inserted_by_queue,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

