# MCP Tool Registry Gate v1 Validation

Generated UTC: 2026-06-21T15:44:14Z
Source packet: `E:\agent-company-lab\reports\mcp-tool-registry-gate-packet-v1-20260617.json`
Schema: `E:\agent-company-lab\architecture\mcp-tool-registry-gate-v1.schema.json`
Validation JSON: `E:\agent-company-lab\reports\mcp-tool-registry-gate-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\mcp-tool-registry-gate-v1-20260617.json`
Fixture directory: `E:\agent-company-lab\reports\mcp-tool-registry-gate-v1-fixtures`

## Summary

- All checks passed: `True`
- Fixture count: `22`
- Accepted fixtures: `1`
- Rejected fixtures: `21`
- MCP server enable allowed: `False`
- MCP tool call allowed: `False`
- MCP servers started: `0`
- MCP tool calls: `False`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_local_report_only_registry_entry` | `accepted` | `True` | `True` |  |
| `negative_unknown_server` | `rejected` | `False` | `True` | server_id_not_registered_for_local_fixture, tool_server_id_must_match_registry_server |
| `negative_unknown_tool` | `rejected` | `False` | `True` | tool_id_must_be_allowlisted |
| `negative_disabled_server_call` | `rejected` | `False` | `True` | default_status_must_be_approved_report_only_for_positive_fixture |
| `negative_revoked_server_call` | `rejected` | `False` | `True` | registry_entry_not_active |
| `negative_implicit_credentials` | `rejected` | `False` | `True` | credential_requirements_must_be_none |
| `negative_missing_identity_envelope` | `rejected` | `False` | `True` | allowed_identity_envelope_ids_must_include_valid_identity |
| `negative_identity_scope_mismatch` | `rejected` | `False` | `True` | allowed_identity_envelope_ids_must_include_valid_identity |
| `negative_missing_egress_event` | `rejected` | `False` | `True` | egress_event_required_must_be_true |
| `negative_missing_operator_decision` | `rejected` | `False` | `True` | tool_requires_operator_decision_must_be_true |
| `negative_write_tool_as_read_only` | `rejected` | `False` | `True` | tool_side_effect_class_must_be_read_only |
| `negative_public_action_without_cro` | `rejected` | `False` | `True` | public_action_capable_must_be_false |
| `negative_wallet_payment_tool_non_deny` | `rejected` | `False` | `True` | payment_or_wallet_capable_must_be_false |
| `negative_missing_schema_artifacts` | `rejected` | `False` | `True` | tool_input_schema_artifact_path_missing |
| `negative_missing_output_artifact` | `rejected` | `False` | `True` | tool_output_schema_artifact_path_missing |
| `negative_unbounded_rate_or_budget` | `rejected` | `False` | `True` | rate_limit_scope_must_be_local_only, budget_scope_must_be_zero_or_not_applicable |
| `negative_network_scope_external` | `rejected` | `False` | `True` | network_scope_must_be_none |
| `negative_file_system_capable` | `rejected` | `False` | `True` | file_system_capable_must_be_false |
| `negative_browser_capable` | `rejected` | `False` | `True` | browser_capable_must_be_false |
| `negative_mcp_server_started` | `rejected` | `False` | `True` | runtime_boundary_mcp_servers_started_must_equal_0 |
| `negative_mcp_tool_called` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_registry_published` | `rejected` | `False` | `True` | runtime_boundary_registry_publications_must_equal_0 |

## Boundary

- This validator creates local fixture/report files only.
- It does not install, start, enable, publish, or call MCP servers or tools.
- A passing entry is only valid as local report-only registry evidence, not as permission to call an MCP tool.
