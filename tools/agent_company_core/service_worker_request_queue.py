"""Service-worker request queue report generation."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    SERVICE_WORKER_REQUEST_QUEUE_JSON,
    SERVICE_WORKER_REQUEST_QUEUE_REPORT,
    SERVICE_WORKER_REQUEST_QUEUE_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import DB_PATH, REPORTS_DIR
from .service_worker_core import (
    service_worker_packet_path,
    synthesize_service_worker_request,
    validate_service_worker_request_object,
)
from .utils import md_cell


def write_service_worker_queue(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_REQUEST_QUEUE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_REQUEST_QUEUE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_REQUEST_QUEUE_VALIDATION_JSON
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
    by_worker_type: dict[str, list[dict[str, Any]]] = {}
    by_risk_gate: dict[str, list[dict[str, Any]]] = {}
    by_status: dict[str, list[dict[str, Any]]] = {}
    worker_requests: list[dict[str, Any]] = []
    validation_errors: dict[str, list[str]] = {}
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
        summary = {
            "worker_request_id": obj["worker_request_id"],
            "source_service_request_id": obj["source_service_request_id"],
            "lane_id": obj["requesting_lane_id"],
            "status": obj["status"],
            "risk_gate": obj["risk_gate"],
            "worker_type": obj["worker_type"],
            "json_path": str(packet_path),
            "source": source,
        }
        by_worker_type.setdefault(obj["worker_type"], []).append(summary)
        by_risk_gate.setdefault(obj["risk_gate"], []).append(summary)
        by_status.setdefault(obj["status"], []).append(summary)
        worker_requests.append({"request": obj, "json_path": str(packet_path), "source": source})
    if validation_errors:
        raise SystemExit(f"Invalid service_worker_request.v1 rows: {json.dumps(validation_errors, sort_keys=True)}")

    queue_payload = {
        "schema_version": "service_worker_request_queue.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "request_count": len(worker_requests),
        "execution_notice": "Read-only queue report. No service request was approved, assigned, started, or executed.",
        "by_worker_type": dict(sorted(by_worker_type.items())),
        "by_risk_gate": dict(sorted(by_risk_gate.items())),
        "by_status": dict(sorted(by_status.items())),
        "worker_requests": worker_requests,
        "external_side_effects": False,
        "approval_granted_by_report": False,
        "service_requests_started_by_report": 0,
    }
    json_output_path.write_text(json.dumps(queue_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    validation_payload = {
        "generated_utc": generated_utc,
        "schema_version": "service_worker_request_queue_validation.v1",
        "queue_path": str(json_output_path),
        "validated_count": len(worker_requests),
        "all_required_fields_present": True,
        "all_worker_types_known": True,
        "side_effect_flags_all_false": True,
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "worker_type_counts": {key: len(value) for key, value in sorted(by_worker_type.items())},
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Service Worker Request Queue",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report is read-only queue infrastructure. It does not approve, assign, start, browse, register, trade, spend, post, submit, call external APIs, or contact anyone.",
        "",
        f"- Worker requests in report: `{len(worker_requests)}`",
        f"- By worker type: `{json.dumps(validation_payload['worker_type_counts'], sort_keys=True)}`",
        f"- By status: `{json.dumps({key: len(value) for key, value in sorted(by_status.items())}, sort_keys=True)}`",
        "",
        "## Queue By Worker Type",
        "",
    ]
    for worker_type, entries in sorted(by_worker_type.items()):
        lines.extend([f"### {worker_type} ({len(entries)})", "", "| Status | Source Request | Lane | Risk Gate | Packet |", "| --- | --- | --- | --- | --- |"])
        for entry in entries:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{entry['status']}`",
                        f"`{entry['source_service_request_id']}`",
                        f"`{entry['lane_id']}`",
                        md_cell(entry["risk_gate"], 160),
                        f"`{entry['json_path']}`",
                    ]
                )
                + " |"
            )
        lines.append("")
    lines.extend(
        [
            "## Next Action",
            "",
            "Use this command as the first-class queue surface, then test DBOS/Hatchet durable queue adapter manifests against these packets with no external actions.",
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
                "count": len(worker_requests),
            },
            indent=2,
        )
    )

__all__ = ["write_service_worker_queue"]
