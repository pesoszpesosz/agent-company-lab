"""Durable-adapter reducer dry-run execution."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    DURABLE_ADAPTER_DRY_RUN_RESULT_SCHEMA_VERSION,
    DURABLE_ADAPTER_FIXTURE_SCHEMA_VERSION,
    DURABLE_ADAPTER_RESUME_REQUIREMENTS_ORDER_POLICY,
)
from .durable_adapter_paths import resolve_durable_adapter_result_path
from .durable_adapter_validation import validate_durable_adapter_fixture_doc
from .io import load_json, now_utc


def dry_run_durable_service_request_reducer(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    fixture_path = Path(args.fixtures)
    fixture_doc = load_json(fixture_path)
    result_path = resolve_durable_adapter_result_path(args.result_path)
    schema_version = fixture_doc.get("schema_version")
    if schema_version != DURABLE_ADAPTER_FIXTURE_SCHEMA_VERSION:
        raise SystemExit(
            "Fixture JSON schema_version must be "
            f"{DURABLE_ADAPTER_FIXTURE_SCHEMA_VERSION}; got {schema_version!r}"
        )
    fixtures = fixture_doc.get("fixtures")
    if not isinstance(fixtures, list):
        raise SystemExit("Fixture JSON must contain a fixtures list")
    validate_durable_adapter_fixture_doc(fixture_doc, fixtures)

    live_statuses: dict[str, dict[str, Any]] = {}
    if args.check_live_status:
        live_statuses = {
            row["request_id"]: dict(row)
            for row in conn.execute(
                """
                SELECT request_id, status, assigned_agent_id, started_at, completed_at, decision_note, updated_at
                FROM service_requests
                """
            )
        }

    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        request_id = fixture.get("request_id")
        fixture_input = fixture.get("input") or {}
        expected = fixture.get("expected_output") or {}
        result = {
            "schema_version": DURABLE_ADAPTER_DRY_RUN_RESULT_SCHEMA_VERSION,
            "fixture_id": fixture_id,
            "request_id": request_id,
            "input_status": fixture_input.get("status_snapshot"),
            "event_name": fixture_input.get("event_name"),
            "risk_gate": fixture_input.get("risk_gate"),
            "worker_type": fixture_input.get("worker_type"),
            "output_state": expected.get("output_state"),
            "parked": expected.get("parked"),
            "terminal": expected.get("terminal"),
            "ledger_mutation_allowed": False,
            "approval_granted": False,
            "assign_worker": False,
            "start_worker": False,
            "emit_followup_event": False,
            "schedule_activity": False,
            "call_api": False,
            "external_side_effects_allowed": False,
            "idempotency_key": fixture_input.get("idempotency_key"),
            "resume_requirements": expected.get("resume_requirements", []),
            "live_status_checked": None,
            "live_status_matches_fixture": True,
            "matches_expected": True,
            "source": "agent_company_cli_fixture_dry_run_no_external_runtime",
        }

        if args.check_live_status:
            live_row = live_statuses.get(str(request_id))
            live_status = live_row["status"] if live_row else None
            result["live_status_checked"] = live_status
            result["live_status_matches_fixture"] = live_status == fixture_input.get("status_snapshot")
            if not result["live_status_matches_fixture"]:
                result["matches_expected"] = False
                failures.append(
                    {
                        "fixture_id": fixture_id,
                        "request_id": request_id,
                        "failure": "live_status_mismatch_or_missing",
                        "expected": fixture_input.get("status_snapshot"),
                        "actual": live_status,
                    }
                )

        for field in [
            "output_state",
            "parked",
            "terminal",
            "ledger_mutation_allowed",
            "approval_granted",
            "assign_worker",
            "start_worker",
            "emit_followup_event",
            "schedule_activity",
            "call_api",
            "external_side_effects_allowed",
            "resume_requirements",
        ]:
            if result.get(field) != expected.get(field):
                result["matches_expected"] = False
                failures.append(
                    {
                        "fixture_id": fixture_id,
                        "request_id": request_id,
                        "failure": f"mismatch:{field}",
                        "expected": expected.get(field),
                        "actual": result.get(field),
                    }
                )
        results.append(result)

    status_counts: dict[str, int] = {}
    output_state_counts: dict[str, int] = {}
    worker_type_counts: dict[str, int] = {}
    for result in results:
        status_counts[str(result["input_status"])] = status_counts.get(str(result["input_status"]), 0) + 1
        output_state_counts[str(result["output_state"])] = output_state_counts.get(str(result["output_state"]), 0) + 1
        worker_type_counts[str(result["worker_type"])] = worker_type_counts.get(str(result["worker_type"]), 0) + 1

    payload = {
        "schema_version": "agent_company.durable_adapter_cli_dry_run_result_set.v1",
        "generated_utc": now_utc(),
        "fixture_path": str(fixture_path),
        "result_count": len(results),
        "status_counts": dict(sorted(status_counts.items())),
        "output_state_counts": dict(sorted(output_state_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
        "resume_requirements_order_policy": DURABLE_ADAPTER_RESUME_REQUIREMENTS_ORDER_POLICY,
        "failure_count": len(failures),
        "failures": failures,
        "all_checks_passed": not failures,
        "runtime_boundary": {
            "dependency_installs": 0,
            "dependency_imports": 0,
            "temporal_server_started": False,
            "temporal_workflows_started": 0,
            "temporal_activities_scheduled": 0,
            "inngest_service_started": False,
            "inngest_functions_registered": 0,
            "inngest_events_emitted": 0,
            "service_requests_updated": 0,
            "service_requests_assigned": 0,
            "approvals_granted": 0,
            "worker_starts": 0,
            "api_calls": False,
            "external_side_effects": False,
        },
        "results": results,
        "api_calls": False,
        "external_side_effects": False,
    }

    if result_path and not failures:
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not result_path:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(json.dumps({"ok": not failures, "path": str(result_path), "failure_count": len(failures)}, indent=2))
    if failures:
        raise SystemExit(1)

__all__ = ["dry_run_durable_service_request_reducer"]
