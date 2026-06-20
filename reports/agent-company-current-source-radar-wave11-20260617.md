# Agent Company Current-Source Radar Wave 11

Generated UTC: 2026-06-17T18:06:33Z
Capture UTC: 2026-06-17T18:05:00Z
Task: `task-agent-company-current-source-radar-wave11-20260617`
Dataset: `E:\agent-company-lab\data\agent-company-current-source-radar-wave11-20260617.json`
CSV: `E:\agent-company-lab\data\agent-company-current-source-radar-wave11-20260617.csv`
Validation: `E:\agent-company-lab\reports\agent-company-current-source-radar-wave11-validation-20260617.json`

## Purpose

Refresh the platform radar for the parts of an agent company that sit around the core runtime: control planes, agent app builders, workflow automation, coding-agent harnesses, and sandboxes. This wave is read-only and does not install, execute, deploy, register, submit, or call model APIs.

## Source Boundary

- GitHub/API metadata rows captured: `11`
- Repos noted but rate-limited before metadata capture: `8`
- Validation failures: `0`

Rate-limited follow-ups to revisit later: `daytonaio/daytona`, `BerriAI/litellm`, `Helicone/helicone`, `AgentOps-AI/agentops`, `microsoft/semantic-kernel`, `Kilo-Org/kilocode`, `sst/opencode`, `Significant-Gravitas/AutoGPT`

## Ranked Current Signals

| Fit | Stars | Last Push | Category | Repo | Local Decision | Gate |
| ---: | ---: | --- | --- | --- | --- | --- |
| `11` | `192938` | `2026-06-17T17:59:25Z` | `workflow_automation` | [n8n-io/n8n](https://github.com/n8n-io/n8n) | `reference_for_service_worker_workflow_ui` | `report_only_no_credentials_no_workflow_execution` |
| `11` | `149790` | `2026-06-17T18:02:48Z` | `agent_app_builder` | [langflow-ai/langflow](https://github.com/langflow-ai/langflow) | `reference_for_visual_flow_patterns` | `report_only_no_flow_execution_no_api_keys` |
| `11` | `145619` | `2026-06-17T17:49:19Z` | `agent_app_builder` | [langgenius/dify](https://github.com/langgenius/dify) | `reference_for_product_studio_and_app_builder` | `report_only_no_container_no_account_no_public_app` |
| `10` | `77538` | `2026-06-17T18:04:44Z` | `coding_agent_harness` | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | `sandboxed_code_worker_pattern_candidate` | `report_only_no_code_execution_no_pr_public_action` |
| `10` | `40749` | `2026-06-17T17:15:36Z` | `agent_platform_control_plane` | [agno-agi/agno](https://github.com/agno-agi/agno) | `study_control_plane_patterns` | `report_only_no_dependency_install_no_runtime_start` |
| `9` | `53686` | `2026-06-16T11:05:50Z` | `agent_app_builder` | [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | `reference_for_low_code_agent_pipeline_ui` | `report_only_no_node_install_no_api_keys` |
| `9` | `25178` | `2026-06-17T18:04:15Z` | `typescript_agent_app_framework` | [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | `watch_ts_agent_app_surface` | `report_only_no_node_install_no_server_start` |
| `9` | `22801` | `2026-06-17T17:22:19Z` | `workflow_automation` | [activepieces/activepieces](https://github.com/activepieces/activepieces) | `watch_as_open_workflow_automation_alternative` | `report_only_no_credentials_no_workflow_execution` |
| `9` | `12632` | `2026-06-17T15:50:01Z` | `sandbox_execution` | [e2b-dev/E2B](https://github.com/e2b-dev/E2B) | `sandbox_contract_candidate` | `report_only_no_cloud_sandbox_no_api_key_no_cost` |
| `9` | `6186` | `2026-06-17T17:10:42Z` | `production_agent_harness` | [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk) | `watch_harness_and_intervention_primitives` | `report_only_no_sdk_install_no_model_api` |
| `7` | `9659` | `2026-06-08T20:06:55Z` | `typescript_agent_ops_platform` | [VoltAgent/voltagent](https://github.com/voltagent/voltagent) | `watch_observability_guardrails_evals` | `report_only_no_console_no_cloud_no_deploy` |

## Architecture Takeaways

1. Agent-platform projects are converging on exactly the company primitives we need: control plane, tracing, scheduling, RBAC, intervention, workflow, memory, evals, and deployment. The right move is a local capability matrix, not an immediate framework replacement.
2. Visual app builders and workflow tools have massive adoption, but their default posture is connector execution. They belong behind service-worker manifests, credential gates, and approval scopes.
3. Coding-agent and sandbox projects are strategically important because future money lanes will ask workers to run code, inspect repos, and make patches. That needs a sandbox execution gate contract first.
4. The current SQLite CEO ledger remains the brain. These projects are pattern sources, UI references, and possible adapters.

## Recommended Local Builds

| Build | Why |
| --- | --- |
| `agent_platform_capability_matrix_v1` | Compare Agno, Mastra, VoltAgent, Strands, and current SQLite control-plane capabilities before any dependency install. |
| `sandbox_execution_gate_contract_v1` | E2B/OpenHands/Daytona-style workers need a local contract for code execution, secrets, files, network, cost, and teardown. |
| `workflow_automation_service_worker_manifest_v1` | n8n, Activepieces, Flowise, Dify, and Langflow should inform service-worker recipe UX while all credentials and actions remain gated. |

## Hold Until Gated

- `workflow execution`
- `container or cloud sandbox start`
- `credential/API key use`
- `public app deployment`
- `model/provider execution`
- `public GitHub or marketplace action`

## Boundary

- Browser sessions started: `0`
- Account/wallet/payment/public/security/real-money actions: `false`
- Model/API calls: `false`
- Dependency installs/imports: `0`
- Runtime starts: `0`
- Service requests updated/assigned: `0`
- Worker starts: `0`
- External side effects: `false`
