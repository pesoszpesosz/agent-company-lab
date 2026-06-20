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


def write_durable_adapter_runtime_human_approval_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_JSON
    validation_path = (
        Path(args.validation_path)
        if args.validation_path
        else DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_VALIDATION_JSON
    )
    manifest_path = (
        Path(args.scaffolding_artifacts_path)
        if args.scaffolding_artifacts_path
        else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_JSON
    )
    manifest_validation_path = (
        Path(args.scaffolding_artifacts_validation_path)
        if args.scaffolding_artifacts_validation_path
        else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_VALIDATION_JSON
    )
    generated_utc = now_utc()
    failures: list[str] = []

    manifest_payload, manifest_errors = load_report_json_or_error(manifest_path)
    manifest_validation, manifest_validation_errors = load_report_json_or_error(manifest_validation_path)
    failures.extend(manifest_errors + manifest_validation_errors)
    manifest_validation_passed = bool(
        manifest_validation
        and manifest_validation.get("schema_version")
        == "temporal_inngest_adapter_runtime_report_only_scaffolding_artifacts_validation.v1"
        and manifest_validation.get("all_checks_passed") is True
        and manifest_validation.get("failure_count") == 0
    )
    if manifest_validation and not manifest_validation_passed:
        failures.append("materialized scaffolding artifacts validation is not passing")

    materialized_artifacts = manifest_payload.get("materialized_artifacts", []) if manifest_payload else []
    if manifest_payload and not isinstance(materialized_artifacts, list):
        failures.append("scaffolding artifacts manifest field materialized_artifacts is not a list")
        materialized_artifacts = []

    traceability_rows: list[dict[str, Any]] = []
    for artifact in materialized_artifacts:
        path = artifact.get("path")
        rows = [
            dict(row)
            for row in conn.execute(
                """
                SELECT artifact_id, kind, task_id, path_or_url, sha256
                FROM artifacts
                WHERE path_or_url = ?
                ORDER BY artifact_id
                """,
                (path,),
            )
        ]
        matching_sha = any(row.get("sha256") == artifact.get("sha256") for row in rows)
        if not rows:
            failures.append(f"materialized artifact is not registered in artifact traceability: {path}")
        if rows and not matching_sha:
            failures.append(f"materialized artifact traceability row has unexpected hash: {path}")
        traceability_rows.append(
            {
                "component_id": artifact.get("component_id"),
                "path": path,
                "expected_sha256": artifact.get("sha256"),
                "registered": bool(rows),
                "matching_sha256": matching_sha,
                "artifact_rows": rows,
            }
        )

    materialized_artifact_count = len(materialized_artifacts)
    artifact_traceability_count = sum(1 for row in traceability_rows if row["registered"] and row["matching_sha256"])
    all_materialized_artifacts_traceable = bool(
        materialized_artifact_count == 5 and artifact_traceability_count == materialized_artifact_count
    )
    all_materialized_artifacts_report_only = bool(
        manifest_validation and manifest_validation.get("all_materialized_artifacts_report_only") is True
    )
    executable_artifact_count = manifest_validation.get("executable_artifact_count") if manifest_validation else None
    runtime_artifact_count = manifest_validation.get("runtime_artifact_count") if manifest_validation else None
    runtime_side_effect_artifact_count = (
        manifest_validation.get("runtime_side_effect_artifact_count") if manifest_validation else None
    )
    runtime_implementation_allowed = bool(
        manifest_validation and manifest_validation.get("runtime_implementation_allowed") is True
    )
    runtime_code_write_allowed = bool(manifest_validation and manifest_validation.get("runtime_code_write_allowed") is True)
    report_only_scaffolding_allowed = bool(
        manifest_validation and manifest_validation.get("report_only_scaffolding_allowed") is True
    )
    if materialized_artifact_count != 5:
        failures.append(f"expected 5 materialized artifacts, got {materialized_artifact_count}")
    if not all_materialized_artifacts_traceable:
        failures.append(
            f"expected 5 traceable materialized artifacts, got {artifact_traceability_count}/{materialized_artifact_count}"
        )
    if executable_artifact_count != 0:
        failures.append(f"expected 0 executable artifacts, got {executable_artifact_count}")
    if runtime_artifact_count != 0:
        failures.append(f"expected 0 runtime artifacts, got {runtime_artifact_count}")
    if runtime_side_effect_artifact_count != 0:
        failures.append(f"expected 0 runtime side-effect artifacts, got {runtime_side_effect_artifact_count}")
    if runtime_implementation_allowed:
        failures.append("runtime implementation is unexpectedly allowed")
    if runtime_code_write_allowed:
        failures.append("runtime code writing is unexpectedly allowed")
    if not report_only_scaffolding_allowed:
        failures.append("report-only scaffolding is not allowed")

    forbidden_imports = forbidden_runtime_imports_in_source()
    if forbidden_imports:
        failures.append(f"forbidden runtime imports detected in source: {len(forbidden_imports)}")

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

    approval_questions = [
        {
            "question_id": "approve_dependency_install_scope",
            "question": "Should dependency installation for Temporal/Inngest adapter implementation be allowed?",
            "current_default": "no",
        },
        {
            "question_id": "approve_runtime_import_scope",
            "question": "Should importing Temporal/Inngest runtime libraries be allowed?",
            "current_default": "no",
        },
        {
            "question_id": "approve_runtime_start_scope",
            "question": "Should starting Temporal/Inngest runtimes, workflows, activities, or event emitters be allowed?",
            "current_default": "no",
        },
        {
            "question_id": "approve_service_request_mutation_scope",
            "question": "Should service request assignment or mutation be allowed from adapter code?",
            "current_default": "no",
        },
        {
            "question_id": "approve_model_api_scope",
            "question": "Should the parked model/API adapter request be assigned or used?",
            "current_default": "no",
        },
        {
            "question_id": "approve_external_side_effect_scope",
            "question": "Should any browser, account, payment, wallet, security-test, or public submission action be allowed?",
            "current_default": "no",
        },
    ]
    approval_question_count = len(approval_questions)
    approval_packet_ready_for_human_review = bool(not failures)
    approval_required_for_runtime_implementation = True
    approval_granted_by_packet = False

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
    payload = {
        "schema_version": "temporal_inngest_adapter_runtime_human_approval_packet.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Human-readable approval packet for future Temporal/Inngest runtime adapter work; this packet does not grant approval.",
        "materialized_artifacts_path": str(manifest_path),
        "materialized_artifacts_validation_path": str(manifest_validation_path),
        "approval_question_count": approval_question_count,
        "approval_questions": approval_questions,
        "traceability_rows": traceability_rows,
        "approval_packet_ready_for_human_review": approval_packet_ready_for_human_review,
        "approval_required_for_runtime_implementation": approval_required_for_runtime_implementation,
        "approval_granted_by_packet": approval_granted_by_packet,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
        "model_api_request": model_request,
        "model_api_pool_registered": model_api_pool_registered,
        "runtime_boundary": runtime_boundary,
        "next_action": "Wait for an explicit human runtime-implementation approval decision packet before writing executable adapter code.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_runtime_human_approval_packet_validation.v1",
        "generated_utc": generated_utc,
        "approval_packet_path": str(json_output_path),
        "approval_question_count": approval_question_count,
        "approval_packet_ready_for_human_review": approval_packet_ready_for_human_review,
        "approval_required_for_runtime_implementation": approval_required_for_runtime_implementation,
        "approval_granted_by_packet": approval_granted_by_packet,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
        "materialized_artifact_count": materialized_artifact_count,
        "artifact_traceability_count": artifact_traceability_count,
        "all_materialized_artifacts_traceable": all_materialized_artifacts_traceable,
        "all_materialized_artifacts_report_only": all_materialized_artifacts_report_only,
        "executable_artifact_count": executable_artifact_count,
        "runtime_artifact_count": runtime_artifact_count,
        "runtime_side_effect_artifact_count": runtime_side_effect_artifact_count,
        "forbidden_runtime_import_count": len(forbidden_imports),
        "no_forbidden_runtime_imports_detected": len(forbidden_imports) == 0,
        "model_api_gate_remains_parked": model_api_gate_remains_parked,
        "model_api_pool_registered": model_api_pool_registered,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Temporal/Inngest Runtime Human Approval Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        "This packet is ready for human review, but it does not grant approval. Runtime implementation, executable adapter code, dependency installs, runtime imports, workflow starts, event emissions, service-request mutations, worker starts, API calls, and external side effects remain blocked.",
        "",
        "## Traceability",
        "",
        f"- Materialized artifacts: `{materialized_artifact_count}`",
        f"- Traceable materialized artifacts: `{artifact_traceability_count}`",
        f"- All materialized artifacts traceable: `{all_materialized_artifacts_traceable}`",
        f"- All materialized artifacts report-only: `{all_materialized_artifacts_report_only}`",
        "",
        "## Approval Questions",
        "",
        "| Question | Current Default |",
        "| --- | --- |",
    ]
    for question in approval_questions:
        lines.append(f"| `{question['question_id']}` - {question['question']} | `{question['current_default']}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            f"- Approval granted by packet: `{approval_granted_by_packet}`",
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
            "Wait for an explicit human runtime-implementation approval decision packet before writing executable adapter code.",
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
                "approval_question_count": approval_question_count,
                "artifact_traceability_count": artifact_traceability_count,
                "approval_granted_by_packet": approval_granted_by_packet,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
