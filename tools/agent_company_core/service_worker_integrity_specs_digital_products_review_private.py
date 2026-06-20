from __future__ import annotations

from typing import Any

"""Private-review digital-product integrity specs."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_PACKET_VALIDATION_JSON,
)


def digital_product_review_private_integrity_specs() -> list[dict[str, Any]]:
    return [
        {
            "id": "digital_products_local_private_review_packet",
            "label": "Digital Products Local Private Review Packet",
            "path": DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_PACKET_VALIDATION_JSON,
            "count_key": "review_artifact_count",
            "expected": {
                "schema_version": "agent_company.digital_products_local_private_review_packet_validation.v1",
                "packet_lane_id": "digital_products_templates_plugins",
                "packet_task_id": "task-digital-products-local-private-review-packet-20260616",
                "source_check_task_id": "task-digital-products-local-completeness-check-20260616",
                "source_check_evidence_id": "digital-products-local-completeness-check-20260616",
                "selected_candidate_id": "ai-builder-launch-checklist-pack",
                "review_artifact_count": 10,
                "review_question_count": 8,
                "decision_option_count": 4,
                "blocked_by_gate_count": 4,
                "local_decision": "private_review_packet_ready_no_public_or_payment_action",
                "live_tasks_created": 1,
                "live_tasks_completed": 1,
                "tasks_table_rows_before": 168,
                "tasks_table_rows_after": 169,
                "task_rows_inserted_by_packet": 1,
                "lane_evidence_rows_before": 85,
                "lane_evidence_rows_after": 86,
                "evidence_rows_inserted_or_updated": 1,
                "all_checks_passed": True,
                "failure_count": 0,
                "browser_sessions_started": 0,
                "account_actions": False,
                "wallet_actions": False,
                "payment_actions": False,
                "public_actions": False,
                "security_testing_actions": False,
                "real_money_actions": False,
                "service_requests_updated": 0,
                "service_requests_assigned": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "digital_products_local_private_review_decision",
            "label": "Digital Products Local Private Review Decision",
            "path": DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_VALIDATION_JSON,
            "count_key": "review_answer_count",
            "expected": {
                "schema_version": "agent_company.digital_products_local_private_review_decision_validation.v1",
                "decision_lane_id": "digital_products_templates_plugins",
                "decision_task_id": "task-digital-products-local-private-review-decision-20260616",
                "source_packet_task_id": "task-digital-products-local-private-review-packet-20260616",
                "source_packet_evidence_id": "digital-products-local-private-review-packet-20260616",
                "selected_candidate_id": "ai-builder-launch-checklist-pack",
                "selected_decision_id": "continue-local",
                "review_answer_count": 8,
                "revision_item_count": 6,
                "blocked_by_gate_count": 4,
                "local_decision": "continue_local_revision_queue_no_external_validation",
                "live_tasks_created": 1,
                "live_tasks_completed": 1,
                "tasks_table_rows_before": 170,
                "tasks_table_rows_after": 171,
                "task_rows_inserted_by_decision": 1,
                "lane_evidence_rows_before": 86,
                "lane_evidence_rows_after": 87,
                "evidence_rows_inserted_or_updated": 1,
                "all_checks_passed": True,
                "failure_count": 0,
                "browser_sessions_started": 0,
                "account_actions": False,
                "wallet_actions": False,
                "payment_actions": False,
                "public_actions": False,
                "security_testing_actions": False,
                "real_money_actions": False,
                "service_requests_updated": 0,
                "service_requests_assigned": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
    ]


__all__ = ["digital_product_review_private_integrity_specs"]
