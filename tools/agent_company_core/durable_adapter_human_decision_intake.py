from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Human approval and human decision intake packets for durable runtime work."""

from .constants import (
    DURABLE_ORCHESTRATION_DIR,
    DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_JSON,
    DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_REPORT,
    DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_VALIDATION_JSON,
    DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_JSON,
    DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_REPORT,
    DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_VALIDATION_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_VALIDATION_JSON,
)
from .io import now_utc
from .service_workers import db_scalar, load_report_json_or_error
from .durable_adapter_runtime_contract import (
    forbidden_runtime_imports_in_source,
)


def write_durable_adapter_runtime_human_decision_intake_packet(
    conn: sqlite3.Connection, args: argparse.Namespace
) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_JSON
    validation_path = (
        Path(args.validation_path)
        if args.validation_path
        else DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_VALIDATION_JSON
    )
    approval_packet_path = (
        Path(args.approval_packet_path)
        if args.approval_packet_path
        else DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_JSON
    )
    approval_validation_path = (
        Path(args.approval_validation_path)
        if args.approval_validation_path
        else DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_VALIDATION_JSON
    )
    generated_utc = now_utc()
    failures: list[str] = []

    approval_packet, approval_packet_errors = load_report_json_or_error(approval_packet_path)
    approval_validation, approval_validation_errors = load_report_json_or_error(approval_validation_path)
    failures.extend(approval_packet_errors + approval_validation_errors)
    source_approval_packet_loaded = approval_packet is not None
    source_approval_packet_validation_loaded = approval_validation is not None
    source_approval_packet_validation_passed = bool(
        approval_validation
        and approval_validation.get("schema_version")
        == "temporal_inngest_adapter_runtime_human_approval_packet_validation.v1"
        and approval_validation.get("all_checks_passed") is True
        and approval_validation.get("failure_count") == 0
        and approval_validation.get("approval_packet_ready_for_human_review") is True
        and approval_validation.get("approval_granted_by_packet") is False
        and approval_validation.get("runtime_implementation_allowed") is False
        and approval_validation.get("runtime_code_write_allowed") is False
    )
    if approval_validation and not source_approval_packet_validation_passed:
        failures.append("source human approval packet validation is not passing or no longer deny-by-default")

    approval_questions = approval_packet.get("approval_questions", []) if approval_packet else []
    if source_approval_packet_loaded and not isinstance(approval_questions, list):
        failures.append("source human approval packet field approval_questions is not a list")
        approval_questions = []
    approval_question_count = len(approval_questions)
    if approval_question_count != 6:
        failures.append(f"expected 6 source approval questions, got {approval_question_count}")

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
    if not model_api_gate_remains_parked:
        failures.append("model/API service request is no longer parked exactly as expected")
    if model_api_pool_registered:
        failures.append("model/API worker pool is registered unexpectedly")

    required_decision_fields = [
        {
            "field_id": "decision_id",
            "required": True,
            "default": "",
            "purpose": "Stable human decision identifier for audit traceability.",
        },
        {
            "field_id": "decision",
            "required": True,
            "default": "deny",
            "allowed_values": ["deny", "approve_limited_runtime_implementation"],
            "purpose": "Explicitly deny or approve a limited implementation scope.",
        },
        {
            "field_id": "approver",
            "required": True,
            "default": "",
            "purpose": "Human approver identity or handle.",
        },
        {
            "field_id": "signed_utc",
            "required": True,
            "default": "",
            "purpose": "UTC timestamp when the human decision was made.",
        },
        {
            "field_id": "expires_utc",
            "required": True,
            "default": "",
            "purpose": "Expiry timestamp for any approval scope.",
        },
        {
            "field_id": "approved_question_ids",
            "required": True,
            "default": [],
            "purpose": "Exact approval question IDs granted by the decision.",
        },
        {
            "field_id": "denied_question_ids",
            "required": True,
            "default": [question.get("question_id") for question in approval_questions],
            "purpose": "Exact approval question IDs denied or still parked.",
        },
        {
            "field_id": "provider_model_and_cost_cap",
            "required": True,
            "default": "none",
            "purpose": "Provider, model, max cost, and data scope if model/API work is approved.",
        },
        {
            "field_id": "artifact_output_path",
            "required": True,
            "default": "",
            "purpose": "Allowed local output artifact path for implementation or runtime evidence.",
        },
        {
            "field_id": "allowed_runtime_side_effects",
            "required": True,
            "default": [],
            "purpose": "Exact runtime side effects allowed; empty means none.",
        },
        {
            "field_id": "rollback_plan",
            "required": True,
            "default": "",
            "purpose": "How to stop/revert any approved runtime work.",
        },
        {
            "field_id": "human_notes",
            "required": False,
            "default": "",
            "purpose": "Optional human rationale or constraints.",
        },
    ]
    decision_field_count = len(required_decision_fields)
    if decision_field_count != 12:
        failures.append(f"expected 12 decision fields, got {decision_field_count}")

    runtime_boundary = {
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
    }
    approval_granted_by_intake_packet = False
    runtime_implementation_allowed = False
    runtime_code_write_allowed = False
    requires_explicit_signed_decision = True
    requires_all_questions_answered = True
    requires_scope_expiration = True
    requires_budget_cap = True
    requires_artifact_output_path = True
    requires_rollback_plan = True
    requires_no_external_side_effects_default = True
    decision_packet_ready_for_human_review = bool(not failures)

    payload = {
        "schema_version": "temporal_inngest_adapter_runtime_human_decision_intake_packet.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Human decision intake packet for a future Temporal/Inngest runtime adapter approval decision; this packet records required fields but grants no approval.",
        "source_approval_packet_path": str(approval_packet_path),
        "source_approval_packet_validation_path": str(approval_validation_path),
        "approval_question_count": approval_question_count,
        "approval_questions": approval_questions,
        "decision_field_count": decision_field_count,
        "required_decision_fields": required_decision_fields,
        "decision_packet_ready_for_human_review": decision_packet_ready_for_human_review,
        "approval_granted_by_intake_packet": approval_granted_by_intake_packet,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "requires_explicit_signed_decision": requires_explicit_signed_decision,
        "requires_all_questions_answered": requires_all_questions_answered,
        "requires_scope_expiration": requires_scope_expiration,
        "requires_budget_cap": requires_budget_cap,
        "requires_artifact_output_path": requires_artifact_output_path,
        "requires_rollback_plan": requires_rollback_plan,
        "requires_no_external_side_effects_default": requires_no_external_side_effects_default,
        "model_api_request": model_request,
        "model_api_pool_registered": model_api_pool_registered,
        "runtime_boundary": runtime_boundary,
        "next_action": "Human may fill this decision intake packet, but executable runtime code remains blocked until an explicit signed approval artifact exists and is validated.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_runtime_human_decision_intake_packet_validation.v1",
        "generated_utc": generated_utc,
        "decision_intake_packet_path": str(json_output_path),
        "decision_field_count": decision_field_count,
        "approval_question_count": approval_question_count,
        "source_approval_packet_loaded": source_approval_packet_loaded,
        "source_approval_packet_validation_loaded": source_approval_packet_validation_loaded,
        "source_approval_packet_validation_passed": source_approval_packet_validation_passed,
        "decision_packet_ready_for_human_review": decision_packet_ready_for_human_review,
        "approval_granted_by_intake_packet": approval_granted_by_intake_packet,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "requires_explicit_signed_decision": requires_explicit_signed_decision,
        "requires_all_questions_answered": requires_all_questions_answered,
        "requires_scope_expiration": requires_scope_expiration,
        "requires_budget_cap": requires_budget_cap,
        "requires_artifact_output_path": requires_artifact_output_path,
        "requires_rollback_plan": requires_rollback_plan,
        "requires_no_external_side_effects_default": requires_no_external_side_effects_default,
        "model_api_gate_remains_parked": model_api_gate_remains_parked,
        "model_api_pool_registered": model_api_pool_registered,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Temporal/Inngest Runtime Human Decision Intake Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision Status",
        "",
        "This packet is an intake form for a future human decision. It does not grant approval and does not permit runtime implementation, executable adapter code, dependency installation, runtime imports, worker starts, service-request mutation, model/API use, or external side effects.",
        "",
        "## Required Fields",
        "",
        "| Field | Required | Default |",
        "| --- | --- | --- |",
    ]
    for field in required_decision_fields:
        lines.append(f"| `{field['field_id']}` | `{field['required']}` | `{field['default']}` |")
    lines.extend(
        [
            "",
            "## Source Approval Questions",
            "",
            "| Question | Current Default |",
            "| --- | --- |",
        ]
    )
    for question in approval_questions:
        lines.append(f"| `{question.get('question_id')}` - {question.get('question')} | `{question.get('current_default')}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            f"- Approval granted by intake packet: `{approval_granted_by_intake_packet}`",
            f"- Runtime implementation allowed: `{runtime_implementation_allowed}`",
            f"- Runtime code write allowed: `{runtime_code_write_allowed}`",
            f"- Model/API gate remains parked: `{model_api_gate_remains_parked}`",
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
            "A human may fill a separate signed decision artifact. Runtime implementation remains blocked until that artifact exists, validates, and is explicitly in scope.",
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
                "decision_field_count": decision_field_count,
                "approval_question_count": approval_question_count,
                "approval_granted_by_intake_packet": approval_granted_by_intake_packet,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
