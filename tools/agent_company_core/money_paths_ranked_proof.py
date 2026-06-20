from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""First ranked manager-proof report writer."""

from .constants import (
    FIRST_RANKED_MANAGER_PROOF_JSON,
    FIRST_RANKED_MANAGER_PROOF_REPORT,
    FIRST_RANKED_MANAGER_PROOF_VALIDATION_JSON,
    MANAGER_PROOF_TASK_PROMOTION_QUEUE_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .utils import md_cell
from .money_paths_manager_proof import (
    manager_proof_task_template,
)


def write_first_ranked_manager_proof(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else FIRST_RANKED_MANAGER_PROOF_REPORT
    json_output_path = Path(args.json_path) if args.json_path else FIRST_RANKED_MANAGER_PROOF_JSON
    validation_path = Path(args.validation_path) if args.validation_path else FIRST_RANKED_MANAGER_PROOF_VALIDATION_JSON
    queue_path = Path(args.queue_path) if args.queue_path else MANAGER_PROOF_TASK_PROMOTION_QUEUE_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    try:
        queue_payload = load_json(queue_path)
    except FileNotFoundError:
        raise SystemExit(f"Manager proof-task promotion queue not found: {queue_path}")
    queue_entries = queue_payload.get("queue_entries", [])
    first_entry = queue_entries[0] if queue_entries else {}
    lane_id = first_entry.get("lane_id")
    proof_task_id = first_entry.get("task_id")
    title, next_action = manager_proof_task_template(lane_id or "")
    duplicate_key = f"{lane_id}-first-local-proof-20260615"
    proof_evidence_id = f"first-ranked-local-proof-{lane_id}-20260615"

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_spec = conn.execute(
        "SELECT spec_id, name, source_type, risk_gate, notes FROM source_specs WHERE lane_id = ? ORDER BY spec_id LIMIT 1",
        (lane_id,),
    ).fetchone()
    local_evidence = [
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
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (proof_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))

    if lane_id != "paid_code_bounties":
        failures.append(f"expected queue first lane paid_code_bounties, got {lane_id}")
    if proof_task_id != "task-paid_code_bounties-first-local-proof-20260615":
        failures.append(f"unexpected proof task id: {proof_task_id}")
    if not first_entry.get("ready_for_manual_promotion"):
        failures.append("first queue entry is not ready for manual promotion")
    if target_task_exists_before:
        failures.append(f"target task already existed before proof: {proof_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already existed before proof: {duplicate_key}")
    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("proof lane is missing, inactive, or unowned")
    if not source_spec:
        failures.append("proof lane is missing a source spec")
    if not local_evidence:
        failures.append("proof lane has no local evidence")
    if tasks_table_rows_before != 143:
        failures.append(f"expected 143 task rows before proof, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 73:
        failures.append(f"expected 73 evidence rows before proof, got {lane_evidence_rows_before}")

    proof_summary = (
        "Prepared the first local paid-code bounty duplicate-check proof from existing imported evidence. "
        "The proof narrows the next manager action to local repo/readiness checks and keeps browser, claim, account, payout, and public actions gated."
    )
    proof_next_action = (
        "Have the paid-code lane manager use this proof to draft a local duplicate-check worksheet for the ranked bounty target; "
        "request browser or public claim work only through the parked service request gate."
    )
    proof_payload = {
        "schema_version": "agent_company.first_ranked_manager_proof.v1",
        "generated_utc": generated_utc,
        "queue_path": str(queue_path),
        "queue_first_recommended_lane_id": queue_payload.get("first_recommended_lane_id"),
        "queue_first_recommended_task_id": queue_payload.get("first_recommended_task_id"),
        "proof_lane_id": lane_id,
        "proof_task_id": proof_task_id,
        "proof_evidence_id": proof_evidence_id,
        "proof_title": title,
        "proof_summary": proof_summary,
        "proof_next_action": proof_next_action,
        "source_spec": dict(source_spec) if source_spec else None,
        "input_evidence_count": len(local_evidence),
        "input_evidence": local_evidence,
        "ranked_queue_entry": first_entry,
        "local_checks": [
            "Confirm the target is still represented only by imported local evidence before any browser refresh.",
            "Draft duplicate-check questions: issue already solved, bounty still open, claim rules, repo build/test effort, payout gate.",
            "Separate local proof work from public claim, PR, account, payout, and browser actions.",
        ],
        "forbidden_actions": [
            "Do not browse, use accounts, register, accept terms, claim bounties, submit PRs, comment publicly, or contact maintainers from this proof.",
            "Do not perform security testing, touch wallets/payments, call APIs, assign service workers, or mutate service requests from this proof.",
        ],
    }
    json_output_path.write_text(json.dumps(proof_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# First Ranked Manager Proof",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Selected Candidate",
        "",
        f"- Lane: `{lane_id}`",
        f"- Task: `{proof_task_id}`",
        f"- Queue rank: `{first_entry.get('rank')}`",
        f"- Queue score: `{first_entry.get('score')}`",
        f"- Rationale: {first_entry.get('score_rationale')}",
        "",
        "## Proof",
        "",
        proof_summary,
        "",
        "## Local Evidence Used",
        "",
        "| Evidence | Status | Title | Source |",
        "| --- | --- | --- | --- |",
    ]
    for evidence in local_evidence:
        md_lines.append(
            f"| `{evidence['evidence_id']}` | `{evidence['status']}` | {md_cell(evidence['title'], 120)} | `{evidence['source_path'] or evidence['source_url'] or ''}` |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This proof is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, claim bounties, submit PRs, comment publicly, contact maintainers, perform security testing, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
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
                title,
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
                "title": "First ranked local paid-code duplicate-check proof",
                "status": "local_proof_complete",
                "summary": proof_summary,
                "next_action": proof_next_action,
                "ownership_note": "Generated by platform_engineering from the ranked manager proof queue; paid-code lane manager owns follow-up.",
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
    proof_artifact_count = 2

    if task_rows_inserted_by_proof != 1:
        failures.append(f"expected 1 task row inserted by proof, got {task_rows_inserted_by_proof}")
    if tasks_table_rows_after != 144:
        failures.append(f"expected 144 task rows after proof, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 74:
        failures.append(f"expected 74 evidence rows after proof, got {lane_evidence_rows_after}")
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
    proof_payload.update(
        {
            "proof_artifact_count": proof_artifact_count,
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
    json_output_path.write_text(json.dumps(proof_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.first_ranked_manager_proof_validation.v1",
        "generated_utc": generated_utc,
        "first_ranked_manager_proof_path": str(json_output_path),
        "queue_first_recommended_lane_id": queue_payload.get("first_recommended_lane_id"),
        "queue_first_recommended_task_id": queue_payload.get("first_recommended_task_id"),
        "proof_lane_id": lane_id,
        "proof_task_id": proof_task_id,
        "proof_artifact_count": proof_artifact_count,
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
