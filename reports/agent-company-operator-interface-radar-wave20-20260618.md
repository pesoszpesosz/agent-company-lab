# Agent Company Operator Interface Radar Wave 20

Generated UTC: 2026-06-18T02:49:21Z
Task: `task-agent-company-operator-interface-radar-wave20-20260618`
Dataset: `E:\agent-company-lab\data\agent-company-operator-interface-radar-wave20-20260618.json`
CSV: `E:\agent-company-lab\data\agent-company-operator-interface-radar-wave20-20260618.csv`
Validation: `E:\agent-company-lab\reports\agent-company-operator-interface-radar-wave20-20260618-validation.json`

## Purpose

Refresh the agent-company infrastructure map with current primary-source GitHub evidence for the operator interface layer: agent UI protocols, generative UI, human-in-the-loop workflows, delegated tool authentication, collaborative multi-agent rooms, and governance gateways. This wave is read-only and does not install dependencies, start runtimes, assign service requests, open browsers, call models, call MCP tools, post publicly, touch wallets, or move money.

## Source Boundary

- Candidate rows captured: `9`
- GitHub metadata reads: `9`
- README reads: `8`
- Candidate fetch errors: `0`
- Discarded lookup errors: `1`
- External side effects: `False`

## Ranked Current Signals

| Rank | Score | Stars | Last Push | Category | Repo | Local Decision | Gate |
| ---: | ---: | ---: | --- | --- | --- | --- | --- |
| `1` | `20` | `35261` | `2026-06-18T02:03:39Z` | `agent_native_frontend_and_hitl` | [CopilotKit/CopilotKit](https://github.com/CopilotKit/CopilotKit) | `reference_operator_console_generative_ui_and_human_review_patterns` | `no_frontend_runtime_model_api_browser_or_public_action_without_signed_scope` |
| `2` | `20` | `28825` | `2026-06-17T16:59:12Z` | `tool_auth_router_and_action_gateway` | [ComposioHQ/composio](https://github.com/ComposioHQ/composio) | `reference_toolkit_auth_context_and_sandboxed_workbench_patterns` | `no_external_app_auth_api_key_tool_execution_or_mcp_call_without_service_request_approval` |
| `3` | `20` | `25182` | `2026-06-18T02:39:16Z` | `typescript_agent_workflow_hitl_mcp_eval` | [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | `reference_workflow_suspend_resume_mcp_server_evals_and_observability_shapes` | `no_dependency_install_model_api_runtime_start_or_mcp_server_without_signed_operator_decision` |
| `4` | `19` | `14320` | `2026-06-17T13:57:41Z` | `agent_user_interaction_protocol` | [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | `adopt_event_vocabulary_for_local_ceo_console_contract` | `no_network_transport_or_agent_runtime_start_without_browser_model_and_runtime_gates` |
| `5` | `17` | `10670` | `2026-06-17T22:29:59Z` | `production_chat_ui_components` | [assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui) | `reference_chat_surface_components_for_local_atlas_and_manager_inboxes` | `no_model_api_no_external_chat_backend_no_dependency_install` |
| `6` | `17` | `4867` | `2026-06-17T05:56:56Z` | `collaborative_multi_agent_os_human_visible_rooms` | [agentscope-ai/HiClaw](https://github.com/agentscope-ai/HiClaw) | `reference_manager_worker_rooms_shared_files_gateway_credentials_and_human_visibility` | `no_kubernetes_container_gateway_matrix_or_worker_runtime_start_without_signed_operator_decision` |
| `7` | `16` | `2934` | `2026-06-13T01:18:43Z` | `langgraph_agent_chat_operator_ui` | [langchain-ai/agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui) | `reference_agent_chat_connection_packet_for_future_approved_langgraph_workers` | `no_langsmith_key_deployment_url_or_remote_graph_call_without_model_api_and_secrets_gates` |
| `8` | `15` | `88` | `2026-02-12T06:31:56Z` | `agent_governance_gateway` | [elliot35/deterministic-agent-control-protocol](https://github.com/elliot35/deterministic-agent-control-protocol) | `reference_policy_audit_reversal_and_mcp_shell_proxy_controls_as_design_input` | `no_proxy_install_shell_governance_mcp_server_or_http_api_start_without_runtime_and_mcp_gates` |
| `9` | `10` | `1858` | `2026-02-25T18:08:15Z` | `archived_no_code_agent_builder_reference` | [langchain-ai/open-agent-platform](https://github.com/langchain-ai/open-agent-platform) | `park_archived_repo_but_mine_builder_information_architecture` | `no_runtime_adoption_archived_repository_only_reference_ui_patterns` |

## Architecture Decisions

1. `ceo_event_surface_before_more_visual_dashboard_work`
   AG-UI and CopilotKit show that agent-human interaction needs a portable event vocabulary: messages, tool states, approvals, shared state, and streamed updates. The local Atlas already visualizes state, but it lacks a stable operator-event contract.
   Next build: `ceo_operator_event_surface_contract_v1`

2. `delegated_tool_auth_packets_before_composio_like_connectors`
   Composio's value is not just many tools; it is auth, context, tool search, and sandboxed action routing. The lab should model delegated tool-auth request packets before any external connector, account, OAuth, or MCP tool execution.
   Next build: `delegated_tool_auth_request_packet_v1`

3. `room_visibility_contract_before_worker_runtime_rooms`
   HiClaw validates the user's company metaphor: manager-worker rooms, human visibility, shared files, gateway-held credentials, and auditable collaboration. The local equivalent should be a no-runtime room/handoff contract first.
   Next build: `multi_agent_room_handoff_contract_v1`

4. `reversibility_policy_before_any_proxy_or_shell_governance`
   The deterministic-agent-control-protocol repo is small but directly relevant to bounded, auditable, reversible action governance. The lab should convert that idea into a local matrix before any proxy, shell, MCP server, or HTTP gateway is started.
   Next build: `agent_action_reversibility_policy_matrix_v1`

## Recommended Next Sequence

1. `ceo_operator_event_surface_contract_v1` - define local event types for manager inboxes, approvals, tool proposals, worker status, route blockers, and CEO review.
2. `delegated_tool_auth_request_packet_v1` - model how agents request external app/tool auth without receiving credentials or executing actions.
3. `multi_agent_room_handoff_contract_v1` - specify local manager-worker-room records, shared-file links, human-visible transcript artifacts, and gateway ownership.
4. `agent_action_reversibility_policy_matrix_v1` - classify actions by reversible, compensating, irreversible, public, secret-bearing, money-bearing, or legal/KYC impact.

## Hold Until Gated

- Dependency installs for CopilotKit, AG-UI, Mastra, Composio, assistant-ui, HiClaw, Agent Chat UI, or governance gateways.
- Runtime starts, browser sessions, Matrix/Kubernetes/container launches, MCP servers, MCP tool calls, model/API calls, OAuth/app authentication, public actions, account actions, wallet/payment actions, telemetry exports, or shell proxy starts.
- Service-request assignments or approvals without explicit signed operator decision artifacts.

## Boundary

- account_actions: `False`
- browser_sessions_started: `0`
- dependency_installs: `0`
- external_side_effects: `False`
- mcp_tool_calls: `False`
- model_api_calls: `False`
- payment_actions: `False`
- public_actions: `False`
- runtime_starts: `0`
- security_testing_actions: `False`
- service_requests_assigned: `0`
- service_requests_updated: `0`
- wallet_actions: `False`
- worker_starts: `0`
