"""Pure content builders for CEO decision parser mutation preflight."""

from __future__ import annotations

from typing import Any

REQUIRED_APPROVAL_FIELDS = [
    "decision_packet_id",
    "selected_option_id",
    "approver_identity",
    "operator_confirmation_text",
    "allowed_action_scope",
    "approved_blocker_ids",
    "expiration_or_review_time",
    "forbidden_actions_acknowledged",
]

FORBIDDEN_ACTIONS = [
    "login",
    "posting",
    "listing",
    "messaging",
    "checkout",
    "account settings",
    "personal data entry",
    "saved changes",
    "payment actions",
    "account actions",
]

APPLY_PREFLIGHT_PRECONDITIONS = [
    "runner validation must remain green",
    "operator must explicitly approve mutation apply, not only read-only browser validation",
    "target service request ids and maximum update count must be named before apply",
    "service request status counts must be snapshotted before and after apply",
    "no browser, account, wallet, payment, public, security-testing, API, worker-start, or real-money action is included",
]


def _accepted_previews(runner_payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        result
        for result in runner_payload.get("parser_results", [])
        if result.get("fixture_type") == "positive"
        and result.get("actual_accepted") is True
        and result.get("actual_preview_state") == "would_create_bounded_service_request_update"
        and result.get("matched_expected") is True
    ]


def build_ceo_decision_parser_mutation_preflight_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    lane_id: str,
    preflight_task_id: str,
    preflight_evidence_id: str,
    source_runner_task_id: str,
    source_runner_evidence_id: str,
    source_runner_validation_path: str,
    runner_payload: dict[str, Any],
    positive_fixture: dict[str, Any],
) -> dict[str, Any]:
    submitted_intake = positive_fixture.get("submitted_intake", {})
    accepted_previews = _accepted_previews(runner_payload)
    required_blocker_ids = list(submitted_intake.get("approved_blocker_ids") or [])
    preflight_packet = {
        "candidate_fixture_id": positive_fixture.get("fixture_id"),
        "candidate_preview_state": accepted_previews[0].get("actual_preview_state") if accepted_previews else None,
        "decision_packet_id": submitted_intake.get("decision_packet_id"),
        "selected_option_id": submitted_intake.get("selected_option_id"),
        "approver_identity": submitted_intake.get("approver_identity"),
        "operator_confirmation_text": submitted_intake.get("operator_confirmation_text"),
        "allowed_action_scope": submitted_intake.get("allowed_action_scope"),
        "approved_blocker_ids": required_blocker_ids,
        "expiration_or_review_time": submitted_intake.get("expiration_or_review_time"),
        "forbidden_actions_acknowledged": submitted_intake.get("forbidden_actions_acknowledged"),
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "apply_preconditions": APPLY_PREFLIGHT_PRECONDITIONS,
    }
    local_decision = "ceo_decision_parser_mutation_preflight_ready_no_apply"
    recommended_default = "require_explicit_operator_mutation_approval_before_apply"
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    summary = (
        "Created a local mutation-preflight packet for the accepted dry-run parser preview. The packet records the exact approval fields, blocker ids, forbidden actions, and apply preconditions required before any service request mutation is eligible."
    )
    next_action = (
        "Do not apply the preview yet; next create a mutation-apply negative fixture set so unauthorized or underspecified apply attempts are rejected before any DB update path exists."
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
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_mutation_preflight.v1",
        "generated_utc": generated_utc,
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "preflight_evidence_id": preflight_evidence_id,
        "source_runner_task_id": source_runner_task_id,
        "source_runner_evidence_id": source_runner_evidence_id,
        "source_runner_validation_path": source_runner_validation_path,
        "candidate_preview_count": len(accepted_previews),
        "required_approval_field_count": len(REQUIRED_APPROVAL_FIELDS),
        "required_blocker_count": len(required_blocker_ids),
        "forbidden_action_count": len(FORBIDDEN_ACTIONS),
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "preflight_packet": preflight_packet,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Parser Mutation Preflight",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        summary,
        "",
        "## Required Approval Fields",
        "",
    ]
    md_lines.extend(f"- `{field}`" for field in REQUIRED_APPROVAL_FIELDS)
    md_lines.extend(["", "## Forbidden Actions", ""])
    md_lines.extend(f"- `{action}`" for action in FORBIDDEN_ACTIONS)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This preflight applies nothing. It records a local approval checklist only and performs no queue mutation, service request update, approval request, browser session, account action, wallet/payment action, public action, security testing, API call, worker start, or real-money action.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {
        "approval_request_count": approval_request_count,
        "candidate_preview_count": len(accepted_previews),
        "forbidden_action_count": len(FORBIDDEN_ACTIONS),
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "local_decision": local_decision,
        "markdown": "\n".join(md_lines) + "\n",
        "mutation_applied_count": mutation_applied_count,
        "next_action": next_action,
        "payload": payload,
        "preflight_packet": preflight_packet,
        "queue_mutation_count": queue_mutation_count,
        "recommended_default": recommended_default,
        "required_approval_field_count": len(REQUIRED_APPROVAL_FIELDS),
        "required_approval_fields": REQUIRED_APPROVAL_FIELDS,
        "required_blocker_count": len(required_blocker_ids),
        "runtime_boundary": runtime_boundary,
        "summary": summary,
    }


__all__ = [
    "APPLY_PREFLIGHT_PRECONDITIONS",
    "FORBIDDEN_ACTIONS",
    "REQUIRED_APPROVAL_FIELDS",
    "build_ceo_decision_parser_mutation_preflight_content",
]
