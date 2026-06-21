# CEO Operator Event Surface Contract v1

Generated UTC: 2026-06-21T15:44:06Z
Report JSON: `E:\agent-company-lab\reports\ceo-operator-event-surface-contract-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\ceo-operator-event-surface-contract-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Contract status: `report_only_event_surface_ready`
- Event types: `12`
- Accepted fixtures: `12`
- Rejected fixtures: `37`
- Event transport enabled: `False`
- SSE enabled: `False`
- WebSocket enabled: `False`
- Operator events emitted: `0`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `False`

## Event Types

| Event Type | Producer | Consumer |
| --- | --- | --- |
| `ceo_review_snapshot` | `ceo` | `all_managers` |
| `manager_status_update` | `lane_manager` | `ceo` |
| `worker_capability_signal` | `service_worker_registry` | `lane_manager` |
| `service_request_gate_ping` | `service_bureau` | `requesting_manager` |
| `tool_auth_request_proposed` | `lane_manager` | `chief_risk_officer` |
| `approval_decision_needed` | `gate_validator` | `human_operator` |
| `route_blocker_changed` | `egress_gateway` | `ceo` |
| `artifact_evidence_attached` | `agent_worker` | `lane_manager` |
| `outcome_realization_recorded` | `lane_manager` | `ceo` |
| `trace_replay_pointer` | `observability_worker` | `ceo` |
| `human_operator_note` | `human_operator` | `lane_manager` |
| `dispatch_next_action` | `ceo` | `lane_manager` |

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_ceo_review_snapshot` | `accepted` | `True` | `True` |  |
| `positive_manager_status_update` | `accepted` | `True` | `True` |  |
| `positive_worker_capability_signal` | `accepted` | `True` | `True` |  |
| `positive_service_request_gate_ping` | `accepted` | `True` | `True` |  |
| `positive_tool_auth_request_proposed` | `accepted` | `True` | `True` |  |
| `positive_approval_decision_needed` | `accepted` | `True` | `True` |  |
| `positive_route_blocker_changed` | `accepted` | `True` | `True` |  |
| `positive_artifact_evidence_attached` | `accepted` | `True` | `True` |  |
| `positive_outcome_realization_recorded` | `accepted` | `True` | `True` |  |
| `positive_trace_replay_pointer` | `accepted` | `True` | `True` |  |
| `positive_human_operator_note` | `accepted` | `True` | `True` |  |
| `positive_dispatch_next_action` | `accepted` | `True` | `True` |  |
| `negative_event_surface_status` | `rejected` | `False` | `True` | event_surface_status_must_be_report_only_contract |
| `negative_event_type` | `rejected` | `False` | `True` | event_type_not_in_contract |
| `negative_producer_role` | `rejected` | `False` | `True` | producer_role_missing |
| `negative_consumer_role` | `rejected` | `False` | `True` | consumer_role_missing |
| `negative_approval_granted_by_event` | `rejected` | `False` | `True` | approval_granted_by_event_must_be_false |
| `negative_event_transport_enabled` | `rejected` | `False` | `True` | event_transport_enabled_must_be_false |
| `negative_sse_enabled` | `rejected` | `False` | `True` | sse_enabled_must_be_false |
| `negative_websocket_enabled` | `rejected` | `False` | `True` | websocket_enabled_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_service_request_mutation_allowed` | `rejected` | `False` | `True` | service_request_mutation_allowed_must_be_false |
| `negative_model_api_call_allowed` | `rejected` | `False` | `True` | model_api_call_allowed_must_be_false |
| `negative_mcp_tool_call_allowed` | `rejected` | `False` | `True` | mcp_tool_call_allowed_must_be_false |
| `negative_public_action_allowed` | `rejected` | `False` | `True` | public_action_allowed_must_be_false |
| `negative_external_side_effects` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_missing_source_paths` | `rejected` | `False` | `True` | source_artifact_paths_must_include_current_operator_sources |
| `negative_outside_source_path` | `rejected` | `False` | `True` | source_artifact_paths_must_include_current_operator_sources, source_artifact_path_must_stay_inside_lab |
| `negative_missing_payload_required_field` | `rejected` | `False` | `True` | payload_required_field_missing:event_type, payload_required_field_missing:lane_id, payload_required_field_missing:task_id, payload_required_field_missing:agent_id |
| `negative_missing_gate` | `rejected` | `False` | `True` | required_gate_missing:agent_egress_event_ledger_v1, required_gate_missing:service_worker_chain_integrity_v1, required_gate_missing:unified_agent_egress_gateway_docket_v1 |
| `negative_boundary_event_transports_started` | `rejected` | `False` | `True` | runtime_boundary_event_transports_started_must_equal_0 |
| `negative_boundary_operator_events_emitted` | `rejected` | `False` | `True` | runtime_boundary_operator_events_emitted_must_equal_0 |
| `negative_boundary_operator_events_persisted` | `rejected` | `False` | `True` | runtime_boundary_operator_events_persisted_must_equal_0 |
| `negative_boundary_approval_rows_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_boundary_decisions_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_boundary_tasks_created` | `rejected` | `False` | `True` | runtime_boundary_tasks_created_must_equal_0 |
| `negative_boundary_tasks_updated` | `rejected` | `False` | `True` | runtime_boundary_tasks_updated_must_equal_0 |
| `negative_boundary_service_requests_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_boundary_service_requests_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_boundary_worker_starts` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_boundary_browser_sessions_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_boundary_runtime_starts` | `rejected` | `False` | `True` | runtime_boundary_runtime_starts_must_equal_0 |
| `negative_boundary_dependency_installs` | `rejected` | `False` | `True` | runtime_boundary_dependency_installs_must_equal_0 |
| `negative_boundary_sse_connections_opened` | `rejected` | `False` | `True` | runtime_boundary_sse_connections_opened_must_equal_0 |
| `negative_boundary_websocket_connections_opened` | `rejected` | `False` | `True` | runtime_boundary_websocket_connections_opened_must_equal_0 |
| `negative_boundary_mcp_tool_calls` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_boundary_model_api_calls` | `rejected` | `False` | `True` | runtime_boundary_model_api_calls_must_equal_False |
| `negative_boundary_public_actions` | `rejected` | `False` | `True` | runtime_boundary_public_actions_must_equal_False |
| `negative_boundary_external_side_effects` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- This contract defines local operator event templates only.
- It does not enable SSE, WebSockets, browser sessions, workers, service-request mutation, model/API calls, MCP tool calls, public actions, account/wallet/payment actions, or external side effects.

Next action: Use this report-only event surface to design local CEO/manager inbox packets; do not enable SSE, WebSockets, browser sessions, worker starts, service-request mutation, model/MCP calls, public actions, or external side effects.
