# Agent Egress Event Ledger Packet v1

Generated UTC: 2026-06-17T19:08:42Z

Lane: platform_engineering

Task: task-agent-egress-event-ledger-packet-v1-20260617

## Purpose

This packet defines the local evidence model required before any future worker can perform an action that leaves the agent-company lab.

The egress ledger is not a live gateway. It is the control-plane contract that says every future model call, MCP tool call, direct API call, browser action, signed-in browser action, public submission, wallet/payment-adjacent action, or agent-to-agent action must have a policy verdict and artifact trail before execution.

Default policy: deny.

## Inputs

- Gateway matrix: `E:\agent-company-lab\reports\agent-company-gateway-candidate-matrix-v1-20260617.json`
- Identity matrix: `E:\agent-company-lab\reports\agent-identity-envelope-matrix-v1-20260617.json`
- Worker-pool operator decision packet: `E:\agent-company-lab\reports\worker-pool-operator-decision-packet-v1-20260617.json`
- Chain integrity validation: `E:\agent-company-lab\reports\service-worker-chain-integrity-validation-latest.json`

## Required Egress Event Fields

Each future egress event must include:

- `egress_event_id`
- `egress_schema_version`
- `created_utc`
- `expires_utc`
- `request_id`
- `task_id`
- `lane_id`
- `agent_id`
- `worker_pool_id`
- `identity_envelope_id`
- `identity_envelope_artifact_path`
- `operator_decision_id`
- `operator_decision_artifact_path`
- `service_request_artifact_path`
- `egress_type`
- `target`
- `tool_or_model`
- `input_artifact_path`
- `output_artifact_path`
- `credential_scope`
- `browser_scope`
- `mcp_scope`
- `model_api_scope`
- `wallet_scope`
- `payment_scope`
- `public_action_scope`
- `budget_scope`
- `rate_limit_scope`
- `policy_verdict`
- `policy_reasons`
- `policy_evaluator`
- `redaction_required`
- `recording_required`
- `rollback_or_teardown_artifact_path`
- `runtime_boundary`
- `external_side_effects_expected`
- `post_execution_evidence_required`
- `revocation_status`

## Egress Types

Allowed `egress_type` values:

- `model_api`
- `mcp_tool`
- `direct_api`
- `browser_read_only`
- `browser_signed_in`
- `computer_use`
- `public_submission`
- `wallet_payment`
- `account_registration`
- `credential_access`
- `github_public_action`
- `marketplace_action`
- `outreach_delivery`
- `agent_to_agent`

## Policy Verdicts

Allowed `policy_verdict` values:

- `deny`
- `pause_for_review`
- `allow_report_only_preflight`
- `allow_after_operator_approval`

This packet does not permit live `allow` execution. Any future live allow state must be added by a separate approved implementation contract and validator.

## Validation Rules

An egress event is valid only if:

1. `egress_schema_version` is `agent_company.agent_egress_event_ledger.v1`.
2. `created_utc` and `expires_utc` are present and ordered correctly.
3. `request_id`, `task_id`, `lane_id`, `agent_id`, and `worker_pool_id` are present.
4. `identity_envelope_id` and `identity_envelope_artifact_path` are present.
5. `operator_decision_id` and `operator_decision_artifact_path` are present for any non-deny verdict.
6. `egress_type` is one of the allowed values.
7. All scope fields are explicit.
8. `policy_verdict` is one of the allowed values.
9. `policy_reasons` is non-empty.
10. `input_artifact_path` is present before execution.
11. `output_artifact_path` is declared before execution.
12. `runtime_boundary.external_side_effects` is false for report-only/preflight events.
13. `external_side_effects_expected` is false unless a future approved live-execution contract exists.
14. The event does not broaden the identity envelope or operator decision scope.
15. Any account, wallet, payment, public submission, marketplace, GitHub public action, outreach, signed-in browser, or credential-access event defaults to `deny` or `pause_for_review`.

## Negative Fixtures

The future validator must reject:

| Fixture id | Reason |
| --- | --- |
| `missing_identity_envelope` | No non-human principal scope. |
| `missing_operator_decision` | No operator authority for non-deny event. |
| `expired_egress_event` | Egress event expired. |
| `unknown_egress_type` | Egress type outside contract. |
| `implicit_credentials` | Credential scope left vague. |
| `implicit_budget` | Cost/rate scope missing. |
| `missing_output_artifact` | Result path not declared before execution. |
| `scope_broadened_from_identity` | Event exceeds identity envelope. |
| `scope_broadened_from_decision` | Event exceeds operator decision. |
| `signed_in_browser_as_read_only` | Signed-in browser hidden under read-only category. |
| `public_action_allowed_without_cro` | Public action lacks CRO/reputation gate. |
| `wallet_payment_non_deny` | Wallet/payment not denied or paused. |
| `model_api_no_provider_cost` | Model/API event missing provider, model, and cost scope. |
| `mcp_server_not_registered` | MCP server/tool not in registry. |
| `external_side_effects_report_only` | Report-only event expects external side effects. |

## Candidate First Egress Events

The first safe events to model later are report-only/preflight events:

| Candidate | Egress type | Verdict | Rationale |
| --- | --- | --- | --- |
| Local runtime adapter dry-run evidence | `direct_api` or `agent_to_agent` | `allow_report_only_preflight` | Local-only, supports future runtime verification, no external side effects. |
| Browser read-only domain probe packet | `browser_read_only` | `pause_for_review` | High service-request demand, but domain/session/recording scope must be explicit. |
| Model API costed dry-run packet | `model_api` | `pause_for_review` | Needs provider/model/cost/input/output scope before any model call. |
| MCP registry review packet | `mcp_tool` | `deny` | Unknown tools must remain disabled until registry gate exists. |

These are candidate event shapes, not approvals.

## Mapping To Future Gateways

If approved later:

- LiteLLM can enforce/model-route approved `model_api` and possibly `mcp_tool` events.
- Portkey can inform model-routing, fallback, and guardrail placement.
- Kong/TrueFoundry/Lunar-style gateways can inform enterprise egress taxonomy.
- The local SQLite ledger remains authoritative for approval, evidence, and chain integrity.

## Runtime Boundary

This packet:

- starts no gateway
- installs no gateway
- creates no API keys
- records no live egress events
- calls no model APIs
- calls no MCP tools
- opens no browser sessions
- registers no worker pools
- assigns no service requests
- starts no workers
- touches no accounts, credentials, wallets, payments, marketplaces, GitHub public actions, X, outreach, or submissions
- changes no external state

## Decision

Recommended next report-only build: `agent_egress_event_ledger_contract_v1` schema, fixtures, and validator design after implementation-design approval.

