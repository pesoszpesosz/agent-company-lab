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

def paid_code_browser_refresh_scope_items() -> list[dict[str, str]]:
    return [
        {
            "scope_id": "issue-open-state",
            "description": "Read the target issue/bounty page to confirm whether it is open and still accepting new work.",
        },
        {
            "scope_id": "claim-and-pr-state",
            "description": "Read comments, linked PRs, and claim indicators to detect active or accepted duplicate work.",
        },
        {
            "scope_id": "bounty-terms-snapshot",
            "description": "Read visible bounty terms, payout wording, attribution requirements, and account/payment caveats without accepting anything.",
        },
        {
            "scope_id": "repo-readiness-snapshot",
            "description": "Read public repo metadata, language/tooling hints, test/build docs, and recent activity to estimate local effort.",
        },
        {
            "scope_id": "refresh-outcome-note",
            "description": "Write a local refresh outcome note that updates go/no-go status; do not claim, comment, fork, or submit.",
        },
    ]


def paid_code_browser_refresh_forbidden_actions() -> list[str]:
    return [
        "Do not sign in, register, accept terms, or change account settings.",
        "Do not claim a bounty, comment, open a PR, fork for submission, contact maintainers, or make any public action.",
        "Do not upload files, download gated/private data, or disclose private/user data.",
        "Do not perform security testing, exploit validation, scanning, fuzzing, or proof-of-concept execution.",
        "Do not touch wallets, payments, payout settings, KYC, tax forms, deposits, withdrawals, or real-money flows.",
        "Do not call model/API providers, assign service workers, start workers, or mutate service requests from this packet.",
    ]


def write_paid_code_browser_refresh_decision_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else PAID_CODE_BROWSER_REFRESH_DECISION_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else PAID_CODE_BROWSER_REFRESH_DECISION_PACKET_JSON
    validation_path = Path(args.validation_path) if args.validation_path else PAID_CODE_BROWSER_REFRESH_DECISION_PACKET_VALIDATION_JSON
    answers_path = Path(args.answers_path) if args.answers_path else PAID_CODE_LOCAL_WORKSHEET_ANSWERS_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    request_id = "req-next-wave-paid-code-algora-archestra-browser-readonly-20260614"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    try:
        answers_payload = load_json(answers_path)
    except FileNotFoundError:
        raise SystemExit(f"Paid-code local worksheet answers not found: {answers_path}")

    request = conn.execute(
        """
        SELECT request_id, service_id, request_type, lane_id, status, risk_gate,
               assigned_agent_id, artifact_path, decision_note
        FROM service_requests
        WHERE request_id = ?
        """,
        (request_id,),
    ).fetchone()
    answers_task = conn.execute(
        "SELECT task_id, status FROM tasks WHERE task_id = ?",
        (answers_payload.get("answer_task_id"),),
    ).fetchone()
    answers_evidence = conn.execute(
        "SELECT evidence_id, status FROM lane_evidence WHERE evidence_id = ?",
        (answers_payload.get("answer_evidence_id"),),
    ).fetchone()
    scope_items = paid_code_browser_refresh_scope_items()
    forbidden_actions = paid_code_browser_refresh_forbidden_actions()
    approval_required = True
    decision_granted = False
    decision_rejected = False

    if not request:
        failures.append(f"service request missing: {request_id}")
    else:
        if request["status"] != "needs_review":
            failures.append(f"expected request status needs_review, got {request['status']}")
        if request["lane_id"] != "paid_code_bounties":
            failures.append(f"expected request lane paid_code_bounties, got {request['lane_id']}")
        if request["service_id"] != "browser_read_only_session":
            failures.append(f"expected browser_read_only_session service, got {request['service_id']}")
        if request["assigned_agent_id"]:
            failures.append("request is already assigned")
        if request["decision_note"]:
            failures.append("request already has a decision note")
    if answers_payload.get("recommended_local_decision") != "no_live_claim_without_refresh_gate":
        failures.append("source answers do not require refresh gate before live claim")
    if not answers_task or answers_task["status"] != "complete":
        failures.append("source answers task is missing or incomplete")
    if not answers_evidence:
        failures.append("source answers evidence is missing")
    if len(scope_items) != 5:
        failures.append(f"expected 5 scope items, got {len(scope_items)}")
    if len(forbidden_actions) != 6:
        failures.append(f"expected 6 forbidden actions, got {len(forbidden_actions)}")
    if tasks_table_rows_before != 149:
        failures.append(f"expected 149 task rows before decision packet, got {tasks_table_rows_before}")

    payload = {
        "schema_version": "agent_company.paid_code_browser_refresh_decision_packet.v1",
        "generated_utc": generated_utc,
        "request_id": request_id,
        "request_status": request["status"] if request else None,
        "request_lane_id": request["lane_id"] if request else None,
        "request_type": request["request_type"] if request else None,
        "service_id": request["service_id"] if request else None,
        "risk_gate": request["risk_gate"] if request else None,
        "request_artifact_path": request["artifact_path"] if request else None,
        "source_answers_path": str(answers_path),
        "source_answers_task_id": answers_payload.get("answer_task_id"),
        "source_answers_evidence_id": answers_payload.get("answer_evidence_id"),
        "recommended_local_decision": answers_payload.get("recommended_local_decision"),
        "approval_required": approval_required,
        "decision_granted": decision_granted,
        "decision_rejected": decision_rejected,
        "scope_item_count": len(scope_items),
        "scope_items": scope_items,
        "forbidden_action_count": len(forbidden_actions),
        "forbidden_actions": forbidden_actions,
        "exact_decision_prompt": "Approve only a read-only browser refresh for the five scope items, or reject/keep parked. This packet does not grant approval by itself.",
        "next_action": "Human/CRO may approve, reject, or keep parked. If approved later, rerun service-worker scope diff, assignment, readiness, and chain integrity before any worker starts.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Paid-Code Browser Refresh Decision Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Request",
        "",
        f"- Request: `{request_id}`",
        f"- Status: `{payload['request_status']}`",
        f"- Lane: `{payload['request_lane_id']}`",
        f"- Service: `{payload['service_id']}`",
        f"- Risk gate: `{payload['risk_gate']}`",
        "",
        "## Exact Read-Only Scope",
        "",
        "| Scope | Description |",
        "| --- | --- |",
    ]
    for item in scope_items:
        md_lines.append(f"| `{item['scope_id']}` | {item['description']} |")
    md_lines.extend(
        [
            "",
            "## Forbidden Actions",
            "",
        ]
    )
    for action in forbidden_actions:
        md_lines.append(f"- {action}")
    md_lines.extend(
        [
            "",
            "## Decision State",
            "",
            "- Approval required: `true`",
            "- Decision granted: `false`",
            "- Decision rejected: `false`",
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
        ]
    )
    output_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_packet = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    if tasks_table_rows_after != 149:
        failures.append(f"expected 149 task rows after decision packet, got {tasks_table_rows_after}")
    if task_rows_inserted_by_packet != 0:
        failures.append(f"expected 0 task rows inserted by packet, got {task_rows_inserted_by_packet}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during decision packet generation")

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
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.paid_code_browser_refresh_decision_packet_validation.v1",
        "generated_utc": generated_utc,
        "decision_packet_path": str(json_output_path),
        "request_id": request_id,
        "request_status": payload["request_status"],
        "request_lane_id": payload["request_lane_id"],
        "source_answers_task_id": payload["source_answers_task_id"],
        "scope_item_count": len(scope_items),
        "forbidden_action_count": len(forbidden_actions),
        "approval_required": approval_required,
        "decision_granted": decision_granted,
        "decision_rejected": decision_rejected,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
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
                "request_id": request_id,
                "scope_item_count": len(scope_items),
                "decision_granted": decision_granted,
                "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

