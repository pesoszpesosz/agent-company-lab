# Agent Company Operator Inbox Radar Wave 21

Generated UTC: 2026-06-18T03:04:00Z

Purpose: collect current primary-source patterns for the next local CEO/manager inbox packet layer after `ceo_operator_event_surface_contract_v1`.

## Recommendation

Build `ceo_manager_inbox_packet_v1` as a local report-only packet contract, not a live inbox, transport, approval runner, or service-request mutator.

The packet should carry a proposed action, allowed decision previews, source evidence, correlation id, lane/manager identity, timeout policy, and explicit branch previews. It should reject any packet that tries to enable SSE, WebSockets, operator event persistence, task mutation, service-request mutation, worker starts, browser sessions, runtime starts, model/API calls, MCP calls, public actions, account actions, wallet/payment actions, security testing, or external side effects.

## Source Patterns

| Source | Pattern | Design Input |
| --- | --- | --- |
| LangGraph interrupts | Dynamic JSON interrupt payloads plus checkpoint/thread resume semantics. | Store source event and correlation data locally; do not start an interrupt transport. |
| LangChain HITL middleware | Policy-driven tool interruption with approve/edit/reject/respond style decisions. | Separate proposed action from allowed decision previews. |
| LangChain Agent Inbox | Concrete inbox UX uses action request, allow flags, and human response types. | Reuse the shape concept locally, but do not connect to a deployment. |
| Temporal message passing | Separates read-only Queries, asynchronous write Signals, and tracked Updates. | Classify inbox packet attention as notice, async decision request, or tracked decision request without writing. |
| Inngest HITL | Uses correlated waits, timeout behavior, and approved/rejected/timed-out branches. | Add `correlation_id`, `timeout_policy`, and branch previews. |
| HumanLayer CodeLayer | Orchestrates parallel coding agents with human-guided workflows. | Keep owner thread, lane, agent, and evidence visible for supervision. |
| AXME async approval | Emphasizes reminders, escalation, and timeout for blocked agents. | Treat reminders/escalations as local preview fields only. |

## Candidate Packet Fields

- `schema_version`
- `packet_status`
- `packet_id`
- `source_event_type`
- `source_event_surface_contract_path`
- `lane_id`
- `manager_agent_id`
- `operator_role`
- `attention_type`
- `priority`
- `summary`
- `action_request`
- `allowed_decision_types`
- `correlation_id`
- `source_artifact_paths`
- `timeout_policy`
- `branch_previews`
- `zero_side_effect_boundary`

## Allowed Attention Types

- `read_only_notice`
- `approval_needed`
- `edit_or_reject_needed`
- `blocked_route_update`
- `dispatch_next_action`

## Allowed Decision Preview Types

- `acknowledge`
- `approve_preview`
- `reject_preview`
- `edit_preview`
- `respond_preview`
- `defer`
- `timeout_noop`

## Hard Denials

- No SSE or WebSocket transport.
- No operator event emission or persistence.
- No task creation or update from the packet itself.
- No service-request assignment, approval, rejection, start, update, or completion.
- No worker, browser, runtime, MCP, or model/API start/call.
- No public, account, wallet, payment, security-testing, legal, or external side effect.

## Source URLs

- https://docs.langchain.com/oss/python/langgraph/interrupts
- https://docs.langchain.com/oss/python/langchain/human-in-the-loop
- https://github.com/langchain-ai/agent-inbox
- https://docs.temporal.io/encyclopedia/workflow-message-passing
- https://www.inngest.com/docs/ai-patterns/human-in-the-loop
- https://github.com/humanlayer/humanlayer
- https://github.com/AxmeAI/async-human-approval-for-ai-agents

## Zero Side-Effect Boundary

- GitHub metadata reads: 3
- Web documentation reads: 4
- Dependency installs: 0
- Runtime starts: 0
- Browser sessions started: 0
- Worker starts: 0
- Operator events emitted: 0
- Operator events persisted: 0
- Tasks created by report: 0
- Tasks updated by report: 0
- Service requests assigned: 0
- Service requests updated: 0
- Approval rows written: 0
- MCP tool calls: false
- Model/API calls: false
- Public/account/wallet/payment/security-testing actions: false
- External side effects: false

## Next Action

Build `ceo_manager_inbox_packet_v1` as a local report-only schema and validator only after explicit design approval; keep all transport, mutation, approval, worker, browser, model/MCP, public, account, wallet, payment, and external actions disabled.
