from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    MONEY_PATH_COVERAGE_AUDIT_JSON,
    MONEY_PATH_COVERAGE_AUDIT_REPORT,
    MONEY_PATH_COVERAGE_AUDIT_VALIDATION_JSON,
)
from .io import now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .utils import sha256_file
from .money_path_coverage_model import build_money_path_coverage_model
from .money_path_coverage_report import render_money_path_coverage_report


def write_money_path_coverage_audit(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else MONEY_PATH_COVERAGE_AUDIT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else MONEY_PATH_COVERAGE_AUDIT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else MONEY_PATH_COVERAGE_AUDIT_VALIDATION_JSON
    generated_utc = now_utc()
    task_id = "task-agent-company-money-path-coverage-audit-20260616"
    evidence_id = "agent-company-money-path-coverage-audit-20260616"
    trace_id = "trace-agent-company-money-path-coverage-audit-20260616"
    failures: list[str] = []

    tasks_before = int(db_scalar(conn, "SELECT COUNT(*) FROM tasks") or 0)
    evidence_before = int(db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence") or 0)
    artifacts_before = int(db_scalar(conn, "SELECT COUNT(*) FROM artifacts") or 0)
    trace_events_before = int(db_scalar(conn, "SELECT COUNT(*) FROM trace_events") or 0)

    lanes = [
        dict(row)
        for row in conn.execute(
            """
            SELECT lane_id, department, owner_agent_id, owner_thread_id, status
            FROM lanes
            ORDER BY lane_id
            """
        )
    ]
    evidence_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM lane_evidence GROUP BY lane_id")
    }
    task_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM tasks GROUP BY lane_id")
    }
    source_spec_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM source_specs GROUP BY lane_id")
    }
    parked_request_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute(
            "SELECT lane_id, COUNT(*) AS count FROM service_requests WHERE status = 'needs_review' GROUP BY lane_id"
        )
    }
    trace_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM trace_events GROUP BY lane_id")
    }
    service_request_status_counts = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    coverage_model = build_money_path_coverage_model(
        lanes=lanes,
        evidence_counts=evidence_counts,
        task_counts=task_counts,
        source_spec_counts=source_spec_counts,
        parked_request_counts=parked_request_counts,
        trace_counts=trace_counts,
    )
    active_lanes = coverage_model["active_lanes"]
    owned_active_lanes = coverage_model["owned_active_lanes"]
    thin_evidence_threshold = coverage_model["thin_evidence_threshold"]
    lane_rows = coverage_model["lane_rows"]
    thin_evidence_rows = coverage_model["thin_evidence_rows"]
    recommended_next_lanes = coverage_model["recommended_next_lanes"]
    recommended_lane_ids = coverage_model["recommended_lane_ids"]
    no_action_lanes = coverage_model["no_action_lanes"]
    runtime_boundary = coverage_model["runtime_boundary"]
    read_only_boundary_preserved = coverage_model["read_only_boundary_preserved"]
    source_spec_count = int(db_scalar(conn, "SELECT COUNT(*) FROM source_specs") or 0)
    service_catalog_count = int(db_scalar(conn, "SELECT COUNT(*) FROM service_catalog") or 0)
    if len(active_lanes) != 12:
        failures.append(f"expected 12 active lanes, got {len(active_lanes)}")
    if len(owned_active_lanes) != 11:
        failures.append(f"expected 11 owned active lanes, got {len(owned_active_lanes)}")
    if source_spec_count != 13:
        failures.append(f"expected 13 source specs, got {source_spec_count}")
    if service_catalog_count != 13:
        failures.append(f"expected 13 service catalog entries, got {service_catalog_count}")
    if len(thin_evidence_rows) != 0:
        failures.append(f"expected 0 thin-evidence actionable money lanes, got {len(thin_evidence_rows)}")
    parked_count = service_request_status_counts.get("needs_review", 0)
    if parked_count < 11:
        failures.append(f"expected at least 11 parked service requests, got {parked_count}")
    if len(recommended_next_lanes) != len(thin_evidence_rows):
        failures.append("recommended lane count did not match thin-evidence lane count")
    if not read_only_boundary_preserved:
        failures.append("submitted_bounty_payouts read-only boundary was not preserved")

    payload = {
        "schema_version": "agent_company.money_path_coverage_audit.v1",
        "generated_utc": generated_utc,
        "audit_task_id": task_id,
        "audit_evidence_id": evidence_id,
        "purpose": "Rank current online money-path lane coverage so the next agent waves target undercovered lanes instead of more platform-only plumbing.",
        "active_lane_count": len(active_lanes),
        "owned_active_lane_count": len(owned_active_lanes),
        "source_spec_count": source_spec_count,
        "service_catalog_count": service_catalog_count,
        "thin_evidence_threshold": thin_evidence_threshold,
        "thin_evidence_lane_count": len(thin_evidence_rows),
        "thin_evidence_lane_ids": [row["lane_id"] for row in thin_evidence_rows],
        "parked_service_request_count": parked_count,
        "service_request_status_counts": service_request_status_counts,
        "recommended_next_lane_count": len(recommended_next_lanes),
        "recommended_next_lanes": recommended_next_lanes,
        "all_lane_rows": lane_rows,
        "no_action_lanes": no_action_lanes,
        "runtime_boundary": runtime_boundary,
        "next_action": "Launch/report the six undercovered money lanes as read-only or local-proof research waves before adding more platform approval plumbing.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    output_path.write_text(
        render_money_path_coverage_report(
            generated_utc=generated_utc,
            json_output_path=json_output_path,
            validation_path=validation_path,
            coverage_model=coverage_model,
            source_spec_count=source_spec_count,
            service_request_status_counts=service_request_status_counts,
            payload=payload,
            failures=failures,
        ),
        encoding="utf-8",
    )
    ts = generated_utc
    conn.execute(
        """
        INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, started_at, completed_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          status=excluded.status,
          priority=excluded.priority,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            task_id,
            "platform_engineering",
            "Create money-path coverage audit and next-lane dispatch order",
            "complete",
            20,
            "recovered-profitable-edge-infra",
            "agent-company-money-path-coverage-audit-20260616",
            str(output_path),
            "Use recommended_next_lanes to run read-only or local-proof research waves for undercovered money paths.",
            ts,
            ts,
            ts,
            ts,
        ),
    )
    upsert_evidence(
        conn,
        {
            "evidence_id": evidence_id,
            "lane_id": "platform_engineering",
            "source_path": str(output_path),
            "source_url": None,
            "title": "Agent company money-path coverage audit",
            "status": "local_agent_company_money_path_coverage_audit_complete",
            "summary": "Coverage audit ranked undercovered money-path lanes and produced a CEO dispatch order for the next read-only/local-proof research waves.",
            "next_action": payload["next_action"],
            "ownership_note": "Platform evidence only; it does not execute money-lane side effects.",
        },
    )
    for artifact_id, kind, path, notes in [
        ("artifact-agent-company-money-path-coverage-audit-md-20260616", "report_md", output_path, "Markdown money-path coverage audit."),
        ("artifact-agent-company-money-path-coverage-audit-json-20260616", "report_json", json_output_path, "Machine-readable money-path coverage audit."),
    ]:
        conn.execute(
            """
            INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
              path_or_url=excluded.path_or_url,
              sha256=excluded.sha256,
              notes=excluded.notes
            """,
            (
                artifact_id,
                "platform_engineering",
                task_id,
                kind,
                str(path),
                sha256_file(path),
                notes,
                ts,
            ),
        )
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path,
          summary=excluded.summary
        """,
        (
            "trace-event-agent-company-money-path-coverage-audit-20260616",
            trace_id,
            "platform_engineering",
            task_id,
            "recovered-profitable-edge-infra",
            "money_path_coverage_audit_written",
            ts,
            "local_cli",
            "Wrote local money-path coverage audit and CEO dispatch order for undercovered lanes.",
            json.dumps(
                {
                    "span_kind": "internal",
                    "runtime": "local_cli",
                    "recommended_lane_ids": recommended_lane_ids,
                    **runtime_boundary,
                },
                sort_keys=True,
            ),
            str(output_path),
            ts,
        ),
    )

    task_present = bool(db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (task_id,)))
    evidence_present = bool(db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (evidence_id,)))
    if not task_present:
        failures.append("coverage audit task row missing")
    if not evidence_present:
        failures.append("coverage audit evidence row missing")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.money_path_coverage_audit_validation.v1",
        "generated_utc": generated_utc,
        "audit_path": str(output_path),
        "audit_json_path": str(json_output_path),
        "active_lane_count": len(active_lanes),
        "owned_active_lane_count": len(owned_active_lanes),
        "source_spec_count": source_spec_count,
        "service_catalog_count": service_catalog_count,
        "thin_evidence_threshold": thin_evidence_threshold,
        "thin_evidence_lane_count": len(thin_evidence_rows),
        "thin_evidence_lane_ids": [row["lane_id"] for row in thin_evidence_rows],
        "parked_service_request_count": service_request_status_counts.get("needs_review", 0),
        "recommended_next_lane_count": len(recommended_next_lanes),
        "recommended_lane_ids": recommended_lane_ids,
        "coverage_audit_task_present": task_present,
        "coverage_audit_evidence_present": evidence_present,
        "tasks_rows_before": tasks_before,
        "tasks_rows_after": int(db_scalar(conn, "SELECT COUNT(*) FROM tasks") or 0),
        "lane_evidence_rows_before": evidence_before,
        "lane_evidence_rows_after": int(db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence") or 0),
        "artifacts_rows_before": artifacts_before,
        "artifacts_rows_after": int(db_scalar(conn, "SELECT COUNT(*) FROM artifacts") or 0),
        "trace_events_rows_before": trace_events_before,
        "trace_events_rows_after": int(db_scalar(conn, "SELECT COUNT(*) FROM trace_events") or 0),
        "read_only_boundary_preserved": read_only_boundary_preserved,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(artifact_id) DO UPDATE SET
          path_or_url=excluded.path_or_url,
          sha256=excluded.sha256,
          notes=excluded.notes
        """,
        (
            "artifact-agent-company-money-path-coverage-audit-validation-20260616",
            "platform_engineering",
            task_id,
            "validation_json",
            str(validation_path),
            sha256_file(validation_path),
            "Validation for money-path coverage audit.",
            ts,
        ),
    )
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "thin_evidence_lane_count": len(thin_evidence_rows),
                "recommended_lane_ids": recommended_lane_ids,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
