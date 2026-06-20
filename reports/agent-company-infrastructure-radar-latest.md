# Agent Company Infrastructure Radar

Generated UTC: 2026-06-16T10:59:47Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-infrastructure-radar-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-infrastructure-radar-validation-latest.json`

## Decision

`agent_company_infrastructure_radar_ready_for_department_design`

Created a primary-source-backed infrastructure radar for the agent company: durable orchestration spine, stateful manager graphs, guarded tool agents, department templates, and approval gates.

## Primary Sources

| Source | Type | Agent Company Takeaway | URL |
| --- | --- | --- | --- |
| LangGraph | `official_github` | Use for stateful CEO/manager graphs, subagent planning, human review pauses, and auditable long-running investigations. | https://github.com/langchain-ai/langgraph |
| CrewAI | `official_github` | Use as the clearest role/team metaphor for departments, managers, seekers, task delegation, and work package templates. | https://github.com/crewAIInc/crewAI |
| Microsoft AutoGen | `official_github` | Use as a reference for agent-to-agent protocols, group chat coordination, and distributed runtime boundaries. | https://github.com/microsoft/autogen |
| Temporal | `official_docs` | Use as the model for durable request lifecycles, retries, suspended work, replayable audit, and worker pools. | https://docs.temporal.io/temporal |
| OpenAI Agents SDK | `official_docs` | Use for local role agents, callable tools, handoffs, guardrails, traceability, and sandboxed execution boundaries. | https://developers.openai.com/api/docs/libraries#use-the-agents-sdk |

## Recommended Spine

- Temporal-style durable service request lifecycle for every path and worker action.
- LangGraph-style stateful CEO/manager/seeker graphs for planning and review.
- OpenAI Agents SDK-style guarded tools, handoffs, tracing, and sandbox execution.
- CrewAI-style department templates for role definitions and repeatable task packets.

## Architecture Mapping

| Layer | Stack | Responsibility |
| --- | --- | --- |
| CEO | Temporal, LangGraph | Portfolio state, policy, priorities, approvals, kill/promote decisions. |
| Managers | LangGraph, CrewAI | Lane plans, task decomposition, evidence quality, worker handoffs. |
| Seekers | OpenAI Agents SDK, LangGraph | Research money paths, normalize leads, write proof packets. |
| Workers | Temporal, OpenAI Agents SDK | Execute approved local tasks, draft artifacts, run scanners, maintain state. |
| Action gates | Temporal, OpenAI Agents SDK guardrails | Pause registration, wallets, payments, public submissions, real-money, and security testing. |
| Evidence ledger | SQLite now, Temporal history later | Durable records for sources, reports, decisions, and next actions. |
| Observability | OpenAI tracing, LangSmith-style traces, local reports | Trace handoffs, tool calls, decisions, failures, and ROI outcomes. |

## Cashflow Lanes

| Lane | Agent Type | Gate |
| --- | --- | --- |
| `paid_code_bounties` | `seeker+patch_worker` | `public_submission_or_pr_requires_operator_approval` |
| `security_bounties` | `scope_researcher+report_drafter` | `security_testing_beyond_read_only_requires_scope_approval` |
| `prediction_markets` | `market_scout+paper_trade_auditor` | `real_money_trading_requires_capital_and_operator_approval` |
| `digital_products` | `demand_researcher+asset_builder` | `marketplace_posting_or_account_action_requires_operator_approval` |
| `affiliate_leads` | `source_scout+compliance_reviewer` | `signup_or outreach requires account and policy approval` |
| `data_arbitrage` | `dataset_scout+license_reviewer` | `paid data access or scraping needs legal review` |
| `automation_services` | `client_researcher+proposal_drafter` | `client contact or offer submission requires approval` |
| `open_source_products` | `repo_scout+maintainer` | `publishing packages, releases, or pricing requires approval` |

## Approval Gates

- `registration_or_login`
- `wallet_or_payment_method`
- `real_money_trade_or_spend`
- `public_submission_or_marketplace_post`
- `security_testing_beyond_read_only`
- `personal_data_or_sensitive_browser_submission`

## Boundary

This radar is local research infrastructure. It does not install dependencies, start workers, call APIs, open browsers, register accounts, create wallets, spend money, submit reports, post publicly, or perform security testing.

## Next Action

Turn this radar into a department architecture packet with concrete tables, service request types, thread templates, and worker pool interfaces.

