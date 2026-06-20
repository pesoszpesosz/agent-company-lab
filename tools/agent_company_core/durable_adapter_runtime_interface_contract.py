from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Service-worker integration and runtime interface contract reports."""

from .constants import (
    DURABLE_ADAPTER_REDUCER_RESULT_JSON,
    DURABLE_ADAPTER_RUNTIME_READINESS_VALIDATION_JSON,
    DURABLE_ORCHESTRATION_DIR,
    DURABLE_RUNTIME_INTERFACE_CONTRACT_JSON,
    DURABLE_RUNTIME_INTERFACE_CONTRACT_REPORT,
    DURABLE_RUNTIME_INTERFACE_CONTRACT_VALIDATION_JSON,
    DURABLE_SERVICE_WORKER_INTEGRATION_JSON,
    DURABLE_SERVICE_WORKER_INTEGRATION_REPORT,
    DURABLE_SERVICE_WORKER_INTEGRATION_VALIDATION_JSON,
    SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_PREFLIGHT_VALIDATION_JSON,
    SERVICE_WORKER_HUMAN_DECISION_PACKETS_VALIDATION_JSON,
    SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_VALIDATION_JSON,
)
from .io import now_utc
from .paths import ROOT
from .service_workers import db_scalar, load_report_json_or_error, service_worker_chain_db_snapshot


from .durable_adapter_runtime_import_guard import forbidden_runtime_imports_in_source

def write_durable_adapter_runtime_interface_contract(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_RUNTIME_INTERFACE_CONTRACT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_RUNTIME_INTERFACE_CONTRACT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DURABLE_RUNTIME_INTERFACE_CONTRACT_VALIDATION_JSON
    reducer_result_path = Path(args.reducer_result_path) if args.reducer_result_path else DURABLE_ADAPTER_REDUCER_RESULT_JSON
    integration_validation_path = (
        Path(args.integration_validation_path)
        if args.integration_validation_path
        else DURABLE_SERVICE_WORKER_INTEGRATION_VALIDATION_JSON
    )
    readiness_validation_path = (
        Path(args.readiness_validation_path)
        if args.readiness_validation_path
        else DURABLE_ADAPTER_RUNTIME_READINESS_VALIDATION_JSON
    )
    generated_utc = now_utc()

    reducer_payload, reducer_errors = load_report_json_or_error(reducer_result_path)
    integration_payload, integration_errors = load_report_json_or_error(integration_validation_path)
    readiness_payload, readiness_errors = load_report_json_or_error(readiness_validation_path)
    failures = reducer_errors + integration_errors + readiness_errors
    reducer_results = reducer_payload.get("results", []) if reducer_payload else []
    if reducer_payload and not isinstance(reducer_results, list):
        failures.append("reducer result payload field results is not a list")
        reducer_results = []

    parked_rows = [row for row in reducer_results if isinstance(row, dict) and row.get("output_state") == "parked.awaiting_human_review"]
    terminal_rows = [
        row
        for row in reducer_results
        if isinstance(row, dict)
        and row.get("output_state")
        in {"terminal.completed_from_ledger_snapshot", "terminal.rejected_from_ledger_snapshot"}
    ]
    forbidden_imports = forbidden_runtime_imports_in_source()
    model_row = conn.execute(
        """
        SELECT request_id, status, assigned_agent_id, started_at, completed_at, decision_note
        FROM service_requests
        WHERE request_id = ?
        """,
        ("req-pydantic-ai-model-backed-adapter-20260614",),
    ).fetchone()
    model_request = dict(model_row) if model_row else None
    model_api_pool_registered = bool(
        db_scalar(conn, "SELECT COUNT(*) FROM agents WHERE agent_id = ?", ("service-worker-model-api-execution-pool",))
    )
    model_api_gate_remains_parked = bool(
        model_request
        and model_request.get("status") == "needs_review"
        and model_request.get("assigned_agent_id") is None
        and model_request.get("started_at") is None
        and model_request.get("completed_at") is None
        and model_request.get("decision_note") is None
    )

    if len(reducer_results) != 14:
        failures.append(f"expected 14 reducer results, got {len(reducer_results)}")
    if len(parked_rows) != 11:
        failures.append(f"expected 11 parked reducer rows, got {len(parked_rows)}")
    if len(terminal_rows) != 3:
        failures.append(f"expected 3 terminal reducer rows, got {len(terminal_rows)}")
    if integration_payload and integration_payload.get("all_checks_passed") is not True:
        failures.append("durable service-worker integration validation is not passing")
    if readiness_payload and readiness_payload.get("all_checks_passed") is not True:
        failures.append("runtime readiness validation is not passing")
    if readiness_payload and readiness_payload.get("checks", {}).get("external_runtime_implementation_allowed_now") is not False:
        failures.append("runtime readiness does not block external runtime implementation")
    if forbidden_imports:
        failures.append(f"forbidden runtime imports detected: {len(forbidden_imports)}")
    if not model_api_gate_remains_parked:
        failures.append("model/API service request is no longer parked exactly as expected")
    if model_api_pool_registered:
        failures.append("model/API worker pool is registered unexpectedly")

    interface_contracts = [
        {
            "contract_id": "temporal_workflow_identity_preview",
            "runtime": "temporal",
            "defined_not_started": True,
            "workflow_type": "ServiceRequestLifecycleWorkflow",
            "workflow_id_template": "agent-company/service-request/{request_id}",
            "source_fields": ["request_id"],
            "start_allowed": False,
            "schedule_activity_allowed": False,
            "reason_blocked": "external runtime start requires explicit approval",
        },
        {
            "contract_id": "inngest_event_identity_preview",
            "runtime": "inngest",
            "defined_not_emitted": True,
            "event_name_template": "agent_company/service_request.{status_event}",
            "idempotency_key_template": "service-request-event:{request_id}:{event_name}:{status_snapshot}:{risk_gate}",
            "source_fields": ["request_id", "event_name", "status_snapshot", "risk_gate"],
            "event_emit_allowed": False,
            "reason_blocked": "event emission requires explicit approval",
        },
        {
            "contract_id": "reducer_to_service_worker_refresh_disposition",
            "runtime": "local_report_only",
            "defined_not_executed": True,
            "parked_state": "parked.awaiting_human_review",
            "parked_disposition": "refresh_local_review_packets_only",
            "terminal_dispositions": [
                "terminal_no_refresh_start_or_replay",
                "terminal_rejected_no_revive_or_replay",
            ],
            "service_request_mutation_allowed": False,
        },
        {
            "contract_id": "runtime_gate_enforcement",
            "runtime": "local_report_only",
            "defined_not_executed": True,
            "forbidden_until_explicit_approval": [
                "dependency install",
                "runtime import",
                "server start",
                "worker start",
                "workflow start",
                "activity schedule",
                "event emit",
                "service request assignment",
                "model API call",
                "external browser/account/payment/wallet/security action",
            ],
            "negative_import_scan_scope": str(Path(__file__)),
            "forbidden_runtime_import_count": len(forbidden_imports),
        },
    ]
    runtime_boundary = {
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
    }
    payload = {
        "schema_version": "temporal_inngest_adapter_runtime_interface_contract.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Define local-only interface contracts for future Temporal/Inngest adapter work without importing, starting, emitting, scheduling, or mutating anything.",
        "source_artifacts": {
            "reducer_result": str(reducer_result_path),
            "integration_validation": str(integration_validation_path),
            "runtime_readiness_validation": str(readiness_validation_path),
        },
        "interface_contract_count": len(interface_contracts),
        "interface_contracts": interface_contracts,
        "reducer_result_count": len(reducer_results),
        "parked_rows": len(parked_rows),
        "terminal_rows": len(terminal_rows),
        "forbidden_runtime_imports": forbidden_imports,
        "model_api_request": model_request,
        "runtime_boundary": runtime_boundary,
        "next_action": "Implement static interface-contract negative fixtures and add this generated contract validation to the orchestration readiness chain before any runtime adapter code.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_runtime_interface_contract_validation.v1",
        "generated_utc": generated_utc,
        "contract_path": str(json_output_path),
        "interface_contract_count": len(interface_contracts),
        "reducer_result_count": len(reducer_results),
        "parked_rows": len(parked_rows),
        "terminal_rows": len(terminal_rows),
        "workflow_start_allowed": False,
        "activity_schedule_allowed": False,
        "event_emit_allowed": False,
        "runtime_import_allowed": False,
        "forbidden_runtime_import_count": len(forbidden_imports),
        "no_forbidden_runtime_imports_detected": len(forbidden_imports) == 0,
        "service_request_mutation_count": 0,
        "model_api_gate_remains_parked": model_api_gate_remains_parked,
        "model_api_pool_registered": model_api_pool_registered,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        "dependency_installs": 0,
        "dependency_imports": 0,
        "temporal_server_started": False,
        "temporal_workflows_started": 0,
        "temporal_activities_scheduled": 0,
        "inngest_service_started": False,
        "inngest_events_emitted": 0,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Temporal/Inngest Runtime Interface Contract",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        "This is a local-only interface contract. It defines identifiers and mappings for future adapter work, but it does not import Temporal/Inngest, start runtimes, emit events, schedule activities, or mutate service requests.",
        "",
        "## Contract Summary",
        "",
        f"- Interface contracts: `{len(interface_contracts)}`",
        f"- Reducer rows: `{len(reducer_results)}`",
        f"- Parked rows: `{len(parked_rows)}`",
        f"- Terminal rows: `{len(terminal_rows)}`",
        f"- Forbidden runtime imports detected: `{len(forbidden_imports)}`",
        f"- Model/API gate remains parked: `{model_api_gate_remains_parked}`",
        "",
        "## Contracts",
        "",
        "| Contract | Runtime | Executed? |",
        "| --- | --- | --- |",
    ]
    for contract in interface_contracts:
        lines.append(f"| `{contract['contract_id']}` | `{contract['runtime']}` | `False` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Dependency installs: `0`",
            "- Runtime imports: `0`",
            "- Temporal workflows started: `0`",
            "- Temporal activities scheduled: `0`",
            "- Inngest events emitted: `0`",
            "- Service requests updated: `0`",
            "- Service requests assigned: `0`",
            "- Worker starts: `0`",
            "- API calls: `False`",
            "- External side effects: `False`",
            "",
            "## Next Action",
            "",
            "Implement static interface-contract negative fixtures and add this generated contract validation to the orchestration readiness chain before any runtime adapter code.",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "interface_contract_count": len(interface_contracts),
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
