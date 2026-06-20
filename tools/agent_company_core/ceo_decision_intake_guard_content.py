"""Pure content builder for the CEO decision intake guard."""

from __future__ import annotations

from typing import Any

LOCAL_DECISION = "ceo_decision_intake_guard_ready_no_decisions_accepted"
RECOMMENDED_DEFAULT = "reject_ambiguous_or_unscoped_decisions"
REQUIRED_FIELDS = [
    "decision_packet_id",
    "selected_option_id",
    "approved_blocker_ids",
    "allowed_action_scope",
    "forbidden_actions_acknowledged",
    "expiration_or_review_time",
    "approver_identity",
    "operator_confirmation_text",
]
INVALID_DECISION_RULES = [
    {
        "rule_id": "reject_missing_packet_id",
        "meaning": "A decision that does not name one known decision packet cannot be accepted.",
    },
    {
        "rule_id": "reject_unknown_option",
        "meaning": "Only the packet's draft option ids are admissible; free-form action words are insufficient.",
    },
    {
        "rule_id": "reject_unbounded_scope",
        "meaning": "Any approval must list exact allowed action scope and blocker ids.",
    },
    {
        "rule_id": "reject_forbidden_action_conflict",
        "meaning": "Any text allowing public, account, payment, wallet, submission, or security-testing side effects outside the packet scope is invalid.",
    },
    {
        "rule_id": "reject_no_expiration_or_review",
        "meaning": "Approvals need a time limit or explicit review point before work can begin.",
    },
    {
        "rule_id": "reject_implicit_or_contextual_approval",
        "meaning": "Casual continuation language, copied packet text, or vague consent cannot be treated as approval.",
    },
]


def build_ceo_decision_intake_guard_content(
    *,
    generated_utc: str,
    json_output_path: object,
    validation_path: object,
    lane_id: str,
    guard_task_id: str,
    guard_evidence_id: str,
    source_drafts_task_id: str,
    source_drafts_evidence_id: str,
    source_drafts_validation_path: object,
    packet_drafts: list[dict[str, Any]],
    source_packet_draft_count: int,
    source_decision_option_count: int,
) -> dict[str, Any]:
    accepted_decision_count = 0
    approval_request_count = 0
    runnable_without_approval_count = 0
    known_packet_ids = [packet["packet_id"] for packet in packet_drafts]
    known_option_ids = sorted(
        {option["option_id"] for packet in packet_drafts for option in packet.get("decision_options", [])}
    )
    example_empty_intake = {
        "decision_packet_id": None,
        "selected_option_id": None,
        "approved_blocker_ids": [],
        "allowed_action_scope": None,
        "forbidden_actions_acknowledged": False,
        "expiration_or_review_time": None,
        "approver_identity": None,
        "operator_confirmation_text": None,
        "accepted": False,
        "acceptance_reason": "No decision submitted; this guard only defines the intake contract.",
    }
    guard_summary = (
        "Created a local CEO decision-intake guard for future packet decisions. It defines required fields and rejection rules, but accepts no decision."
    )
    guard_next_action = (
        "Use this guard to validate any future CEO decision before mutating service requests or starting workers; reject ambiguous or unscoped approvals."
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
        "schema_version": "agent_company.ceo_decision_intake_guard.v1",
        "generated_utc": generated_utc,
        "guard_lane_id": lane_id,
        "guard_task_id": guard_task_id,
        "guard_evidence_id": guard_evidence_id,
        "source_drafts_task_id": source_drafts_task_id,
        "source_drafts_evidence_id": source_drafts_evidence_id,
        "source_drafts_validation_path": str(source_drafts_validation_path),
        "source_packet_draft_count": source_packet_draft_count,
        "source_decision_option_count": source_decision_option_count,
        "local_decision": LOCAL_DECISION,
        "recommended_default": RECOMMENDED_DEFAULT,
        "required_field_count": len(REQUIRED_FIELDS),
        "required_fields": REQUIRED_FIELDS,
        "invalid_decision_rule_count": len(INVALID_DECISION_RULES),
        "invalid_decision_rules": INVALID_DECISION_RULES,
        "known_packet_ids": known_packet_ids,
        "known_option_ids": known_option_ids,
        "example_empty_intake": example_empty_intake,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "summary": guard_summary,
        "next_action": guard_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Intake Guard",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{LOCAL_DECISION}`",
        "",
        guard_summary,
        "",
        "## Required Fields",
        "",
    ]
    md_lines.extend(f"- `{field}`" for field in REQUIRED_FIELDS)
    md_lines.extend(["", "## Invalid Decision Rules", ""])
    md_lines.extend(f"- `{rule['rule_id']}`: {rule['meaning']}" for rule in INVALID_DECISION_RULES)
    md_lines.extend(["", "## Known Packet IDs", ""])
    md_lines.extend(f"- `{packet_id}`" for packet_id in known_packet_ids)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a local intake guard only. It accepts no decisions and does not approve, reject, assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.",
            "",
            "## Next Action",
            "",
            guard_next_action,
            "",
        ]
    )
    return {
        "local_decision": LOCAL_DECISION,
        "recommended_default": RECOMMENDED_DEFAULT,
        "required_field_count": len(REQUIRED_FIELDS),
        "required_fields": REQUIRED_FIELDS,
        "invalid_decision_rule_count": len(INVALID_DECISION_RULES),
        "invalid_decision_rules": INVALID_DECISION_RULES,
        "known_packet_ids": known_packet_ids,
        "known_option_ids": known_option_ids,
        "example_empty_intake": example_empty_intake,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "summary": guard_summary,
        "next_action": guard_next_action,
        "runtime_boundary": runtime_boundary,
        "payload": payload,
        "markdown": "\n".join(md_lines) + "\n",
    }


__all__ = [
    "INVALID_DECISION_RULES",
    "LOCAL_DECISION",
    "RECOMMENDED_DEFAULT",
    "REQUIRED_FIELDS",
    "build_ceo_decision_intake_guard_content",
]