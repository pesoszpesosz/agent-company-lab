from __future__ import annotations

from typing import Any

"""Gate-decision digital-product integrity specs."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_VALIDATION_JSON,
)


def digital_product_review_gate_integrity_specs() -> list[dict[str, Any]]:
    return [
        {
            "id": "digital_products_local_gate_decision_packet",
            "label": "Digital Products Local Gate Decision Packet",
            "path": DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_VALIDATION_JSON,
            "count_key": "gate_option_count",
            "expected": {
                "schema_version": "agent_company.digital_products_local_gate_decision_packet_validation.v1",
                "packet_lane_id": "digital_products_templates_plugins",
                "packet_task_id": "task-digital-products-local-gate-decision-packet-20260616",
                "source_check_task_id": "task-digital-products-local-revised-completeness-20260616",
                "source_check_evidence_id": "digital-products-local-revised-completeness-20260616",
                "selected_candidate_id": "ai-builder-launch-checklist-pack",
                "gate_option_count": 4,
                "recommended_option_id": "continue-local",
                "approval_request_count": 0,
                "blocked_by_gate_count": 4,
                "local_decision": "gate_decision_packet_ready_no_gate_requested",
                "live_tasks_created": 1,
                "live_tasks_completed": 1,
                "tasks_table_rows_before": 176,
                "tasks_table_rows_after": 177,
                "task_rows_inserted_by_packet": 1,
                "lane_evidence_rows_before": 89,
                "lane_evidence_rows_after": 90,
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
            "id": "digital_products_local_gate_choice",
            "label": "Digital Products Local Gate Choice",
            "path": DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_VALIDATION_JSON,
            "count_key": "followup_item_count",
            "expected": {
                "schema_version": "agent_company.digital_products_local_gate_choice_validation.v1",
                "choice_lane_id": "digital_products_templates_plugins",
                "choice_task_id": "task-digital-products-local-gate-choice-20260616",
                "source_packet_task_id": "task-digital-products-local-gate-decision-packet-20260616",
                "source_packet_evidence_id": "digital-products-local-gate-decision-packet-20260616",
                "selected_candidate_id": "ai-builder-launch-checklist-pack",
                "selected_option_id": "continue-local",
                "approval_request_count": 0,
                "followup_item_count": 3,
                "blocked_by_gate_count": 4,
                "local_decision": "continue_local_no_gate_exercised",
                "live_tasks_created": 1,
                "live_tasks_completed": 1,
                "tasks_table_rows_before": 178,
                "tasks_table_rows_after": 179,
                "task_rows_inserted_by_choice": 1,
                "lane_evidence_rows_before": 90,
                "lane_evidence_rows_after": 91,
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


__all__ = ["digital_product_review_gate_integrity_specs"]
