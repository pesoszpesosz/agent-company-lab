from __future__ import annotations

from typing import Any

"""
Durable runtime human approval and decision-intake integrity specs.
"""

from .constants import (
    DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_VALIDATION_JSON,
    DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_VALIDATION_JSON,
)


def durable_human_decision_integrity_specs() -> list[dict[str, Any]]:
    return [
        {
            "id": "durable_runtime_human_approval_packet",
            "label": "Durable Runtime Human Approval Packet",
            "path": DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_VALIDATION_JSON,
            "count_key": "approval_question_count",
            "expected": {
                "schema_version": "temporal_inngest_adapter_runtime_human_approval_packet_validation.v1",
                "approval_question_count": 6,
                "approval_packet_ready_for_human_review": True,
                "approval_required_for_runtime_implementation": True,
                "approval_granted_by_packet": False,
                "runtime_implementation_allowed": False,
                "runtime_code_write_allowed": False,
                "report_only_scaffolding_allowed": True,
                "materialized_artifact_count": 5,
                "artifact_traceability_count": 5,
                "all_materialized_artifacts_traceable": True,
                "all_materialized_artifacts_report_only": True,
                "executable_artifact_count": 0,
                "runtime_artifact_count": 0,
                "runtime_side_effect_artifact_count": 0,
                "forbidden_runtime_import_count": 0,
                "no_forbidden_runtime_imports_detected": True,
                "model_api_gate_remains_parked": True,
                "model_api_pool_registered": False,
                "all_checks_passed": True,
                "failure_count": 0,
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
            },
        },
        {
            "id": "durable_runtime_human_decision_intake_packet",
            "label": "Durable Runtime Human Decision Intake Packet",
            "path": DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_VALIDATION_JSON,
            "count_key": "decision_field_count",
            "expected": {
                "schema_version": "temporal_inngest_adapter_runtime_human_decision_intake_packet_validation.v1",
                "decision_field_count": 12,
                "approval_question_count": 6,
                "source_approval_packet_loaded": True,
                "source_approval_packet_validation_loaded": True,
                "source_approval_packet_validation_passed": True,
                "decision_packet_ready_for_human_review": True,
                "approval_granted_by_intake_packet": False,
                "runtime_implementation_allowed": False,
                "runtime_code_write_allowed": False,
                "requires_explicit_signed_decision": True,
                "requires_all_questions_answered": True,
                "requires_scope_expiration": True,
                "requires_budget_cap": True,
                "requires_artifact_output_path": True,
                "requires_rollback_plan": True,
                "requires_no_external_side_effects_default": True,
                "model_api_gate_remains_parked": True,
                "model_api_pool_registered": False,
                "all_checks_passed": True,
                "failure_count": 0,
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
            },
        },
    ]


__all__ = ["durable_human_decision_integrity_specs"]
