# Agent Company Deep Research Wave 3

Generated UTC: 2026-06-14T13:08:14Z

Workspace: `E:\agent-company-lab`

Purpose: extend the agent-company infrastructure research after all seven lane-manager startups became durable. This wave focuses on the next scaling layer: durable work queues, service-worker approvals, browser/account workers, multi-agent coding workspaces, and human-review artifacts.

This is platform-engineering research only. It does not execute any money lane, account action, wallet action, public post, PR, bounty claim, trade, deposit, withdrawal, or browser side effect.

## Executive Update

The system has crossed the first useful threshold: seven separate lane-manager chats exist and all seven launched lane startups are recorded in SQLite with artifacts, outcomes, and traces.

The next bottleneck is no longer "can managers start?" It is "can managers request privileged help without malformed intake, duplicate work, or side effects leaking through chat?"

Wave-3 recommendation:

1. Keep `E:\agent-company-lab\state\agent_company.sqlite` as the local company source of truth.
2. Add service-request scaffolding before adding another agent runtime. Managers need valid request packets for account registration, browser research, wallet setup, public actions, legal/KYC/payment review, real-money gate review, model/API execution, outreach, GitHub public actions, security-report submission, secrets handling, and paid data/API access.
3. Treat every external side effect as a HumanLayer-style decision artifact: case, evidence, exact requested action, stop condition, approval, execution proof, and outcome.
4. Evaluate durable workflow engines only for service departments, not for lane ownership. Hatchet, Inngest, Trigger.dev, DBOS, and Temporal all solve durable execution, but the lab should first standardize the service-request contract.
5. Treat browser automation frameworks as service-worker implementations. `agent-browser`, Stagehand, browser-use, and Skyvern should never become default powers for seekers or managers.
6. Learn from Vibe Kanban, Crystal/Nimbalyst, and CodeLayer, but do not migrate the control plane into a coding-agent workspace tool. They validate the worktree/session-isolation pattern; our multi-thread Codex setup already has the essential primitive.

## Current System State

Relevant current local state after this wave:

- lane-manager monitor: 7 of 7 launched lane managers are `startup_complete`
- replacement prediction manager thread: `019ec637-a391-7693-915f-5ec5e5d82ee7`
- full artifact inventory after recovery: 78 artifacts
- trace report after recovery: 31 trace events
- service catalog: 13 service-worker entries with required intake fields
- validator: missing catalog-backed intake blocks creation/start

New wave-3 data artifacts:

- `E:\agent-company-lab\data\github-repo-wave3-raw-20260614.jsonl`
- `E:\agent-company-lab\data\github-repo-agent-orchestrators-wave3-raw-20260614.jsonl`
- `E:\agent-company-lab\data\curated-infra-repos-wave3-20260614.json`
- `E:\agent-company-lab\data\curated-infra-repos-wave3-20260614.csv`

## Live GitHub Snapshot

Captured with `gh repo view` on 2026-06-14. Stars and releases are volatile; use this as a dated evidence snapshot, not permanent truth.

| Repo | Stars | Latest Release | Updated UTC | Fit For Agent Company |
| --- | ---: | --- | --- | --- |
| `modelcontextprotocol/servers` | 87,202 | `2026.1.26`, 2026-01-27 | 2026-06-14T12:36:38Z | MCP server catalog/reference; useful, but high supply-chain review burden. |
| `crewAIInc/crewAI` | 53,527 | `1.14.7`, 2026-06-11 | 2026-06-14T12:26:39Z | Role/crew prototyping; not source of truth. |
| `agno-agi/agno` | 40,675 | `v2.6.14`, 2026-06-12 | 2026-06-14T11:52:41Z | High-adoption agent platform candidate; evaluate only after typed contract is stable. |
| `langchain-ai/langgraph` | 34,695 | `1.2.5`, 2026-06-12 | 2026-06-14T12:38:39Z | Strong manager-orchestration pattern: persistence, interrupts, stateful graphs. |
| `microsoft/semantic-kernel` | 28,114 | `python-1.43.0`, 2026-06-03 | 2026-06-14T12:35:20Z | Microsoft ecosystem and planner/kernel reference. |
| `openai/openai-agents-python` | 27,139 | `v0.17.5`, 2026-06-11 | 2026-06-14T12:01:09Z | OpenAI-first runtime for handoffs, guardrails, tracing, sandbox execution. |
| `BloopAI/vibe-kanban` | 26,995 | `v0.1.44`, 2026-04-24 | 2026-06-14T12:51:09Z | Validates kanban plus worktree/session model, but README says project is sunsetting. |
| `a2aproject/A2A` | 24,277 | `v1.0.1`, 2026-05-28 | 2026-06-14T12:26:00Z | Later inter-agent service protocol, not a control plane. |
| `browserbase/stagehand` | 23,102 | `2.5.9`, 2026-06-11 | 2026-06-14T11:27:51Z | Browser service-worker candidate for code-plus-natural-language automation. |
| `promptfoo/promptfoo` | 22,184 | `0.121.15`, 2026-06-05 | 2026-06-14T12:35:30Z | Prompt/agent regression testing and red-team gate. |
| `Skyvern-AI/skyvern` | 21,902 | `v1.0.41`, 2026-06-11 | 2026-06-14T12:06:32Z | Browser/RPA service-worker candidate; AGPL licensing matters. |
| `triggerdotdev/trigger.dev` | 15,341 | `v4.4.6`, 2026-05-12 | 2026-06-14T10:35:17Z | TypeScript AI workflows, queues, retries, observability. |
| `ag-ui-protocol/ag-ui` | 14,253 | `release/2026-06-12` | 2026-06-14T12:37:34Z | Future approval/review UI protocol. |
| `microsoft/agent-framework` | 11,325 | `dotnet-1.10.0`, 2026-06-10 | 2026-06-14T11:18:54Z | Microsoft successor path for AutoGen/Semantic Kernel style agents. |
| `humanlayer/humanlayer` | 10,988 | `pro-0.20.0`, 2025-12-23 | 2026-06-14T08:44:48Z | Strong design inspiration for human approval and coding-agent orchestration. |
| `hatchet-dev/hatchet` | 7,340 | `v0.89.0`, 2026-06-10 | 2026-06-13T22:23:29Z | Durable workflow/service-task engine with MCP bridge; very relevant later. |
| `inngest/inngest` | 5,487 | `v1.27.0`, 2026-06-09 | 2026-06-14T10:35:14Z | Durable event-driven functions and wait-for-event human-in-loop pattern. |
| `openai/openai-agents-js` | 3,213 | `v0.11.6`, 2026-05-29 | 2026-06-14T10:41:20Z | TypeScript OpenAI agent runtime option. |
| `stravu/crystal` | 3,082 | `v0.3.5`, 2026-02-26 | 2026-06-14T04:11:50Z | Deprecated, but validates parallel Codex/Claude worktree sessions. |
| `dbos-inc/dbos-transact-py` | 1,419 | `2.23.0`, 2026-06-01 | 2026-06-14T04:47:54Z | Postgres/SQLite-backed durable Python workflows; strong conceptual fit. |
| `nimbalyst/nimbalyst` | 823 | `v0.64.4`, 2026-06-03 | 2026-06-14T08:26:47Z | Active successor-style visual workspace for Codex/Claude sessions. |
| `andyrewlee/awesome-agent-orchestrators` | 718 | none | 2026-06-14T06:53:56Z | Discovery index for orchestration tools; not production dependency. |
| `nwiizo/ccswarm` | 141 | `v0.9.1`, 2026-06-10 | 2026-06-14T08:21:43Z | Small but relevant worktree/specialist-agent orchestration example. |
| `untra/operator` | 26 | `v0.2.1`, 2026-06-03 | 2026-06-08T08:46:34Z | Early Rust kanban/tmux/zellij operator pattern. |

## Source Findings

### 1. Durable Workflow Engines Are Service Infrastructure, Not Company Memory

Hatchet's docs describe a platform for AI agents, durable workflows, and background tasks with queues, retries, monitoring, alerting, logging, durable event logs, replay, priorities, worker slot control, and Postgres-based self-hosting. Its MCP cookbook is especially relevant: expose a workflow/task as a typed tool, let the agent invoke the tool, and let workers execute the durable work with observability.

Inngest positions itself as event-driven durable execution that handles queueing, scaling, concurrency, throttling, rate limiting, and observability. Its `waitForEvent` pattern maps directly to our approval gate: a service workflow can pause until a user/reviewer event arrives, with audit trails.

DBOS is the most conceptually close to the local lab because it uses database-backed workflows. Its queue docs say enqueue returns a handle and guarantees eventual execution even after interruption. It defaults to SQLite for easy setup and recommends Postgres for production.

Trigger.dev is strongest for TypeScript long-running AI tasks, queues, retries, observability, and no-timeout background jobs. It is useful if the future UI/service layer moves TypeScript-first.

Decision: do not pick a workflow engine yet. First standardize service-request packets. Then benchmark DBOS and Hatchet against exactly one workflow: a browser-read-only request that waits for user approval, captures evidence, and records artifact/outcome/trace.

### 2. Handoffs Need Ownership Semantics

OpenAI's Agents SDK docs say it is for code-first orchestration involving agents, tools, handoffs, guardrails, tracing, and sandbox execution. The official handoff docs define handoffs as delegation from one agent to another specialist agent and represent handoffs as tools to the model.

For our lab, that means:

- use "agent as tool" when the manager remains accountable;
- use "handoff" only when ownership transfers to another specialist;
- never let an LLM handoff mutate lane ownership directly;
- record the handoff in `tasks`, `service_requests`, or `trace_events`.

The current design already has the right substrate: lane managers own lanes, service workers own privileged requests, and platform engineering owns control-plane changes.

### 3. Human Approval Is A First-Class Artifact

HumanLayer's 12-factor-agents pattern is highly aligned with this lab. Its deployment example pauses high-stakes actions for human approval, then lets deterministic code execute after approval. The article also argues for owning prompts as first-class code and owning the control loop/context accumulation rather than outsourcing everything to a black-box framework.

Translate this into the agent-company model:

- every side-effect-adjacent request is a case file;
- deterministic code validates the intake before any worker starts;
- the LLM can draft and reason, but it cannot grant itself permission;
- approval/rejection must create a durable artifact with scope, rationale, timestamp, and expiry if relevant;
- execution proof must be separate from approval proof.

This is the missing layer between manager threads and service workers.

### 4. Browser Automation Should Be Split Into "Read", "Draft", And "Execute"

Stagehand's README frames it as combining AI with the precision of code for production browser automation. This is useful because it avoids the two bad extremes: brittle low-level Playwright-only scripts and unpredictable full-browser agents.

The lab should treat browser work as three service levels:

| Level | Allowed Without User Approval? | Example |
| --- | --- | --- |
| read-only capture | with explicit manager/service request | inspect public docs, capture screenshot/DOM text |
| draft/preflight | with service request, no submit | fill a local form packet or draft action text |
| execute public/account action | only after exact approval | post, reply, submit, apply, connect, buy, trade |

Candidate implementations:

- `agent-browser`: CLI-friendly, deterministic accessibility tree, good for service worker proof capture.
- Stagehand: good for TypeScript browser worker with code plus natural-language actions.
- browser-use: popular Python option, higher autonomy and therefore higher gating burden.
- Skyvern: strong RPA/browser automation, but AGPL license requires care.

Decision: build the service request contract before choosing the browser engine.

### 5. Coding-Agent Workspaces Validate Our Thread-Per-Lane Model

Vibe Kanban, Crystal/Nimbalyst, and CodeLayer are all converging on the same idea: many agents need isolated workspaces, visible task boards, review loops, and a human coordinator.

Lessons to copy:

- one task card maps to one agent attempt;
- each attempt gets isolated workspace/session state;
- review happens through artifacts and diffs, not trust;
- managers compare outputs and synthesize, instead of blindly merging;
- notifications matter, but the durable state must remain queryable.

Lessons not to copy yet:

- do not move money-lane ownership into a kanban UI;
- do not rely on a sunsetting tool as core infra;
- do not let a coding-workspace tool become the policy engine for wallets, accounts, or public actions.

Our local Codex threads are already the session layer. The missing piece is a richer local board/report that maps thread IDs to lanes, tasks, service requests, evidence, and blockers.

## Recommended Next Architecture Slice

Build a "Service Request Packet Factory" after design approval.

Scope:

- input: `service_id` or `request_type`, lane id, requester id, and a few high-level values;
- output: a Markdown packet and JSON intake file with every required field named;
- validation: packet cannot be used unless the required intake fields pass current catalog validation;
- no side effects: it only writes local templates and creates `needs_review` requests;
- artifact registration: every generated packet becomes an artifact;
- trace: every generated packet records a trace event with `api_calls=false`.

Why this matters:

- lane managers can stop hand-writing malformed JSON;
- service workers get consistent case files;
- the CEO can review approval queues without reading chat history;
- future DBOS/Hatchet/Temporal workflows can use the exact same packet schema;
- browser/Grok/wallet/account/API work becomes routable without accidental execution.

Proposed command shape after approval:

```powershell
python E:\agent-company-lab\tools\agent_company.py scaffold-service-request `
  --service-id browser_read_only_session `
  --lane-id content_and_social_growth `
  --requester-agent-id lane-manager-content_and_social_growth-019ec613 `
  --output-dir E:\agent-company-lab\requests\service-requests
```

Generated files:

- `requests/service-requests/REQ_ID/intake.json`
- `requests/service-requests/REQ_ID/packet.md`
- optional `requests/service-requests/REQ_ID/checklist.md`

Fields should come directly from `architecture/service-catalog-draft.json` / `service_catalog` rows, not from copied prompt text.

## Later Workflow Engine Evaluation

Only after packet scaffolding works, run this tiny bake-off:

| Engine | Test Workflow | Pass Criteria |
| --- | --- | --- |
| DBOS | local approval wait plus artifact write | runs with SQLite locally, resumes after interruption, records DB handle |
| Hatchet | browser-read-only request as MCP-exposed task | typed input schema, worker execution proof, trace/export link |
| Inngest | wait-for-event approval pattern | clean pause/resume, audit event, no external side effect |
| Trigger.dev | TypeScript long-running model/API dry run | no-timeout run, retries, logs, cost-proof artifact |
| Temporal | account-registration intake workflow | deterministic workflow, activities isolated, approval wait, compensation sketch |

Do not evaluate them with vague demos. Each must run the same service-request contract.

## Safety And Governance Decisions

The agent company should preserve these hard rules:

1. Lane managers can request service help, but cannot approve their own side-effect requests.
2. Service workers can prepare packets, but cannot create accounts, accept terms, trade, send wallet addresses, post, submit, or buy without exact approval.
3. Browser workers must classify every page action as read-only, draft/preflight, or execution.
4. Public actions require reputation review and exact final text/destination.
5. Model/API execution requires provider, model, max cost, data scope, tools, prompt version, eval run, and output path.
6. Real-money work requires paper evidence, fees/depth, venue eligibility, max loss, capital limit, and kill switch.
7. Every blocked request must still create a useful blocker artifact.

## Build Priority

1. Service-request packet factory.
2. Service-request review dashboard/report grouped by risk gate and missing fields.
3. Thread/lane map refresh that includes all current lane-manager thread IDs and replacement/superseded status.
4. Read-only browser service dry-run packet for X/Grok/Radar/Gemini, without opening browser or taking account actions.
5. DBOS or Hatchet bake-off using the exact service-request packet.
6. AG-UI review-console design after the command-line packet/report flow proves useful.

## Sources

Primary sources used:

- OpenAI Agents SDK docs: https://developers.openai.com/api/docs/guides/agents
- OpenAI SDK/library docs: https://developers.openai.com/api/docs/libraries#use-the-agents-sdk
- OpenAI Agents SDK handoffs: https://openai.github.io/openai-agents-python/handoffs/
- Hatchet docs: https://docs.hatchet.run/
- Hatchet MCP tools cookbook: https://docs.hatchet.run/cookbooks/hatchet-and-mcp
- Inngest docs: https://www.inngest.com/docs
- Inngest wait-for-event docs: https://www.inngest.com/docs/features/inngest-functions/steps-workflows/wait-for-event
- DBOS queue docs: https://docs.dbos.dev/python/reference/queues
- Trigger.dev docs: https://trigger.dev/docs/introduction
- HumanLayer 12 Factor Agents: https://www.humanlayer.dev/blog/12-factor-agents
- Stagehand GitHub: https://github.com/browserbase/stagehand
- Vibe Kanban GitHub: https://github.com/BloopAI/vibe-kanban
- Crystal/Nimbalyst GitHub: https://github.com/stravu/crystal
- Nimbalyst GitHub: https://github.com/nimbalyst/nimbalyst
- A2A GitHub: https://github.com/a2aproject/A2A
- AG-UI GitHub: https://github.com/ag-ui-protocol/ag-ui
- Promptfoo GitHub: https://github.com/promptfoo/promptfoo

Local data artifacts:

- `E:\agent-company-lab\data\curated-infra-repos-wave3-20260614.json`
- `E:\agent-company-lab\data\curated-infra-repos-wave3-20260614.csv`
