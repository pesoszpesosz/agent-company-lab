# Agent Company Department Architecture Packet

Generated UTC: 2026-06-16T11:10:37Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-department-architecture-packet-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-department-architecture-packet-validation-latest.json`

## Decision

`agent_company_department_architecture_packet_ready_for_schema_plan`

Converted the infrastructure radar into a concrete department architecture packet: departments, table blueprints, service request types, thread templates, worker pool interfaces, and approval gates.

## Departments

| Department | Manager | Purpose | Stack |
| --- | --- | --- | --- |
| `ceo_office` | `ceo_agent` | Portfolio policy, approval, capital allocation, kill/promote decisions. | Temporal, LangGraph |
| `platform_engineering` | `platform_manager` | Schemas, orchestration, worker pools, evidence integrity, observability. | Temporal, OpenAI Agents SDK |
| `opportunity_research` | `research_manager` | Find and normalize new online money paths and source-backed leads. | LangGraph, OpenAI Agents SDK |
| `bounty_and_security` | `bounty_manager` | Paid code bounties, public code review, report drafting, security scope control. | LangGraph, CrewAI |
| `markets_and_capital` | `market_manager` | Prediction markets, paper trades, capital gates, risk ledgers. | Temporal, LangGraph |
| `digital_products` | `product_manager` | Demand research, asset creation, quality, packaging, marketplace readiness. | CrewAI, OpenAI Agents SDK |
| `compliance_and_approvals` | `compliance_manager` | Registration, wallets, public actions, real-money, policy, and rollback approvals. | Temporal, guardrails |

## Table Blueprints

- `agent_threads`: One row per IDE/chat agent thread with lane, role, state, owner, and handoff status.
- `departments`: Department definitions, manager role, active lanes, and escalation policy.
- `money_paths`: Canonical online money path taxonomy with legality, payout, proofability, and gates.
- `opportunity_leads`: Normalized leads from seekers, including source, payout, account needs, next action.
- `worker_pool_interfaces`: Local worker capabilities, allowed inputs, forbidden actions, and approval requirements.
- `approval_gates`: Durable gate records for login, wallet, payment, public action, security testing, and personal data.
- `evidence_packets`: Structured proof artifacts, source backing, confidence, and reviewer notes.
- `task_handoffs`: Agent-to-agent handoffs, requested worker type, response artifact, and status.
- `experiment_runs`: Paper-trade, scanner, local build, and research experiment metrics.
- `roi_ledger`: Expected value, time spent, realized revenue, costs, and killed-lane reasons.

## Service Request Types

- `research_money_path`
- `normalize_opportunity_lead`
- `draft_bounty_patch`
- `draft_security_report`
- `paper_trade_market`
- `build_digital_asset`
- `quality_review_artifact`
- `request_registration_worker`
- `request_wallet_worker`
- `request_public_submission`
- `request_real_money_action`
- `request_security_scope_review`

## Thread Templates

- `ceo_review_thread` (CEO): portfolio status, blockers, promote/kill recommendations
- `department_manager_thread` (Manager): lane queue, evidence gaps, worker requests
- `money_path_seeker_thread` (Seeker): source scan, lead normalization, next proof artifact
- `bounty_worker_thread` (Worker): repo scope, issue proof, patch/report draft
- `market_worker_thread` (Worker): market hypothesis, paper-trade record, risk memo
- `product_worker_thread` (Worker): demand proof, asset draft, packaging checklist
- `approval_worker_thread` (Gatekeeper): exact requested gated action, scope, rollback, expiration
- `observability_thread` (Auditor): chain integrity, stale evidence, ROI drift

## Worker Pool Interfaces

- `research_scout_pool`: allowed=public-source research and local summaries; forbidden=login, outreach, purchase
- `code_patch_pool`: allowed=local code review, patch drafts, tests; forbidden=PR submission without approval
- `security_review_pool`: allowed=read-only public code review; forbidden=probing live systems without scope
- `market_analysis_pool`: allowed=paper trading and local market notes; forbidden=real-money orders
- `asset_build_pool`: allowed=local product drafts and packaging; forbidden=marketplace posting
- `account_gate_pool`: allowed=approval packet drafting; forbidden=registration/login without approval
- `observability_pool`: allowed=local chain audits and report refresh; forbidden=state mutation outside approved commands

## Approval Gates

- `registration_or_login`
- `wallet_or_payment_method`
- `real_money_trade_or_spend`
- `public_submission_or_marketplace_post`
- `security_testing_beyond_read_only`
- `personal_data_or_sensitive_browser_submission`

## Boundary

This packet is local architecture only. It does not create tables, start workers, assign requests, call APIs, open browsers, register accounts, create wallets, spend money, submit reports, post publicly, or perform security testing.

## Next Action

Materialize a schema plan for these tables and request types next, without starting workers or taking external actions.

