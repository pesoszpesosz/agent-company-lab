# Agent-Company Deep Research Wave 9

Generated: `2026-06-15T14:21:53Z`

## Focus

Durable orchestration, human-in-the-loop control planes, event-driven workers, and production agent runtime patterns for the online money-path agent company.

## Decision Summary

- Keep the current SQLite/report control plane as the authority.
- Design Temporal and Inngest adapter manifests next, without installing or running either engine.
- Keep OpenAI Agents SDK behind the existing model/API approval gate.
- Use Prefect as an operations-runner/pool-concurrency reference, and Dagster as an evidence/sensor reference.
- Fold 12-factor agent principles into our packet schemas: explicit business state, pause/resume, humans as tool/workflow events, small focused agents, owned control flow.

## Source Findings

### OpenAI Agents SDK - choose your starting point
Source: https://developers.openai.com/api/docs/guides/agents#choose-your-starting-point
- OpenAI positions the Agents SDK around code-first agent apps, specialist definitions, runtime loop/state, sandbox agents, orchestration/handoffs, guardrails and human review, results/state, tools/MCP, tracing, and evals.
- This maps strongly to our seeker/manager/service-worker runtime once model/API execution is explicitly approved.
- Architecture use: Use as the model-backed specialist/handoff/guardrail runtime after local approval and cost gates, not as the authoritative ledger.

### Temporal Platform docs - durable execution and workflows
Source: https://docs.temporal.io/temporal
- Temporal is described as a scalable runtime for durable function executions, with Workflow Executions that maintain state through failures using Event History.
- Temporal applications can consist of very large numbers of lightweight Workflow Executions; suspended workflows consume little/no compute, and workflows are resumable, recoverable, and reactive.
- Architecture use: Strong candidate for future durable service-request lifecycle engine once the SQLite packet schemas stabilize.

### Temporal Workflow docs - replay and Activities
Source: https://docs.temporal.io/workflows
- Temporal records workflow commands/events in Event History, replays history to restore state, and requires deterministic workflow decisions.
- External interactions such as API calls, database queries, LLM invocations, and file I/O belong in Activities, whose results are recorded and reused on replay.
- Architecture use: Important design pattern: keep CEO/manager state deterministic; isolate browser/API/model/payment work as gated Activities.

### Prefect docs - flows, tasks, concurrency
Source: https://docs.prefect.io/v3/how-to-guides/workflows/run-work-concurrently
- Prefect workflows are Python functions decorated as flows; tasks can run concurrently with submit/map and futures.
- This is a good fit for local scans, queue rebuilds, report generation, and artifact fan-out where Python ergonomics matter more than years-long durable state.
- Architecture use: Useful as a local operations runner candidate; not the first authority for service-request approval state.

### Prefect docs - work pools
Source: https://docs.prefect.io/v3/how-to-guides/deployment_infra/manage-work-pools
- Prefect work pools can be created, inspected, previewed, paused/resumed, deleted, and assigned concurrency limits via CLI/UI/API.
- Base job templates can restrict deployment infrastructure customization in secure environments.
- Architecture use: Useful pattern for our service-worker pool registry: pool pause/resume, preview, capacity, and restricted templates.

### Dagster docs - sensors
Source: https://docs.dagster.io/guides/automate/sensors
- Dagster sensors respond to internal/external events, either launching runs or yielding skip reasons.
- Run keys prevent duplicate runs; cursors support high-volume event tracking.
- Architecture use: Good fit for evidence/source freshness sensors and deduplicated scan triggers; less direct fit for approval-bound service-worker lifecycles.

### Inngest docs - durable event-driven functions
Source: https://www.inngest.com/docs
- Inngest describes itself as an event-driven durable execution platform for reliable code on any platform, handling backend infrastructure, queueing, scaling, concurrency, throttling, rate limiting, and observability.
- It exposes agent resources, a dev-server MCP, and LLM-friendly docs.
- Architecture use: Strong lightweight candidate for event-driven manager/seeker triggers and workflow steps after local schemas are stable.

### Inngest docs - functions and steps
Source: https://www.inngest.com/docs/features/inngest-functions
- Inngest functions are triggered by events, cron schedules, or webhooks; flow control includes concurrency/throttling; steps create retriable checkpoints.
- Patterns include background jobs, delayed functions, cron functions, and workflows.
- Architecture use: Useful for future event-to-work-packet pipeline and retryable local proof steps.

### HumanLayer 12-factor agents
Source: https://github.com/humanlayer/12-factor-agents
- The guide argues production agents are mostly software with LLM steps inserted carefully, and recommends principles such as owning prompts/context/control flow, unifying execution and business state, launch/pause/resume APIs, contacting humans with tool calls, small focused agents, and stateless reducers.
- It cautions against overcommitting to frameworks before understanding the control flow and quality bar.
- Architecture use: Matches our current SQLite-first approach: keep business state explicit, use small focused workers, and model human approvals as first-class tool/workflow events.

### HumanLayer / CodeLayer repository
Source: https://github.com/humanlayer/humanlayer
- The current HumanLayer repo has shifted toward CodeLayer, an open-source IDE for orchestrating AI coding agents, with workflows for complex codebases and parallel Claude Code sessions.
- It is useful as a UX/workflow reference for multi-agent coding, but not a direct service-worker control plane for money-path operations.
- Architecture use: Reference for IDE-side human experience and parallel worktree/session UX, not core backend authority.

## Candidate Scorecard

| Candidate | Fit | Decision | Role |
|---|---:|---|---|
| `current_sqlite_control_plane` | 98 | `keep_as_authority` | authoritative task/artifact/service-request ledger |
| `temporal` | 92 | `design_adapter_not_install_yet` | durable long-running service-request lifecycle engine |
| `inngest` | 86 | `design_adapter_not_install_yet` | event-driven durable function and trigger layer |
| `openai_agents_sdk` | 84 | `keep_behind_model_api_gate` | model-backed specialist/handoff/guardrail runtime |
| `prefect` | 76 | `use_as_pattern_or_later_local_runner` | local ops runner, pool/concurrency pattern reference |
| `dagster` | 73 | `use_as_sensor_asset_reference` | source/evidence asset automation and sensors |
| `humanlayer_12_factor_agents` | 82 | `adopt_principles_not_framework_dependency` | architecture principles and UX/control-flow reference |

## Next Local Proof

Write a `temporal_inngest_service_request_adapter_manifest` that maps existing service request states to durable workflow concepts, with zero installs, starts, API calls, approvals, assignments, or external side effects.

## No-Action Audit

- Dependency installs/imports: `0 / 0`
- Worker starts: `0`
- Service updates/assignments: `0 / 0`
- Approvals/pool registrations: `0 / 0`
- API calls/external side effects: `false / false`
