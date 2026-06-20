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


def write_durable_adapter_service_worker_integration(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_SERVICE_WORKER_INTEGRATION_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_SERVICE_WORKER_INTEGRATION_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DURABLE_SERVICE_WORKER_INTEGRATION_VALIDATION_JSON
    reducer_result_path = Path(args.reducer_result_path) if args.reducer_result_path else DURABLE_ADAPTER_REDUCER_RESULT_JSON
    generated_utc = now_utc()

    reducer_payload, reducer_errors = load_report_json_or_error(reducer_result_path)
    human_payload, human_errors = load_report_json_or_error(SERVICE_WORKER_HUMAN_DECISION_PACKETS_VALIDATION_JSON)
    refresh_payload, refresh_errors = load_report_json_or_error(SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_VALIDATION_JSON)
    preflight_payload, preflight_errors = load_report_json_or_error(SERVICE_WORKER_DECISION_PREFLIGHT_VALIDATION_JSON)
    chain_payload, chain_errors = load_report_json_or_error(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON)
    failures = reducer_errors + human_errors + refresh_errors + preflight_errors + chain_errors

    reducer_results = reducer_payload.get("results", []) if reducer_payload else []
    if reducer_payload and not isinstance(reducer_results, list):
        failures.append("reducer result payload field results is not a list")
        reducer_results = []

    request_rows: list[dict[str, Any]] = []
    output_state_counts: dict[str, int] = {}
    for row in reducer_results:
        if not isinstance(row, dict):
            continue
        output_state = row.get("output_state")
        output_state_counts[str(output_state)] = output_state_counts.get(str(output_state), 0) + 1
        if output_state == "parked.awaiting_human_review":
            disposition = "refresh_local_review_packets_only"
        elif output_state == "terminal.completed_from_ledger_snapshot":
            disposition = "terminal_no_refresh_start_or_replay"
        elif output_state == "terminal.rejected_from_ledger_snapshot":
            disposition = "terminal_rejected_no_revive_or_replay"
        else:
            disposition = "unknown_output_state_blocked"
            failures.append(f"unknown reducer output_state for {row.get('request_id')}: {output_state!r}")
        request_rows.append(
            {
                "request_id": row.get("request_id"),
                "input_status": row.get("input_status"),
                "output_state": output_state,
                "worker_type": row.get("worker_type"),
                "integration_disposition": disposition,
            }
        )

    parked_count = output_state_counts.get("parked.awaiting_human_review", 0)
    terminal_completed_count = output_state_counts.get("terminal.completed_from_ledger_snapshot", 0)
    terminal_rejected_count = output_state_counts.get("terminal.rejected_from_ledger_snapshot", 0)
    human_count = human_payload.get("decision_packet_count") if human_payload else None
    refresh_count = refresh_payload.get("refresh_plan_count") if refresh_payload else None
    preflight_count = preflight_payload.get("preflight_count") if preflight_payload else None
    chain_ok = bool(chain_payload and chain_payload.get("all_checks_passed") is True)

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

    if reducer_payload and reducer_payload.get("failure_count") != 0:
        failures.append("hardened reducer result has nonzero failure_count")
    if len(reducer_results) != 14:
        failures.append(f"expected 14 reducer results, got {len(reducer_results)}")
    if parked_count != 11:
        failures.append(f"expected 11 parked reducer rows, got {parked_count}")
    if terminal_completed_count != 1:
        failures.append(f"expected 1 completed terminal reducer row, got {terminal_completed_count}")
    if terminal_rejected_count != 2:
        failures.append(f"expected 2 rejected terminal reducer rows, got {terminal_rejected_count}")
    if human_count != parked_count:
        failures.append(f"human decision packet count {human_count!r} does not match parked count {parked_count}")
    if refresh_count != parked_count:
        failures.append(f"post-decision refresh plan count {refresh_count!r} does not match parked count {parked_count}")
    if preflight_count != parked_count:
        failures.append(f"decision preflight count {preflight_count!r} does not match parked count {parked_count}")
    if not chain_ok:
        failures.append("service-worker chain integrity is not passing")
    if not model_api_gate_remains_parked:
        failures.append("model/API service request is no longer parked exactly as expected")
    if model_api_pool_registered:
        failures.append("model/API worker pool is registered unexpectedly")

    command_previews = [
        ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-gate-map"],
        ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-human-decision-packets"],
        ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-post-decision-simulation"],
        ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-post-decision-refresh-plan"],
        ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-decision-preflight"],
        ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-chain-integrity"],
    ]
    state_mapping = [
        {
            "reducer_output_state": "parked.awaiting_human_review",
            "row_count": parked_count,
            "service_request_statuses": ["needs_review"],
            "integration_disposition": "refresh_local_review_packets_only",
            "allowed_followup_command_previews": command_previews,
            "blocked_actions": [
                "approve-service-request",
                "assign-service-request",
                "start-service-request",
                "complete-service-request",
                "Temporal workflow start",
                "Temporal activity schedule",
                "Inngest event emit",
                "worker process start",
                "API call",
                "external browser/account/payment/wallet/security action",
            ],
            "resume_requirements_source": "Use reducer result resume_requirements in strict order when rendering human review packet display.",
        },
        {
            "reducer_output_state": "terminal.completed_from_ledger_snapshot",
            "row_count": terminal_completed_count,
            "service_request_statuses": ["complete"],
            "integration_disposition": "terminal_no_refresh_start_or_replay",
            "allowed_followup_command_previews": [
                ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-chain-integrity"],
            ],
            "blocked_actions": [
                "approve-service-request",
                "assign-service-request",
                "start-service-request",
                "complete-service-request",
                "Temporal workflow replay start",
                "Inngest event emit",
            ],
        },
        {
            "reducer_output_state": "terminal.rejected_from_ledger_snapshot",
            "row_count": terminal_rejected_count,
            "service_request_statuses": ["rejected"],
            "integration_disposition": "terminal_rejected_no_revive_or_replay",
            "allowed_followup_command_previews": [
                ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-chain-integrity"],
            ],
            "blocked_actions": [
                "approve-service-request",
                "assign-service-request",
                "start-service-request",
                "complete-service-request",
                "Temporal workflow replay start",
                "Inngest event emit",
            ],
        },
    ]
    runtime_boundary = {
        "commands_executed_by_this_report": 0,
        "approval_granted": False,
        "rejection_granted": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "temporal_server_started": False,
        "temporal_workflows_started": 0,
        "temporal_activities_scheduled": 0,
        "inngest_service_started": False,
        "inngest_events_emitted": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    payload = {
        "schema_version": "temporal_inngest_adapter_service_worker_refresh_integration.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Map the hardened durable reducer dry-run contract to existing service-worker decision packet refresh commands without starting external orchestration runtimes or mutating service requests.",
        "source_artifacts": {
            "hardened_reducer_result": str(reducer_result_path),
            "human_decision_packets_validation": str(SERVICE_WORKER_HUMAN_DECISION_PACKETS_VALIDATION_JSON),
            "post_decision_refresh_plan_validation": str(SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_VALIDATION_JSON),
            "decision_preflight_validation": str(SERVICE_WORKER_DECISION_PREFLIGHT_VALIDATION_JSON),
            "chain_integrity_validation": str(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON),
        },
        "current_state": {
            "reducer_result_count": len(reducer_results),
            "reducer_failure_count": reducer_payload.get("failure_count") if reducer_payload else None,
            "reducer_output_state_counts": dict(sorted(output_state_counts.items())),
            "human_decision_packet_count": human_count,
            "post_decision_refresh_plan_count": refresh_count,
            "decision_preflight_count": preflight_count,
            "chain_integrity_checked_report_count": chain_payload.get("checked_report_count") if chain_payload else None,
            "chain_integrity_failure_count": chain_payload.get("failure_count") if chain_payload else None,
            "resume_requirements_order_policy": reducer_payload.get("resume_requirements_order_policy") if reducer_payload else None,
        },
        "state_mapping": state_mapping,
        "request_rows": request_rows,
        "adapter_integration_contract": {
            "authority": "SQLite service_requests ledger remains authoritative; reducer output is a deterministic preview and must not mutate authority state.",
            "idempotency": "Reducer idempotency keys remain preview keys. Report refresh commands may be rerun, but they do not grant approvals or start workers.",
            "human_review_packet_refresh": "Only parked.awaiting_human_review rows are eligible for local packet refresh.",
            "terminal_row_policy": "Completed and rejected rows are terminal evidence rows and must not be revived, replay-started, or converted into review packets by orchestration adapters.",
            "external_runtime_policy": "Temporal and Inngest integration remains manifest/report-only until a separate explicit runtime approval exists.",
            "model_api_gate_policy": "req-pydantic-ai-model-backed-adapter-20260614 remains parked until provider, model, cost, credential route, scope, and worker pool are approved.",
        },
        "runtime_boundary": runtime_boundary,
        "next_action": "Add generated durable integration validation to the refreshed chain-integrity report, then use the report-only integration command before any future orchestration adapter work.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_service_worker_refresh_integration_validation.v1",
        "generated_utc": generated_utc,
        "integration_map_path": str(json_output_path),
        "reducer_result_count": len(reducer_results),
        "parked_rows_mapped_to_review_refresh": parked_count,
        "terminal_completed_rows_mapped_to_no_replay": terminal_completed_count,
        "terminal_rejected_rows_mapped_to_no_revive": terminal_rejected_count,
        "human_decision_packet_count_matches_parked_rows": human_count == parked_count,
        "post_decision_refresh_plan_count_matches_parked_rows": refresh_count == parked_count,
        "decision_preflight_count_matches_parked_rows": preflight_count == parked_count,
        "chain_integrity_all_checks_passed": chain_ok,
        "model_api_gate_remains_parked": model_api_gate_remains_parked,
        "model_api_pool_registered": model_api_pool_registered,
        "no_external_runtime_started": True,
        "no_actions_granted": True,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        "approval_granted": False,
        "rejection_granted": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "service_requests_by_status": service_worker_chain_db_snapshot(conn)["service_status_counts"],
        "model_api_request": model_request,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Durable Adapter To Service-Worker Refresh Integration",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Scope",
        "",
        "This report maps the hardened durable reducer dry-run output to existing service-worker packet refresh commands. It is local-only and report-only.",
        "",
        "## Current Counts",
        "",
        f"- Reducer rows: `{len(reducer_results)}`",
        f"- Parked rows: `{parked_count}`",
        f"- Terminal completed rows: `{terminal_completed_count}`",
        f"- Terminal rejected rows: `{terminal_rejected_count}`",
        f"- Human decision packets: `{human_count}`",
        f"- Post-decision refresh plans: `{refresh_count}`",
        f"- Decision preflight rows: `{preflight_count}`",
        f"- Chain integrity currently passing: `{chain_ok}`",
        "",
        "## Mapping",
        "",
        "| Reducer State | Rows | Disposition |",
        "| --- | ---: | --- |",
    ]
    for mapping in state_mapping:
        lines.append(
            f"| `{mapping['reducer_output_state']}` | `{mapping['row_count']}` | `{mapping['integration_disposition']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- SQLite `service_requests` remains the authority.",
            "- Reducer output is a deterministic preview.",
            "- `resume_requirements` order is semantic for review packet display.",
            "- Model/API execution remains parked until provider, model, cost, credential route, artifact scope, and worker pool are approved.",
            "- Temporal/Inngest integration remains manifest/report-only until an explicit runtime approval exists.",
            "",
            "## Runtime Effects",
            "",
            "- Approvals granted: `False`",
            "- Service requests assigned: `0`",
            "- Service requests updated: `0`",
            "- Worker starts: `0`",
            "- API calls: `False`",
            "- External side effects: `False`",
            "",
            "## Next Action",
            "",
            "Add generated durable integration validation to the refreshed chain-integrity report, then use the report-only integration command before any future orchestration adapter work.",
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
                "reducer_result_count": len(reducer_results),
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
