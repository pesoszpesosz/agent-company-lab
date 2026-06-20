from __future__ import annotations

from typing import Any

"""Copy-polish and readiness digital-product integrity specs."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_VALIDATION_JSON,
)


def digital_product_review_polish_integrity_specs() -> list[dict[str, Any]]:
    return [
        {
            "id": "digital_products_local_copy_polish",
            "label": "Digital Products Local Copy Polish",
            "path": DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_VALIDATION_JSON,
            "count_key": "polished_file_count",
            "expected": {
                "schema_version": "agent_company.digital_products_local_copy_polish_validation.v1",
                "polish_lane_id": "digital_products_templates_plugins",
                "polish_task_id": "task-digital-products-local-copy-polish-20260616",
                "source_choice_task_id": "task-digital-products-local-gate-choice-20260616",
                "source_choice_evidence_id": "digital-products-local-gate-choice-20260616",
                "selected_candidate_id": "ai-builder-launch-checklist-pack",
                "selected_option_id": "continue-local",
                "polished_file_count": 6,
                "copy_change_count": 9,
                "boundary_phrase_count": 7,
                "approval_request_count": 0,
                "blocked_by_gate_count": 4,
                "local_decision": "copy_polish_complete_no_gate_exercised",
                "live_tasks_created": 1,
                "live_tasks_completed": 1,
                "tasks_table_rows_before": 180,
                "tasks_table_rows_after": 181,
                "task_rows_inserted_by_polish": 1,
                "lane_evidence_rows_before": 91,
                "lane_evidence_rows_after": 92,
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
            "id": "digital_products_local_post_polish_readiness",
            "label": "Digital Products Local Post-Polish Readiness",
            "path": DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_VALIDATION_JSON,
            "count_key": "readiness_check_count",
            "expected": {
                "schema_version": "agent_company.digital_products_local_post_polish_readiness_validation.v1",
                "readiness_lane_id": "digital_products_templates_plugins",
                "readiness_task_id": "task-digital-products-local-post-polish-readiness-20260616",
                "source_polish_task_id": "task-digital-products-local-copy-polish-20260616",
                "source_polish_evidence_id": "digital-products-local-copy-polish-20260616",
                "selected_candidate_id": "ai-builder-launch-checklist-pack",
                "selected_option_id": "continue-local",
                "readiness_check_count": 7,
                "passed_check_count": 7,
                "recommended_next_option_id": "draft-future-approval-packets",
                "approval_request_count": 0,
                "blocked_by_gate_count": 4,
                "local_decision": "post_polish_ready_for_local_approval_packet_drafts",
                "live_tasks_created": 1,
                "live_tasks_completed": 1,
                "tasks_table_rows_before": 182,
                "tasks_table_rows_after": 183,
                "task_rows_inserted_by_readiness": 1,
                "lane_evidence_rows_before": 92,
                "lane_evidence_rows_after": 93,
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


__all__ = ["digital_product_review_polish_integrity_specs"]
