# Agent Company Infrastructure Research

Date: 2026-06-14  
Workspace: `E:\agent-company-lab`  
Source lab imported: `E:\profit-edge-lab`  

## Executive Decision

Build an agent-company operating system before launching more money-seeking agents.

The immediate failure mode in the current setup is not lack of agent effort. It is missing coordination: two workers can read the same queue, chase the same payout lane, and confuse ownership. Scaling that pattern would create more duplicated work, reputation risk, and account-action risk.

The next system should have:

1. A CEO/orchestrator that owns portfolio allocation and lane ownership.
2. Department managers for each money path.
3. Seekers that only discover and normalize opportunities.
4. Evidence builders that produce proofs, patches, simulations, reports, or draft packets.
5. Service departments for account registration, wallet operations, browser actions, public communications, and risk review.
6. A durable queue, artifact store, trace store, approval queue, and outcome ledger.

## Current Local Assets To Reuse

### `E:\profit-edge-lab`

Useful as a lane prototype. It already has:

- Opportunity scanners for paid code, security bounties, prediction markets, Kalshi, Polymarket, Algora, Opire, BountyHub, Gibwork, ProjectDiscovery, UnitOneAI, IssueHunt, Sherlock, and GitHub bounty pulse.
- Queue generation: `reports\daily-action-queue-latest.md/json`.
- Ledger: `opportunities\opportunity-ledger.jsonl`.
- SQLite learning DB: `state\profit_edge.sqlite`.
- Outcome recorder: `scripts\Record-Outcome.ps1`.
- Strategy evolution and market replay machinery.

Problem to fix before reuse: the shared daily queue promotes one global next action, so independent workers can duplicate the same lane. The new infrastructure needs lane ownership and task leases.

### `C:\Users\matth\Documents\Codex\2026-06-12\recovered-x-account-manager`

Useful for social/growth department. Existing skills include:

- `x-ai-profile-manager`
- `x-fast-reply-executor`
- `x-radar-research`
- `grok-x-research`

Grok API keys were missing in the current shell. Web Grok is possible but operationally brittle and should be wrapped as a service worker, not used ad hoc by every agent.

### `E:\hermes_agent_latest`

Useful as a local agent-runtime reference. It contains:

- `mcp_serve.py`
- `batch_runner.py`
- `run_agent.py`
- `hermes_state.py`
- `skills/`
- `tools/`
- `gateway/`
- Docker and CLI config examples.

This should be inspected as an implementation source before building from scratch.

### `E:\openclaw-unified`

Useful as a local operations platform and memory/account reference. It contains:

- `ops/`
- `memory/`
- `accounts.json`
- `accounts_master.csv/xlsx`
- `codex-session-broker/`
- `v2/`

Risk: account material must not be casually consumed by new agents. The new company needs a secret/access layer.

## Current Open-Source Landscape

Raw data saved:

- `E:\agent-company-lab\data\curated-infra-repos-20260614.json`
- `E:\agent-company-lab\data\curated-infra-repos-20260614.csv`
- `E:\agent-company-lab\data\github-search-*.json`

### Agent Frameworks

| Candidate | Current signal | Fit |
| --- | ---: | --- |
| `langchain-ai/langgraph` | 34,691 stars, active 2026-06-14 | Best fit for stateful, durable, human-in-loop agent workflows. |
| `openai/openai-agents-python` | 27,137 stars, active 2026-06-13 | Good fit for typed tools, handoffs, guardrails, tracing, sandbox agents. |
| `crewAIInc/crewAI` | 53,523 stars, active 2026-06-14 | Good fit for role/crew metaphors; likely fast for prototypes. |
| `microsoft/semantic-kernel` / Microsoft Agent Framework | 28,115 stars for Semantic Kernel | Best fit if we standardize on Microsoft/.NET/enterprise connectors. |
| `microsoft/autogen` | 58,940 stars but maintenance-mode signal | Useful conceptually; avoid betting new core on old AutoGen line. |
| `pydantic/pydantic-ai` | 17,746 stars, active | Good fit for typed Python agent tools and strict schemas. |
| `FoundationAgents/MetaGPT` / `OpenBMB/ChatDev` | Company/team metaphors | Useful inspiration, less likely core infra choice. |

Recommendation: start with a thin internal orchestration schema that can run Codex-thread agents today, then prototype LangGraph or OpenAI Agents SDK as the first programmable orchestrator. Do not hard-couple business state to a framework-specific memory layer.

### Workflow Engines and Durable Execution

| Candidate | Current signal | Fit |
| --- | ---: | --- |
| `temporalio/temporal` | 20,961 stars, active | Strongest durable execution model for long-running workflows and retries. |
| `PrefectHQ/prefect` | 22,602 stars | Good for scheduled data/scanner flows. |
| `dagster-io/dagster` | 15,682 stars | Good for data assets and materialized reports. |
| `apache/airflow` | 45,803 stars | Mature scheduler, heavier and less agent-native. |
| `ray-project/ray` | 42,865 stars | Useful for distributed compute/backtests, not the primary business queue. |

Recommendation: use SQLite/Postgres task tables first; add Temporal when side-effect workflows need durable retries and human approval resumption. Prefect/Dagster can run scanner/report pipelines.

### Browser and Computer-Use Workers

| Candidate | Current signal | Fit |
| --- | ---: | --- |
| `browser-use/browser-use` | 98,747 stars | Strong browser-agent ecosystem; evaluate for web tasks with screenshots and recovery. |
| `browser-use/browser-harness` | 14,797 stars | Lower-level CDP harness; useful for controlled browser workers. |
| `vercel-labs/agent-browser` | 36,020 stars | New Rust CLI browser automation candidate. |
| Codex in-app browser skills | Already installed | Best current route for local browser tasks, but must be wrapped with gates. |

Recommendation: browser workers should be service departments, not general agent powers. They receive a scoped request, run, save proof, and stop at login/terms/payment gates.

### Protocols and Tool Registries

| Candidate | Current signal | Fit |
| --- | ---: | --- |
| MCP | `modelcontextprotocol/servers`: 87,195 stars | Best current tool/context integration protocol. |
| A2A | `a2aproject/A2A`: 24,275 stars | Best current agent-to-agent interoperability protocol. |
| FastMCP | 25,620 stars under current repo metadata | Useful for building internal MCP servers quickly. |

Recommendation: use MCP internally for service tools and data sources. Use A2A later for inter-agent messaging if multiple runtimes need to interoperate. Do not expose arbitrary MCP servers without review; MCP has real RCE/supply-chain risk.

### Observability, Evals, and Prompt Management

| Candidate | Current signal | Fit |
| --- | ---: | --- |
| `langfuse/langfuse` | 29,039 stars | Strong open-source tracing, prompt management, evals, cost/latency tracking. |
| `Arize-ai/phoenix` | 10,130 stars | Strong local/self-host tracing and evaluations via OpenTelemetry/OpenInference. |
| OpenAI Agents SDK tracing | Built in | Useful if using Agents SDK. |

Recommendation: instrument every agent run with trace IDs, task IDs, source IDs, cost estimates, and artifact paths. Start simple in SQLite/JSONL, then add Langfuse or Phoenix when run volume grows.

### Visual/Low-Code Workflow Platforms

| Candidate | Current signal | Fit |
| --- | ---: | --- |
| `n8n-io/n8n` | 192,443 stars | Excellent deterministic workflow automations and integrations. |
| `langgenius/dify` | 145,153 stars | Visual agentic workflow builder, RAG, model management, observability integrations. |
| `FlowiseAI/Flowise` | 53,558 stars | Visual LLM workflow builder. |

Recommendation: use these for deterministic service workflows and dashboards, not as the central source of truth. Security matters: exposed workflow engines are high-risk if misconfigured.

## Architecture Model

### Layer 1: Company Control Plane

Required tables:

- `agents`: agent identity, role, owner thread, model, permissions, status.
- `departments`: money lane groupings and managers.
- `lanes`: money path taxonomy, gates, active owner, promotion criteria.
- `tasks`: durable work items with leases, dependencies, priority, and owner.
- `service_requests`: account, wallet, browser, public-action, legal, KYC, billing, and trading requests.
- `approvals`: user or risk-officer approvals with exact scope and expiration.
- `artifacts`: reports, patches, screenshots, data snapshots, PR links, draft submissions.
- `outcomes`: accepted, rejected, paid, parked, paper win/loss, duplicate, blocked.
- `traces`: prompt/model/tool/cost/runtime metadata.

### Layer 2: Department Managers

Each manager owns one lane and one queue slice. It can spawn seekers and evidence builders, but it cannot directly use privileged service workers.

Suggested initial departments:

1. Cashflow Engineering: paid code bounties and scoped fixes.
2. Revenue Collection: submitted bounty payout monitoring. Owned by the other worker for now.
3. Security Research: private report candidates and scoped review.
4. Markets Research: Kalshi/Polymarket/trading data, paper-only until gates clear.
5. Venture/Hackathon Desk: grants, hackathons, airdrops, testnet campaigns.
6. Growth/Sales: lead generation and service offers.
7. Audience/Distribution: X/Grok/Radar/content growth.
8. Platform Engineering: infra, queues, observability, duplication prevention.
9. Risk/Treasury/Ops: legal, account, wallet, payment, KYC, side-effect approvals.

### Layer 3: Worker Agents

Common worker types:

- Seeker: finds and normalizes leads.
- Triage agent: verifies payout path, scope, competition, and account needs.
- Evidence builder: writes code/report/proof/simulation.
- Reviewer: checks quality, reputational risk, and gates.
- Runner: executes approved deterministic actions.
- Monitor: watches external state and records changes.

### Layer 4: Service Departments

These are not ordinary agents. They are controlled interfaces for side effects.

- Account Registration Worker: prepares registration packets; stops at terms/KYC/billing.
- Wallet Ops Worker: tracks public addresses and transaction evidence; does not hold seeds.
- Browser Action Worker: executes bounded browser tasks with screenshots and DOM proof.
- Public Comms Worker: posts comments/replies only from approved drafts.
- GitHub Worker: forks/branches/PRs/comments only for assigned lanes.
- Treasury/Risk Worker: position sizing, max-loss checks, capital approvals.
- Secret Vault Worker: grants scoped access to credentials, never raw dumps.

## Money-Path Portfolio

The system should track all paths, but not assign equal effort to all paths.

### High fit now

- Paid code bounties with explicit payout and low competition.
- Security private-report candidates from public source review.
- Market-data scanners and paper-only edge detection.
- Existing local trading strategy mining.
- X/social growth as lead generation and distribution.

### Medium fit

- Web3 audit contests and bug bounties.
- Grants/hackathons with deadlines and account terms.
- Freelance/service lead generation.
- AI automation templates or small SaaS/productized services.

### Low fit unless explicitly chosen

- KYC-heavy platforms.
- Off-platform payment/Discord coordination.
- High-touch sales requiring personal identity.
- Real-money trading without venue eligibility and risk gates.
- Airdrops/testnets requiring wallet churn or capital movement.

## Immediate Build Plan

### Phase 0: Coordination Guard

Implement first:

- Lane ownership file/table.
- Task leases.
- "Do not duplicate active lane" check.
- Side-effect request schema.
- Artifact registry.

Definition of done: two active Codex threads cannot both promote the same lane unless one is manager and one is explicitly assigned worker.

Current status on 2026-06-14: initial Phase 0 skeleton exists.

- SQLite DB: `E:\agent-company-lab\state\agent_company.sqlite`
- CLI: `E:\agent-company-lab\tools\agent_company.py`
- Seed source: `E:\agent-company-lab\architecture\role-registry-draft.json`
- Seed source: `E:\agent-company-lab\architecture\lane-taxonomy-draft.json`
- Claimed lane: `platform_engineering`
- Owner agent: `recovered-profitable-edge-infra`
- Owner thread: `019ebbda-2002-7361-8597-03625189c3ff`
- Explicit non-owner lane: `submitted_bounty_payouts`, noted as owned by the other Find profitable edge worker.
- Recorded service request: `req-grok-research-worker-20260614`
- Recorded task: `task-phase0-control-plane-hardening-20260614`
- Recorded outcome: `outcome-phase0-infra-research-and-skeleton-20260614`
- Task lease commands: `acquire-task`, `release-task`, `complete-task`
- Launch packets: `E:\agent-company-lab\reports\launch-packets\*-launch-packet.md`
- Dashboard export: `E:\agent-company-lab\reports\control-plane-status-latest.md`

What is still missing:

- Artifact listing/filter commands.
- Department manager launch packet review/selection.
- A CEO weekly review report that ranks lanes by evidence, risk, and expected dollars per hour.
- Separate lane-manager launches using the generated manager packets while model-backed execution stays gated.

### Phase 1: Local Control Plane

Use `E:\agent-company-lab` with SQLite first.

Minimum schema:

- `agents`
- `departments`
- `lanes`
- `tasks`
- `service_requests`
- `approvals`
- `artifacts`
- `outcomes`

Use PowerShell/Node/Python scripts to create and query state. Keep it framework-neutral.

### Phase 2: Department Launch

Launch three non-overlapping departments first:

1. Platform Engineering: builds the control plane.
2. Markets Research: owns market/prediction/trading research only.
3. Security Research: owns private-report candidates only.

Leave GitHub payout monitoring to the other active worker until that lane is resolved.

### Phase 3: Framework Prototype

Prototype one lane using:

- LangGraph if durable state/human-in-loop graph control is the main need.
- OpenAI Agents SDK if typed tools, handoffs, sandbox agents, and tracing are the main need.
- CrewAI only if the role/crew abstraction materially speeds prototypes.

Do not migrate the whole company into a framework until the control plane proves stable.

### Phase 4: Service Workers

Build service workers as gated queues:

- Account registration request packet generator.
- Wallet public-address registry and transaction verifier.
- Browser action runner with screenshot/DOM proof.
- GitHub action runner with reputation review.
- X/Grok/Radar scout runner.

### Phase 5: Observability

Start with local traces in SQLite/JSONL. Then evaluate:

- Langfuse for open-source prompt/tracing/eval management.
- Phoenix for OpenTelemetry/OpenInference tracing and evals.

## Critical Design Rules

1. Agents do not own credentials. Service departments grant scoped capabilities.
2. Agents do not directly create accounts or wallets. They request a service action.
3. Every side effect has an artifact: screenshot, URL, comment body, tx hash, PR link, or submission packet.
4. Every task has an owner, lease, status, and duplicate key.
5. Every lane has explicit gates and promotion criteria.
6. The CEO promotes or kills lanes based on outcomes, not effort.
7. No global "next action" should override lane ownership.
8. Public reputation is a first-class asset; low-quality volume is a cost.

## Recommended Stack For This PC

Initial:

- State: SQLite.
- Artifacts: filesystem under `E:\agent-company-lab`.
- Scripts: PowerShell + Python.
- Current agent runtime: Codex threads.
- Existing lane input: `E:\profit-edge-lab` reports and DB.

Near term:

- Queue/control API: small FastAPI or Node service.
- Observability: Langfuse or Phoenix self-host/local.
- Browser workers: Codex browser first; browser-use or agent-browser in isolated worker later.
- Tool protocol: MCP for internal services.

Later:

- Durable workflows: Temporal.
- Agent graph runtime: LangGraph or OpenAI Agents SDK.
- Visual ops: n8n/Dify only for deterministic service workflows or dashboards.
- Inter-agent protocol: A2A if multiple runtimes need to communicate.

## Source Index

Primary sources and current references:

- LangGraph docs: https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph GitHub: https://github.com/langchain-ai/langgraph
- OpenAI Agents SDK GitHub: https://github.com/openai/openai-agents-python
- OpenAI Agents SDK tracing docs: https://openai.github.io/openai-agents-python/tracing/
- Microsoft Agent Framework overview: https://learn.microsoft.com/en-us/agent-framework/overview/
- AutoGen docs: https://microsoft.github.io/autogen/stable//index.html
- CrewAI docs: https://docs.crewai.com/
- Temporal: https://temporal.io/
- Temporal durable execution: https://temporal.io/blog/what-is-durable-execution
- MCP servers: https://github.com/modelcontextprotocol/servers
- MCP registry: https://registry.modelcontextprotocol.io/
- A2A: https://github.com/a2aproject/A2A
- browser-use: https://github.com/browser-use/browser-use
- browser-harness: https://github.com/browser-use/browser-harness
- Vercel agent-browser: https://github.com/vercel-labs/agent-browser
- Langfuse: https://langfuse.com/docs
- Phoenix: https://arize.com/docs/phoenix
- Dify: https://github.com/langgenius/dify
- n8n docs: https://docs.n8n.io/advanced-ai/intro-tutorial/

## Source Summary Refresh - 2026-06-14

Recent/current source checks reinforce the architecture:

### LangGraph

LangGraph positions itself as the orchestration runtime layer: durable execution, streaming, human-in-the-loop, and persistence. Its persistence model separates thread-scoped checkpoints from long-term stores, which maps directly to our need for task continuation, interruption recovery, and cross-thread memory.

Implication: LangGraph is a strong candidate for agent control flows, but the business source of truth should remain in the company control plane. Use LangGraph to run workflows, not to define lane ownership.

Sources:

- https://docs.langchain.com/oss/python/langgraph/overview
- https://docs.langchain.com/oss/python/langgraph/persistence
- https://docs.langchain.com/oss/python/langgraph/interrupts

### OpenAI Agents SDK

The Agents SDK models agents as instructions plus tools with optional handoffs, guardrails, structured outputs, sessions, tracing, and human review. Handoffs are represented as tools to the model, and tracing captures model generations, tool calls, handoffs, guardrails, and custom events.

Implication: this is a good candidate for controlled specialist agents and service-worker wrappers. It supports the exact pattern we need: orchestrator in control, specialists invoked through typed tools or handoffs, and guardrails around side effects.

Sources:

- https://developers.openai.com/api/docs/guides/agents
- https://openai.github.io/openai-agents-python/agents/
- https://openai.github.io/openai-agents-python/handoffs/
- https://github.com/openai/openai-agents-python/blob/main/docs/tracing.md

### MCP and A2A

MCP is a standard for connecting AI applications to external data, tools, and workflows. A2A is a protocol for interoperability between independent agent systems. They solve different problems: MCP is "what tools/context can this agent use"; A2A is "which other agent can help."

Implication: use MCP for internal tools like lane registry, account-service requests, browser-service requests, and profit-edge data access. Use A2A later only if multiple independent agent runtimes need to coordinate. Do not let every worker mount arbitrary MCP servers; exposed tools are execution capability.

Sources:

- https://modelcontextprotocol.io/docs/getting-started/intro
- https://modelcontextprotocol.io/specification/2025-06-18
- https://github.com/modelcontextprotocol/servers
- https://github.com/a2aproject/A2A
- https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/1108

### Temporal / Durable Workflow Engines

Temporal's core value is durable execution: workflows retain state and recover across crashes, retries, timeouts, and intermittent failures. Temporal is a fit for long-running side-effect workflows such as account registration packets, approval wait/resume, payout collection, and market-data capture schedules.

Implication: do not introduce Temporal before we have the control-plane schema stable. Add it when side-effect workflows need durable retry/resume semantics that SQLite scripts cannot comfortably provide.

Sources:

- https://temporal.io/
- https://github.com/temporalio/temporal
- https://docs.temporal.io/develop/python/best-practices/error-handling

### Observability

Langfuse focuses on traces, prompt management, evaluations, experiments, cost/latency, human annotation, and self-hosting. Phoenix focuses on OpenTelemetry/OpenInference tracing and evaluation for agents, RAG, and LLM applications.

Implication: start with local SQLite trace/event records; graduate to Langfuse if prompt/version/eval workflow becomes important, or Phoenix if OpenTelemetry-first local debugging is the priority.

Sources:

- https://langfuse.com/docs
- https://langfuse.com/docs/observability/overview
- https://langfuse.com/docs/prompt-management/overview
- https://arize.com/docs/phoenix
- https://github.com/Arize-ai/phoenix

### Browser Workers

Browser-use and agent-browser are current browser-agent candidates. Browser-use now describes a Python API into a Rust core and browser harness; agent-browser is a Rust CLI with compact output for AI agents. These are useful, but browser automation is a high-risk service department because it can touch logged-in accounts, terms, payment flows, and public actions.

Implication: browser workers must operate from service requests with screenshots/DOM proof and stop conditions. They should not be mounted as general tools for seekers.

Sources:

- https://github.com/browser-use/browser-use
- https://browser-use.com/
- https://github.com/vercel-labs/agent-browser
- https://agent-browser.dev/

## Next Action

Build the Phase 0 control-plane skeleton in `E:\agent-company-lab`:

1. SQLite schema for agents, lanes, tasks, service requests, artifacts, outcomes.
2. Seed lane taxonomy from `architecture/lane-taxonomy-draft.json`.
3. Seed role registry from `architecture/role-registry-draft.json`.
4. Add a `claim-lane` command that prevents duplicate ownership.
5. Add a `create-service-request` command for account/wallet/browser/public-action work.

## Phase 0 Control Plane Status - 2026-06-14

Implemented in `E:\agent-company-lab\tools\agent_company.py`:

- SQLite control plane with roles, departments, agents, lanes, tasks, service requests, approvals, artifacts, outcomes, and lane evidence.
- Lane ownership lock for `platform_engineering`; `submitted_bounty_payouts` remains explicitly assigned to the parallel payout-monitoring worker, not this thread.
- Task leasing commands for acquire/release/complete, so multiple Codex threads can avoid stepping on the same work.
- Launch-packet generator for all lanes under `E:\agent-company-lab\reports\launch-packets`.
- Dashboard generator at `E:\agent-company-lab\reports\control-plane-status-latest.md`.
- Read-only profit-edge import bridge at `import-profit-edge`.
- CEO review generator at `write-ceo-review`.
- Service-request lifecycle commands: approve, reject, assign, start, complete.
- Source-spec registry with 10 specs across 8 lanes, seeded from `E:\agent-company-lab\architecture\source-specs-draft.json`.
- Manager-packet generator at `write-manager-packets`, writing one packet per lane plus `E:\agent-company-lab\reports\manager-packets\index.md`.
- Lane-manager thread launch manifest generator at `write-lane-thread-manifest`, writing a 7-lane launch queue plus held-lane boundaries for `platform_engineering` and `submitted_bounty_payouts`.
- Trace-events table and commands: `record-trace-event`, `list-trace-events`, and `write-trace-report`.
- Artifact listing/report commands: `list-artifacts` and `write-artifacts-report`.
- Pydantic-only typed worker prototype at `E:\agent-company-lab\tools\typed_worker_runtime.py`.
- Runtime selection report: Pydantic AI first, OpenAI Agents SDK second.
- Isolated Pydantic AI eval in `.venv-runtime` passed offline with `TestModel` and `api_calls=false`.
- Gated Pydantic AI adapter shell at `E:\agent-company-lab\tools\pydantic_ai_model_adapter.py`; real mode refuses unless the service request is approved.
- Wave-2 deep research report at `E:\agent-company-lab\reports\agent-company-deep-research-wave2-20260614.md`.
- Prompt/eval/review control-plane tables and commands: `prompt_templates`, `prompt_versions`, `eval_datasets`, `eval_runs`, `human_reviews`, plus `write-prompt-eval-report`.
- Canonical lane-manager prompt v2 and safety dataset with a deterministic local static eval score of `1.0` across 6 cases.
- OpenInference-style trace metadata conventions for `trace_events.metadata_json`.
- Seven projectless Codex lane-manager chats created and titled from the launch manifest; launch run recorded at `E:\agent-company-lab\reports\lane-manager-thread-launch-run-20260614.md`.
- CEO lane-manager monitor at `E:\agent-company-lab\reports\lane-manager-monitor-latest.md`; latest state is 6 of 7 startup-complete, with `prediction_market_research` still not recorded in the shared control plane.

The import bridge currently ingests 67 evidence rows from `E:\profit-edge-lab` into lane-specific evidence:

- `paid_code_bounties`: 15 rows.
- `security_bounty_private_reports`: 19 rows.
- `submitted_bounty_payouts`: 21 rows, all marked read-only and owned by the parallel payout worker.
- `prediction_market_research`: 9 rows.
- `web3_airdrops_grants_hackathons`: 1 row.
- `platform_engineering`: 2 rows.

Current generated import report:

- `E:\agent-company-lab\reports\profit-edge-import-latest.md`

Current generated executive review:

- `E:\agent-company-lab\reports\ceo-review-latest.md`

Current generated source-spec report:

- `E:\agent-company-lab\reports\source-specs-latest.md`

Current generated manager-packet index:

- `E:\agent-company-lab\reports\manager-packets\index.md`

Current generated lane-manager launch manifest:

- `E:\agent-company-lab\reports\lane-manager-thread-launch-manifest-latest.md`
- `E:\agent-company-lab\reports\lane-manager-thread-launch-manifest-latest.json`

Current lane-manager launch run:

- `E:\agent-company-lab\reports\lane-manager-thread-launch-run-20260614.md`
- `E:\agent-company-lab\reports\lane-manager-thread-launch-run-20260614.json`

Current lane-manager monitor:

- `E:\agent-company-lab\reports\lane-manager-monitor-latest.md`
- `E:\agent-company-lab\reports\lane-manager-monitor-latest.json`

Current generated trace report:

- `E:\agent-company-lab\reports\trace-events-latest.md`

Current generated artifact reports:

- `E:\agent-company-lab\reports\artifacts-latest.md`
- `E:\agent-company-lab\reports\artifacts-control-plane-code-latest.md`

Current prompt/eval/review artifacts:

- `E:\agent-company-lab\reports\prompt-eval-review-latest.md`
- `E:\agent-company-lab\prompts\lane-manager-startup-prompt-v2.txt`
- `E:\agent-company-lab\evals\manager-prompt-safety-cases-20260614.json`
- `E:\agent-company-lab\tools\eval_manager_prompt.py`
- `E:\agent-company-lab\reports\prompt-evals\manager-prompt-safety-local-eval-v2-20260614.md`

Current trace convention artifacts:

- `E:\agent-company-lab\architecture\openinference-trace-metadata-v1.json`
- `E:\agent-company-lab\reports\openinference-trace-conventions-20260614.md`

Current typed worker prototype artifacts:

- `E:\agent-company-lab\reports\worker-runtime\prediction_market_research-typed-worker-proposal.md`
- `E:\agent-company-lab\reports\worker-runtime\submitted_bounty_payouts-typed-worker-proposal.md`

Current model-runtime artifacts:

- `E:\agent-company-lab\reports\model-runtime-selection-20260614.md`
- `E:\agent-company-lab\reports\worker-runtime\pydantic-ai-install-latest.md`
- `E:\agent-company-lab\reports\worker-runtime\pydantic-ai-eval-latest.md`
- `E:\agent-company-lab\reports\worker-runtime\pydantic-ai-adapter-gate-latest.md`

Pending model/API service request:

- `req-pydantic-ai-model-backed-adapter-20260614` - status `needs_review`; real model execution remains blocked.

Next platform work:

1. Produce a CEO digest of completed lane startup memos and cross-lane service-gate needs.
2. Re-run the lane-manager monitor after the prediction manager responds; if prediction remains missing across repeated checks, record startup failure and relaunch/reassign the lane.
3. Add behavioral model evals only after `req-pydantic-ai-model-backed-adapter-20260614` is explicitly approved with provider, model, max cost, allowed lanes, output artifact path, and credential route.
