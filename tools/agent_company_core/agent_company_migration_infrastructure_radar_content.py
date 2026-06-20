from __future__ import annotations


def build_agent_company_infrastructure_radar_model() -> dict[str, object]:
    primary_sources = [
            {
                "source_id": "langgraph_github",
                "name": "LangGraph",
                "url": "https://github.com/langchain-ai/langgraph",
                "source_type": "official_github",
                "observed_fact": "Low-level orchestration framework for long-running, stateful agents with durable execution, human-in-the-loop, memory, tracing, and deployment support.",
                "agent_company_takeaway": "Use for stateful CEO/manager graphs, subagent planning, human review pauses, and auditable long-running investigations.",
            },
            {
                "source_id": "crewai_github",
                "name": "CrewAI",
                "url": "https://github.com/crewAIInc/crewAI",
                "source_type": "official_github",
                "observed_fact": "Crews model role-based autonomous collaboration; Flows provide production-ready event-driven workflows, secure state management, and conditional branching.",
                "agent_company_takeaway": "Use as the clearest role/team metaphor for departments, managers, seekers, task delegation, and work package templates.",
            },
            {
                "source_id": "autogen_github",
                "name": "Microsoft AutoGen",
                "url": "https://github.com/microsoft/autogen",
                "source_type": "official_github",
                "observed_fact": "Core API implements message passing, event-driven agents, and local/distributed runtime; AgentChat supports common multi-agent patterns.",
                "agent_company_takeaway": "Use as a reference for agent-to-agent protocols, group chat coordination, and distributed runtime boundaries.",
            },
            {
                "source_id": "temporal_docs",
                "name": "Temporal",
                "url": "https://docs.temporal.io/temporal",
                "source_type": "official_docs",
                "observed_fact": "Temporal is a scalable runtime for durable executions; workflows preserve state through failures, workers execute code, and event history is source of truth.",
                "agent_company_takeaway": "Use as the model for durable request lifecycles, retries, suspended work, replayable audit, and worker pools.",
            },
            {
                "source_id": "openai_agents_sdk_docs",
                "name": "OpenAI Agents SDK",
                "url": "https://developers.openai.com/api/docs/libraries#use-the-agents-sdk",
                "source_type": "official_docs",
                "observed_fact": "Agents SDK is intended for code-first orchestration of agents, tools, handoffs, guardrails, tracing, and sandbox execution.",
                "agent_company_takeaway": "Use for local role agents, callable tools, handoffs, guardrails, traceability, and sandboxed execution boundaries.",
            },
        ]
    candidates = [
            {
                "candidate_id": "temporal_durable_spine",
                "source_id": "temporal_docs",
                "fit": "durable_orchestration_spine",
                "recommended_role": "system_of_record_for_workflow_state",
                "why": "The agent company needs long-lived service requests, paused approvals, retries, and replayable state.",
                "risk": "Needs careful deterministic workflow design and activity boundaries for model calls and external actions.",
            },
            {
                "candidate_id": "langgraph_stateful_manager_layer",
                "source_id": "langgraph_github",
                "fit": "stateful_agent_graphs",
                "recommended_role": "ceo_manager_seeker_graphs",
                "why": "Maps naturally to long-running stateful agents, subgraphs, human-in-the-loop checkpoints, and memory.",
                "risk": "Should not be the only durable system of record until persistence/replay boundaries are explicit.",
            },
            {
                "candidate_id": "openai_agents_sdk_guarded_tool_layer",
                "source_id": "openai_agents_sdk_docs",
                "fit": "guarded_tool_agents",
                "recommended_role": "tool_calling_handoffs_guardrails_tracing",
                "why": "Directly matches the need for specialized agents, handoffs, tool schemas, guardrails, tracing, and sandboxing.",
                "risk": "Model/API cost and external side effects need explicit budget and action gates.",
            },
            {
                "candidate_id": "crewai_department_pattern",
                "source_id": "crewai_github",
                "fit": "role_based_department_design",
                "recommended_role": "department_templates_and_task_delegation",
                "why": "Crews and Flows provide a clean vocabulary for role-based work and event-driven process control.",
                "risk": "Must separate autonomous brainstorming from approval-gated execution.",
            },
            {
                "candidate_id": "autogen_agent_protocol_reference",
                "source_id": "autogen_github",
                "fit": "agent_to_agent_runtime_patterns",
                "recommended_role": "message_passing_and_group_coordination_reference",
                "why": "Event-driven agents and distributed runtime concepts are useful for multi-chat, multi-worker coordination.",
                "risk": "Framework migration churn and overlapping abstractions require a narrow adoption surface.",
            },
        ]
    architecture_mappings = [
            {"layer": "CEO", "recommended_stack": ["Temporal", "LangGraph"], "responsibility": "Portfolio state, policy, priorities, approvals, kill/promote decisions."},
            {"layer": "Managers", "recommended_stack": ["LangGraph", "CrewAI"], "responsibility": "Lane plans, task decomposition, evidence quality, worker handoffs."},
            {"layer": "Seekers", "recommended_stack": ["OpenAI Agents SDK", "LangGraph"], "responsibility": "Research money paths, normalize leads, write proof packets."},
            {"layer": "Workers", "recommended_stack": ["Temporal", "OpenAI Agents SDK"], "responsibility": "Execute approved local tasks, draft artifacts, run scanners, maintain state."},
            {"layer": "Action gates", "recommended_stack": ["Temporal", "OpenAI Agents SDK guardrails"], "responsibility": "Pause registration, wallets, payments, public submissions, real-money, and security testing."},
            {"layer": "Evidence ledger", "recommended_stack": ["SQLite now", "Temporal history later"], "responsibility": "Durable records for sources, reports, decisions, and next actions."},
            {"layer": "Observability", "recommended_stack": ["OpenAI tracing", "LangSmith-style traces", "local reports"], "responsibility": "Trace handoffs, tool calls, decisions, failures, and ROI outcomes."},
        ]
    recommended_spine = [
            "Temporal-style durable service request lifecycle for every path and worker action.",
            "LangGraph-style stateful CEO/manager/seeker graphs for planning and review.",
            "OpenAI Agents SDK-style guarded tools, handoffs, tracing, and sandbox execution.",
            "CrewAI-style department templates for role definitions and repeatable task packets.",
        ]
    cashflow_lane_mappings = [
            {"lane": "paid_code_bounties", "agent_type": "seeker+patch_worker", "gate": "public_submission_or_pr_requires_operator_approval"},
            {"lane": "security_bounties", "agent_type": "scope_researcher+report_drafter", "gate": "security_testing_beyond_read_only_requires_scope_approval"},
            {"lane": "prediction_markets", "agent_type": "market_scout+paper_trade_auditor", "gate": "real_money_trading_requires_capital_and_operator_approval"},
            {"lane": "digital_products", "agent_type": "demand_researcher+asset_builder", "gate": "marketplace_posting_or_account_action_requires_operator_approval"},
            {"lane": "affiliate_leads", "agent_type": "source_scout+compliance_reviewer", "gate": "signup_or outreach requires account and policy approval"},
            {"lane": "data_arbitrage", "agent_type": "dataset_scout+license_reviewer", "gate": "paid data access or scraping needs legal review"},
            {"lane": "automation_services", "agent_type": "client_researcher+proposal_drafter", "gate": "client contact or offer submission requires approval"},
            {"lane": "open_source_products", "agent_type": "repo_scout+maintainer", "gate": "publishing packages, releases, or pricing requires approval"},
        ]
    approval_gates = [
            "registration_or_login",
            "wallet_or_payment_method",
            "real_money_trade_or_spend",
            "public_submission_or_marketplace_post",
            "security_testing_beyond_read_only",
            "personal_data_or_sensitive_browser_submission",
        ]
    return {
        "infrastructure_radar_count": 1,
        "primary_sources": primary_sources,
        "candidates": candidates,
        "architecture_mappings": architecture_mappings,
        "recommended_spine": recommended_spine,
        "cashflow_lane_mappings": cashflow_lane_mappings,
        "approval_gates": approval_gates,
        "primary_source_count": len(primary_sources),
        "candidate_count": len(candidates),
        "architecture_mapping_count": len(architecture_mappings),
        "recommended_spine_count": len(recommended_spine),
        "cashflow_lane_mapping_count": len(cashflow_lane_mappings),
        "approval_gate_count": len(approval_gates),
    }


__all__ = ["build_agent_company_infrastructure_radar_model"]
