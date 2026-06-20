# Agent Platform Capability Matrix v1

Generated UTC: 2026-06-17T18:09:30Z
Task: `task-agent-platform-capability-matrix-v1-20260617`
Source radar: `E:\agent-company-lab\data\agent-company-current-source-radar-wave11-20260617.json`
Matrix JSON: `E:\agent-company-lab\reports\agent-platform-capability-matrix-v1-20260617.json`
CSV: `E:\agent-company-lab\reports\agent-platform-capability-matrix-v1-20260617.csv`
Validation: `E:\agent-company-lab\reports\agent-platform-capability-matrix-v1-validation-20260617.json`

## Summary

- Source repo rows: `11`
- Matrix rows: `11`
- Rate-limited follow-ups preserved: `8`
- Local runtime apply allowed: `False`
- Validation failures: `0`

## Local Baseline

- Current company brain: `agent_company_sqlite_control_plane`
- Chain integrity layers checked: `133`
- Human/CRO-gated service requests: `11`
- Note: Current local source of truth: task/evidence/artifact/trace/outcome ledger plus service-worker gate maps and runtime preflight blockers.

## Ranked Matrix

| Score | Posture | Category | Repo | Stars | Why |
| ---: | --- | --- | --- | ---: | --- |
| `36` | `promote_to_control_plane_pattern_matrix` | `agent_platform_control_plane` | [agno-agi/agno](https://github.com/agno-agi/agno) | `40749` | Directly aligned with running agent platforms with tracing, scheduling, RBAC, and a control plane; compare to our SQLite CEO ledger before any install. |
| `35` | `watch_as_pattern_source` | `typescript_agent_ops_platform` | [VoltAgent/voltagent](https://github.com/voltagent/voltagent) | `9659` | Combines framework primitives with operations-console ideas: observability, evals, guardrails, deployment, prompts, automation. |
| `30` | `promote_to_sandbox_gate_contract` | `coding_agent_harness` | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | `77538` | High-adoption autonomous coding agent harness; relevant for future code-worker lanes, but only inside strict workspace/sandbox and public-action gates. |
| `29` | `pattern_only_until_dependency_review` | `production_agent_harness` | [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk) | `6186` | Production-agent harness direction with Python/TypeScript SDKs; useful as a pattern source for intervention, tools, memory, and multi-agent harnessing. |
| `22` | `pattern_only_high_side_effect_risk` | `workflow_automation` | [n8n-io/n8n](https://github.com/n8n-io/n8n) | `192938` | Very high adoption for workflow automation and integrations; relevant for service-worker queues, but dangerous around credentials and public actions. |
| `20` | `promote_to_sandbox_gate_contract` | `sandbox_execution` | [e2b-dev/E2B](https://github.com/e2b-dev/E2B) | `12632` | Agent sandboxing is a likely missing department primitive for untrusted code, generated tools, and reproducible worker runs. |
| `19` | `pattern_only_until_dependency_review` | `agent_app_builder` | [langflow-ai/langflow](https://github.com/langflow-ai/langflow) | `149790` | Large visual-flow adoption signal; useful for UI/graph inspiration and productization routes, not for autonomous execution gates. |
| `19` | `pattern_only_until_dependency_review` | `agent_app_builder` | [langgenius/dify](https://github.com/langgenius/dify) | `145619` | Huge adoption signal for visual agent/RAG/app building; useful as a product-studio reference, not as the internal company source of truth. |
| `17` | `pattern_only_high_side_effect_risk` | `workflow_automation` | [activepieces/activepieces](https://github.com/activepieces/activepieces) | `22801` | Open workflow automation surface that may inspire service-worker recipes and approval-gated integrations. |
| `15` | `pattern_only_until_dependency_review` | `agent_app_builder` | [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | `53686` | Mature low-code LLM/agent workflow builder; useful for comparing productized dashboard UX and connector patterns. |
| `15` | `pattern_only_until_dependency_review` | `typescript_agent_app_framework` | [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | `25178` | Modern TypeScript agent app stack with workflows, agents, memory, and observability; useful if the company needs a web-facing agent app layer. |

## Recommended Next Builds

| Build | Reason |
| --- | --- |
| `sandbox_execution_gate_contract_v1` | OpenHands and E2B score highly for future code-worker lanes, but only after local sandbox limits for filesystem, network, secrets, cost, teardown, and proof capture exist. |
| `workflow_automation_service_worker_manifest_v1` | n8n, Activepieces, Dify, Langflow, and Flowise have high adoption but require credential/public-action gates before any execution. |
| `agent_platform_control_plane_gap_map_v1` | Agno/VoltAgent/Strands expose useful scheduling, RBAC, tracing, intervention, and ops-console ideas to compare against the SQLite CEO ledger. |

## Hold Until Gated

- `dependency installs/imports`
- `runtime or server starts`
- `workflow/connector execution`
- `credentials/API keys/secrets`
- `browser sessions`
- `public actions or PR/comment/submission flows`
- `cloud sandbox start or billable execution`
- `service_request mutation`

## Boundary

- This matrix is local and report-only.
- It performs no dependency install/import, runtime/server start, workflow execution, credential/API-key use, browser session, public action, cloud sandbox start, service-request mutation, worker start, model/API call, payment, wallet, security-testing, real-money action, or external side effect.
