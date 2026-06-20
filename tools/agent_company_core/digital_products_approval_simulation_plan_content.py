from __future__ import annotations

from typing import Any


def build_digital_products_post_approval_simulation_plan_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_brief_validation_path: str,
    lane_id: str,
    plan_task_id: str,
    plan_evidence_id: str,
    source_brief_task_id: str,
    source_brief_evidence_id: str,
    selected_candidate_id: str,
    blocked_questions: list[dict[str, Any]],
    requires_explicit_approval_count: int,
) -> dict[str, Any]:
    local_decision = "post_approval_simulation_plan_ready_not_executed"
    recommended_default = "hold_until_explicit_user_approval"
    approval_request_count = 0
    simulated_browser_sessions = 0
    simulated_legal_payment_reviews = 0
    simulation_scenarios = [
        {
            "scenario_id": "if-read-only-browser-validation-approved",
            "source_decision_id": "approve-read-only-browser-validation",
            "requires_explicit_approval": True,
            "gate_required": "browser_read_only_session",
            "execution_status": "not_executed",
            "simulated_worker": "service-worker-browser-readonly",
            "planned_inputs": [
                "Polished candidate: ai-builder-launch-checklist-pack.",
                "Public marketplace/category pages chosen by operator after approval.",
                "Allowed signal fields: demand language, price bands, saturation notes, buyer objections, and comparable packaging.",
            ],
            "planned_outputs": [
                "Read-only demand-validation notes.",
                "No-login source list with observed category/price/saturation signals.",
                "Go/no-go recommendation for private listing preparation.",
            ],
            "must_not_do": [
                "Do not log in, create accounts, post, list, message, checkout, save changes, enter personal data, or configure settings.",
                "Do not treat simulated approval as actual approval.",
            ],
        },
        {
            "scenario_id": "if-legal-payment-review-approved",
            "source_decision_id": "approve-legal-payment-review",
            "requires_explicit_approval": True,
            "gate_required": "legal_kyc_tax_payment",
            "execution_status": "not_executed",
            "simulated_worker": "service-worker-legal-payment-review",
            "planned_inputs": [
                "Candidate sales motion: digital checklist/template pack for AI builders.",
                "Platform terms, fees, refund, tax/KYC, and payout pages selected by operator after approval.",
                "Existing local gate decision packet and operator approval brief.",
            ],
            "planned_outputs": [
                "Terms/fees/risk memo with unresolved user decisions.",
                "Payment/KYC/tax blocker list.",
                "Allowed next local packaging action if legal/payment risk remains acceptable.",
            ],
            "must_not_do": [
                "Do not accept agreements, create seller accounts, configure payouts, connect payment methods, provide KYC/tax data, or list products.",
                "Do not treat simulated approval as actual approval.",
            ],
        },
    ]
    plan_summary = (
        "Prepared a local post-approval simulation plan for the two possible approved next steps. The plan describes worker inputs, outputs, and prohibited actions, but executes nothing."
    )
    plan_next_action = (
        "Keep the digital-products lane on hold until explicit user approval is given for a listed decision item; after approval, run only the matching bounded scenario."
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
        "schema_version": "agent_company.digital_products_local_post_approval_simulation_plan.v1",
        "generated_utc": generated_utc,
        "plan_lane_id": lane_id,
        "plan_task_id": plan_task_id,
        "plan_evidence_id": plan_evidence_id,
        "source_brief_task_id": source_brief_task_id,
        "source_brief_evidence_id": source_brief_evidence_id,
        "source_brief_validation_path": source_brief_validation_path,
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "approval_request_count": approval_request_count,
        "simulation_scenario_count": len(simulation_scenarios),
        "requires_explicit_approval_count": requires_explicit_approval_count,
        "simulated_browser_sessions": simulated_browser_sessions,
        "simulated_legal_payment_reviews": simulated_legal_payment_reviews,
        "simulation_scenarios": simulation_scenarios,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": plan_summary,
        "next_action": plan_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# Digital Products Local Post-Approval Simulation Plan",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        plan_summary,
        "",
        f"Recommended default: `{recommended_default}`",
        "",
        "## Simulation Scenarios",
        "",
    ]
    for scenario in simulation_scenarios:
        md_lines.extend(
            [
                f"### {scenario['scenario_id']}",
                "",
                f"Source decision: `{scenario['source_decision_id']}`",
                f"Gate: `{scenario['gate_required']}`",
                f"Execution status: `{scenario['execution_status']}`",
                f"Simulated worker: `{scenario['simulated_worker']}`",
                "",
                "Planned inputs:",
            ]
        )
        for item in scenario["planned_inputs"]:
            md_lines.append(f"- {item}")
        md_lines.extend(["", "Planned outputs:"])
        for item in scenario["planned_outputs"]:
            md_lines.append(f"- {item}")
        md_lines.extend(["", "Must not do:"])
        for item in scenario["must_not_do"]:
            md_lines.append(f"- {item}")
        md_lines.append("")
    md_lines.extend(["## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a local simulation plan only. It does not request approval, run browser sessions, perform legal/payment review, open accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            plan_next_action,
            "",
        ]
    )
    return {
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "approval_request_count": approval_request_count,
        "simulated_browser_sessions": simulated_browser_sessions,
        "simulated_legal_payment_reviews": simulated_legal_payment_reviews,
        "simulation_scenarios": simulation_scenarios,
        "simulation_scenario_count": len(simulation_scenarios),
        "summary": plan_summary,
        "next_action": plan_next_action,
        "runtime_boundary": runtime_boundary,
        "payload": payload,
        "markdown": "\n".join(md_lines) + "\n",
    }


__all__ = ["build_digital_products_post_approval_simulation_plan_content"]
