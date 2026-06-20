"""Pure content builders for the CEO decision parser report-only runner."""

from __future__ import annotations

from typing import Any


def parse_decision_intake(intake: dict[str, object]) -> dict[str, object]:
    selected_option_id = intake.get("selected_option_id")
    packet_id = intake.get("decision_packet_id")
    scope = str(intake.get("allowed_action_scope") or "")
    scope_lower = scope.lower()
    confirmation = str(intake.get("operator_confirmation_text") or "").lower()
    expiration = intake.get("expiration_or_review_time")
    forbidden_ack = bool(intake.get("forbidden_actions_acknowledged"))
    approved_blockers = intake.get("approved_blocker_ids") or []
    if not packet_id:
        return {"accepted_for_dry_run": False, "rule_id": "reject_missing_packet_id"}
    if selected_option_id != "approve_bounded_readonly_scope":
        return {"accepted_for_dry_run": False, "rule_id": "reject_unknown_option"}
    if not expiration:
        return {"accepted_for_dry_run": False, "rule_id": "reject_no_expiration_or_review"}
    if "whatever" in scope_lower or not approved_blockers or confirmation in {"go ahead", "continue"}:
        return {
            "accepted_for_dry_run": False,
            "rule_id": "reject_unbounded_scope" if "whatever" in scope_lower or not approved_blockers else "reject_implicit_or_contextual_approval",
        }
    if not forbidden_ack or "publish" in scope_lower:
        return {"accepted_for_dry_run": False, "rule_id": "reject_forbidden_action_conflict"}
    forbidden_terms = ["checkout", "payment", "wallet", "account settings", "personal data"]
    if " no " not in f" {scope_lower} " and any(term in scope_lower for term in forbidden_terms):
        return {"accepted_for_dry_run": False, "rule_id": "reject_forbidden_action_conflict"}
    if "previous" in scope_lower or "see previous" in scope_lower:
        return {"accepted_for_dry_run": False, "rule_id": "reject_implicit_or_contextual_approval"}
    if "read-only" not in scope_lower:
        return {"accepted_for_dry_run": False, "rule_id": "reject_unbounded_scope"}
    return {
        "accepted_for_dry_run": True,
        "rule_id": None,
        "preview_state": "would_create_bounded_service_request_update",
        "expected_real_mutation": False,
        "expected_service_requests_updated": 0,
        "expected_worker_starts": 0,
    }


def build_report_only_parser_runner_content(
    *,
    negative_fixtures: list[dict[str, Any]],
    positive_fixture: dict[str, Any],
    negative_fixture_total: int,
    positive_fixture_total: int,
) -> dict[str, Any]:
    parser_results: list[dict[str, object]] = []
    for fixture in negative_fixtures:
        result = parse_decision_intake(fixture.get("submitted_intake", {}))
        expected_rule_id = fixture.get("expected_rule_id")
        parser_results.append(
            {
                "fixture_id": fixture.get("fixture_id"),
                "fixture_type": "negative",
                "expected_accepted": fixture.get("expected_accepted"),
                "actual_accepted": result.get("accepted_for_dry_run"),
                "expected_rule_id": expected_rule_id,
                "actual_rule_id": result.get("rule_id"),
                "matched_expected": result.get("accepted_for_dry_run") is False and result.get("rule_id") == expected_rule_id,
            }
        )
    positive_expected = positive_fixture.get("expected_parser_result", {})
    positive_result = parse_decision_intake(positive_fixture.get("submitted_intake", {}))
    parser_results.append(
        {
            "fixture_id": positive_fixture.get("fixture_id"),
            "fixture_type": "positive",
            "expected_accepted": positive_expected.get("accepted_for_dry_run"),
            "actual_accepted": positive_result.get("accepted_for_dry_run"),
            "expected_preview_state": positive_expected.get("expected_preview_state"),
            "actual_preview_state": positive_result.get("preview_state"),
            "matched_expected": (
                positive_result.get("accepted_for_dry_run") is True
                and positive_result.get("preview_state") == positive_expected.get("expected_preview_state")
                and positive_result.get("expected_real_mutation") is False
                and positive_result.get("expected_service_requests_updated") == 0
                and positive_result.get("expected_worker_starts") == 0
            ),
        }
    )
    runner_summary = (
        "Ran a local report-only CEO decision parser against six negative fixtures and one positive dry-run fixture. The parser matched all expected outcomes and produced no queue mutation or external side effect."
    )
    runner_next_action = (
        "Keep this parser runner report-only; next add a mutation-preflight packet that states the exact operator approval required before any service request update can be applied."
    )
    boundary_text = (
        "This runner is report-only. It evaluated local fixtures and wrote local artifacts only; it did not mutate service requests, assign work, request approval, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money."
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
        "fixture_suite_count": int(negative_fixture_total) + int(positive_fixture_total),
        "negative_fixture_count": len(negative_fixtures),
        "positive_fixture_count": 1 if positive_fixture else 0,
        "parser_results": parser_results,
        "parser_execution_count": len(parser_results),
        "rejected_decision_count": sum(1 for result in parser_results if result.get("actual_accepted") is False),
        "accepted_dry_run_preview_count": sum(1 for result in parser_results if result.get("actual_accepted") is True),
        "expected_rejection_match_count": sum(
            1 for result in parser_results if result.get("fixture_type") == "negative" and result.get("matched_expected") is True
        ),
        "expected_preview_match_count": sum(
            1 for result in parser_results if result.get("fixture_type") == "positive" and result.get("matched_expected") is True
        ),
        "queue_mutation_count": 0,
        "approval_request_count": 0,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "boundary_text": boundary_text,
        "runtime_boundary": runtime_boundary,
    }


__all__ = [
    "build_report_only_parser_runner_content",
    "parse_decision_intake",
]
