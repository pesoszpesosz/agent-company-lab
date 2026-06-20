from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    FIRST_RANKED_MANAGER_PROOF_JSON,
    PAID_CODE_BROWSER_REFRESH_DECISION_PACKET_JSON,
    PAID_CODE_BROWSER_REFRESH_DECISION_PACKET_REPORT,
    PAID_CODE_BROWSER_REFRESH_DECISION_PACKET_VALIDATION_JSON,
    PAID_CODE_DUPLICATE_CHECK_WORKSHEET_JSON,
    PAID_CODE_DUPLICATE_CHECK_WORKSHEET_REPORT,
    PAID_CODE_DUPLICATE_CHECK_WORKSHEET_VALIDATION_JSON,
    PAID_CODE_LOCAL_WORKSHEET_ANSWERS_JSON,
    PAID_CODE_LOCAL_WORKSHEET_ANSWERS_REPORT,
    PAID_CODE_LOCAL_WORKSHEET_ANSWERS_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .utils import md_cell

def paid_code_duplicate_check_items() -> list[dict[str, Any]]:
    return [
        {
            "item_id": "local-evidence-normalization",
            "question": "Summarize the imported evidence row in one sentence and identify why it was parked, rejected, or still candidate-worthy.",
            "mode": "local_only",
            "gate_required": None,
        },
        {
            "item_id": "candidate-status-from-import",
            "question": "Classify the candidate as rejected, parked, or needs fresh triage using only local imported status and next_action fields.",
            "mode": "local_only",
            "gate_required": None,
        },
        {
            "item_id": "duplicate-risk-from-import",
            "question": "Extract known duplicate signals such as active PRs, many comments, existing claims, owner hold, or rewarded duplicate work.",
            "mode": "local_only",
            "gate_required": None,
        },
        {
            "item_id": "payout-trust-from-import",
            "question": "Record any local evidence about escrow, paid state, bounty amount confidence, attribution, or payment gate risk.",
            "mode": "local_only",
            "gate_required": None,
        },
        {
            "item_id": "effort-shape-from-import",
            "question": "Infer repo/language/test/build effort only from local scan summaries; mark unknowns instead of browsing.",
            "mode": "local_only",
            "gate_required": None,
        },
        {
            "item_id": "local-go-no-go-note",
            "question": "Write a no-browser go/no-go note and the exact gate that would be needed before refreshing the candidate live.",
            "mode": "local_only",
            "gate_required": None,
        },
        {
            "item_id": "live-open-state-check",
            "question": "Verify whether the issue is still open and the bounty still accepts new work.",
            "mode": "blocked_by_gate",
            "gate_required": "browser_read_only_session",
        },
        {
            "item_id": "live-pr-claim-check",
            "question": "Check live PRs, comments, claims, and maintainer signals for duplicate or stale work.",
            "mode": "blocked_by_gate",
            "gate_required": "browser_read_only_session",
        },
        {
            "item_id": "terms-and-payout-check",
            "question": "Confirm current bounty terms, payout route, attribution, and any account or payment requirements.",
            "mode": "blocked_by_gate",
            "gate_required": "legal_kyc_tax_payment",
        },
        {
            "item_id": "repo-build-feasibility-check",
            "question": "Inspect repo setup, tests, language/tooling, and likely implementation surface.",
            "mode": "blocked_by_gate",
            "gate_required": "browser_read_only_session",
        },
        {
            "item_id": "public-claim-or-pr-action",
            "question": "Comment, claim, submit PR, or otherwise make a public action.",
            "mode": "blocked_by_gate",
            "gate_required": "public_action_approval",
        },
        {
            "item_id": "security-sensitive-review",
            "question": "Run exploit/security testing or security-sensitive validation beyond public code review.",
            "mode": "blocked_by_gate",
            "gate_required": "security_testing_approval",
        },
    ]


def write_paid_code_duplicate_check_worksheet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else PAID_CODE_DUPLICATE_CHECK_WORKSHEET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else PAID_CODE_DUPLICATE_CHECK_WORKSHEET_JSON
    validation_path = Path(args.validation_path) if args.validation_path else PAID_CODE_DUPLICATE_CHECK_WORKSHEET_VALIDATION_JSON
    proof_path = Path(args.proof_path) if args.proof_path else FIRST_RANKED_MANAGER_PROOF_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    try:
        proof_payload = load_json(proof_path)
    except FileNotFoundError:
        raise SystemExit(f"First ranked manager proof not found: {proof_path}")

    lane_id = "paid_code_bounties"
    worksheet_task_id = "task-paid-code-duplicate-check-worksheet-20260615"
    source_proof_task_id = proof_payload.get("proof_task_id")
    worksheet_evidence_id = "paid-code-duplicate-check-worksheet-20260615"
    worksheet_items = paid_code_duplicate_check_items()
    local_only_item_count = sum(1 for item in worksheet_items if item["mode"] == "local_only")
    blocked_by_gate_count = sum(1 for item in worksheet_items if item["mode"] == "blocked_by_gate")

    proof_task = conn.execute("SELECT task_id, status FROM tasks WHERE task_id = ?", (source_proof_task_id,)).fetchone()
    proof_evidence = conn.execute(
        "SELECT evidence_id, status FROM lane_evidence WHERE evidence_id = ?",
        (proof_payload.get("proof_evidence_id"),),
    ).fetchone()
    worksheet_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (worksheet_task_id,))
    worksheet_evidence_exists_before = db_scalar(
        conn,
        "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?",
        (worksheet_evidence_id,),
    )
    lane = conn.execute("SELECT lane_id, owner_agent_id, status FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()

    if proof_payload.get("proof_lane_id") != lane_id:
        failures.append(f"expected source proof lane {lane_id}, got {proof_payload.get('proof_lane_id')}")
    if source_proof_task_id != "task-paid_code_bounties-first-local-proof-20260615":
        failures.append(f"unexpected source proof task id: {source_proof_task_id}")
    if not proof_task or proof_task["status"] != "complete":
        failures.append("source proof task is missing or incomplete")
    if not proof_evidence:
        failures.append("source proof evidence is missing")
    if worksheet_task_exists_before:
        failures.append(f"worksheet task already exists: {worksheet_task_id}")
    if worksheet_evidence_exists_before:
        failures.append(f"worksheet evidence already exists: {worksheet_evidence_id}")
    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("paid-code lane is missing, inactive, or unowned")
    if len(worksheet_items) != 12:
        failures.append(f"expected 12 worksheet items, got {len(worksheet_items)}")
    if local_only_item_count != 6:
        failures.append(f"expected 6 local-only items, got {local_only_item_count}")
    if blocked_by_gate_count != 6:
        failures.append(f"expected 6 blocked-by-gate items, got {blocked_by_gate_count}")
    if tasks_table_rows_before != 145:
        failures.append(f"expected 145 task rows before worksheet, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 74:
        failures.append(f"expected 74 evidence rows before worksheet, got {lane_evidence_rows_before}")

    worksheet_summary = (
        "Built a paid-code duplicate-check worksheet from the completed first ranked proof. "
        "It separates six local-only checks from six gated checks that require explicit browser, legal/payment, public-action, or security approval."
    )
    worksheet_next_action = (
        "Paid-code lane manager should complete the six local-only worksheet items first; any live issue refresh, claim, PR, payout, or security-sensitive step must go through service requests."
    )
    payload = {
        "schema_version": "agent_company.paid_code_duplicate_check_worksheet.v1",
        "generated_utc": generated_utc,
        "worksheet_lane_id": lane_id,
        "worksheet_task_id": worksheet_task_id,
        "worksheet_evidence_id": worksheet_evidence_id,
        "source_proof_path": str(proof_path),
        "source_proof_task_id": source_proof_task_id,
        "source_proof_evidence_id": proof_payload.get("proof_evidence_id"),
        "worksheet_item_count": len(worksheet_items),
        "local_only_item_count": local_only_item_count,
        "blocked_by_gate_count": blocked_by_gate_count,
        "worksheet_items": worksheet_items,
        "summary": worksheet_summary,
        "next_action": worksheet_next_action,
        "forbidden_actions": [
            "Do not browse, use accounts, register, accept terms, claim bounties, submit PRs, comment publicly, or contact maintainers from this worksheet.",
            "Do not perform security testing, touch wallets/payments, call APIs, assign service workers, or mutate service requests from this worksheet.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Paid-Code Duplicate-Check Worksheet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        f"Source proof: `{proof_path}`",
        "",
        "## Summary",
        "",
        worksheet_summary,
        "",
        "## Worksheet",
        "",
        "| Item | Mode | Gate | Question |",
        "| --- | --- | --- | --- |",
    ]
    for item in worksheet_items:
        md_lines.append(
            f"| `{item['item_id']}` | `{item['mode']}` | `{item['gate_required'] or ''}` | {item['question']} |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This worksheet is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, claim bounties, submit PRs, comment publicly, contact maintainers, perform security testing, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
            "",
            "## Next Action",
            "",
            worksheet_next_action,
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
                worksheet_task_id,
                lane_id,
                "Draft paid-code duplicate-check worksheet from first local proof",
                85,
                lane["owner_agent_id"],
                "paid-code-duplicate-check-worksheet-20260615",
                str(output_path),
                worksheet_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": worksheet_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Paid-code duplicate-check worksheet",
                "status": "local_worksheet_complete",
                "summary": worksheet_summary,
                "next_action": worksheet_next_action,
                "ownership_note": "Generated by platform_engineering from the completed first ranked paid-code proof; paid-code lane manager owns local worksheet completion.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_worksheet = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (worksheet_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (worksheet_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (worksheet_task_id,)) else 0

    if task_rows_inserted_by_worksheet != 1:
        failures.append(f"expected 1 task row inserted by worksheet, got {task_rows_inserted_by_worksheet}")
    if tasks_table_rows_after != 146:
        failures.append(f"expected 146 task rows after worksheet, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 75:
        failures.append(f"expected 75 evidence rows after worksheet, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("worksheet evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during worksheet generation")

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
            "task_rows_inserted_by_worksheet": task_rows_inserted_by_worksheet,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.paid_code_duplicate_check_worksheet_validation.v1",
        "generated_utc": generated_utc,
        "worksheet_path": str(json_output_path),
        "worksheet_lane_id": lane_id,
        "worksheet_task_id": worksheet_task_id,
        "source_proof_task_id": source_proof_task_id,
        "worksheet_item_count": len(worksheet_items),
        "blocked_by_gate_count": blocked_by_gate_count,
        "local_only_item_count": local_only_item_count,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_worksheet": task_rows_inserted_by_worksheet,
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
                "worksheet_task_id": worksheet_task_id,
                "worksheet_item_count": len(worksheet_items),
                "task_rows_inserted_by_worksheet": task_rows_inserted_by_worksheet,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

