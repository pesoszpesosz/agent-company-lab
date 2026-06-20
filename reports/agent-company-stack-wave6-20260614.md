# Agent Company Stack Wave 6 - 2026-06-14

## Scope

This is a source-backed current repo metadata refresh for the `platform_engineering` lane. It uses read-only GitHub repository metadata collected on 2026-06-14 and updates the agent-company architecture decision for money-path execution.

No browser session, account registration, legal/KYC/tax/payment action, wallet action, API/model call, public post, marketplace listing, bounty claim, PR comment, trade, deposit, withdrawal, or real-money action was performed.

## Executive Decision

Keep the SQLite company ledger as the source of truth. Do not adopt a new top-level agent framework yet.

Promote two next local infrastructure tasks:

1. `service_request_execution_plan.v1`: schema and approval-safe worker packets for read-only service requests.
2. `source_freshness_scheduler.v1`: local planner for recurring source checks without executing browser/account/API/payment/public work.

Use OpenAI Agents, Pydantic AI, and LangGraph as adapters, not as the control plane. Browser Use and Skyvern remain service-worker candidates only behind `browser_read_only_session`. Temporal, DBOS, Hatchet, Inngest, and Trigger remain durable-workflow candidates, but only after the local service-request lifecycle has enough repeated approved work to justify them. Langfuse and Phoenix remain observability candidates after local trace density and UI needs grow beyond Markdown/SQLite reports.

## Current Source Table

| Repo | Category | Stars | Forks | Latest release | Release date | Updated | Platform use |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| `openai/openai-agents-python` | agent runtime | 27,141 | 4,190 | `v0.17.5` | 2026-06-11 | 2026-06-14 | Static/sandbox adapter first; model/API mode stays gated. |
| `pydantic/pydantic-ai` | agent runtime | 17,751 | 2,213 | `v1.107.0 (2026-06-10)` | 2026-06-10 | 2026-06-14 | Offline typed/TestModel adapter remains useful. |
| `langchain-ai/langgraph` | agent runtime | 34,712 | 5,826 | `langgraph==1.2.5` | 2026-06-12 | 2026-06-14 | Static graph adapter and orchestration pattern, not ledger. |
| `modelcontextprotocol/modelcontextprotocol` | protocol | 8,398 | 1,589 | `2025-11-25` | 2025-11-25 | 2026-06-14 | First protocol layer for tools and services. |
| `a2aproject/A2A` | protocol | 24,280 | 2,465 | `v1.0.1` | 2026-05-28 | 2026-06-14 | Later interop layer for independent agent apps. |
| `temporalio/temporal` | durable workflow | 20,966 | 1,655 | `v1.29.7` | 2026-06-12 | 2026-06-14 | Candidate for approved service-job durability. |
| `dbos-inc/dbos-transact-py` | durable workflow | 1,419 | 71 | `2.23.0` | 2026-06-01 | 2026-06-14 | Lightweight Python durable workflow candidate. |
| `browser-use/browser-use` | browser worker | 98,793 | 11,022 | `0.13.2` | 2026-06-12 | 2026-06-14 | Browser worker only behind scoped approval. |
| `Skyvern-AI/skyvern` | browser worker | 21,907 | 2,038 | `Release v1.0.41` | 2026-06-11 | 2026-06-14 | Browser worker only behind scoped approval. |
| `langfuse/langfuse` | observability | 29,057 | 3,011 | `v3.185.0` | 2026-06-12 | 2026-06-14 | Candidate after local trace density grows. |
| `Arize-ai/phoenix` | observability | 10,130 | 923 | `arize-phoenix: v17.5.0` | 2026-06-12 | 2026-06-14 | Candidate after local trace data needs UI/evals. |
| `hatchet-dev/hatchet` | durable workflow | 7,341 | 416 | `Hatchet v0.89.0` | 2026-06-10 | 2026-06-14 | Evaluate only after service execution plans are used. |
| `inngest/inngest` | durable workflow | 5,488 | 318 | `v1.27.0` | 2026-06-09 | 2026-06-14 | Step-function candidate for approved jobs. |
| `triggerdotdev/trigger.dev` | durable workflow | 15,342 | 1,302 | `trigger.dev v4.4.6` | 2026-05-12 | 2026-06-14 | Managed workflow candidate later, not immediate. |

Machine-readable mirror: `E:\agent-company-lab\data\curated-infra-repos-wave6-20260614.json`.

## Architecture Implications

The multi-agent company should be a ledger plus packets plus service gates plus runtime adapters plus observability. It should not be "one framework" with free-running authority.

Protocol layer:

- MCP first for tools and services.
- A2A later for independent agent-app interoperability.

Browser-service layer:

- Must include exact URL scope.
- Must list allowed pages and allowed actions.
- Must list prohibited actions.
- Must require evidence artifacts.
- Must define stop conditions.

Durable workflow:

- Should manage approved service jobs.
- Should not manage lane creativity or approval decisions.
- Should only be introduced after repeated approved service execution creates operational pain in the SQLite/CLI lifecycle.

Observability:

- Local `trace_events` and artifact reports remain enough for now.
- Langfuse/Phoenix become useful when traces are dense enough that filtering, evals, and UI inspection materially improve decisions.

## Money-Making Implication

The immediate unblock is not more autonomous browsing. The immediate unblock is creating safe service execution packets so the user can approve one read-only marketplace/security/paid-code check with exact scope and stop conditions.

Best near-term lane remains `digital_products_templates_plugins` because the lab already has:

- local Agent Skill Starter Kit v0 product folder;
- marketplace readiness matrix;
- direct-download listing readiness packet;
- package manifest/checklist;
- blocked service requests for marketplace terms and legal/payment review.

Secondary lanes:

- `security_bounty_private_reports`: read-only rules/scope checks after approval.
- `paid_code_bounties`: read-only bounty verification after approval.
- `money_source_discovery`: source freshness checks after read-only browser/current-source approval.

## Selected Next Build

Create `service_request_execution_plan.v1` and one concrete plan for `req-next-wave-digital-marketplace-browser-readonly-20260614`.

Required scope for that plan:

- public pages only;
- Gumroad, Lemon Squeezy, and PromptBase terms/fees/listing requirements;
- no login;
- no signup;
- no seller account creation;
- no listing/upload;
- no payment setup;
- no legal/tax/KYC commitment;
- no public action;
- evidence-only output.

This selected next build is a local artifact and does not approve or start the service request.

## Gate State

- External actions performed: no.
- Browser actions performed: no.
- Public actions performed: no.
- API/model actions performed: no.
- Real-money actions performed: no.
- Digital marketplace service requests remain `needs_review`.
