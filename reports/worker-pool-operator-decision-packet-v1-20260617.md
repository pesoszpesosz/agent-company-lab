# Worker Pool Operator Decision Packet v1

Generated UTC: 2026-06-17T19:06:41Z

Lane: platform_engineering

Task: task-worker-pool-operator-decision-packet-v1-20260617

## Purpose

This packet defines the decision artifact required before any worker pool can be registered from the existing worker-pool registration review packets.

The control rule is simple: a command preview is not authority. A future `register-agent` command may only be considered after a signed operator decision references the exact worker pool, approval scope, identity envelope, expiry, and permitted next action.

## Inputs

- Source registration review: `E:\agent-company-lab\reports\worker-pool-registration-review-v1-20260617.json`
- Source identity envelope matrix: `E:\agent-company-lab\reports\agent-identity-envelope-matrix-v1-20260617.json`
- Current integrity validation: `E:\agent-company-lab\reports\service-worker-chain-integrity-validation-latest.json`

## Source State

The source review contains 7 worker-pool review packets:

| Worker pool | Priority | Review route | Current request count | Required posture |
| --- | --- | --- | ---: | --- |
| `service-worker-browser-read-only-pool` | high | manual_review_register_later | 7 | Candidate for first approval after identity envelope exists |
| `service-worker-signed-in-browser-read-only-pool` | low | manual_review_hold | 1 | Hold until signed-in browser safety and session policy exist |
| `service-worker-legal-kyc-payment-review-pool` | medium | manual_review_register_later | 1 | Candidate only with CRO/legal/payment scope |
| `service-worker-local-runtime-adapter-pool` | high | manual_review_register_later | 2 | Candidate for local-only runtime review after identity envelope exists |
| `service-worker-model-api-execution-pool` | medium | manual_review_register_later | 1 | Candidate only with provider/model/cost/input/output scope |
| `service-worker-other-gated-work-pool` | low | manual_review_hold | 1 | Hold until request type is narrowed |
| `service-worker-public-submission-review-pool` | medium | manual_review_register_later | 1 | Candidate only with CRO/reputation/public-action review scope |

## Decision Types

Allowed decision values:

- `approve_identity_envelope_draft`: permits drafting an identity envelope only. Does not register a pool.
- `approve_register_later_preflight`: permits a report-only preflight for a future registration. Does not register a pool.
- `hold`: explicitly keeps the pool blocked.
- `reject`: closes the pool registration path until a new review packet exists.
- `request_more_evidence`: asks for a narrower review artifact before any next step.

No decision type in this packet permits direct registration, assignment, worker start, browser use, API/model/MCP call, credential use, wallet/payment/account action, public action, or external side effect.

## Required Operator Decision Fields

Every decision artifact must include:

- `decision_id`
- `decision_schema_version`
- `created_utc`
- `expires_utc`
- `operator_id`
- `operator_attestation`
- `source_review_packet_id`
- `source_review_artifact_path`
- `worker_pool_id`
- `decision`
- `decision_rationale`
- `allowed_next_action`
- `identity_envelope_required`
- `identity_envelope_artifact_path`
- `allowed_service_request_types`
- `allowed_egress_types`
- `credential_scope`
- `browser_scope`
- `mcp_scope`
- `model_api_scope`
- `wallet_scope`
- `payment_scope`
- `public_action_scope`
- `budget_scope`
- `recording_required`
- `redaction_required`
- `runtime_boundary`
- `must_not_do`
- `approval_limitations`
- `supersedes_decision_id`
- `revocation_status`

## Decision Validation Rules

A decision is valid only if:

1. `decision_schema_version` is `agent_company.worker_pool_operator_decision.v1`.
2. `worker_pool_id` exists in the source registration review.
3. `source_review_packet_id` matches the named pool.
4. `expires_utc` is present and later than `created_utc`.
5. `operator_id` and `operator_attestation` are non-empty.
6. `decision` is one of the allowed decision values.
7. `allowed_next_action` is compatible with `decision`.
8. `identity_envelope_required` is true for every non-terminal decision.
9. `credential_scope`, `browser_scope`, `mcp_scope`, `model_api_scope`, `wallet_scope`, `payment_scope`, and `public_action_scope` are explicit.
10. `runtime_boundary.external_side_effects` is false.
11. `runtime_boundary.registers_pools` is false.
12. `runtime_boundary.assigns_service_requests` is false.
13. `runtime_boundary.starts_workers` is false.
14. `runtime_boundary.calls_apis` is false.
15. The decision does not broaden scope beyond the source review packet.

## Negative Fixtures

The following decision shapes must be rejected by a future validator:

| Fixture id | Reason |
| --- | --- |
| `missing_operator_attestation` | No accountable operator approval. |
| `expired_decision` | Decision cannot authorize future work after expiry. |
| `unknown_pool_id` | Pool not present in the source review. |
| `packet_pool_mismatch` | Review packet id does not match worker pool id. |
| `direct_register_action` | Attempts to use a decision as registration authority. |
| `assign_service_request_action` | Attempts to assign requests without a separate approved assignment gate. |
| `starts_worker_action` | Attempts to start a worker. |
| `browser_scope_escalation` | Escalates read-only browser pool to signed-in browser use. |
| `credential_scope_implicit` | Leaves credential authority vague. |
| `public_action_escalation` | Allows public submission without CRO/reputation gate. |
| `model_api_cost_missing` | Allows model/API execution without provider/model/cost scope. |
| `wallet_payment_allowed` | Allows wallet/payment work without explicit separate legal/payment approval. |

## Recommended First Decisions

The first two safe decisions to prepare later are:

1. `service-worker-local-runtime-adapter-pool`
   - Decision: `approve_identity_envelope_draft`
   - Rationale: local-only runtime review has lower external-action risk and supports future verification infrastructure.

2. `service-worker-browser-read-only-pool`
   - Decision: `approve_identity_envelope_draft`
   - Rationale: highest request count, but must stay read-only with explicit domain/session/recording policy.

These are not approvals. They are candidate decision shapes for a future operator-signed artifact.

## Runtime Boundary

This packet:

- registers no worker pools
- assigns no service requests
- starts no workers
- executes no command previews
- opens no browser sessions
- calls no model/API/MCP tools
- creates no credentials
- touches no accounts, wallets, payments, trades, public submissions, GitHub, X, or marketplaces
- changes no external state

## Decision

Recommended next report-only build: `worker_pool_operator_decision_contract_v1` schema and negative fixture suite, after implementation-design approval.

