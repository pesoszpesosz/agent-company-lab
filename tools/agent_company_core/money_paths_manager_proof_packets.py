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


from .money_paths_manager_proof_core import manager_proof_task_template

def write_manager_proof_task_packets(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    packet_dir = Path(args.packet_dir) if args.packet_dir else MANAGER_PROOF_TASK_PACKET_DIR
    packet_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else MANAGER_PROOF_TASK_PACKETS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else MANAGER_PROOF_TASK_PACKETS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else MANAGER_PROOF_TASK_PACKETS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    target_rows = [
        dict(row)
        for row in conn.execute(
            """
            WITH parked AS (
              SELECT lane_id,
                     COUNT(DISTINCT request_id) AS parked_requests,
                     GROUP_CONCAT(DISTINCT request_id) AS request_ids
              FROM service_requests
              WHERE status = 'needs_review'
              GROUP BY lane_id
            ),
            evidence AS (
              SELECT lane_id, MIN(evidence_id) AS evidence_id, COUNT(*) AS evidence_count
              FROM lane_evidence
              GROUP BY lane_id
            ),
            specs AS (
              SELECT lane_id, MIN(spec_id) AS spec_id, COUNT(*) AS spec_count
              FROM source_specs
              GROUP BY lane_id
            )
            SELECT l.lane_id, l.department, l.owner_agent_id,
                   parked.parked_requests, parked.request_ids,
                   evidence.evidence_id, evidence.evidence_count,
                   specs.spec_id, specs.spec_count
            FROM lanes l
            JOIN parked ON parked.lane_id = l.lane_id
            LEFT JOIN evidence ON evidence.lane_id = l.lane_id
            LEFT JOIN specs ON specs.lane_id = l.lane_id
            WHERE l.status = 'active'
              AND l.owner_agent_id IS NOT NULL
              AND l.lane_id NOT IN ('platform_engineering', 'submitted_bounty_payouts')
            ORDER BY parked.parked_requests DESC, l.lane_id
            """
        )
    ]
    source_spec_gap_count = db_scalar(
        conn,
        """
        SELECT COUNT(*)
        FROM lanes
        WHERE status = 'active'
          AND owner_agent_id IS NOT NULL
          AND lane_id NOT IN ('platform_engineering', 'submitted_bounty_payouts')
          AND lane_id NOT IN (SELECT lane_id FROM source_specs)
        """,
    )
    evidence_gap_count = db_scalar(
        conn,
        """
        SELECT COUNT(*)
        FROM lanes
        WHERE status = 'active'
          AND owner_agent_id IS NOT NULL
          AND lane_id NOT IN ('platform_engineering', 'submitted_bounty_payouts')
          AND lane_id NOT IN (SELECT lane_id FROM lane_evidence)
        """,
    )

    packet_rows: list[dict[str, Any]] = []
    for row in target_rows:
        lane_id = row["lane_id"]
        safe_lane = safe_id_fragment(lane_id, 48)
        title, next_action = manager_proof_task_template(lane_id)
        task_id = f"task-{safe_lane}-first-local-proof-20260615"
        duplicate_key = f"{lane_id}-first-local-proof-20260615"
        packet_path = packet_dir / f"{lane_id}-manager-proof-task-20260615.json"
        md_path = packet_dir / f"{lane_id}-manager-proof-task-20260615.md"
        request_ids = [item for item in (row["request_ids"] or "").split(",") if item]
        command_preview = (
            f"python {ROOT / 'tools' / 'agent_company.py'} create-task "
            f"--task-id {task_id} --lane-id {lane_id} --title {json.dumps(title)} "
            f"--priority 86 --owner-agent-id {row['owner_agent_id']} "
            f"--duplicate-key {duplicate_key} --evidence-required {md_path} "
            f"--next-action {json.dumps(next_action)}"
        )
        packet = {
            "schema_version": "agent_company.manager_proof_task_packet.v1",
            "generated_utc": generated_utc,
            "lane_id": lane_id,
            "department": row["department"],
            "owner_agent_id": row["owner_agent_id"],
            "parked_request_ids": request_ids,
            "parked_request_count": int(row["parked_requests"]),
            "source_spec_id": row["spec_id"],
            "source_spec_count": int(row["spec_count"] or 0),
            "evidence_id": row["evidence_id"],
            "evidence_count": int(row["evidence_count"] or 0),
            "proposed_task": {
                "task_id": task_id,
                "lane_id": lane_id,
                "title": title,
                "priority": 86,
                "owner_agent_id": row["owner_agent_id"],
                "duplicate_key": duplicate_key,
                "evidence_required": str(md_path),
                "next_action": next_action,
            },
            "command_preview": command_preview,
            "report_only": True,
            "live_task_created": False,
            "forbidden_actions": [
                "Do not execute the command preview without explicit human approval.",
                "Do not browse, use accounts, register, accept terms, upload data, publish, submit, contact anyone, trade, touch wallets/payments, or call model/API services from this packet.",
                "Do not mutate service requests, assign service workers, start workers, perform security testing, or create external side effects from this packet.",
            ],
        }
        packet_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        md_lines = [
            f"# Manager Proof Task Packet: {lane_id}",
            "",
            f"Generated UTC: {generated_utc}",
            f"JSON mirror: `{packet_path}`",
            "",
            "## Proposed Task",
            "",
            f"- Task ID: `{task_id}`",
            f"- Title: {title}",
            f"- Priority: `86`",
            f"- Owner: `{row['owner_agent_id']}`",
            f"- Duplicate key: `{duplicate_key}`",
            "",
            "## Inputs",
            "",
            f"- Parked service requests: `{int(row['parked_requests'])}`",
            f"- Source spec: `{row['spec_id']}`",
            f"- Evidence: `{row['evidence_id']}`",
            "",
            "## Next Action",
            "",
            next_action,
            "",
            "## Command Preview",
            "",
            "```powershell",
            command_preview,
            "```",
            "",
            "## Boundary",
            "",
            "This packet is report-only. It does not create a live task, browse, use accounts, accept terms, upload/download gated data, publish, submit, contact anyone, trade, touch wallets/payments, mutate service requests, assign/start workers, call APIs, perform security testing, or create external side effects.",
            "",
        ]
        md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        packet_rows.append(
            {
                "lane_id": lane_id,
                "task_id": task_id,
                "packet_path": str(packet_path),
                "markdown_path": str(md_path),
                "parked_request_count": int(row["parked_requests"]),
                "parked_request_ids": request_ids,
                "source_spec_id": row["spec_id"],
                "evidence_id": row["evidence_id"],
                "report_only": True,
                "live_task_created": False,
            }
        )

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    task_rows_inserted_by_packet = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    parked_lane_count = len(target_rows)
    parked_service_request_count = sum(int(row["parked_requests"]) for row in target_rows)
    all_packets_report_only = all(row["report_only"] and not row["live_task_created"] for row in packet_rows)
    all_packets_have_source_spec = all(row["source_spec_id"] for row in packet_rows)
    all_packets_have_evidence = all(row["evidence_id"] for row in packet_rows)
    live_tasks_created = sum(1 for row in packet_rows if row["live_task_created"])

    if len(packet_rows) != 6:
        failures.append(f"expected 6 manager proof-task packets, got {len(packet_rows)}")
    if parked_lane_count != 6:
        failures.append(f"expected 6 parked lanes, got {parked_lane_count}")
    if parked_service_request_count != 9:
        failures.append(f"expected 9 distinct parked service requests, got {parked_service_request_count}")
    if not all_packets_report_only:
        failures.append("not all manager proof-task packets are report-only")
    if not all_packets_have_source_spec:
        failures.append("not all manager proof-task packets have a source spec")
    if not all_packets_have_evidence:
        failures.append("not all manager proof-task packets have evidence")
    if live_tasks_created != 0:
        failures.append(f"expected 0 live tasks created, got {live_tasks_created}")
    if tasks_table_rows_before != 140:
        failures.append(f"expected 140 task rows before packet generation, got {tasks_table_rows_before}")
    if tasks_table_rows_after != 140:
        failures.append(f"expected 140 task rows after packet generation, got {tasks_table_rows_after}")
    if task_rows_inserted_by_packet != 0:
        failures.append(f"expected 0 task rows inserted by packet, got {task_rows_inserted_by_packet}")
    if source_spec_gap_count != 0:
        failures.append(f"expected 0 source-spec gaps, got {source_spec_gap_count}")
    if evidence_gap_count != 0:
        failures.append(f"expected 0 evidence gaps, got {evidence_gap_count}")

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
        "schema_version": "agent_company.manager_proof_task_packets.v1",
        "generated_utc": generated_utc,
        "purpose": "Generate report-only proposed manager proof tasks for owned non-platform lanes that still have parked service requests.",
        "packet_dir": str(packet_dir),
        "proof_task_packet_count": len(packet_rows),
        "parked_lane_count": parked_lane_count,
        "parked_service_request_count": parked_service_request_count,
        "all_packets_report_only": all_packets_report_only,
        "all_packets_have_source_spec": all_packets_have_source_spec,
        "all_packets_have_evidence": all_packets_have_evidence,
        "live_tasks_created": live_tasks_created,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
        "source_spec_gap_count": source_spec_gap_count,
        "evidence_gap_count": evidence_gap_count,
        "packet_rows": packet_rows,
        "runtime_boundary": runtime_boundary,
        "next_action": "Review manager proof-task packets and explicitly create live lane tasks only after choosing which manager should proceed.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.manager_proof_task_packets_validation.v1",
        "generated_utc": generated_utc,
        "proof_task_packets_path": str(json_output_path),
        "proof_task_packet_count": len(packet_rows),
        "parked_lane_count": parked_lane_count,
        "parked_service_request_count": parked_service_request_count,
        "all_packets_report_only": all_packets_report_only,
        "all_packets_have_source_spec": all_packets_have_source_spec,
        "all_packets_have_evidence": all_packets_have_evidence,
        "live_tasks_created": live_tasks_created,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
        "source_spec_gap_count": source_spec_gap_count,
        "evidence_gap_count": evidence_gap_count,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Manager Proof Task Packets",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        f"- Parked lanes packetized: `{parked_lane_count}`",
        f"- Distinct parked service requests covered: `{parked_service_request_count}`",
        f"- Proof-task packets generated: `{len(packet_rows)}`",
        f"- Live tasks created: `{live_tasks_created}`",
        f"- Task rows before/after: `{tasks_table_rows_before}` / `{tasks_table_rows_after}`",
        f"- Source-spec gaps: `{source_spec_gap_count}`",
        f"- Evidence gaps: `{evidence_gap_count}`",
        "",
        "## Packets",
        "",
        "| Lane | Proposed Task | Requests | Source Spec | Evidence | JSON | Markdown |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in packet_rows:
        lines.append(
            f"| `{row['lane_id']}` | `{row['task_id']}` | `{row['parked_request_count']}` | `{row['source_spec_id']}` | `{row['evidence_id']}` | `{row['packet_path']}` | `{row['markdown_path']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- These packets are report-only proposed tasks.",
            "- They do not create tasks, browse, register accounts, accept terms, upload/download gated data, publish, submit, contact anyone, trade, touch wallets/payments, mutate service requests, assign/start workers, call APIs, perform security testing, or create external side effects.",
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
                "packet_dir": str(packet_dir),
                "proof_task_packet_count": len(packet_rows),
                "parked_service_request_count": parked_service_request_count,
                "live_tasks_created": live_tasks_created,
                "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

