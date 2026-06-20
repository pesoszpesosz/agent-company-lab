from __future__ import annotations

from pathlib import Path
from typing import Any


DEFAULT_APPROVAL_GATES = [
    "registration_or_login",
    "wallet_or_payment_method",
    "real_money_trade_or_spend",
    "public_submission_or_marketplace_post",
    "security_testing_beyond_read_only",
    "personal_data_or_sensitive_browser_submission",
]


def build_agent_company_department_architecture_packet_model(approval_gates: list[str] | None = None) -> dict[str, Any]:
    departments = [
        {"department_id": "ceo_office", "purpose": "Portfolio policy, approval, capital allocation, kill/promote decisions.", "manager_role": "ceo_agent", "default_stack": ["Temporal", "LangGraph"]},
        {"department_id": "platform_engineering", "purpose": "Schemas, orchestration, worker pools, evidence integrity, observability.", "manager_role": "platform_manager", "default_stack": ["Temporal", "OpenAI Agents SDK"]},
        {"department_id": "opportunity_research", "purpose": "Find and normalize new online money paths and source-backed leads.", "manager_role": "research_manager", "default_stack": ["LangGraph", "OpenAI Agents SDK"]},
        {"department_id": "bounty_and_security", "purpose": "Paid code bounties, public code review, report drafting, security scope control.", "manager_role": "bounty_manager", "default_stack": ["LangGraph", "CrewAI"]},
        {"department_id": "markets_and_capital", "purpose": "Prediction markets, paper trades, capital gates, risk ledgers.", "manager_role": "market_manager", "default_stack": ["Temporal", "LangGraph"]},
        {"department_id": "digital_products", "purpose": "Demand research, asset creation, quality, packaging, marketplace readiness.", "manager_role": "product_manager", "default_stack": ["CrewAI", "OpenAI Agents SDK"]},
        {"department_id": "compliance_and_approvals", "purpose": "Registration, wallets, public actions, real-money, policy, and rollback approvals.", "manager_role": "compliance_manager", "default_stack": ["Temporal", "guardrails"]},
    ]
    table_blueprints = [
        {"table": "agent_threads", "purpose": "One row per IDE/chat agent thread with lane, role, state, owner, and handoff status."},
        {"table": "departments", "purpose": "Department definitions, manager role, active lanes, and escalation policy."},
        {"table": "money_paths", "purpose": "Canonical online money path taxonomy with legality, payout, proofability, and gates."},
        {"table": "opportunity_leads", "purpose": "Normalized leads from seekers, including source, payout, account needs, next action."},
        {"table": "worker_pool_interfaces", "purpose": "Local worker capabilities, allowed inputs, forbidden actions, and approval requirements."},
        {"table": "approval_gates", "purpose": "Durable gate records for login, wallet, payment, public action, security testing, and personal data."},
        {"table": "evidence_packets", "purpose": "Structured proof artifacts, source backing, confidence, and reviewer notes."},
        {"table": "task_handoffs", "purpose": "Agent-to-agent handoffs, requested worker type, response artifact, and status."},
        {"table": "experiment_runs", "purpose": "Paper-trade, scanner, local build, and research experiment metrics."},
        {"table": "roi_ledger", "purpose": "Expected value, time spent, realized revenue, costs, and killed-lane reasons."},
    ]
    service_request_types = [
        "research_money_path",
        "normalize_opportunity_lead",
        "draft_bounty_patch",
        "draft_security_report",
        "paper_trade_market",
        "build_digital_asset",
        "quality_review_artifact",
        "request_registration_worker",
        "request_wallet_worker",
        "request_public_submission",
        "request_real_money_action",
        "request_security_scope_review",
    ]
    thread_templates = [
        {"template_id": "ceo_review_thread", "role": "CEO", "starts_with": "portfolio status, blockers, promote/kill recommendations"},
        {"template_id": "department_manager_thread", "role": "Manager", "starts_with": "lane queue, evidence gaps, worker requests"},
        {"template_id": "money_path_seeker_thread", "role": "Seeker", "starts_with": "source scan, lead normalization, next proof artifact"},
        {"template_id": "bounty_worker_thread", "role": "Worker", "starts_with": "repo scope, issue proof, patch/report draft"},
        {"template_id": "market_worker_thread", "role": "Worker", "starts_with": "market hypothesis, paper-trade record, risk memo"},
        {"template_id": "product_worker_thread", "role": "Worker", "starts_with": "demand proof, asset draft, packaging checklist"},
        {"template_id": "approval_worker_thread", "role": "Gatekeeper", "starts_with": "exact requested gated action, scope, rollback, expiration"},
        {"template_id": "observability_thread", "role": "Auditor", "starts_with": "chain integrity, stale evidence, ROI drift"},
    ]
    worker_pool_interfaces = [
        {"pool_id": "research_scout_pool", "allowed": "public-source research and local summaries", "forbidden": "login, outreach, purchase"},
        {"pool_id": "code_patch_pool", "allowed": "local code review, patch drafts, tests", "forbidden": "PR submission without approval"},
        {"pool_id": "security_review_pool", "allowed": "read-only public code review", "forbidden": "probing live systems without scope"},
        {"pool_id": "market_analysis_pool", "allowed": "paper trading and local market notes", "forbidden": "real-money orders"},
        {"pool_id": "asset_build_pool", "allowed": "local product drafts and packaging", "forbidden": "marketplace posting"},
        {"pool_id": "account_gate_pool", "allowed": "approval packet drafting", "forbidden": "registration/login without approval"},
        {"pool_id": "observability_pool", "allowed": "local chain audits and report refresh", "forbidden": "state mutation outside approved commands"},
    ]
    selected_approval_gates = approval_gates or DEFAULT_APPROVAL_GATES
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
        "department_architecture_packet_count": 1,
        "department_count": len(departments),
        "table_blueprint_count": len(table_blueprints),
        "service_request_type_count": len(service_request_types),
        "thread_template_count": len(thread_templates),
        "worker_pool_interface_count": len(worker_pool_interfaces),
        "approval_gate_count": len(selected_approval_gates),
        "departments": departments,
        "table_blueprints": table_blueprints,
        "service_request_types": service_request_types,
        "thread_templates": thread_templates,
        "worker_pool_interfaces": worker_pool_interfaces,
        "approval_gates": selected_approval_gates,
        "local_decision": "agent_company_department_architecture_packet_ready_for_schema_plan",
        "recommended_default": "materialize_schema_plan_next_without_starting_workers_or_external_actions",
        "summary": "Converted the infrastructure radar into a concrete department architecture packet: departments, table blueprints, service request types, thread templates, worker pool interfaces, and approval gates.",
        "next_action": "Materialize a schema plan for these tables and request types next, without starting workers or taking external actions.",
        "runtime_boundary": runtime_boundary,
    }


def build_agent_company_department_architecture_packet_markdown_lines(
    *,
    model: dict[str, Any],
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
) -> list[str]:
    lines = [
        "# Agent Company Department Architecture Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{model['local_decision']}`",
        "",
        str(model["summary"]),
        "",
        "## Departments",
        "",
        "| Department | Manager | Purpose | Stack |",
        "| --- | --- | --- | --- |",
    ]
    for item in model["departments"]:
        lines.append(f"| `{item['department_id']}` | `{item['manager_role']}` | {item['purpose']} | {', '.join(item['default_stack'])} |")
    lines.extend(["", "## Table Blueprints", ""])
    lines.extend(f"- `{item['table']}`: {item['purpose']}" for item in model["table_blueprints"])
    lines.extend(["", "## Service Request Types", ""])
    lines.extend(f"- `{item}`" for item in model["service_request_types"])
    lines.extend(["", "## Thread Templates", ""])
    lines.extend(f"- `{item['template_id']}` ({item['role']}): {item['starts_with']}" for item in model["thread_templates"])
    lines.extend(["", "## Worker Pool Interfaces", ""])
    lines.extend(f"- `{item['pool_id']}`: allowed={item['allowed']}; forbidden={item['forbidden']}" for item in model["worker_pool_interfaces"])
    lines.extend(["", "## Approval Gates", ""])
    lines.extend(f"- `{gate}`" for gate in model["approval_gates"])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet is local architecture only. It does not create tables, start workers, assign requests, call APIs, open browsers, register accounts, create wallets, spend money, submit reports, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            str(model["next_action"]),
            "",
        ]
    )
    return lines


__all__ = [
    "build_agent_company_department_architecture_packet_markdown_lines",
    "build_agent_company_department_architecture_packet_model",
]
