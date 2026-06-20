from __future__ import annotations

from typing import Any


def build_digital_products_gated_hold_register_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_plan_validation_path: str,
    lane_id: str,
    register_task_id: str,
    register_evidence_id: str,
    source_plan_task_id: str,
    source_plan_evidence_id: str,
    selected_candidate_id: str,
    blocked_questions: list[dict[str, Any]],
    source_simulation_scenario_count: int,
) -> dict[str, Any]:
    local_decision = "gated_hold_register_active"
    recommended_default = "hold_until_explicit_user_approval"
    approval_request_count = 0
    runnable_without_approval_count = 0
    hold_entries = [
        {
            "hold_id": "hold-live-marketplace-demand",
            "source_question_id": "live-marketplace-demand",
            "gate_required": "browser_read_only_session",
            "status": "active_hold",
            "resume_trigger": "Explicit user approval for approve-read-only-browser-validation.",
            "resume_command_candidate": "write a bounded read-only browser validation task packet",
            "related_scenario_id": "if-read-only-browser-validation-approved",
            "must_remain_frozen": [
                "Opening marketplace/category pages.",
                "Collecting live browser evidence.",
                "Any login, posting, messaging, checkout, saved change, account setting, or personal-data entry.",
            ],
        },
        {
            "hold_id": "hold-live-terms-and-fees",
            "source_question_id": "live-terms-and-fees",
            "gate_required": "legal_kyc_tax_payment",
            "status": "active_hold",
            "resume_trigger": "Explicit user approval for approve-legal-payment-review.",
            "resume_command_candidate": "write a bounded legal/payment review task packet",
            "related_scenario_id": "if-legal-payment-review-approved",
            "must_remain_frozen": [
                "Accepting terms or agreements.",
                "Providing tax, KYC, payout, or payment data.",
                "Creating seller accounts or configuring payouts.",
            ],
        },
        {
            "hold_id": "hold-public-listing-action",
            "source_question_id": "public-listing-action",
            "gate_required": "public_action_approval",
            "status": "active_hold",
            "resume_trigger": "Explicit user approval after browser and legal/payment review evidence is complete.",
            "resume_command_candidate": "write a public-listing preflight packet",
            "related_scenario_id": None,
            "must_remain_frozen": [
                "Creating, publishing, updating, or promoting any marketplace listing.",
                "Posting public product pages, comments, messages, or claims.",
                "Setting a live public price or launch promise.",
            ],
        },
        {
            "hold_id": "hold-account-or-payment-setup",
            "source_question_id": "account-or-payment-setup",
            "gate_required": "account_payment_approval",
            "status": "active_hold",
            "resume_trigger": "Explicit user approval after terms, KYC/tax, and payout risks are understood.",
            "resume_command_candidate": "write an account/payment setup preflight packet",
            "related_scenario_id": None,
            "must_remain_frozen": [
                "Creating seller accounts.",
                "Connecting payment methods or payout accounts.",
                "Accepting agreements or configuring account/payment settings.",
            ],
        },
    ]
    active_hold_count = sum(1 for entry in hold_entries if entry.get("status") == "active_hold")
    explicit_approval_required_count = len(hold_entries)
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
    register_summary = (
        "Created a local gated hold register for the digital-products lane, preserving four active holds and exact resume triggers without requesting approval or executing gated work."
    )
    register_next_action = (
        "Keep all four holds active until explicit user approval is given for a specific gate; after approval, resume only the matching bounded task packet."
    )
    payload = {
        "schema_version": "agent_company.digital_products_local_gated_hold_register.v1",
        "generated_utc": generated_utc,
        "register_lane_id": lane_id,
        "register_task_id": register_task_id,
        "register_evidence_id": register_evidence_id,
        "source_plan_task_id": source_plan_task_id,
        "source_plan_evidence_id": source_plan_evidence_id,
        "source_plan_validation_path": source_plan_validation_path,
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "approval_request_count": approval_request_count,
        "hold_entry_count": len(hold_entries),
        "source_simulation_scenario_count": source_simulation_scenario_count,
        "active_hold_count": active_hold_count,
        "explicit_approval_required_count": explicit_approval_required_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "blocked_by_gate_count": len(blocked_questions),
        "hold_entries": hold_entries,
        "blocked_by_gate_questions": blocked_questions,
        "summary": register_summary,
        "next_action": register_next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Digital Products Local Gated Hold Register",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        register_summary,
        "",
        f"Recommended default: `{recommended_default}`",
        "",
        "## Active Holds",
        "",
        "| Hold | Gate | Resume Trigger |",
        "| --- | --- | --- |",
    ]
    for entry in hold_entries:
        md_lines.append(f"| `{entry['hold_id']}` | `{entry['gate_required']}` | {entry['resume_trigger']} |")
    md_lines.extend(["", "## Frozen Actions", ""])
    for entry in hold_entries:
        md_lines.extend([f"### {entry['hold_id']}", ""])
        for item in entry["must_remain_frozen"]:
            md_lines.append(f"- {item}")
        md_lines.append("")
    md_lines.extend(
        [
            "## Boundary",
            "",
            "This is a local hold register only. It does not request approval, run browser sessions, perform legal/payment review, open accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            register_next_action,
            "",
        ]
    )

    return {
        "active_hold_count": active_hold_count,
        "approval_request_count": approval_request_count,
        "explicit_approval_required_count": explicit_approval_required_count,
        "hold_entries": hold_entries,
        "hold_entry_count": len(hold_entries),
        "local_decision": local_decision,
        "markdown": "\n".join(md_lines) + "\n",
        "next_action": register_next_action,
        "payload": payload,
        "recommended_default": recommended_default,
        "runnable_without_approval_count": runnable_without_approval_count,
        "runtime_boundary": runtime_boundary,
        "summary": register_summary,
    }


__all__ = ["build_digital_products_gated_hold_register_content"]
