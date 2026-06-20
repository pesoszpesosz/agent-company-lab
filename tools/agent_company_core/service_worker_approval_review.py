from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

"""Scope-diff, scope-template, and approval-review reporting for service workers."""

from .constants import (
    SERVICE_WORKER_APPROVAL_REVIEW_JSON,
    SERVICE_WORKER_APPROVAL_REVIEW_REPORT,
    SERVICE_WORKER_APPROVAL_REVIEW_VALIDATION_JSON,
    SERVICE_WORKER_SCOPE_DIFF_JSON,
    SERVICE_WORKER_SCOPE_DIFF_REPORT,
    SERVICE_WORKER_SCOPE_DIFF_VALIDATION_JSON,
    SERVICE_WORKER_SCOPE_TEMPLATE_JSON,
    SERVICE_WORKER_SCOPE_TEMPLATE_REPORT,
    SERVICE_WORKER_SCOPE_TEMPLATE_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import DB_PATH, REPORTS_DIR, ROOT
from .utils import compact_text, md_cell
from .service_worker_core import (
    approval_not_expired,
    latest_approval_for_request,
    service_worker_packet_path,
    synthesize_service_worker_request,
    validate_service_worker_request_object,
)


SIDE_EFFECT_SCOPE_RULES = [
    {
        "key": "credential_boundary",
        "packet_flag": None,
        "required_denial_terms": ["credential", "credentials", "otp", "private data", "private files", "secrets"],
        "conflict_terms": ["enter credentials", "use credentials", "otp", "password", "private data", "private file", "secret"],
    },
    {
        "key": "account_boundary",
        "packet_flag": "account_or_identity_action_allowed",
        "required_denial_terms": ["login", "signup", "account", "settings", "terms acceptance"],
        "conflict_terms": ["login", "log in", "sign in", "signup", "sign up", "create account", "settings", "accept terms"],
    },
    {
        "key": "money_boundary",
        "packet_flag": "real_money_allowed",
        "required_denial_terms": ["payment", "wallet", "purchase", "deposit", "withdraw", "trade", "real money"],
        "conflict_terms": ["payment", "wallet", "purchase", "deposit", "withdraw", "trade", "buy", "sell", "real money"],
    },
    {
        "key": "public_action_boundary",
        "packet_flag": "public_action_allowed",
        "required_denial_terms": ["post", "comment", "message", "submit", "publish", "listing", "upload", "public action"],
        "conflict_terms": ["post", "comment", "message", "submit", "publish", "listing", "upload", "reply", "contact"],
    },
    {
        "key": "model_or_api_cost",
        "packet_flag": "model_or_api_cost_allowed",
        "required_denial_terms": ["api", "model", "cost", "provider"],
        "conflict_terms": ["api call", "model call", "provider", "paid api", "cost"],
    },
    {
        "key": "external_side_effects",
        "packet_flag": "external_side_effects_allowed",
        "required_denial_terms": ["external action", "external side effect", "no side effect"],
        "conflict_terms": ["external action", "side effect", "start worker", "execute worker"],
    },
]


NEGATION_MARKERS = ["no", "not", "never", "without", "do not", "don't", "cannot", "may not", "must not"]


from .service_worker_scope_diff import service_worker_scope_diff_entry
from .service_worker_scope_templates import service_worker_scope_template_entry
def service_worker_approval_review_entry(conn: sqlite3.Connection, row: dict[str, Any], generated_utc: str) -> dict[str, Any]:
    template = service_worker_scope_template_entry(conn, row, generated_utc)
    scope_diff = service_worker_scope_diff_entry(conn, row, generated_utc)
    request_id = row["request_id"]
    packet_valid = not template["packet_errors"]
    terminal = row["status"] in {"complete", "rejected", "cancelled"}
    if terminal:
        route = f"terminal_{row['status']}_do_not_review_for_approval"
        review_priority = 90
        recommended_decision = "do_not_approve_terminal_request"
        next_action = "Keep terminal audit evidence or create a fresh service request if work is still needed."
    elif not packet_valid:
        route = "blocked_until_packet_valid"
        review_priority = 80
        recommended_decision = "repair_packet_before_review"
        next_action = "Repair service-worker packet validation errors before any approval review."
    elif row["status"] != "needs_review":
        route = f"non_review_status_{row['status']}_manual_audit"
        review_priority = 70
        recommended_decision = "manual_audit_before_any_decision"
        next_action = "Audit current service status before creating an approval or rejection decision."
    else:
        high_risk_worker = template.get("worker_type") in {
            "browser_signed_in_read_only",
            "legal_kyc_tax_payment_review",
            "model_api_execution",
            "public_submission",
        }
        route = "ready_for_human_cro_review_high_risk" if high_risk_worker else "ready_for_human_cro_review"
        review_priority = 20 if high_risk_worker else 10
        recommended_decision = "human_cro_review_required"
        next_action = "Human/CRO can approve, reject, or revise the exact scope after checking the packet, lane, risk gate, and current site/account context."
    approve_preview = [
        "python",
        str(ROOT / "tools" / "agent_company.py"),
        "approve-service-request",
        "--request-id",
        request_id,
        "--approved-by",
        "USER_OR_CRO",
        "--exact-scope",
        "REPLACE_WITH_MANUALLY_REVIEWED_EXACT_SCOPE_FROM_SUGGESTED_SCOPE",
        "--decision-note",
        "Manual approval after reviewing packet, risk gate, exact scope, and stop conditions.",
    ]
    reject_preview = [
        "python",
        str(ROOT / "tools" / "agent_company.py"),
        "reject-service-request",
        "--request-id",
        request_id,
        "--rejected-by",
        "USER_OR_CRO",
        "--reason",
        "Manual rejection after reviewing packet, risk gate, exact scope, and stop conditions.",
    ]
    if terminal or not packet_valid:
        approve_preview = []
        reject_preview = []
    return {
        "source_service_request_id": request_id,
        "worker_request_id": template.get("worker_request_id"),
        "lane_id": template.get("lane_id"),
        "worker_type": template.get("worker_type"),
        "service_id": template.get("service_id"),
        "request_type": template.get("request_type"),
        "service_status": template.get("service_status"),
        "packet_status": template.get("packet_status"),
        "risk_gate": template.get("risk_gate"),
        "packet_path": template.get("packet_path"),
        "packet_errors": template.get("packet_errors", []),
        "template_route": template.get("template_route"),
        "scope_diff_route": scope_diff.get("route"),
        "scope_compatible_with_packet": scope_diff.get("scope_compatible_with_packet"),
        "missing_or_failed_scope_checks": scope_diff.get("missing_or_failed_checks", []),
        "review_route": route,
        "review_priority": review_priority,
        "recommended_decision": recommended_decision,
        "next_action": next_action,
        "suggested_exact_scope": template["suggested_exact_scope"],
        "approve_command_preview_argv": approve_preview,
        "reject_command_preview_argv": reject_preview,
        "command_previews_require_manual_review": True,
        "approval_granted_by_review": False,
        "service_request_updated": False,
        "worker_started": False,
        "api_calls": False,
        "external_side_effects": False,
    }


def write_service_worker_approval_review(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_APPROVAL_REVIEW_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_APPROVAL_REVIEW_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_APPROVAL_REVIEW_VALIDATION_JSON
    generated_utc = now_utc()
    clauses: list[str] = []
    params: list[Any] = []
    if args.request_id:
        clauses.append("sr.request_id = ?")
        params.append(args.request_id)
    if args.lane_id:
        clauses.append("sr.lane_id = ?")
        params.append(args.lane_id)
    if args.status:
        clauses.append("sr.status = ?")
        params.append(args.status)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT sr.*, l.department
            FROM service_requests sr
            LEFT JOIN lanes l ON l.lane_id = sr.lane_id
            {where}
            ORDER BY sr.request_id
            """,
            params,
        )
    ]
    entries = [service_worker_approval_review_entry(conn, row, generated_utc) for row in rows]
    entries.sort(key=lambda item: (item["review_priority"], item["source_service_request_id"]))
    route_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    decision_counts: dict[str, int] = {}
    worker_type_counts: dict[str, int] = {}
    for entry in entries:
        route_counts[entry["review_route"]] = route_counts.get(entry["review_route"], 0) + 1
        status_counts[entry["service_status"]] = status_counts.get(entry["service_status"], 0) + 1
        decision_counts[entry["recommended_decision"]] = decision_counts.get(entry["recommended_decision"], 0) + 1
        worker_type = entry.get("worker_type") or "unknown"
        worker_type_counts[worker_type] = worker_type_counts.get(worker_type, 0) + 1
    review_candidate_count = sum(1 for item in entries if item["recommended_decision"] == "human_cro_review_required")
    approve_preview_count = sum(1 for item in entries if item["approve_command_preview_argv"])
    reject_preview_count = sum(1 for item in entries if item["reject_command_preview_argv"])
    payload = {
        "schema_version": "service_worker_cro_approval_review.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "filters": {
            "request_id": args.request_id,
            "lane_id": args.lane_id,
            "status": args.status,
        },
        "reviewed_count": len(entries),
        "review_candidate_count": review_candidate_count,
        "approve_command_preview_count": approve_preview_count,
        "reject_command_preview_count": reject_preview_count,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
        "approval_reviews": entries,
        "execution_notice": "CRO approval review queue only. Command previews are not executed and this report grants no approval, assignment, start, update, or external action.",
        "approval_granted_by_review": False,
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "service_requests_updated_by_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_cro_approval_review_validation.v1",
        "generated_utc": generated_utc,
        "approval_review_path": str(json_output_path),
        "reviewed_count": len(entries),
        "review_candidate_count": review_candidate_count,
        "approve_command_preview_count": approve_preview_count,
        "reject_command_preview_count": reject_preview_count,
        "all_command_previews_require_manual_review": all(item["command_previews_require_manual_review"] for item in entries),
        "all_reviews_no_approval": all(not item["approval_granted_by_review"] for item in entries),
        "approval_granted_by_review": False,
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "service_requests_updated_by_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker CRO Approval Review Queue",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report creates a local CRO review queue with draft approve/reject command previews. It grants no approval and does not assign, start, complete, enqueue, update, browse, call APIs, post, submit, register, trade, spend, or contact anyone.",
        "",
        f"- Requests reviewed: `{len(entries)}`",
        f"- Human/CRO review candidates: `{review_candidate_count}`",
        f"- Approve command previews: `{approve_preview_count}`",
        f"- Reject command previews: `{reject_preview_count}`",
        f"- Route counts: `{json.dumps(validation_payload['route_counts'], sort_keys=True)}`",
        f"- Decision counts: `{json.dumps(validation_payload['decision_counts'], sort_keys=True)}`",
        f"- Approval granted by review: `False`",
        f"- Worker starts: `0`",
        f"- Service requests updated: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Review Queue",
        "",
        "| Priority | Status | Route | Request | Worker Type | Recommended Decision | Next Action |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(entry["review_priority"]),
                    f"`{entry['service_status']}`",
                    f"`{entry['review_route']}`",
                    f"`{entry['source_service_request_id']}`",
                    f"`{entry.get('worker_type') or ''}`",
                    f"`{entry['recommended_decision']}`",
                    md_cell(entry["next_action"], 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Command Preview Notes", ""])
    for entry in entries:
        lines.extend(
            [
                f"### {entry['source_service_request_id']}",
                "",
                f"- Recommended decision: `{entry['recommended_decision']}`",
                f"- Review route: `{entry['review_route']}`",
                f"- Scope diff route: `{entry['scope_diff_route']}`",
                f"- Command previews require manual review: `{entry['command_previews_require_manual_review']}`",
                "",
            ]
        )
        if entry["approve_command_preview_argv"]:
            lines.extend(["Approve preview argv:", "", "```json", json.dumps(entry["approve_command_preview_argv"], indent=2), "```", ""])
        else:
            lines.extend(["Approve preview argv: `[]`", ""])
        lines.extend(["Reject preview argv:", "", "```json", json.dumps(entry["reject_command_preview_argv"], indent=2), "```", ""])
    lines.extend(
        [
            "## Next Action",
            "",
            "Use this queue as a human/CRO decision board. If a request is approved separately, rerun the scope diff and execution-readiness verifier before assigning or starting any worker.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "count": len(entries),
                "review_candidate_count": review_candidate_count,
            },
            indent=2,
        )
    )

