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


def write_manager_proof_task_promotion_preflight(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_VALIDATION_JSON
    packets_path = Path(args.packets_path) if args.packets_path else MANAGER_PROOF_TASK_PACKETS_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    try:
        packet_payload = load_json(packets_path)
    except FileNotFoundError:
        raise SystemExit(f"Manager proof-task packet manifest not found: {packets_path}")
    packet_rows = packet_payload.get("packet_rows", [])
    candidate_rows: list[dict[str, Any]] = []
    seen_task_ids: set[str] = set()
    seen_duplicate_keys: set[str] = set()

    for row in packet_rows:
        lane_id = row.get("lane_id")
        packet_path = Path(row.get("packet_path", ""))
        packet_blockers: list[str] = []
        packet = load_json(packet_path) if packet_path.exists() else {}
        proposed_task = packet.get("proposed_task", {})
        task_id = proposed_task.get("task_id") or row.get("task_id")
        duplicate_key = proposed_task.get("duplicate_key")
        request_ids = packet.get("parked_request_ids", row.get("parked_request_ids", []))

        lane = conn.execute(
            "SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?",
            (lane_id,),
        ).fetchone()
        owner_agent = None
        if lane and lane["owner_agent_id"]:
            owner_agent = conn.execute("SELECT agent_id FROM agents WHERE agent_id = ?", (lane["owner_agent_id"],)).fetchone()
        source_spec = conn.execute(
            "SELECT spec_id FROM source_specs WHERE spec_id = ? AND lane_id = ?",
            (row.get("source_spec_id"), lane_id),
        ).fetchone()
        evidence = conn.execute(
            "SELECT evidence_id FROM lane_evidence WHERE evidence_id = ? AND lane_id = ?",
            (row.get("evidence_id"), lane_id),
        ).fetchone()
        task_id_exists = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (task_id,))
        duplicate_key_exists = (
            db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
            if duplicate_key
            else 0
        )
        request_status_rows = [
            dict(req)
            for req in conn.execute(
                f"SELECT request_id, status FROM service_requests WHERE request_id IN ({','.join('?' for _ in request_ids)})"
                if request_ids
                else "SELECT request_id, status FROM service_requests WHERE 0",
                tuple(request_ids),
            )
        ]
        request_status_by_id = {req["request_id"]: req["status"] for req in request_status_rows}
        missing_requests = [request_id for request_id in request_ids if request_id not in request_status_by_id]
        non_parked_requests = [
            {"request_id": request_id, "status": status}
            for request_id, status in request_status_by_id.items()
            if status != "needs_review"
        ]

        if not packet_path.exists():
            packet_blockers.append(f"packet file missing: {packet_path}")
        if packet.get("schema_version") != "agent_company.manager_proof_task_packet.v1":
            packet_blockers.append("packet schema mismatch")
        if not packet.get("report_only") or packet.get("live_task_created"):
            packet_blockers.append("packet is not report-only")
        if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
            packet_blockers.append("lane is missing, inactive, or unowned")
        if not owner_agent:
            packet_blockers.append("owner agent is not registered")
        if not source_spec:
            packet_blockers.append("source spec is missing")
        if not evidence:
            packet_blockers.append("evidence is missing")
        if task_id in seen_task_ids:
            packet_blockers.append("task id is duplicated among packets")
        if duplicate_key in seen_duplicate_keys:
            packet_blockers.append("duplicate key is duplicated among packets")
        if task_id_exists:
            packet_blockers.append("task id already exists in tasks table")
        if duplicate_key_exists:
            packet_blockers.append("duplicate key already exists in tasks table")
        if missing_requests:
            packet_blockers.append(f"missing referenced service requests: {', '.join(missing_requests)}")
        if non_parked_requests:
            packet_blockers.append("not all referenced service requests remain parked")

        seen_task_ids.add(task_id)
        if duplicate_key:
            seen_duplicate_keys.add(duplicate_key)
        command_preview = packet.get("command_preview")
        candidate_rows.append(
            {
                "lane_id": lane_id,
                "task_id": task_id,
                "duplicate_key": duplicate_key,
                "owner_agent_id": lane["owner_agent_id"] if lane else None,
                "packet_path": str(packet_path),
                "markdown_path": row.get("markdown_path"),
                "source_spec_id": row.get("source_spec_id"),
                "evidence_id": row.get("evidence_id"),
                "parked_request_ids": request_ids,
                "task_id_exists": bool(task_id_exists),
                "duplicate_key_exists": bool(duplicate_key_exists),
                "missing_request_count": len(missing_requests),
                "non_parked_request_count": len(non_parked_requests),
                "command_preview": command_preview,
                "ready_for_manual_promotion": not packet_blockers,
                "blockers": packet_blockers,
            }
        )

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_preflight = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    ready_for_manual_promotion_count = sum(1 for row in candidate_rows if row["ready_for_manual_promotion"])
    blocked_candidate_count = len(candidate_rows) - ready_for_manual_promotion_count
    duplicate_task_id_count = sum(1 for row in candidate_rows if row["task_id_exists"])
    duplicate_duplicate_key_count = sum(1 for row in candidate_rows if row["duplicate_key_exists"])
    all_owner_agents_registered = all(not any("owner agent" in blocker for blocker in row["blockers"]) for row in candidate_rows)
    all_lanes_active_and_owned = all(not any("lane is" in blocker for blocker in row["blockers"]) for row in candidate_rows)
    all_source_specs_present = all(not any("source spec" in blocker for blocker in row["blockers"]) for row in candidate_rows)
    all_evidence_present = all(not any("evidence is" in blocker for blocker in row["blockers"]) for row in candidate_rows)
    all_referenced_service_requests_parked = all(
        row["missing_request_count"] == 0 and row["non_parked_request_count"] == 0 for row in candidate_rows
    )
    all_packets_report_only = all(not any("report-only" in blocker for blocker in row["blockers"]) for row in candidate_rows)
    live_tasks_created = 0

    if len(packet_rows) != 6:
        failures.append(f"expected 6 proof-task packets, got {len(packet_rows)}")
    if len(candidate_rows) != 6:
        failures.append(f"expected 6 promotion candidates, got {len(candidate_rows)}")
    if ready_for_manual_promotion_count != 6:
        failures.append(f"expected 6 ready candidates, got {ready_for_manual_promotion_count}")
    if blocked_candidate_count != 0:
        failures.append(f"expected 0 blocked candidates, got {blocked_candidate_count}")
    if duplicate_task_id_count != 0:
        failures.append(f"expected 0 duplicate task IDs, got {duplicate_task_id_count}")
    if duplicate_duplicate_key_count != 0:
        failures.append(f"expected 0 duplicate duplicate keys, got {duplicate_duplicate_key_count}")
    if not all_owner_agents_registered:
        failures.append("not all owner agents are registered")
    if not all_lanes_active_and_owned:
        failures.append("not all lanes are active and owned")
    if not all_source_specs_present:
        failures.append("not all source specs are present")
    if not all_evidence_present:
        failures.append("not all evidence rows are present")
    if not all_referenced_service_requests_parked:
        failures.append("not all referenced service requests remain parked")
    if not all_packets_report_only:
        failures.append("not all packets remain report-only")
    if tasks_table_rows_before != 141:
        failures.append(f"expected 141 task rows before preflight, got {tasks_table_rows_before}")
    if tasks_table_rows_after != 141:
        failures.append(f"expected 141 task rows after preflight, got {tasks_table_rows_after}")
    if task_rows_inserted_by_preflight != 0:
        failures.append(f"expected 0 task rows inserted by preflight, got {task_rows_inserted_by_preflight}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during preflight")

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
        "schema_version": "agent_company.manager_proof_task_promotion_preflight.v1",
        "generated_utc": generated_utc,
        "purpose": "Verify report-only manager proof-task packets are clean for later explicit manual promotion to live local tasks.",
        "proof_task_packets_path": str(packets_path),
        "proof_task_packet_count": len(packet_rows),
        "promotion_candidate_count": len(candidate_rows),
        "ready_for_manual_promotion_count": ready_for_manual_promotion_count,
        "blocked_candidate_count": blocked_candidate_count,
        "duplicate_task_id_count": duplicate_task_id_count,
        "duplicate_duplicate_key_count": duplicate_duplicate_key_count,
        "all_owner_agents_registered": all_owner_agents_registered,
        "all_lanes_active_and_owned": all_lanes_active_and_owned,
        "all_source_specs_present": all_source_specs_present,
        "all_evidence_present": all_evidence_present,
        "all_referenced_service_requests_parked": all_referenced_service_requests_parked,
        "all_packets_report_only": all_packets_report_only,
        "live_tasks_created": live_tasks_created,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
        "service_requests_before": service_requests_before,
        "service_requests_after": service_requests_after,
        "candidate_rows": candidate_rows,
        "runtime_boundary": runtime_boundary,
        "next_action": "Choose which ready manager proof task to promote, then create the live local task explicitly; do not start browser/account/payment/security/API workers without separate approval.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.manager_proof_task_promotion_preflight_validation.v1",
        "generated_utc": generated_utc,
        "promotion_preflight_path": str(json_output_path),
        "proof_task_packet_count": len(packet_rows),
        "promotion_candidate_count": len(candidate_rows),
        "ready_for_manual_promotion_count": ready_for_manual_promotion_count,
        "blocked_candidate_count": blocked_candidate_count,
        "duplicate_task_id_count": duplicate_task_id_count,
        "duplicate_duplicate_key_count": duplicate_duplicate_key_count,
        "all_owner_agents_registered": all_owner_agents_registered,
        "all_lanes_active_and_owned": all_lanes_active_and_owned,
        "all_source_specs_present": all_source_specs_present,
        "all_evidence_present": all_evidence_present,
        "all_referenced_service_requests_parked": all_referenced_service_requests_parked,
        "all_packets_report_only": all_packets_report_only,
        "live_tasks_created": live_tasks_created,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Manager Proof Task Promotion Preflight",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        f"- Proof-task packets checked: `{len(packet_rows)}`",
        f"- Promotion candidates: `{len(candidate_rows)}`",
        f"- Ready for manual promotion: `{ready_for_manual_promotion_count}`",
        f"- Blocked candidates: `{blocked_candidate_count}`",
        f"- Duplicate task IDs: `{duplicate_task_id_count}`",
        f"- Duplicate duplicate keys: `{duplicate_duplicate_key_count}`",
        f"- Task rows before/after: `{tasks_table_rows_before}` / `{tasks_table_rows_after}`",
        "",
        "## Candidates",
        "",
        "| Lane | Proposed Task | Ready | Requests | Command Preview |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in candidate_rows:
        ready = "yes" if row["ready_for_manual_promotion"] else "no"
        lines.append(
            f"| `{row['lane_id']}` | `{row['task_id']}` | `{ready}` | `{len(row['parked_request_ids'])}` | `{row['command_preview']}` |"
        )
        if row["blockers"]:
            for blocker in row["blockers"]:
                lines.append(f"| `{row['lane_id']}` | blocker | no |  | {blocker} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This is a preflight only. It does not create live tasks, mutate service requests, browse, register accounts, accept terms, upload/download gated data, publish, submit, contact anyone, trade, touch wallets/payments, assign/start workers, call APIs, perform security testing, or create external side effects.",
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
                "promotion_candidate_count": len(candidate_rows),
                "ready_for_manual_promotion_count": ready_for_manual_promotion_count,
                "blocked_candidate_count": blocked_candidate_count,
                "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

