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

def paid_code_local_answer_payloads() -> list[dict[str, Any]]:
    return [
        {
            "item_id": "local-evidence-normalization",
            "answer": "Imported paid-code evidence is mostly negative or parked: owner-hold items, active competing PRs, crowded bounty threads, low-trust security-bounty forks, and aggregator noise. The clean local output is a triage note, not a claim.",
            "confidence": "high",
        },
        {
            "item_id": "candidate-status-from-import",
            "answer": "Classify current imported candidates as no live claim from local evidence. Several are explicitly rejected; the remaining parked rows need live browser refresh and terms/payout checks before any work starts.",
            "confidence": "high",
        },
        {
            "item_id": "duplicate-risk-from-import",
            "answer": "Duplicate risk is high across the imported set: active PRs, same-scope submissions, many comments, owner holds, rewarded duplicates, and claim-like activity are repeatedly present in the local evidence.",
            "confidence": "high",
        },
        {
            "item_id": "payout-trust-from-import",
            "answer": "Payout trust is unproven from local evidence alone. Some rows have scanner amount false positives, attribution/payment-account ambiguity, broad bounty wording, or unclear direct payout routes.",
            "confidence": "medium",
        },
        {
            "item_id": "effort-shape-from-import",
            "answer": "Likely effort ranges from repo triage to specialist-heavy implementation, but build/test surface is unknown without a gated browser/repo refresh. Treat local effort estimates as provisional.",
            "confidence": "medium",
        },
        {
            "item_id": "local-go-no-go-note",
            "answer": "No-go for public claim or implementation from local evidence alone. Go only for a read-only live refresh through the existing browser gate, then legal/payment/public-action gates if a clean open candidate survives.",
            "confidence": "high",
        },
    ]


def write_paid_code_local_worksheet_answers(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else PAID_CODE_LOCAL_WORKSHEET_ANSWERS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else PAID_CODE_LOCAL_WORKSHEET_ANSWERS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else PAID_CODE_LOCAL_WORKSHEET_ANSWERS_VALIDATION_JSON
    worksheet_path = Path(args.worksheet_path) if args.worksheet_path else PAID_CODE_DUPLICATE_CHECK_WORKSHEET_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    try:
        worksheet_payload = load_json(worksheet_path)
    except FileNotFoundError:
        raise SystemExit(f"Paid-code duplicate-check worksheet not found: {worksheet_path}")

    lane_id = "paid_code_bounties"
    answer_task_id = "task-paid-code-local-worksheet-answers-20260615"
    answer_evidence_id = "paid-code-local-worksheet-answers-20260615"
    source_worksheet_task_id = worksheet_payload.get("worksheet_task_id")
    worksheet_items = worksheet_payload.get("worksheet_items", [])
    local_items = [item for item in worksheet_items if item.get("mode") == "local_only"]
    gated_items = [item for item in worksheet_items if item.get("mode") == "blocked_by_gate"]
    answer_rows = paid_code_local_answer_payloads()
    answer_by_id = {row["item_id"]: row for row in answer_rows}
    local_items_answered = all(item.get("item_id") in answer_by_id for item in local_items)
    gated_items_preserved = all(item.get("gate_required") for item in gated_items)
    recommended_local_decision = "no_live_claim_without_refresh_gate"

    worksheet_task = conn.execute("SELECT task_id, status FROM tasks WHERE task_id = ?", (source_worksheet_task_id,)).fetchone()
    worksheet_evidence = conn.execute(
        "SELECT evidence_id, status FROM lane_evidence WHERE evidence_id = ?",
        (worksheet_payload.get("worksheet_evidence_id"),),
    ).fetchone()
    answer_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (answer_task_id,))
    answer_evidence_exists_before = db_scalar(
        conn,
        "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?",
        (answer_evidence_id,),
    )
    lane = conn.execute("SELECT lane_id, owner_agent_id, status FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()

    if worksheet_payload.get("worksheet_lane_id") != lane_id:
        failures.append(f"expected worksheet lane {lane_id}, got {worksheet_payload.get('worksheet_lane_id')}")
    if source_worksheet_task_id != "task-paid-code-duplicate-check-worksheet-20260615":
        failures.append(f"unexpected source worksheet task id: {source_worksheet_task_id}")
    if not worksheet_task or worksheet_task["status"] != "complete":
        failures.append("source worksheet task is missing or incomplete")
    if not worksheet_evidence:
        failures.append("source worksheet evidence is missing")
    if answer_task_exists_before:
        failures.append(f"answer task already exists: {answer_task_id}")
    if answer_evidence_exists_before:
        failures.append(f"answer evidence already exists: {answer_evidence_id}")
    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("paid-code lane is missing, inactive, or unowned")
    if len(worksheet_items) != 12:
        failures.append(f"expected 12 worksheet items, got {len(worksheet_items)}")
    if len(answer_rows) != 6:
        failures.append(f"expected 6 local answers, got {len(answer_rows)}")
    if len(gated_items) != 6:
        failures.append(f"expected 6 gated items, got {len(gated_items)}")
    if not local_items_answered:
        failures.append("not all local-only worksheet items have answers")
    if not gated_items_preserved:
        failures.append("not all gated worksheet items preserve gate requirements")
    if tasks_table_rows_before != 147:
        failures.append(f"expected 147 task rows before answers, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 75:
        failures.append(f"expected 75 evidence rows before answers, got {lane_evidence_rows_before}")

    answer_summary = (
        "Answered the six local-only paid-code duplicate-check worksheet items. The local decision is no live claim or implementation from current evidence; a gated read-only refresh is the next possible step."
    )
    answer_next_action = (
        "Paid-code lane manager should request a browser_read_only_session only if they want to refresh one candidate live; public claim, PR, payout, or security-sensitive steps remain separately gated."
    )
    payload = {
        "schema_version": "agent_company.paid_code_local_worksheet_answers.v1",
        "generated_utc": generated_utc,
        "answer_lane_id": lane_id,
        "answer_task_id": answer_task_id,
        "answer_evidence_id": answer_evidence_id,
        "source_worksheet_path": str(worksheet_path),
        "source_worksheet_task_id": source_worksheet_task_id,
        "source_worksheet_evidence_id": worksheet_payload.get("worksheet_evidence_id"),
        "worksheet_item_count": len(worksheet_items),
        "local_answer_count": len(answer_rows),
        "gated_item_count": len(gated_items),
        "local_items_answered": local_items_answered,
        "gated_items_preserved": gated_items_preserved,
        "recommended_local_decision": recommended_local_decision,
        "answers": answer_rows,
        "gated_items": gated_items,
        "summary": answer_summary,
        "next_action": answer_next_action,
        "forbidden_actions": [
            "Do not browse, use accounts, register, accept terms, claim bounties, submit PRs, comment publicly, or contact maintainers from these local answers.",
            "Do not perform security testing, touch wallets/payments, call APIs, assign service workers, or mutate service requests from these local answers.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Paid-Code Local Worksheet Answers",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        f"Source worksheet: `{worksheet_path}`",
        "",
        "## Summary",
        "",
        answer_summary,
        "",
        "## Local Answers",
        "",
        "| Item | Confidence | Answer |",
        "| --- | --- | --- |",
    ]
    for row in answer_rows:
        md_lines.append(f"| `{row['item_id']}` | `{row['confidence']}` | {row['answer']} |")
    md_lines.extend(
        [
            "",
            "## Preserved Gated Items",
            "",
            "| Item | Gate | Question |",
            "| --- | --- | --- |",
        ]
    )
    for item in gated_items:
        md_lines.append(f"| `{item['item_id']}` | `{item['gate_required']}` | {item['question']} |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "These answers are local only. They create and complete one local coordination task and add one local evidence row; they do not browse, use accounts, accept terms, claim bounties, submit PRs, comment publicly, contact maintainers, perform security testing, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
            "",
            "## Next Action",
            "",
            answer_next_action,
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
                answer_task_id,
                lane_id,
                "Answer paid-code duplicate-check worksheet local items",
                84,
                lane["owner_agent_id"],
                "paid-code-local-worksheet-answers-20260615",
                str(output_path),
                answer_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": answer_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Paid-code local worksheet answers",
                "status": "local_answers_complete",
                "summary": answer_summary,
                "next_action": answer_next_action,
                "ownership_note": "Generated by platform_engineering from the paid-code duplicate-check worksheet; paid-code lane manager owns any gated refresh request.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_answers = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (answer_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (answer_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (answer_task_id,)) else 0

    if task_rows_inserted_by_answers != 1:
        failures.append(f"expected 1 task row inserted by answers, got {task_rows_inserted_by_answers}")
    if tasks_table_rows_after != 148:
        failures.append(f"expected 148 task rows after answers, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 76:
        failures.append(f"expected 76 evidence rows after answers, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("answer evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during answer generation")

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
            "task_rows_inserted_by_answers": task_rows_inserted_by_answers,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.paid_code_local_worksheet_answers_validation.v1",
        "generated_utc": generated_utc,
        "answers_path": str(json_output_path),
        "answer_lane_id": lane_id,
        "answer_task_id": answer_task_id,
        "source_worksheet_task_id": source_worksheet_task_id,
        "worksheet_item_count": len(worksheet_items),
        "local_answer_count": len(answer_rows),
        "gated_item_count": len(gated_items),
        "local_items_answered": local_items_answered,
        "gated_items_preserved": gated_items_preserved,
        "recommended_local_decision": recommended_local_decision,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_answers": task_rows_inserted_by_answers,
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
                "answer_task_id": answer_task_id,
                "local_answer_count": len(answer_rows),
                "gated_item_count": len(gated_items),
                "task_rows_inserted_by_answers": task_rows_inserted_by_answers,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

