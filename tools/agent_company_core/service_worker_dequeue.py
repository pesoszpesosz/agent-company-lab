"""Service-worker dequeue dry-run planning."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    SERVICE_WORKER_DEQUEUE_JSON,
    SERVICE_WORKER_DEQUEUE_REPORT,
    SERVICE_WORKER_DEQUEUE_RESULT_DIR,
    SERVICE_WORKER_DEQUEUE_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import DB_PATH, REPORTS_DIR
from .service_worker_core import (
    service_worker_packet_path,
    synthesize_service_worker_request,
    validate_service_worker_request_object,
)
from .utils import safe_id_fragment


def service_worker_dequeue_route(obj: dict[str, Any]) -> dict[str, Any]:
    status = obj.get("status")
    worker_type = obj.get("worker_type")
    if status == "complete":
        route = "terminal_complete_no_worker_start"
        reason = "Source service request is already complete; retain audit evidence only."
    elif status == "rejected":
        route = "terminal_rejected_no_worker_start"
        reason = "Source service request is rejected; do not reopen without a new service request."
    elif status in {"approved", "assigned"} and worker_type == "local_runtime_adapter":
        route = "ready_for_manual_local_runtime_review_no_worker_start"
        reason = "Local-runtime packet has an approval-like status, but this command is a dry-run and never starts workers."
    elif status in {"approved", "assigned"}:
        route = "approved_scope_requires_worker_boundary_review_no_worker_start"
        reason = "Approval-like status still requires exact scope, lease, and worker-boundary verification outside this dry-run."
    else:
        route = "hold_for_approval_no_worker_start"
        reason = f"Source service request is {status}; no approval or worker start is granted by this dry-run."
    return {
        "route": route,
        "dequeue_allowed": False,
        "worker_started": False,
        "service_request_updated": False,
        "approval_granted": False,
        "reason": reason,
    }


def service_worker_dequeue_result_paths(result_dir: Path, worker_request_id: str) -> tuple[Path, Path]:
    safe_id = safe_id_fragment(worker_request_id, 96)
    return result_dir / f"{safe_id}-dequeue-result.json", result_dir / f"{safe_id}-dequeue-result.md"


def write_service_worker_dequeue_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    result_dir = Path(args.result_dir) if args.result_dir else SERVICE_WORKER_DEQUEUE_RESULT_DIR
    result_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_DEQUEUE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_DEQUEUE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_DEQUEUE_VALIDATION_JSON
    generated_utc = now_utc()

    rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT sr.*, l.department
            FROM service_requests sr
            LEFT JOIN lanes l ON l.lane_id = sr.lane_id
            ORDER BY sr.request_id
            """
        )
    ]
    result_entries: list[dict[str, Any]] = []
    validation_errors: dict[str, list[str]] = {}
    route_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    worker_type_counts: dict[str, int] = {}

    for row in rows:
        packet_path = service_worker_packet_path(row["request_id"])
        if packet_path.exists():
            obj = load_json(packet_path)
            source = "existing_packet"
        else:
            obj = synthesize_service_worker_request(row, generated_utc)
            source = "synthesized_from_db"
        errors = validate_service_worker_request_object(obj)
        if errors:
            validation_errors[row["request_id"]] = errors
            continue
        decision = service_worker_dequeue_route(obj)
        result_json_path, result_md_path = service_worker_dequeue_result_paths(result_dir, obj["worker_request_id"])
        result_payload = {
            "schema_version": "service_worker_dequeue_result.v1",
            "generated_utc": generated_utc,
            "worker_request_id": obj["worker_request_id"],
            "source_service_request_id": obj["source_service_request_id"],
            "requesting_lane_id": obj["requesting_lane_id"],
            "worker_type": obj["worker_type"],
            "service_id": obj["service_id"],
            "status_snapshot": obj["status"],
            "approval_status_snapshot": obj["approval_status_snapshot"],
            "risk_gate": obj["risk_gate"],
            "packet_path": str(packet_path),
            "packet_source": source,
            "route": decision["route"],
            "reason": decision["reason"],
            "dequeue_allowed": decision["dequeue_allowed"],
            "worker_started": decision["worker_started"],
            "service_request_updated": decision["service_request_updated"],
            "approval_granted": decision["approval_granted"],
            "api_calls": False,
            "external_side_effects": False,
            "browser_opened": False,
            "account_action": False,
            "public_action": False,
            "payment_or_wallet_action": False,
            "real_money_action": False,
            "expected_worker_result_artifact_path": obj["result_artifact_path"],
            "local_dequeue_result_json": str(result_json_path),
            "local_dequeue_result_md": str(result_md_path),
            "decision_note": "Deterministic local dequeue dry-run only. No worker was started and no service request row was changed.",
            "next_action": "Approve exact scope separately before any real worker execution; otherwise keep packet parked.",
        }
        result_json_path.write_text(json.dumps(result_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result_lines = [
            f"# Service Worker Dequeue Result - {obj['worker_request_id']}",
            "",
            f"Generated UTC: {generated_utc}",
            "",
            f"- Source service request: `{obj['source_service_request_id']}`",
            f"- Lane: `{obj['requesting_lane_id']}`",
            f"- Worker type: `{obj['worker_type']}`",
            f"- Status snapshot: `{obj['status']}`",
            f"- Risk gate: {obj['risk_gate']}",
            f"- Route: `{decision['route']}`",
            f"- Dequeue allowed: `{decision['dequeue_allowed']}`",
            f"- Worker started: `{decision['worker_started']}`",
            f"- Service request updated: `{decision['service_request_updated']}`",
            f"- Approval granted: `{decision['approval_granted']}`",
            f"- API calls: `False`",
            f"- External side effects: `False`",
            "",
            "## Reason",
            "",
            decision["reason"],
            "",
            "## Next Action",
            "",
            "Approve exact scope separately before any real worker execution; otherwise keep packet parked.",
            "",
        ]
        result_md_path.write_text("\n".join(result_lines), encoding="utf-8")
        result_entry = {
            "worker_request_id": obj["worker_request_id"],
            "source_service_request_id": obj["source_service_request_id"],
            "lane_id": obj["requesting_lane_id"],
            "worker_type": obj["worker_type"],
            "status": obj["status"],
            "risk_gate": obj["risk_gate"],
            "route": decision["route"],
            "dequeue_allowed": decision["dequeue_allowed"],
            "worker_started": decision["worker_started"],
            "json_result_path": str(result_json_path),
            "md_result_path": str(result_md_path),
            "packet_path": str(packet_path),
        }
        result_entries.append(result_entry)
        route_counts[decision["route"]] = route_counts.get(decision["route"], 0) + 1
        status_counts[obj["status"]] = status_counts.get(obj["status"], 0) + 1
        worker_type_counts[obj["worker_type"]] = worker_type_counts.get(obj["worker_type"], 0) + 1

    if validation_errors:
        raise SystemExit(f"Invalid service_worker_request.v1 rows: {json.dumps(validation_errors, sort_keys=True)}")

    plan_payload = {
        "schema_version": "service_worker_dequeue_plan.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "source_contract": "service_worker_request.v1",
        "result_dir": str(result_dir),
        "request_count": len(result_entries),
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
        "dequeue_results": result_entries,
        "execution_notice": "Local deterministic dequeue dry-run. No service request was approved, assigned, started, completed, or externally executed.",
        "service_requests_approved_by_plan": 0,
        "service_requests_started_by_plan": 0,
        "service_requests_updated_by_plan": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(plan_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    validation_payload = {
        "schema_version": "service_worker_dequeue_plan_validation.v1",
        "generated_utc": generated_utc,
        "plan_path": str(json_output_path),
        "validated_count": len(result_entries),
        "result_files_written": len(result_entries) * 2,
        "all_dequeue_allowed_false": all(not item["dequeue_allowed"] for item in result_entries),
        "all_worker_started_false": all(not item["worker_started"] for item in result_entries),
        "service_requests_approved_by_plan": 0,
        "service_requests_started_by_plan": 0,
        "service_requests_updated_by_plan": 0,
        "api_calls": False,
        "external_side_effects": False,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Service Worker Dequeue Plan",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        f"Result directory: `{result_dir}`",
        "",
        "## Operating Rule",
        "",
        "This command is a local deterministic dequeue dry-run. It writes local result placeholders only. It does not approve, assign, start, complete, browse, register, trade, spend, post, submit, call external APIs, enqueue external jobs, or contact anyone.",
        "",
        f"- Worker requests evaluated: `{len(result_entries)}`",
        f"- Result files written: `{validation_payload['result_files_written']}`",
        f"- Route counts: `{json.dumps(validation_payload['route_counts'], sort_keys=True)}`",
        f"- By status: `{json.dumps(validation_payload['status_counts'], sort_keys=True)}`",
        f"- By worker type: `{json.dumps(validation_payload['worker_type_counts'], sort_keys=True)}`",
        f"- Worker starts: `0`",
        f"- Service requests updated: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Results",
        "",
        "| Status | Route | Source Request | Lane | Worker Type | Result |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in result_entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['status']}`",
                    f"`{item['route']}`",
                    f"`{item['source_service_request_id']}`",
                    f"`{item['lane_id']}`",
                    f"`{item['worker_type']}`",
                    f"`{item['md_result_path']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "Promote the SQLite path only after adding a worker lease check and exact approval-scope verifier. Keep DBOS, Hatchet, and Temporal at manifest-only status until this local dry-run contract is boring and repeatable.",
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
                "result_dir": str(result_dir),
                "count": len(result_entries),
                "result_files_written": validation_payload["result_files_written"],
            },
            indent=2,
        )
    )

__all__ = [
    "service_worker_dequeue_result_paths",
    "service_worker_dequeue_route",
    "write_service_worker_dequeue_plan",
]
