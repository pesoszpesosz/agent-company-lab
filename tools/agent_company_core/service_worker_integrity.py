from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    SERVICE_WORKER_CHAIN_INTEGRITY_JSON,
    SERVICE_WORKER_CHAIN_INTEGRITY_REPORT,
    SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON,
)
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR
from .service_worker_integrity_specs import service_worker_chain_integrity_specs
from .service_workers import (
    check_expected_values,
    load_report_json_or_error,
    service_worker_chain_db_snapshot,
)
from .utils import md_cell


def write_service_worker_chain_integrity(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_CHAIN_INTEGRITY_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_CHAIN_INTEGRITY_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []
    validation_reports: list[dict[str, Any]] = []
    for spec in service_worker_chain_integrity_specs():
        payload, load_errors = load_report_json_or_error(spec["path"])
        failures.extend(load_errors)
        checks, check_failures = check_expected_values(payload, spec["expected"], spec["id"])
        failures.extend(check_failures)
        key_count = payload.get(spec["count_key"]) if payload else None
        validation_reports.append(
            {
                "id": spec["id"],
                "label": spec["label"],
                "path": str(spec["path"]),
                "loaded": payload is not None,
                "schema_version": payload.get("schema_version") if payload else None,
                "generated_utc": payload.get("generated_utc") if payload else None,
                "key_count_name": spec["count_key"],
                "key_count": key_count,
                "checks_passed": bool(payload is not None and all(check["passed"] for check in checks)),
                "checks": checks,
            }
        )

    db_snapshot = service_worker_chain_db_snapshot(conn)
    expected_service_status_counts = dict(db_snapshot["service_status_counts"])
    expected_assigned_rows = [
        {
            "request_id": "req-test-lifecycle-approve-20260614",
            "status": "complete",
            "assigned_agent_id": "recovered-profitable-edge-infra",
            "updated_at": "2026-06-14T11:14:06Z",
        }
    ]
    db_checks = [
        {
            "key": "open_tasks_queued_only",
            "expected": 0,
            "actual": db_snapshot["open_tasks_started_or_leased"],
        },
        {
            "key": "open_tasks_have_evidence_required",
            "expected": 0,
            "actual": db_snapshot["open_tasks_missing_evidence_required"],
        },
        {
            "key": "service_status_counts",
            "expected": expected_service_status_counts,
            "actual": db_snapshot["service_status_counts"],
        },
        {
            "key": "agents_total",
            "expected": 11,
            "actual": db_snapshot["agents_total"],
        },
        {
            "key": "assigned_service_requests",
            "expected": expected_assigned_rows,
            "actual": db_snapshot["assigned_service_requests"],
        },
    ]
    for check in db_checks:
        check["passed"] = check["actual"] == check["expected"]
        check["failure"] = None if check["passed"] else (
            f"db.{check['key']} expected {check['expected']!r}, got {check['actual']!r}"
        )
        if check["failure"]:
            failures.append(check["failure"])
    service_status_counts = db_snapshot["service_status_counts"]
    if service_status_counts.get("complete", 0) != 1:
        failures.append(f"db.service_status_counts.complete expected 1, got {service_status_counts.get('complete', 0)}")
    if service_status_counts.get("rejected", 0) != 2:
        failures.append(f"db.service_status_counts.rejected expected 2, got {service_status_counts.get('rejected', 0)}")
    if service_status_counts.get("needs_review", 0) < 11:
        failures.append(f"db.service_status_counts.needs_review expected at least 11, got {service_status_counts.get('needs_review', 0)}")

    all_checks_passed = not failures
    payload = {
        "schema_version": "service_worker_chain_integrity.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "db_snapshot": db_snapshot,
        "db_checks": db_checks,
        "checked_report_count": len(validation_reports),
        "validation_reports": validation_reports,
        "all_checks_passed": all_checks_passed,
        "failures": failures,
        "approval_granted_by_integrity_report": False,
        "pools_registered_by_integrity_report": 0,
        "service_requests_assigned_by_integrity_report": 0,
        "service_requests_updated_by_integrity_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_chain_integrity_validation.v1",
        "generated_utc": generated_utc,
        "integrity_report_path": str(json_output_path),
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        "checked_report_count": len(validation_reports),
        "db_counts": {
            "tasks_total": db_snapshot["tasks_total"],
            "tasks_complete": db_snapshot["tasks_complete"],
            "tasks_open": db_snapshot["tasks_open"],
            "artifacts_total": db_snapshot["artifacts_total"],
            "trace_events_total": db_snapshot["trace_events_total"],
            "agents_total": db_snapshot["agents_total"],
            "service_requests_total": db_snapshot["service_requests_total"],
        },
        "service_status_counts": db_snapshot["service_status_counts"],
        "approval_granted_by_integrity_report": False,
        "pools_registered_by_integrity_report": 0,
        "service_requests_assigned_by_integrity_report": 0,
        "service_requests_updated_by_integrity_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Service Worker Chain Integrity",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This is a local integrity report only. It grants no approval, registers no pools, assigns no service requests, updates no service requests, starts no workers, calls no APIs, and performs no external side effects.",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{all_checks_passed}`",
        f"- Failures: `{len(failures)}`",
        f"- Validation layers checked: `{len(validation_reports)}`",
        f"- Service status counts: `{json.dumps(db_snapshot['service_status_counts'], sort_keys=True)}`",
        f"- Tasks: `{db_snapshot['tasks_complete']}` complete of `{db_snapshot['tasks_total']}`",
        f"- Open queued tasks: `{db_snapshot['tasks_open']}`",
        f"- Artifacts: `{db_snapshot['artifacts_total']}`",
        f"- Trace events: `{db_snapshot['trace_events_total']}`",
        f"- Agents: `{db_snapshot['agents_total']}`",
        f"- Pools registered by integrity report: `0`",
        f"- Service requests assigned by integrity report: `0`",
        f"- Service requests updated by integrity report: `0`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Layer Checks",
        "",
        "| Layer | Status | Key Count | Validation File |",
        "| --- | --- | ---: | --- |",
    ]
    for report in validation_reports:
        status = "pass" if report["checks_passed"] else "fail"
        lines.append(
            "| "
            + " | ".join(
                [
                    report["label"],
                    f"`{status}`",
                    f"`{report['key_count']}`",
                    f"`{report['path']}`",
                ]
            )
            + " |"
        )
    lines.extend(["", "## Database Checks", "", "| Check | Status | Actual |", "| --- | --- | --- |"])
    for check in db_checks:
        status = "pass" if check["passed"] else "fail"
        lines.append(f"| `{check['key']}` | `{status}` | `{md_cell(json.dumps(check['actual'], sort_keys=True), 220)}` |")
    if failures:
        lines.extend(["", "## Failures", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "Refresh the full service-worker report chain before any CRO decision, then use the gate map and exact-scope templates for human review. Do not assign or start service workers until approvals, scope compatibility, pool registration, readiness, and manual assignment are all separately satisfied.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "checked_report_count": len(validation_reports),
                "failure_count": len(failures),
            },
            indent=2,
        )
    )



