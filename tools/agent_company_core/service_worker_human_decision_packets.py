from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

"""Human-decision packet, post-decision, drift, command-safety, authority, and preflight reporting."""

from .constants import (
    SERVICE_WORKER_APPROVAL_REVIEW_JSON,
    SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON,
    SERVICE_WORKER_GATE_MAP_JSON,
    SERVICE_WORKER_HUMAN_DECISION_PACKET_DIR,
    SERVICE_WORKER_HUMAN_DECISION_PACKETS_JSON,
    SERVICE_WORKER_HUMAN_DECISION_PACKETS_REPORT,
    SERVICE_WORKER_HUMAN_DECISION_PACKETS_VALIDATION_JSON,
    SERVICE_WORKER_POST_DECISION_SIMULATION_JSON,
    SERVICE_WORKER_POST_DECISION_SIMULATION_REPORT,
    SERVICE_WORKER_POST_DECISION_SIMULATION_VALIDATION_JSON,
    SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_JSON,
    SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_REPORT,
    SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_DRIFT_JSON,
    SERVICE_WORKER_DECISION_DRIFT_REPORT,
    SERVICE_WORKER_DECISION_DRIFT_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_COMMAND_SAFETY_JSON,
    SERVICE_WORKER_DECISION_COMMAND_SAFETY_REPORT,
    SERVICE_WORKER_DECISION_COMMAND_SAFETY_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_JSON,
    SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_REPORT,
    SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_PREFLIGHT_JSON,
    SERVICE_WORKER_DECISION_PREFLIGHT_REPORT,
    SERVICE_WORKER_DECISION_PREFLIGHT_VALIDATION_JSON,
)
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR, ROLE_REGISTRY_PATH, ROOT
from .utils import md_cell, safe_id_fragment
from .service_worker_utils import (
    db_scalar,
    load_report_json_or_error,
)


def service_worker_human_decision_packet_rows(packet_dir: Path, generated_utc: str) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    approval_payload, approval_errors = load_report_json_or_error(SERVICE_WORKER_APPROVAL_REVIEW_JSON)
    gate_payload, gate_errors = load_report_json_or_error(SERVICE_WORKER_GATE_MAP_JSON)
    integrity_payload, integrity_errors = load_report_json_or_error(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON)
    failures = approval_errors + gate_errors + integrity_errors
    approval_reviews = approval_payload.get("approval_reviews", []) if approval_payload else []
    gate_rows = gate_payload.get("gate_map", []) if gate_payload else []
    if approval_payload and not isinstance(approval_reviews, list):
        failures.append("approval review payload field approval_reviews is not a list")
        approval_reviews = []
    if gate_payload and not isinstance(gate_rows, list):
        failures.append("gate map payload field gate_map is not a list")
        gate_rows = []
    gate_by_request = {
        row.get("source_service_request_id"): row
        for row in gate_rows
        if isinstance(row, dict) and row.get("source_service_request_id")
    }
    chain_ok = bool(integrity_payload and integrity_payload.get("all_checks_passed") is True)
    if integrity_payload and not chain_ok:
        failures.append("chain integrity validation is not passing")
    packets: list[dict[str, Any]] = []
    for review in approval_reviews:
        if not isinstance(review, dict):
            continue
        request_id = review.get("source_service_request_id")
        if review.get("recommended_decision") != "human_cro_review_required":
            continue
        if not request_id:
            failures.append("approval review candidate is missing source_service_request_id")
            continue
        gate = gate_by_request.get(request_id, {})
        filename = safe_id_fragment(request_id, 140)
        md_path = packet_dir / f"{filename}.md"
        json_path = packet_dir / f"{filename}.json"
        approval_preview = review.get("approve_command_preview_argv") or []
        reject_preview = review.get("reject_command_preview_argv") or []
        preconditions = {
            "chain_integrity_all_checks_passed": chain_ok,
            "service_status_needs_review": review.get("service_status") == "needs_review",
            "packet_valid": not review.get("packet_errors"),
            "current_gate_human_cro_approval_required": gate.get("current_blocking_gate") == "human_cro_approval_required",
            "manual_review_required": review.get("command_previews_require_manual_review") is True,
            "approve_preview_present": bool(approval_preview),
            "reject_preview_present": bool(reject_preview),
        }
        packet = {
            "schema_version": "service_worker_human_decision_packet.v1",
            "generated_utc": generated_utc,
            "source_service_request_id": request_id,
            "lane_id": review.get("lane_id"),
            "service_id": review.get("service_id"),
            "request_type": review.get("request_type"),
            "worker_type": review.get("worker_type"),
            "service_status": review.get("service_status"),
            "risk_gate": review.get("risk_gate"),
            "review_route": review.get("review_route"),
            "review_priority": review.get("review_priority"),
            "current_blocking_gate": gate.get("current_blocking_gate"),
            "recommended_worker_pool_id": gate.get("recommended_worker_pool_id"),
            "recommended_worker_role_id": gate.get("recommended_worker_role_id"),
            "pool_status": gate.get("pool_status"),
            "registration_required": gate.get("registration_required"),
            "scope_diff_route": review.get("scope_diff_route"),
            "scope_compatible_with_packet": review.get("scope_compatible_with_packet"),
            "missing_or_failed_scope_checks": review.get("missing_or_failed_scope_checks", []),
            "packet_path": review.get("packet_path"),
            "packet_errors": review.get("packet_errors", []),
            "suggested_exact_scope": review.get("suggested_exact_scope"),
            "approve_command_preview_argv": approval_preview,
            "reject_command_preview_argv": reject_preview,
            "preconditions": preconditions,
            "all_preconditions_for_human_decision_packet": all(preconditions.values()),
            "human_decision_required": True,
            "command_previews_require_manual_review": True,
            "decision_packet_markdown_path": str(md_path),
            "decision_packet_json_path": str(json_path),
            "next_action": "Human/CRO must review the packet, risk gate, exact scope, gate map, and current external context before running any approve/reject command manually.",
            "approval_granted_by_decision_packet": False,
            "pool_registered_by_decision_packet": False,
            "service_request_assigned_by_decision_packet": False,
            "service_request_updated_by_decision_packet": False,
            "worker_started_by_decision_packet": False,
            "api_calls": False,
            "external_side_effects": False,
        }
        packets.append(packet)
    return packets, {
        "chain_integrity_validation_loaded": integrity_payload is not None,
        "chain_integrity_all_checks_passed": chain_ok,
        "chain_integrity_generated_utc": integrity_payload.get("generated_utc") if integrity_payload else None,
        "approval_review_generated_utc": approval_payload.get("generated_utc") if approval_payload else None,
        "gate_map_generated_utc": gate_payload.get("generated_utc") if gate_payload else None,
    }, failures


def write_service_worker_human_decision_packets(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_HUMAN_DECISION_PACKETS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_HUMAN_DECISION_PACKETS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_HUMAN_DECISION_PACKETS_VALIDATION_JSON
    packet_dir = Path(args.packet_dir) if args.packet_dir else SERVICE_WORKER_HUMAN_DECISION_PACKET_DIR
    packet_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = now_utc()
    packets, source_state, failures = service_worker_human_decision_packet_rows(packet_dir, generated_utc)
    for packet in packets:
        Path(packet["decision_packet_json_path"]).write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        lines = [
            "# Service Worker Human Decision Packet",
            "",
            f"Generated UTC: {generated_utc}",
            f"Request: `{packet['source_service_request_id']}`",
            f"Lane: `{packet.get('lane_id') or ''}`",
            f"Worker type: `{packet.get('worker_type') or ''}`",
            f"Risk gate: `{packet.get('risk_gate') or ''}`",
            "",
            "## Operating Rule",
            "",
            "This packet is for human/CRO decision support only. It does not approve, reject, register, assign, update, start, browse, call APIs, post, submit, pay, trade, or contact anyone.",
            "",
            "## Gate State",
            "",
            f"- Current blocking gate: `{packet.get('current_blocking_gate') or ''}`",
            f"- Review route: `{packet.get('review_route') or ''}`",
            f"- Scope diff route: `{packet.get('scope_diff_route') or ''}`",
            f"- Scope compatible with packet: `{packet.get('scope_compatible_with_packet')}`",
            f"- Recommended worker pool: `{packet.get('recommended_worker_pool_id') or ''}`",
            f"- Pool status: `{packet.get('pool_status') or ''}`",
            "",
            "## Preconditions",
            "",
            "| Check | Passed |",
            "| --- | --- |",
        ]
        for key, value in packet["preconditions"].items():
            lines.append(f"| `{key}` | `{value}` |")
        lines.extend(
            [
                "",
                "## Suggested Exact Scope",
                "",
                packet.get("suggested_exact_scope") or "",
                "",
                "## Approve Preview",
                "",
                "```json",
                json.dumps(packet["approve_command_preview_argv"], indent=2),
                "```",
                "",
                "## Reject Preview",
                "",
                "```json",
                json.dumps(packet["reject_command_preview_argv"], indent=2),
                "```",
                "",
                "## Next Action",
                "",
                packet["next_action"],
                "",
            ]
        )
        Path(packet["decision_packet_markdown_path"]).write_text("\n".join(lines) + "\n", encoding="utf-8")
    terminal_do_not_approve_count = int(
        db_scalar(
            conn,
            "SELECT COUNT(*) FROM service_requests WHERE status IN ('complete', 'rejected', 'cancelled')",
        )
        or 0
    )
    approve_preview_count = sum(1 for packet in packets if packet["approve_command_preview_argv"])
    reject_preview_count = sum(1 for packet in packets if packet["reject_command_preview_argv"])
    all_preconditions = all(packet["all_preconditions_for_human_decision_packet"] for packet in packets)
    validation_failures = list(failures)
    if len(packets) != 11:
        validation_failures.append(f"expected 11 human decision packets, wrote {len(packets)}")
    if terminal_do_not_approve_count != 3:
        validation_failures.append(f"expected 3 terminal do-not-approve rows, found {terminal_do_not_approve_count}")
    if not all_preconditions:
        validation_failures.append("one or more decision packets failed local preconditions")
    payload = {
        "schema_version": "service_worker_human_decision_packets.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "packet_dir": str(packet_dir),
        "source_state": source_state,
        "decision_packet_count": len(packets),
        "terminal_do_not_approve_count": terminal_do_not_approve_count,
        "approve_command_preview_count": approve_preview_count,
        "reject_command_preview_count": reject_preview_count,
        "all_preconditions_for_human_decision_packets": all_preconditions,
        "decision_packets": packets,
        "execution_notice": "Human decision packets only. Command previews are not executed and this report grants no approval, registration, assignment, update, start, or external action.",
        "approval_granted_by_decision_packets": False,
        "pools_registered_by_decision_packets": 0,
        "service_requests_assigned_by_decision_packets": 0,
        "service_requests_updated_by_decision_packets": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": validation_failures,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_human_decision_packets_validation.v1",
        "generated_utc": generated_utc,
        "decision_packets_path": str(json_output_path),
        "packet_dir": str(packet_dir),
        "decision_packet_count": len(packets),
        "terminal_do_not_approve_count": terminal_do_not_approve_count,
        "approve_command_preview_count": approve_preview_count,
        "reject_command_preview_count": reject_preview_count,
        "all_preconditions_for_human_decision_packets": all_preconditions,
        "all_packets_require_manual_review": all(packet["command_previews_require_manual_review"] for packet in packets),
        "all_packets_no_approval": all(not packet["approval_granted_by_decision_packet"] for packet in packets),
        "all_packets_no_registration": all(not packet["pool_registered_by_decision_packet"] for packet in packets),
        "all_packets_no_assignment": all(not packet["service_request_assigned_by_decision_packet"] for packet in packets),
        "approval_granted_by_decision_packets": False,
        "pools_registered_by_decision_packets": 0,
        "service_requests_assigned_by_decision_packets": 0,
        "service_requests_updated_by_decision_packets": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failure_count": len(validation_failures),
        "failures": validation_failures,
        "source_state": source_state,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Human Decision Packets",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"Packet directory: `{packet_dir}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report writes local human/CRO decision packets only. It does not approve, reject, register, assign, update, start, browse, call APIs, post, submit, pay, trade, or contact anyone.",
        "",
        f"- Decision packets: `{len(packets)}`",
        f"- Terminal do-not-approve rows: `{terminal_do_not_approve_count}`",
        f"- Approve previews: `{approve_preview_count}`",
        f"- Reject previews: `{reject_preview_count}`",
        f"- Validation failures: `{len(validation_failures)}`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Packets",
        "",
        "| Request | Lane | Worker Type | Gate | Pool | Packet |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for packet in packets:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{packet['source_service_request_id']}`",
                    f"`{packet.get('lane_id') or ''}`",
                    f"`{packet.get('worker_type') or ''}`",
                    f"`{packet.get('current_blocking_gate') or ''}`",
                    f"`{packet.get('recommended_worker_pool_id') or ''}`",
                    f"`{packet['decision_packet_markdown_path']}`",
                ]
            )
            + " |"
        )
    if validation_failures:
        lines.extend(["", "## Validation Failures", ""])
        for failure in validation_failures:
            lines.append(f"- {failure}")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "A human/CRO can open a packet, revise the suggested exact scope if needed, and manually run either the approve or reject preview. Pool registration, assignment, readiness, and worker start remain separate later gates.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": not validation_failures,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "packet_dir": str(packet_dir),
                "decision_packet_count": len(packets),
                "failure_count": len(validation_failures),
            },
            indent=2,
        )
    )
