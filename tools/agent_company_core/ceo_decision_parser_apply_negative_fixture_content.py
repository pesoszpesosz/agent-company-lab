"""Pure content builders for CEO decision parser apply negative fixtures."""

from __future__ import annotations

from typing import Any

REQUIRED_APPLY_FIELDS = [
    "approval_packet_id",
    "explicit_mutation_approval_text",
    "target_service_request_ids",
    "max_update_count",
    "runner_validation_path",
    "service_request_status_snapshot_required",
    "forbidden_actions_acknowledged",
]

TARGET_SERVICE_REQUEST_ID = "req-wave4-digital-products-browser-readonly-20260614"


def build_ceo_decision_parser_apply_negative_fixture_content(
    *,
    preflight_packet: dict[str, Any],
    runner_validation_path: object,
) -> dict[str, Any]:
    approval_packet_id = preflight_packet.get("decision_packet_id")
    negative_apply_fixtures = [
        {
            "fixture_id": "missing-explicit-mutation-approval",
            "expected_accepted": False,
            "expected_rule_id": "reject_missing_explicit_mutation_approval",
            "submitted_apply": {
                "approval_packet_id": approval_packet_id,
                "explicit_mutation_approval_text": None,
                "target_service_request_ids": [TARGET_SERVICE_REQUEST_ID],
                "max_update_count": 1,
                "runner_validation_path": str(runner_validation_path),
                "service_request_status_snapshot_required": True,
                "forbidden_actions_acknowledged": True,
            },
        },
        {
            "fixture_id": "readonly-approval-not-mutation-approval",
            "expected_accepted": False,
            "expected_rule_id": "reject_readonly_scope_not_mutation_approval",
            "submitted_apply": {
                "approval_packet_id": approval_packet_id,
                "explicit_mutation_approval_text": preflight_packet.get("operator_confirmation_text"),
                "target_service_request_ids": [TARGET_SERVICE_REQUEST_ID],
                "max_update_count": 1,
                "runner_validation_path": str(runner_validation_path),
                "service_request_status_snapshot_required": True,
                "forbidden_actions_acknowledged": True,
            },
        },
        {
            "fixture_id": "missing-target-service-request-ids",
            "expected_accepted": False,
            "expected_rule_id": "reject_missing_target_service_request_ids",
            "submitted_apply": {
                "approval_packet_id": approval_packet_id,
                "explicit_mutation_approval_text": "I explicitly approve applying exactly one parser preview mutation to the named service request ids.",
                "target_service_request_ids": [],
                "max_update_count": 1,
                "runner_validation_path": str(runner_validation_path),
                "service_request_status_snapshot_required": True,
                "forbidden_actions_acknowledged": True,
            },
        },
        {
            "fixture_id": "unbounded-update-count",
            "expected_accepted": False,
            "expected_rule_id": "reject_unbounded_or_excessive_update_count",
            "submitted_apply": {
                "approval_packet_id": approval_packet_id,
                "explicit_mutation_approval_text": "I explicitly approve applying parser preview mutations.",
                "target_service_request_ids": [TARGET_SERVICE_REQUEST_ID],
                "max_update_count": 99,
                "runner_validation_path": str(runner_validation_path),
                "service_request_status_snapshot_required": True,
                "forbidden_actions_acknowledged": True,
            },
        },
        {
            "fixture_id": "forbidden-action-requested",
            "expected_accepted": False,
            "expected_rule_id": "reject_forbidden_action_requested",
            "submitted_apply": {
                "approval_packet_id": approval_packet_id,
                "explicit_mutation_approval_text": "I explicitly approve applying the preview and opening the marketplace listing.",
                "target_service_request_ids": [TARGET_SERVICE_REQUEST_ID],
                "max_update_count": 1,
                "runner_validation_path": str(runner_validation_path),
                "service_request_status_snapshot_required": True,
                "forbidden_actions_acknowledged": False,
            },
        },
        {
            "fixture_id": "missing-status-snapshot",
            "expected_accepted": False,
            "expected_rule_id": "reject_missing_service_request_status_snapshot",
            "submitted_apply": {
                "approval_packet_id": approval_packet_id,
                "explicit_mutation_approval_text": "I explicitly approve applying exactly one parser preview mutation to the named service request ids.",
                "target_service_request_ids": [TARGET_SERVICE_REQUEST_ID],
                "max_update_count": 1,
                "runner_validation_path": str(runner_validation_path),
                "service_request_status_snapshot_required": False,
                "forbidden_actions_acknowledged": True,
            },
        },
    ]
    fixture_summary = (
        "Created local negative fixtures for the future CEO decision parser apply path, covering missing mutation approval, read-only-only approval, missing targets, excessive update count, forbidden action conflict, and missing status snapshot."
    )
    fixture_next_action = (
        "Use these fixtures before building any apply path; every unauthorized or underspecified apply attempt must be rejected before service request mutations are allowed."
    )
    boundary_text = (
        "These are local negative fixtures only. They apply no mutation, update no service request, request no approval, start no worker, call no API, open no browser, and perform no account, wallet, payment, public, security-testing, external, or real-money action."
    )
    runtime_boundary = {
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
    }
    return {
        "required_apply_fields": REQUIRED_APPLY_FIELDS,
        "required_apply_field_count": len(REQUIRED_APPLY_FIELDS),
        "negative_apply_fixtures": negative_apply_fixtures,
        "negative_apply_fixture_count": len(negative_apply_fixtures),
        "expected_rejection_count": sum(1 for fixture in negative_apply_fixtures if fixture.get("expected_accepted") is False),
        "accepted_apply_count": 0,
        "mutation_applied_count": 0,
        "queue_mutation_count": 0,
        "approval_request_count": 0,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "boundary_text": boundary_text,
        "runtime_boundary": runtime_boundary,
    }


__all__ = [
    "REQUIRED_APPLY_FIELDS",
    "TARGET_SERVICE_REQUEST_ID",
    "build_ceo_decision_parser_apply_negative_fixture_content",
]
