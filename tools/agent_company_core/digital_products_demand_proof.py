from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Discovery, demand proof, and build brief writers for local digital-product work."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_VALIDATION_JSON,
)
from .io import now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .digital_products_demand_proof_content import digital_products_demand_questions


def write_digital_products_local_demand_proof(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    proof_task_id = "task-digital_products_templates_plugins-first-local-proof-20260615"
    proof_evidence_id = "digital-products-local-demand-proof-20260615"
    duplicate_key = f"{lane_id}-first-local-proof-20260615"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_spec = conn.execute(
        "SELECT spec_id, name, source_type, risk_gate, notes FROM source_specs WHERE lane_id = ? ORDER BY spec_id LIMIT 1",
        (lane_id,),
    ).fetchone()
    evidence = [
        dict(row)
        for row in conn.execute(
            """
            SELECT evidence_id, status, title, source_path, source_url, summary, next_action, ownership_note, updated_at
            FROM lane_evidence
            WHERE lane_id = ?
            ORDER BY updated_at DESC, evidence_id
            LIMIT 8
            """,
            (lane_id,),
        )
    ]
    parked_requests = [
        dict(row)
        for row in conn.execute(
            """
            SELECT request_id, service_id, request_type, status, risk_gate, assigned_agent_id, decision_note
            FROM service_requests
            WHERE lane_id = ? AND status = 'needs_review'
            ORDER BY request_id
            """,
            (lane_id,),
        )
    ]
    questions = digital_products_demand_questions()
    local_only_question_count = sum(1 for item in questions if item["mode"] == "local_only")
    blocked_by_gate_count = sum(1 for item in questions if item["mode"] == "blocked_by_gate")
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (proof_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    proof_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (proof_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_spec or source_spec["spec_id"] != "digital_products_marketplace_demand_source_seed":
        failures.append("digital products source spec is missing or unexpected")
    if not evidence:
        failures.append("digital products lane has no local evidence")
    if len(parked_requests) != 3:
        failures.append(f"expected 3 parked digital service requests, got {len(parked_requests)}")
    if target_task_exists_before:
        failures.append(f"target task already exists: {proof_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if proof_evidence_exists_before:
        failures.append(f"proof evidence already exists: {proof_evidence_id}")
    if len(questions) != 8:
        failures.append(f"expected 8 proof questions, got {len(questions)}")
    if local_only_question_count != 4:
        failures.append(f"expected 4 local-only questions, got {local_only_question_count}")
    if blocked_by_gate_count != 4:
        failures.append(f"expected 4 blocked questions, got {blocked_by_gate_count}")
    if tasks_table_rows_before != 150:
        failures.append(f"expected 150 task rows before proof, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 76:
        failures.append(f"expected 76 evidence rows before proof, got {lane_evidence_rows_before}")

    proof_summary = (
        "Prepared a local digital-products demand proof from existing source spec and bootstrap evidence. "
        "It frames a small template/plugin pack as the first plausible product path, while marketplace browsing, seller terms, listings, and payment setup remain gated."
    )
    proof_next_action = (
        "Digital-products lane manager should draft a local demand memo and only request marketplace/browser or legal/payment gates if they want live demand validation."
    )
    payload = {
        "schema_version": "agent_company.digital_products_local_demand_proof.v1",
        "generated_utc": generated_utc,
        "proof_lane_id": lane_id,
        "proof_task_id": proof_task_id,
        "proof_evidence_id": proof_evidence_id,
        "source_spec_id": source_spec["spec_id"] if source_spec else None,
        "source_spec": dict(source_spec) if source_spec else None,
        "parked_service_request_count": len(parked_requests),
        "parked_service_requests": parked_requests,
        "input_evidence_count": len(evidence),
        "input_evidence": evidence,
        "proof_question_count": len(questions),
        "local_only_question_count": local_only_question_count,
        "blocked_by_gate_count": blocked_by_gate_count,
        "questions": questions,
        "summary": proof_summary,
        "next_action": proof_next_action,
        "forbidden_actions": [
            "Do not browse marketplace pages, create accounts, accept terms, list products, publish pages, or configure payouts from this proof.",
            "Do not touch wallets/payments, use APIs, assign service workers, start workers, mutate service requests, or create external side effects from this proof.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_lines = [
        "# Digital Products Local Demand Proof",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        proof_summary,
        "",
        "## Questions",
        "",
        "| Question | Mode | Gate | Answer |",
        "| --- | --- | --- | --- |",
    ]
    for item in questions:
        md_lines.append(
            f"| `{item['question_id']}` | `{item['mode']}` | `{item['gate_required'] or ''}` | {item['answer'] or item['question']} |"
        )
    md_lines.extend(
        [
            "",
            "## Parked Service Requests",
            "",
            "| Request | Service | Status | Gate |",
            "| --- | --- | --- | --- |",
        ]
    )
    for request in parked_requests:
        md_lines.append(
            f"| `{request['request_id']}` | `{request['service_id']}` | `{request['status']}` | `{request['risk_gate']}` |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This proof is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, list products, publish pages, configure payouts, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
            "",
            "## Next Action",
            "",
            proof_next_action,
            "",
        ]
    )
    output_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                proof_task_id,
                lane_id,
                "Prepare first local marketplace demand proof packet",
                86,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                proof_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": proof_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local demand proof",
                "status": "local_proof_complete",
                "summary": proof_summary,
                "next_action": proof_next_action,
                "ownership_note": "Generated by platform_engineering from the digital products source spec and bootstrap evidence; digital-products lane manager owns follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_proof = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (proof_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (proof_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (proof_task_id,)) else 0
    if task_rows_inserted_by_proof != 1:
        failures.append(f"expected 1 task row inserted by proof, got {task_rows_inserted_by_proof}")
    if tasks_table_rows_after != 151:
        failures.append(f"expected 151 task rows after proof, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 77:
        failures.append(f"expected 77 evidence rows after proof, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("proof evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during proof")
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
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_proof": task_rows_inserted_by_proof,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_demand_proof_validation.v1",
        "generated_utc": generated_utc,
        "proof_path": str(json_output_path),
        "proof_lane_id": lane_id,
        "proof_task_id": proof_task_id,
        "source_spec_id": payload["source_spec_id"],
        "parked_service_request_count": len(parked_requests),
        "proof_question_count": len(questions),
        "blocked_by_gate_count": blocked_by_gate_count,
        "local_only_question_count": local_only_question_count,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_proof": task_rows_inserted_by_proof,
        "lane_evidence_rows_before": lane_evidence_rows_before,
        "lane_evidence_rows_after": lane_evidence_rows_after,
        "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "proof_lane_id": lane_id,
                "proof_task_id": proof_task_id,
                "task_rows_inserted_by_proof": task_rows_inserted_by_proof,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

