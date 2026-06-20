# Agent Company Execution Governance Radar Wave 12

Generated UTC: 2026-06-17T18:28:51Z
Capture UTC: 2026-06-17T18:25:00Z
Task: `task-agent-company-execution-governance-radar-wave12-20260617`
Dataset: `E:\agent-company-lab\data\agent-company-execution-governance-radar-wave12-20260617.json`
Validation: `E:\agent-company-lab\reports\agent-company-execution-governance-radar-wave12-validation-20260617.json`

## Purpose

Refresh current open-source and GitHub signals specifically for scalable agent execution governance: goal-to-DAG orchestration, policy control planes, computer/browser-use sandboxes, agent observability, and incident/SRE gates.

## Source Boundary

- Source rows: `13`
- Directly opened/captured source rows: `8`
- Search-result captured rows: `5`
- GitHub API batch result: `HTTP 403 rate limit exceeded for the selected repo metadata batch`
- Validation failures: `0`

## Ranked Signals

| Score | Category | Source | Signal | Local Implication | Gate |
| ---: | --- | --- | --- | --- | --- |
| `12` | `governance_control_plane` | [cordum-io/cordum](https://github.com/cordum-io/cordum) | GitHub topic listing describes an open agent control plane with pre-execution policy enforcement, approval gates, and audit trails. | Promote a policy-kernel comparison against current approval, scope, command-safety, authority, and preflight reports. | `report_only_no_dependency_install_no_policy_runtime` |
| `11` | `goal_to_dag_orchestration` | [open-multi-agent/open-multi-agent](https://github.com/open-multi-agent/open-multi-agent) | Recent TypeScript-native framework that turns a goal into a task DAG, parallelizes independent work, and provides a post-run dashboard. | Add a local report-only task-DAG contract before launching many more lane-agent chats. | `report_only_no_node_install_no_model_key_no_runtime_start` |
| `10` | `operating_model_reference` | [GitHub: What is AI agent orchestration?](https://github.com/resources/articles/what-is-ai-agent-orchestration) | Defines agent orchestration as the control layer for managing execution, shared context, collaboration, guardrails, cost limits, and HITL checkpoints. | The company needs a deterministic policy layer around dynamic agent planning, not just task prompts. | `public_read_only_reference_no_runtime_action` |
| `10` | `computer_use_sandbox` | [agent-infra/sandbox](https://github.com/agent-infra/sandbox) | All-in-one agent sandbox combining browser, shell, file, MCP operations, VSCode Server, VNC, Jupyter, and terminal in one container. | Extend the sandbox execution gate contract with browser/file/shell/MCP cross-contamination checks before any container start. | `report_only_no_docker_no_vnc_no_mcp_server_start` |
| `9` | `browser_worker_harness` | [browser-use/browser-use](https://github.com/browser-use/browser-use) | Browser Use 0.13 introduces a beta agent with Rust core, browser harness, persistent tools, and recovery loops inspired by coding agents. | Keep browser workers behind exact-scope packets and add recovery-loop logging requirements. | `report_only_no_browser_start_no_api_key_no_public_action` |
| `9` | `agent_team_optimization` | [NVIDIA/NeMo-Agent-Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) | Open-source toolkit for connecting and optimizing teams of AI agents, with instrumentation, observability, continuous learning, MCP publishing, and workflow UI ideas. | The local company needs eval/learning loops per lane before it scales worker count. | `report_only_no_pip_install_no_workflow_execution_no_model_api` |
| `9` | `agent_observability_eval` | [mlflow/mlflow](https://github.com/mlflow/mlflow) | MLflow positions itself as an AI engineering platform for agents with debugging, evaluation, monitoring, OpenTelemetry, MCP, cost, and safety monitoring. | Promote a local trace-to-eval export contract before integrating Langfuse/Phoenix/MLflow/AgentOps. | `report_only_no_backend_no_tracking_server_no_api_key` |
| `8` | `agent_router` | [2FastLabs/agent-squad](https://github.com/2FastLabs/agent-squad) | Framework for routing among multiple agents and maintaining context across interactions. | Add explicit route-decision evidence rows whenever the CEO sends work to lane managers. | `report_only_no_framework_import_no_cloud_deploy` |
| `8` | `agent_sre_governance` | [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) | Search result highlights Agent SRE, OpenTelemetry, Prometheus, and integrations with observability platforms. | Add local agent-SRE severity, rollback, and pause contracts before enabling worker starts. | `report_only_no_agent_sre_runtime_no_prometheus_export` |
| `7` | `browser_worker_harness` | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | New browser automation CLI for AI agents, described as a fast native Rust CLI. | Browser workers should have a CLI-command safety review similar to service-worker decision command safety. | `report_only_no_npm_install_no_chrome_download_no_browser_start` |
| `6` | `desktop_computer_use` | [trycua/cua](https://github.com/trycua/cua) | GitHub topic result describes open-source infrastructure for computer-use agents controlling full desktops across operating systems. | Desktop-control workers need the strictest service gate: screen recording, action allowlist, credential masking, and kill switch. | `report_only_no_desktop_control_no_vm_start_no_credentials` |
| `6` | `sandbox_execution` | [opensandbox-group/OpenSandbox](https://github.com/opensandbox-group/OpenSandbox) | GitHub result describes a sandbox runtime for AI agents with SDK usage, integrations, browser automation, and training workloads. | Sandbox selection should be delayed until the local boundary matrix and cost/secrets controls are complete. | `report_only_no_sdk_install_no_sandbox_start` |
| `6` | `agent_workspace_safety` | [auto-use/Auto-Use](https://github.com/auto-use/Auto-Use) | Search result describes sandboxed Bash confined to a desktop workspace with path blocklists, timeouts, and stdin detection plus browser automation. | Our sandbox gate should require path allowlists/blocklists, idle/total timeouts, and interactive-stdin rejection. | `report_only_no_shell_harness_install_no_browser_action` |

## Recommended Local Builds

| Build | Why | Informed By |
| --- | --- | --- |
| `agent_task_dag_contract_v1` | Before launching many autonomous lane chats, define how one CEO goal becomes tasks, dependencies, assignees, checkpoints, and synthesis evidence. | `open_multi_agent_goal_to_dag`, `github_ai_agent_orchestration_article` |
| `agent_governance_policy_kernel_gap_map_v1` | Compare the existing approval/scope/authority/preflight chain with external governance-control-plane patterns. | `cordum_governance_control_plane`, `microsoft_agent_governance_toolkit` |
| `computer_use_sandbox_boundary_matrix_v1` | Browser, shell, file, MCP, VSCode, and desktop-control surfaces must be isolated before external workers can act safely. | `agent_infra_aio_sandbox`, `trycua_computer_use`, `opensandbox_group_opensandbox`, `auto_use_desktop_workspace` |
| `browser_worker_recovery_loop_contract_v1` | Browser automation should log recoveries, retries, observed state, and stop reasons before any approved public action worker exists. | `browser_use_rust_core`, `vercel_agent_browser` |
| `agent_trace_eval_export_contract_v1` | Scale requires per-lane learning/eval loops, cost/safety monitoring, and trace export without immediately adopting a hosted backend. | `mlflow_agents_engineering_platform`, `nvidia_nemo_agent_toolkit` |

## Architecture Decision

Keep the SQLite CEO ledger and service-request chain as source of truth. Add goal-to-DAG, governance-policy, sandbox-boundary, browser-recovery, and trace/eval contracts before any dependency install or external worker start.

## Boundary

- Browser sessions started: `0`
- Account/wallet/payment/public/security/real-money actions: `false`
- Model/API calls: `false`
- Dependency installs/imports: `0`
- Runtime starts: `0`
- Service requests updated/assigned: `0`
- Worker starts: `0`
- External side effects: `false`
