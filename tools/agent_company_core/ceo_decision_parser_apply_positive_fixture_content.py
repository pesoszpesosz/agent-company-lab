"""Pure content builder for the CEO decision parser apply positive fixture."""

from __future__ import annotations

from typing import Any

LOCAL_DECISION = "ceo_decision_parser_apply_positive_fixture_ready_preview_only"
RECOMMENDED_DEFAULT = "preview_single_service_request_update_before_apply"


def build_ceo_decision_parser_apply_positive_fixture_content(
    *,
    generated_utc: str,
    json_output_path: object,
    validation_path: object,
    lane_id: str,
    fixture_task_id: str,
    fixture_evidence_id: str,
    source_guard_runner_task_id: str,
    source_guard_runner_evidence_id: str,
    source_guard_runner_validation_path: object,
    preflight_packet: dict[str, Any],
    target_request_id: str,
    target_status_before: str | None,
    target_approval_scope_before: str | None,
    target_decision_note_before: str | None,
) -> dict[str, Any]:
    positive_apply_fixture_count = 1
    expected_preview_update_count = 1
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    apply_text = (
        "I explicitly approve applying exactly one parser preview mutation to the named service request id "
        f"{target_request_id}; do not open browsers, start workers, or perform account/payment/public actions."
    )
    positive_apply_fixture = {
        "fixture_id": "valid-single-service-request-approval-scope-preview",
        "expected_accepted": True,
        "expected_preview_state": "would_update_single_service_request_approval_scope",
        "expected_real_mutation": False,
        "submitted_apply": {
            "approval_packet_id": preflight_packet.get("decision_packet_id"),
            "explicit_mutation_approval_text": apply_text,
            "target_service_request_ids": [target_request_id],
            "max_update_count": 1,
            "runner_validation_path": str(source_guard_runner_validation_path),
            "service_request_status_snapshot_required": True,
            "forbidden_actions_acknowledged": True,
        },
    }
    preview_update = {
        "request_id": target_request_id,
        "field_updates": {
            "approval_scope": preflight_packet.get("allowed_action_scope"),
            "decision_note": "parser_apply_dry_run_preview_only_no_mutation",
        },
        "status_before": target_status_before,
        "status_after": target_status_before,
        "approval_scope_before": target_approval_scope_before,
        "decision_note_before": target_decision_note_before,
        "would_update_count": expected_preview_update_count,
        "applied": False,
    }
    fixture_summary = (
        "Created one positive apply dry-run fixture that previews a single bounded service-request approval-scope update without applying it."
    )
    fixture_next_action = (
        "Use this positive fixture with the apply guard before building any real apply path; the next step is a report-only apply dry-run runner that confirms the preview while leaving the DB unchanged."
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
        "schema_version": "agent_company.ceo_decision_parser_apply_positive_fixture.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_guard_runner_task_id": source_guard_runner_task_id,
        "source_guard_runner_evidence_id": source_guard_runner_evidence_id,
        "source_guard_runner_validation_path": str(source_guard_runner_validation_path),
        "positive_apply_fixture_count": positive_apply_fixture_count,
        "expected_preview_update_count": expected_preview_update_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_before,
        "positive_apply_fixture": positive_apply_fixture,
        "preview_update": preview_update,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "local_decision": LOCAL_DECISION,
        "recommended_default": RECOMMENDED_DEFAULT,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Parser Apply Positive Fixture",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{LOCAL_DECISION}`",
        "",
        fixture_summary,
        "",
        "## Preview",
        "",
        f"- Target request: `{target_request_id}`",
        f"- Preview state: `{positive_apply_fixture['expected_preview_state']}`",
        "- Applied: `False`",
        "",
        "## Boundary",
        "",
        "This is a local positive dry-run fixture only. It previews one service-request field update and applies nothing; it does not update service requests, request approval, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
        "",
        "## Next Action",
        "",
        fixture_next_action,
        "",
    ]
    return {
        "positive_apply_fixture_count": positive_apply_fixture_count,
        "expected_preview_update_count": expected_preview_update_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_after": target_status_before,
        "positive_apply_fixture": positive_apply_fixture,
        "preview_update": preview_update,
        "local_decision": LOCAL_DECISION,
        "recommended_default": RECOMMENDED_DEFAULT,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
        "payload": payload,
        "markdown": "\n".join(md_lines) + "\n",
    }


__all__ = [
    "LOCAL_DECISION",
    "RECOMMENDED_DEFAULT",
    "build_ceo_decision_parser_apply_positive_fixture_content",
]