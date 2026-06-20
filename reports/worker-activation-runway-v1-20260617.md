# Worker Activation Runway v1

Generated UTC: 2026-06-17T19:13:40Z

Lane: platform_engineering

Task: task-worker-activation-runway-v1-20260617

## Purpose

This runway consolidates the worker-pool review, operator decision, identity envelope, egress ledger, and MCP registry gates into one activation sequence.

It does not approve registration or execution. It defines the order of evidence required before any worker pool can move from review to live work.

## Source Artifacts

- Worker-pool registration review: `E:\agent-company-lab\reports\worker-pool-registration-review-v1-20260617.json`
- Worker-pool operator decision packet: `E:\agent-company-lab\reports\worker-pool-operator-decision-packet-v1-20260617.json`
- Agent identity envelope matrix: `E:\agent-company-lab\reports\agent-identity-envelope-matrix-v1-20260617.json`
- Agent egress event ledger packet: `E:\agent-company-lab\reports\agent-egress-event-ledger-packet-v1-20260617.json`
- MCP tool registry gate packet: `E:\agent-company-lab\reports\mcp-tool-registry-gate-packet-v1-20260617.json`
- Current chain integrity validation: `E:\agent-company-lab\reports\service-worker-chain-integrity-validation-latest.json`

## Activation Sequence

Required order:

1. `review_packet_exists`
   - Source review packet names the worker pool and review route.
2. `operator_decision_artifact`
   - Operator decision names the exact pool, action, scope, expiry, and limitations.
3. `identity_envelope_artifact`
   - Worker pool has scoped non-human identity, allowed request types, allowed egress, credential/browser/MCP/model/wallet/payment/public-action policies, expiry, and revocation status.
4. `egress_ledger_contract`
   - Any future external action has a deny-by-default egress event with policy verdict, artifacts, budget/rate scope, and runtime boundary.
5. `tool_registry_gate`
   - MCP tools are default-disabled unless registered and matched to identity plus egress event.
6. `assignment_preflight`
   - Service request assignment proves request status, pool status, identity scope, operator decision, and egress policy match.
7. `runtime_start_preflight`
   - Worker start proves local/live boundary, recording, output artifact path, teardown/rollback, and post-execution evidence.
8. `execution`
   - Only possible after separate approval and validator implementation. Not permitted by this runway.
9. `evidence_seal`
   - Output artifact, trace event, outcome, and chain-integrity row must exist after any future execution.

## Pool Readiness Board

| Worker pool | Current request count | Current review route | Best next evidence | Activation status | Reason |
| --- | ---: | --- | --- | --- | --- |
| `service-worker-local-runtime-adapter-pool` | 2 | manual_review_register_later | identity envelope draft + operator decision contract | closest_to_local_pilot | Local-only boundary reduces external risk and supports infrastructure verification. |
| `service-worker-browser-read-only-pool` | 7 | manual_review_register_later | identity envelope draft + browser scope + recording/teardown policy | high_value_blocked | Highest request count, but browser domain/session policy is missing. |
| `service-worker-model-api-execution-pool` | 1 | manual_review_register_later | identity envelope draft + egress ledger + provider/model/cost scope | blocked_cost_and_api | Model/API calls need explicit cost, provider, input, and output artifact scope. |
| `service-worker-public-submission-review-pool` | 1 | manual_review_register_later | CRO/reputation gate + public-action scope | blocked_public_action | Public action authority cannot be inferred from registration review. |
| `service-worker-legal-kyc-payment-review-pool` | 1 | manual_review_register_later | CRO/legal/payment scope | blocked_legal_payment | Legal, KYC, tax, and payment commitments require explicit user/CRO approval. |
| `service-worker-signed-in-browser-read-only-pool` | 1 | manual_review_hold | signed-in browser safety packet | hold | Signed-in browser state is higher risk than read-only browser research. |
| `service-worker-other-gated-work-pool` | 1 | manual_review_hold | narrower request-type definition | hold | Request type is too broad to activate safely. |

## First Safe Pilot Candidate

The first candidate for future approval is:

`service-worker-local-runtime-adapter-pool`

Reason:

- It has a high-priority review route.
- It is local-only.
- It supports infrastructure validation before external work.
- It can produce evidence without browser, wallet, payment, account, public, model/API, or MCP side effects.

Required next artifacts before any registration:

1. `worker_pool_operator_decision_contract_v1`
2. `agent_identity_envelope_contract_v1`
3. `agent_egress_event_ledger_contract_v1`
4. `local_runtime_adapter_pool_activation_preflight_v1`

This runway does not approve those artifacts. It only defines the path.

## Hard Blockers

No worker pool may be registered until:

- an operator decision contract exists
- an identity envelope contract exists
- a validator or equivalent review artifact confirms the decision and identity envelope match
- command previews remain non-authoritative
- chain-integrity coverage includes the new gate

No worker may be started until:

- service request is approved
- pool is registered under a valid identity envelope
- assignment preflight passes
- egress event is declared if any external action is possible
- output artifact path is declared
- recording/redaction/teardown policy exists
- post-execution evidence requirements are defined

No external action may occur until:

- egress ledger contract exists
- operator decision explicitly allows the action
- identity envelope allows the target/action
- MCP/tool registry allows any tool involved
- credential/budget/rate/public-action scopes are explicit
- user/CRO approval exists for legal/KYC/tax/payment/wallet/public/security-report submission risks

## Runtime Boundary

This runway:

- registers no worker pools
- assigns no service requests
- starts no workers
- executes no command previews
- opens no browser sessions
- calls no model APIs
- calls no MCP tools
- installs no gateway or MCP server
- creates no credentials
- touches no wallet, payment, account, public, GitHub, X, marketplace, or legal/KYC state
- changes no external state

## Decision

Recommended next report-only build: `local_runtime_adapter_pool_activation_preflight_v1`, after implementation-design approval, because it is the lowest-risk pool to turn into a validator-backed activation path.

