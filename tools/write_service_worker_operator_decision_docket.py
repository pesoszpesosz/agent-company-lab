#!/usr/bin/env python3
"""Write a report-only operator docket for parked service-worker decisions."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from atomic_writes import write_json_atomic


ROOT = Path(r"E:\agent-company-lab")
DB_PATH = ROOT / "state" / "agent_company.sqlite"
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "service-worker-operator-decision-docket-v1.schema.json"
HUMAN_PACKETS = REPORTS / "service-worker-human-decision-packets-latest.json"
HUMAN_PACKETS_VALIDATION = REPORTS / "service-worker-human-decision-packets-validation-latest.json"
DECISION_PREFLIGHT = REPORTS / "service-worker-decision-preflight-latest.json"
DECISION_PREFLIGHT_VALIDATION = REPORTS / "service-worker-decision-preflight-validation-latest.json"
CHAIN_INTEGRITY_VALIDATION = REPORTS / "service-worker-chain-integrity-validation-latest.json"
REPORT_JSON = REPORTS / "service-worker-operator-decision-docket-v1-20260617.json"
VALIDATION_JSON = REPORTS / "service-worker-operator-decision-docket-v1-validation-20260617.json"
REPORT_MD = REPORTS / "service-worker-operator-decision-docket-v1-20260617.md"

LANE_WEIGHT = {
    "security_bounty_private_reports": 45,
    "paid_code_bounties": 42,
    "digital_products_templates_plugins": 36,
    "money_source_discovery": 31,
    "ai_ml_competitions": 27,
    "content_and_social_growth": 21,
    "platform_engineering": 18,
}

REQUEST_WEIGHT = {
    "security_report_submission": 48,
    "legal_kyc_tax_payment": 42,
    "model_api_execution": 36,
    "browser_research": 28,
    "research_enrichment": 22,
}

ZERO_BOUNDARY = {
    "report_only": True,
    "approval_granted_by_docket": False,
    "decision_authority_granted_by_docket": False,
    "rejection_granted_by_docket": False,
    "approval_rows_written": 0,
    "service_requests_assigned_by_docket": 0,
    "service_requests_updated_by_docket": 0,
    "service_requests_mutated_by_docket": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "security_testing_actions": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows_by_id(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(row.get(key)): row for row in rows if row.get(key)}


def decision_mode(request_type: str, worker_type: str) -> str:
    if request_type == "browser_research":
        return "approve_assignment_preflight_only"
    if request_type in {"legal_kyc_tax_payment", "security_report_submission", "model_api_execution", "research_enrichment"}:
        return "approve_review_packet_only"
    if worker_type in {"public_submission", "browser_signed_in_read_only"}:
        return "approve_review_packet_only"
    return "deny_or_request_more_scope"


def priority_score(packet: dict[str, Any], preflight: dict[str, Any]) -> int:
    lane_id = str(packet.get("lane_id", ""))
    request_type = str(packet.get("request_type", ""))
    authorities = preflight.get("required_authorities", [])
    base = int(packet.get("review_priority") or 0)
    score = base + LANE_WEIGHT.get(lane_id, 10) + REQUEST_WEIGHT.get(request_type, 10)
    if "human_user" in authorities:
        score += 6
    if "chief_risk_officer" in authorities:
        score += 4
    if "reputation_review_worker" in authorities:
        score += 3
    return score


def next_review_question(request_type: str, lane_id: str) -> str:
    if request_type == "security_report_submission":
        return "Is the report route in-scope, safe-harbor covered, non-duplicative, and approved for private submission review only?"
    if request_type == "legal_kyc_tax_payment":
        return "Are the marketplace, payout, tax, KYC, refund, and account-contract obligations acceptable before any seller action?"
    if request_type == "model_api_execution":
        return "Are provider, model, max cost, credential route, allowed lane, and output artifact path explicit enough for a dry run?"
    if request_type == "research_enrichment":
        return "Is signed-in read-only X/Grok research allowed without posting, following, liking, replying, or changing settings?"
    if lane_id == "paid_code_bounties":
        return "Is the issue still open, unclaimed, non-duplicative, and worth a later gated public-action request?"
    if lane_id == "digital_products_templates_plugins":
        return "Which public marketplace facts are needed before seller account, listing, payment, or legal commitments?"
    if lane_id == "security_bounty_private_reports":
        return "Which public program rules and scope facts are needed before any report/submission decision?"
    return "Is the exact read-only scope narrow, current, and worth approving for evidence capture?"


def build_docket() -> tuple[dict[str, Any], dict[str, Any]]:
    generated = utc_now()
    schema = load_json(SCHEMA_PATH)
    human = load_json(HUMAN_PACKETS)
    human_validation = load_json(HUMAN_PACKETS_VALIDATION)
    preflight = load_json(DECISION_PREFLIGHT)
    preflight_validation = load_json(DECISION_PREFLIGHT_VALIDATION)
    chain_validation = load_json(CHAIN_INTEGRITY_VALIDATION)
    failures: list[str] = []

    if schema.get("properties", {}).get("docket_status", {}).get("enum", [None])[0] != "ready_for_manual_operator_review":
        failures.append("schema_docket_status_must_start_ready_for_manual_operator_review")
    if human_validation.get("failure_count") != 0 or human_validation.get("decision_packet_count") != 11:
        failures.append("human_decision_packets_validation_not_ready")
    if preflight_validation.get("failure_count") != 0 or preflight_validation.get("preflight_count") != 11:
        failures.append("decision_preflight_validation_not_ready")
    if chain_validation.get("all_checks_passed") is not True:
        failures.append("chain_integrity_not_passing")

    packets = human.get("decision_packets", [])
    preflight_rows = rows_by_id(preflight.get("preflight_rows", []), "source_service_request_id")
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        db_rows = {
            row["request_id"]: dict(row)
            for row in con.execute("SELECT * FROM service_requests WHERE status = 'needs_review'").fetchall()
        }

    docket_rows: list[dict[str, Any]] = []
    for packet in packets:
        request_id = str(packet.get("source_service_request_id", ""))
        request = db_rows.get(request_id)
        preflight_row = preflight_rows.get(request_id, {})
        if not request:
            failures.append(f"missing_needs_review_service_request:{request_id}")
            continue
        if not preflight_row:
            failures.append(f"missing_decision_preflight_row:{request_id}")
        mode = decision_mode(str(packet.get("request_type", "")), str(preflight_row.get("worker_type", packet.get("worker_type", ""))))
        score = priority_score(packet, preflight_row)
        docket_rows.append(
            {
                "schema_version": "agent_company.service_worker_operator_decision_docket_row.v1",
                "rank": 0,
                "priority_score": score,
                "source_service_request_id": request_id,
                "lane_id": packet.get("lane_id"),
                "request_type": packet.get("request_type"),
                "service_id": packet.get("service_id"),
                "worker_type": preflight_row.get("worker_type", packet.get("worker_type")),
                "risk_gate": packet.get("risk_gate"),
                "service_status": request.get("status"),
                "recommended_decision_mode": mode,
                "required_authorities": preflight_row.get("required_authorities", []),
                "authority_route": preflight_row.get("authority_route"),
                "manual_review_ready": bool(preflight_row.get("manual_decision_ready_for_human_review")),
                "decision_packet_markdown_path": packet.get("decision_packet_markdown_path"),
                "decision_packet_json_path": packet.get("decision_packet_json_path"),
                "approve_preview_present": bool(packet.get("approve_command_preview_argv")),
                "reject_preview_present": bool(packet.get("reject_command_preview_argv")),
                "approval_granted_by_docket_row": False,
                "decision_authority_granted_by_docket_row": False,
                "assignment_allowed_by_docket_row": False,
                "worker_start_allowed_by_docket_row": False,
                "next_review_question": next_review_question(str(packet.get("request_type", "")), str(packet.get("lane_id", ""))),
            }
        )

    docket_rows.sort(key=lambda row: (-int(row["priority_score"]), str(row["source_service_request_id"])))
    for index, row in enumerate(docket_rows, start=1):
        row["rank"] = index

    ready_count = sum(1 for row in docket_rows if row["manual_review_ready"])
    if len(docket_rows) != 11:
        failures.append(f"expected_11_docket_rows_got_{len(docket_rows)}")
    if ready_count != len(docket_rows):
        failures.append("not_all_docket_rows_ready_for_manual_review")
    if any(row["service_status"] != "needs_review" for row in docket_rows):
        failures.append("one_or_more_docket_rows_not_needs_review")
    if any(not row["approve_preview_present"] or not row["reject_preview_present"] for row in docket_rows):
        failures.append("one_or_more_docket_rows_missing_command_preview")

    status = "ready_for_manual_operator_review" if not failures else "blocked_input_validation_failed"
    report = {
        "schema_version": "agent_company.service_worker_operator_decision_docket.v1",
        "generated_utc": generated,
        "db": str(DB_PATH),
        "schema_path": str(SCHEMA_PATH),
        "source_artifacts": {
            "human_decision_packets": str(HUMAN_PACKETS),
            "human_decision_packets_sha256": sha256_path(HUMAN_PACKETS),
            "decision_preflight": str(DECISION_PREFLIGHT),
            "decision_preflight_sha256": sha256_path(DECISION_PREFLIGHT),
            "chain_integrity_validation": str(CHAIN_INTEGRITY_VALIDATION),
            "chain_integrity_validation_sha256": sha256_path(CHAIN_INTEGRITY_VALIDATION),
        },
        "docket_status": status,
        "docket_count": len(docket_rows),
        "ready_for_manual_review_count": ready_count,
        "docket_rows": docket_rows,
        **ZERO_BOUNDARY,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": "Human/CRO can review ranked packet markdown files and either manually reject stale/low-value requests or provide exact signed approval artifacts. This docket grants no approval and starts nothing.",
    }
    validation = {
        "schema_version": "agent_company.service_worker_operator_decision_docket_validation.v1",
        "generated_utc": generated,
        "docket_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "docket_status": status,
        "docket_count": len(docket_rows),
        "ready_for_manual_review_count": ready_count,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Service Worker Operator Decision Docket v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Docket JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Docket status: `{validation['docket_status']}`",
        f"- Docket rows: `{validation['docket_count']}`",
        f"- Ready for manual review: `{validation['ready_for_manual_review_count']}`",
        f"- Approval granted by docket: `{validation['approval_granted_by_docket']}`",
        f"- Service requests updated: `{validation['service_requests_updated_by_docket']}`",
        f"- Worker starts: `{validation['worker_starts']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Ranked Docket",
        "",
        "| Rank | Score | Lane | Request | Decision Mode | Authorities | Review Question |",
        "| ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in report["docket_rows"]:
        authorities = ", ".join(row["required_authorities"])
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["rank"]),
                    str(row["priority_score"]),
                    f"`{row['lane_id']}`",
                    f"`{row['source_service_request_id']}`",
                    f"`{row['recommended_decision_mode']}`",
                    authorities,
                    row["next_review_question"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This docket is a ranked manual review surface only.",
            "- It does not approve, reject, assign, update, start, browse, call APIs, post, pay, trade, connect wallets, or submit security reports.",
            "- Command previews in source packets remain placeholders requiring separate human/CRO action.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    report, validation = build_docket()
    write_json_atomic(REPORT_JSON, report)
    write_json_atomic(VALIDATION_JSON, validation)
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
