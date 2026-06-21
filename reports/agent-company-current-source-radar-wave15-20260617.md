# Agent Company Current-Source Radar Wave 15

Generated UTC: 2026-06-21T15:44:04Z
Capture UTC: 2026-06-17T20:46:01Z
Task: `task-agent-company-current-source-radar-wave15-20260617`
Dataset: `E:\agent-company-lab\data\agent-company-current-source-radar-wave15-20260617.json`
CSV: `E:\agent-company-lab\data\agent-company-current-source-radar-wave15-20260617.csv`
Validation: `E:\agent-company-lab\reports\agent-company-current-source-radar-wave15-validation-20260617.json`

## Purpose

Refresh the agent-company infrastructure radar using current primary sources for multi-agent orchestration, durable execution, human-in-the-loop approval, and coding-agent harnesses. This wave is read-only: it installs nothing, starts no runtime, approves no service request, and performs no public action.

## Source Boundary

- Repository metadata rows captured: `7`
- Official/doc/source rows mapped: `10`
- Public GitHub metadata reads: `7`
- Validation failures: `0`
- External side effects: `False`

## Ranked Current Signals

| Fit | Stars | Last Push | Category | Repo | Local Decision | Gate |
| ---: | ---: | --- | --- | --- | --- | --- |
| `12` | `77551` | `2026-06-17T19:45:27Z` | `coding_agent_harness` | [All-Hands-AI/OpenHands](https://github.com/OpenHands/OpenHands) | `treat_as_sandboxed_code_worker_reference_not_runtime_dependency` | `sandbox_execution_gate_and_github_public_action_gate_required` |
| `12` | `35051` | `2026-06-17T20:45:03Z` | `durable_agent_graph_hitl` | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | `reference_interrupt_checkpoint_human_review_pattern` | `no_runtime_adoption_until_checkpoint_schema_and_apply_guard` |
| `12` | `21029` | `2026-06-17T20:41:36Z` | `durable_execution_runtime` | [temporalio/temporal](https://github.com/temporalio/temporal) | `keep_as_future_durable_orchestration_candidate` | `runtime_start_preflight_and_signed_operator_decision_required` |
| `12` | `4021` | `2026-06-17T18:08:53Z` | `durable_agent_runtime` | [restatedev/restate](https://github.com/restatedev/restate) | `reference_journaled_tool_and_llm_step_recovery_pattern` | `no_server_start_no_container_no_cloud_until_runtime_start_preflight` |
| `11` | `53815` | `2026-06-17T19:01:37Z` | `multi_agent_orchestration` | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | `study_role_team_patterns_but_keep_shared_state_in_local_db` | `no_dependency_install_no_worker_start` |
| `11` | `11428` | `2026-06-17T20:18:09Z` | `multi_agent_workflow_hitl` | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | `reference_manager_worker_reviewer_escalation_pattern` | `no_foundry_or_cloud_runtime_without_exact_scope_and_cost_gate` |
| `10` | `20157` | `2026-06-17T20:40:14Z` | `agent_app_framework` | [google/adk-python](https://github.com/google/adk-python) | `study_eval_deploy_agent_packaging_patterns` | `model_api_execution_gate_and_dependency_install_gate_required` |

## Primary-Source Takeaways

| Source | Takeaway | Local Mapping |
| --- | --- | --- |
| [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | LangGraph positions durable execution, streaming, and human-in-the-loop as core orchestration primitives. | Use its checkpoint/interrupt concept as a reference for CEO/CRO decision pauses, while keeping local SQLite as the authority. |
| [LangChain Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) | Tool calls can be paused by policy and resumed after a human decision. | Matches service-worker signed decision guard plus apply-preflight blocker. |
| [Temporal durable execution guide](https://temporal.io/blog/what-is-durable-execution) | Durable execution treats long-running work as crash-proof execution with persisted history. | Keep our trace_events/outcomes/artifacts as the lightweight history before any Temporal adoption. |
| [Temporal Workflow documentation](https://docs.temporal.io/workflows) | Workflow definitions, executions, schedules, and handlers are separate concepts. | Use this to split lane manager tasks, service requests, and worker starts in our schema. |
| [Restate durable agents](https://docs.restate.dev/ai/patterns/durable-agents) | Agent steps such as LLM calls, tool executions, and routing decisions can be durably persisted. | Promote tool/LLM calls to first-class trace events before runtime execution is allowed. |
| [Restate AI agents use case](https://docs.restate.dev/use-cases/ai-agents) | The runtime emphasizes retries, persisted progress, and suspension of idle long-running agents. | Add idle/lease/resume fields before local worker pool activation. |
| [Microsoft Agent Framework human-in-the-loop workflow sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/03-workflows/agents/workflow_as_agent_human_in_the_loop.py) | A worker/reviewer/manager escalation flow is an explicit sample shape. | Map to seeker, lane manager, CRO/CEO, and service-worker roles. |
| [Google ADK Python repository](https://github.com/google/adk-python) | ADK is code-first and includes build/evaluate/deploy framing. | Useful later for eval packaging; blocked until model/API/provider/cost gates are explicit. |
| [CrewAI dynamic agent dependency graph issue](https://github.com/crewAIInc/crewAI/issues/6118) | Static orchestration is called out as breaking down at scale. | Reinforces that our task DAG and dispatch docket should support dynamic dependencies. |
| [OpenHands repository](https://github.com/OpenHands/OpenHands) | Coding-agent harnesses need repo, issue, token, and public-action boundaries. | Keep code workers behind sandbox execution and GitHub public-action gates. |

## Architecture Decisions

1. `keep_local_sqlite_control_plane_as_brain`
   Reason: Every source points toward durable state, checkpoints, and explicit human review. Our current DB already stores tasks, artifacts, outcomes, service requests, and trace events.
   Next build: `checkpoint_interrupt_contract_v1 for lane manager handoffs and service-worker decisions.`
2. `separate_human_review_from_apply`
   Reason: LangChain HITL, LangGraph interrupts, Microsoft HITL workflow, and our service-worker guards all converge on pause/review/resume rather than instant execution.
   Next build: `signed_decision_apply_command_contract only after a real signed decision artifact exists.`
3. `treat_frameworks_as_patterns_before_dependencies`
   Reason: High-star frameworks are active, but adopting them now would add runtime, credentials, and model/API gates before our local company loop is complete.
   Next build: `adapter_candidate_scorecard_v1 covering LangGraph, Temporal, Restate, ADK, Microsoft Agent Framework, CrewAI, and OpenHands.`

## Hold Until Gated

- External framework dependency install/import.
- Temporal, Restate, LangGraph, ADK, Microsoft Agent Framework, CrewAI, or OpenHands runtime start.
- Model/provider/API execution.
- Browser/account/public/GitHub/security/payment/wallet action.
- Worker pool registration or assignment.

## Boundary

- Model/API calls: `False`
- Dependency installs: `0`
- Runtime starts: `0`
- Worker starts: `0`
- Service requests assigned/updated: `0` / `0`
- Browser sessions started: `0`
- Public/payment/wallet actions: `False` / `False` / `False`
- External side effects: `False`
