from __future__ import annotations

from typing import Any

"""Lifecycle service-worker integrity specs for queue, scope, assignment, pools, and gate map."""

from .constants import (
    SERVICE_WORKER_APPROVAL_REVIEW_VALIDATION_JSON,
    SERVICE_WORKER_ASSIGNMENT_PLAN_VALIDATION_JSON,
    SERVICE_WORKER_DEQUEUE_VALIDATION_JSON,
    SERVICE_WORKER_GATE_MAP_VALIDATION_JSON,
    SERVICE_WORKER_POOL_REGISTRATION_VALIDATION_JSON,
    SERVICE_WORKER_POOL_REGISTRY_VALIDATION_JSON,
    SERVICE_WORKER_READINESS_VALIDATION_JSON,
    SERVICE_WORKER_REQUEST_QUEUE_VALIDATION_JSON,
    SERVICE_WORKER_SCOPE_DIFF_VALIDATION_JSON,
    SERVICE_WORKER_SCOPE_TEMPLATE_VALIDATION_JSON,
)


def service_worker_lifecycle_integrity_specs() -> list[dict[str, Any]]:
    return [
        {
            "id": "queue",
            "label": "Request Queue",
            "path": SERVICE_WORKER_REQUEST_QUEUE_VALIDATION_JSON,
            "count_key": "validated_count",
            "expected": {
                "schema_version": "service_worker_request_queue_validation.v1",
                "validated_count": 16,
                "side_effect_flags_all_false": True,
                "service_requests_approved_by_report": 0,
                "service_requests_started_by_report": 0,
            },
        },
        {
            "id": "dequeue",
            "label": "Dequeue Plan",
            "path": SERVICE_WORKER_DEQUEUE_VALIDATION_JSON,
            "count_key": "validated_count",
            "expected": {
                "schema_version": "service_worker_dequeue_plan_validation.v1",
                "validated_count": 16,
                "result_files_written": 32,
                "service_requests_approved_by_plan": 0,
                "service_requests_started_by_plan": 0,
                "service_requests_updated_by_plan": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "readiness",
            "label": "Execution Readiness",
            "path": SERVICE_WORKER_READINESS_VALIDATION_JSON,
            "count_key": "validated_count",
            "expected": {
                "schema_version": "service_worker_execution_readiness_validation.v1",
                "validated_count": 14,
                "ready_to_start_count": 0,
                "service_requests_approved_by_report": 0,
                "service_requests_started_by_report": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "scope_diff",
            "label": "Scope Diff",
            "path": SERVICE_WORKER_SCOPE_DIFF_VALIDATION_JSON,
            "count_key": "validated_count",
            "expected": {
                "schema_version": "service_worker_approval_scope_diff_validation.v1",
                "validated_count": 14,
                "scope_compatible_count": 0,
                "service_requests_approved_by_report": 0,
                "service_requests_started_by_report": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "scope_templates",
            "label": "Scope Templates",
            "path": SERVICE_WORKER_SCOPE_TEMPLATE_VALIDATION_JSON,
            "count_key": "validated_count",
            "expected": {
                "schema_version": "service_worker_exact_scope_templates_validation.v1",
                "validated_count": 14,
                "draft_templates_written": 14,
                "templates_grant_approval": False,
                "all_templates_no_approval": True,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "approval_review",
            "label": "CRO Approval Review",
            "path": SERVICE_WORKER_APPROVAL_REVIEW_VALIDATION_JSON,
            "count_key": "reviewed_count",
            "expected": {
                "schema_version": "service_worker_cro_approval_review_validation.v1",
                "reviewed_count": 14,
                "review_candidate_count": 11,
                "approval_granted_by_review": False,
                "all_reviews_no_approval": True,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "assignment_plan",
            "label": "Assignment Plan",
            "path": SERVICE_WORKER_ASSIGNMENT_PLAN_VALIDATION_JSON,
            "count_key": "planned_count",
            "expected": {
                "schema_version": "service_worker_assignment_plan_validation.v1",
                "planned_count": 14,
                "assignable_now_count": 0,
                "service_requests_assigned_by_plan": 0,
                "all_plans_no_assignment": True,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "pool_registry",
            "label": "Pool Registry",
            "path": SERVICE_WORKER_POOL_REGISTRY_VALIDATION_JSON,
            "count_key": "pool_count",
            "expected": {
                "schema_version": "service_worker_pool_registry_validation.v1",
                "pool_count": 7,
                "missing_pool_count": 7,
                "all_registry_rows_no_assignment": True,
                "service_requests_assigned_by_registry": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "pool_registration",
            "label": "Pool Registration Plan",
            "path": SERVICE_WORKER_POOL_REGISTRATION_VALIDATION_JSON,
            "count_key": "registration_packet_count",
            "expected": {
                "schema_version": "service_worker_pool_registration_plan_validation.v1",
                "registration_packet_count": 7,
                "register_command_preview_count": 7,
                "all_plans_no_registration": True,
                "pools_registered_by_plan": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "gate_map",
            "label": "Gate Map",
            "path": SERVICE_WORKER_GATE_MAP_VALIDATION_JSON,
            "count_key": "mapped_count",
            "expected": {
                "schema_version": "service_worker_gate_map_validation.v1",
                "mapped_count": 16,
                "ready_for_assignment_count": 0,
                "gate_counts": {
                    "human_cro_approval_required": 13,
                    "terminal_no_execution": 3,
                },
                "all_rows_no_approval": True,
                "all_rows_no_registration": True,
                "all_rows_no_assignment": True,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
    ]


__all__ = ["service_worker_lifecycle_integrity_specs"]
