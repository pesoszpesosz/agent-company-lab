"""Pure content builders for CEO decision intake negative fixtures."""

from __future__ import annotations

from typing import Any


def build_ceo_decision_intake_negative_fixture_content(
    *,
    known_packet_ids: list[Any],
    known_option_ids: list[Any],
) -> dict[str, Any]:
    first_packet_id = known_packet_ids[0] if known_packet_ids else "unknown"
    first_option_id = known_option_ids[0] if known_option_ids else "unknown"
    negative_fixtures = [
        {
            "fixture_id": "missing-packet-id",
            "expected_rule_id": "reject_missing_packet_id",
            "submitted_intake": {
                "decision_packet_id": None,
                "selected_option_id": first_option_id,
                "approved_blocker_ids": ["req-wave4-digital-products-browser-readonly-20260614"],
                "allowed_action_scope": "Read-only public pages only.",
                "forbidden_actions_acknowledged": True,
                "expiration_or_review_time": "2026-06-16T23:59:59Z",
                "approver_identity": "user",
                "operator_confirmation_text": "approve this exact scope",
            },
            "expected_accepted": False,
        },
        {
            "fixture_id": "unknown-option",
            "expected_rule_id": "reject_unknown_option",
            "submitted_intake": {
                "decision_packet_id": first_packet_id,
                "selected_option_id": "just_go_do_it",
                "approved_blocker_ids": ["req-wave4-digital-products-browser-readonly-20260614"],
                "allowed_action_scope": "Read-only public pages only.",
                "forbidden_actions_acknowledged": True,
                "expiration_or_review_time": "2026-06-16T23:59:59Z",
                "approver_identity": "user",
                "operator_confirmation_text": "approve this exact scope",
            },
            "expected_accepted": False,
        },
        {
            "fixture_id": "unbounded-scope",
            "expected_rule_id": "reject_unbounded_scope",
            "submitted_intake": {
                "decision_packet_id": first_packet_id,
                "selected_option_id": first_option_id,
                "approved_blocker_ids": [],
                "allowed_action_scope": "Do whatever is needed.",
                "forbidden_actions_acknowledged": True,
                "expiration_or_review_time": "2026-06-16T23:59:59Z",
                "approver_identity": "user",
                "operator_confirmation_text": "go ahead",
            },
            "expected_accepted": False,
        },
        {
            "fixture_id": "forbidden-action-conflict",
            "expected_rule_id": "reject_forbidden_action_conflict",
            "submitted_intake": {
                "decision_packet_id": first_packet_id,
                "selected_option_id": first_option_id,
                "approved_blocker_ids": ["hold-public-listing-action"],
                "allowed_action_scope": "Create and publish the listing after checking pages.",
                "forbidden_actions_acknowledged": False,
                "expiration_or_review_time": "2026-06-16T23:59:59Z",
                "approver_identity": "user",
                "operator_confirmation_text": "publish it",
            },
            "expected_accepted": False,
        },
        {
            "fixture_id": "no-expiration",
            "expected_rule_id": "reject_no_expiration_or_review",
            "submitted_intake": {
                "decision_packet_id": first_packet_id,
                "selected_option_id": first_option_id,
                "approved_blocker_ids": ["req-wave4-digital-products-browser-readonly-20260614"],
                "allowed_action_scope": "Read-only public pages only.",
                "forbidden_actions_acknowledged": True,
                "expiration_or_review_time": None,
                "approver_identity": "user",
                "operator_confirmation_text": "approve this exact scope",
            },
            "expected_accepted": False,
        },
        {
            "fixture_id": "implicit-contextual-approval",
            "expected_rule_id": "reject_implicit_or_contextual_approval",
            "submitted_intake": {
                "decision_packet_id": first_packet_id,
                "selected_option_id": first_option_id,
                "approved_blocker_ids": ["req-wave4-digital-products-browser-readonly-20260614"],
                "allowed_action_scope": "See previous packet.",
                "forbidden_actions_acknowledged": True,
                "expiration_or_review_time": "2026-06-16T23:59:59Z",
                "approver_identity": "user",
                "operator_confirmation_text": "continue",
            },
            "expected_accepted": False,
        },
    ]
    return {
        "negative_fixtures": negative_fixtures,
        "negative_fixture_count": len(negative_fixtures),
        "expected_rejection_count": sum(1 for fixture in negative_fixtures if not fixture["expected_accepted"]),
        "accepted_fixture_count": sum(1 for fixture in negative_fixtures if fixture["expected_accepted"]),
        "covered_rule_ids": sorted({fixture["expected_rule_id"] for fixture in negative_fixtures}),
    }


__all__ = ["build_ceo_decision_intake_negative_fixture_content"]
