# Adapter Candidate Scorecard v1

Generated UTC: 2026-06-21T15:44:02Z
Scorecard JSON: `E:\agent-company-lab\reports\adapter-candidate-scorecard-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\adapter-candidate-scorecard-v1-validation-20260617.json`
Source dataset: `E:\agent-company-lab\data\agent-company-current-source-radar-wave15-20260617.json`
Checkpoint validation: `E:\agent-company-lab\reports\checkpoint-interrupt-contract-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Candidate count: `7`
- Selected for runtime adoption: `0`
- Recommended next candidate: `langchain-ai/langgraph`
- Recommended next local build: `checkpoint_interrupt_bridge_fixture`
- Dependency installs: `0`
- Runtime starts: `0`
- Worker starts: `0`
- External side effects: `False`

## Ranked Candidates

| Rank | Score | Candidate | Class | First Local Adapter | Required Gates | Recommendation |
| ---: | ---: | --- | --- | --- | --- | --- |
| 1 | `95` | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | `checkpoint_graph_runtime_candidate` | `checkpoint_interrupt_bridge_fixture` | checkpoint_interrupt_contract_v1, runtime_start_preflight, signed_operator_runtime_decision, model_api_execution_gate | `pattern_first_score_high` |
| 2 | `87` | [restatedev/restate](https://github.com/restatedev/restate) | `durable_agent_runtime_candidate` | `journaled_tool_call_fixture` | checkpoint_interrupt_contract_v1, runtime_start_preflight, signed_operator_runtime_decision, egress_event_ledger | `pattern_first_score_high` |
| 3 | `87` | [temporalio/temporal](https://github.com/temporalio/temporal) | `durable_workflow_runtime_candidate` | `service_request_history_replay_manifest` | checkpoint_interrupt_contract_v1, runtime_start_preflight, signed_operator_runtime_decision, dependency_install_gate | `defer_until_runtime_adoption_packet` |
| 4 | `82` | [All-Hands-AI/OpenHands](https://github.com/OpenHands/OpenHands) | `coding_agent_harness_candidate` | `sandboxed_code_worker_scope_fixture` | sandbox_execution_gate, github_public_action_gate, secrets_credentials_handling_gate, checkpoint_interrupt_contract_v1 | `only_after_sandbox_execution_contract` |
| 5 | `82` | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | `manager_worker_reviewer_workflow_candidate` | `manager_reviewer_escalation_fixture` | checkpoint_interrupt_contract_v1, model_api_execution_gate, cloud_or_foundry_scope_gate, signed_operator_runtime_decision | `study_hitl_workflow_before_runtime` |
| 6 | `81` | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | `role_team_orchestration_candidate` | `role_team_dispatch_fixture` | checkpoint_interrupt_contract_v1, dependency_install_gate, model_api_execution_gate | `extract_role_taxonomy_not_runtime` |
| 7 | `74` | [google/adk-python](https://github.com/google/adk-python) | `agent_packaging_eval_candidate` | `eval_packaging_manifest_fixture` | model_api_execution_gate, dependency_install_gate, credential_scope_gate, checkpoint_interrupt_contract_v1 | `study_eval_packaging_later` |

## Boundary

- This scorecard selects zero candidates for runtime adoption.
- It installs no dependencies and imports no external frameworks.
- It starts no runtime, worker, browser session, model call, MCP tool, public action, payment, or wallet action.
- Every candidate remains behind checkpoint interrupt, runtime/dependency, credential, cost, sandbox, or public-action gates as applicable.
