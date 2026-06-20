# Local Runtime Adapter Pool Activation Preflight v1

Generated UTC: 2026-06-17T19:16:01Z

Lane: platform_engineering

Task: task-local-runtime-adapter-pool-activation-preflight-v1-20260617

## Purpose

This preflight defines the evidence required before `service-worker-local-runtime-adapter-pool` can move from review candidate to a future registration candidate.

This is report-only. It does not register the pool, assign requests, start workers, execute commands, or mutate service requests.

## Candidate Pool

- Worker pool id: `service-worker-local-runtime-adapter-pool`
- Role id: `observability_worker`
- Department id: `service_worker_observability`
- Worker type: `local_runtime_adapter`
- Source review route: `manual_review_register_later`
- Current request count: 2
- Runway status: `closest_to_local_pilot`

## Source Artifacts

- Worker activation runway: `E:\agent-company-lab\reports\worker-activation-runway-v1-20260617.json`
- Worker-pool registration review: `E:\agent-company-lab\reports\worker-pool-registration-review-v1-20260617.json`
- Worker-pool operator decision packet: `E:\agent-company-lab\reports\worker-pool-operator-decision-packet-v1-20260617.json`
- Agent identity envelope matrix: `E:\agent-company-lab\reports\agent-identity-envelope-matrix-v1-20260617.json`
- Agent egress event ledger packet: `E:\agent-company-lab\reports\agent-egress-event-ledger-packet-v1-20260617.json`
- Current worker-pool assignment preflight: `E:\agent-company-lab\reports\worker-pool-assignment-preflight-v1-20260617.json`
- Current chain integrity validation: `E:\agent-company-lab\reports\service-worker-chain-integrity-validation-latest.json`

## Required Evidence Before Registration Candidate Status

The pool is not ready for registration. It can become a registration candidate only after these artifacts exist:

1. `operator_decision_contract`
   - Must allow only `approve_identity_envelope_draft` or `approve_register_later_preflight`.
   - Must explicitly state that registration is not authorized.
2. `identity_envelope_contract`
   - Must bind the pool to `observability_worker`, `service_worker_observability`, and local-only runtime adapter work.
   - Must deny browser, model/API, MCP, wallet, payment, account, credential, public, and marketplace actions.
3. `egress_ledger_contract`
   - Must deny live egress and allow only report-only/local preflight events.
4. `assignment_preflight_contract`
   - Must prove no service request can be assigned until the pool exists and request approval matches identity scope.
5. `runtime_start_preflight_contract`
   - Must require output artifact path, trace id, teardown/rollback policy, and post-run evidence seal.
6. `chain_integrity_layer`
   - Must make the new preflight visible to integrity checks before any future registration or start.

## Preflight Verdict

Current verdict: `not_ready_register_candidate`

Reasons:

- Operator decision contract does not yet exist as an executable validator.
- Identity envelope contract does not yet exist as a validator.
- Egress ledger contract exists only as a packet, not a validator.
- Assignment preflight reports 0 assignable requests.
- All required dedicated worker pools remain missing.
- Ready-to-start count remains 0.
- Human/CRO gates still cover most non-terminal service requests.

## Allowed Next Actions

Allowed now:

- write report-only contract packets
- write validator design packets
- write negative fixture suites
- refresh dashboards, audits, traces, and integrity reports

Not allowed now:

- execute the `register-agent` command preview
- register the pool
- assign service requests
- start workers
- start local runtime processes
- call APIs
- open browser sessions
- touch credentials, wallets, payments, accounts, public submissions, GitHub public actions, X, marketplaces, legal/KYC, or tax state

## Negative Fixtures

Future validator must reject:

| Fixture id | Reason |
| --- | --- |
| `register_without_operator_decision` | Registration attempted without signed decision artifact. |
| `register_without_identity_envelope` | Pool lacks scoped non-human identity. |
| `identity_allows_browser` | Local runtime adapter identity permits browser use. |
| `identity_allows_model_api` | Local runtime adapter identity permits model/API calls. |
| `identity_allows_mcp` | Local runtime adapter identity permits MCP tools. |
| `identity_allows_wallet_payment` | Identity permits wallet/payment scope. |
| `assignment_before_pool_exists` | Service request assigned before pool registration. |
| `assignment_without_approved_request` | Request not approved for this pool. |
| `worker_start_without_runtime_preflight` | Worker start lacks runtime start preflight. |
| `missing_output_artifact_path` | Future local run has no declared output path. |
| `missing_trace_id` | Future local run cannot be audited. |
| `external_side_effects_true` | Local runtime adapter preflight expects external side effects. |
| `command_preview_executed` | Command preview treated as authority. |

## Minimal Future Runtime Boundary

If this pool is ever approved later, its first live boundary should be:

- local filesystem reads limited to declared artifact paths
- local filesystem writes limited to declared report/output paths
- no network
- no browser
- no model/API calls
- no MCP tools
- no credentials
- no account/wallet/payment/public actions
- deterministic command preview or dry-run only
- required trace event and output artifact
- post-run evidence seal

## Activation Score

Current score: 4 / 10

Scoring:

- +2 source review exists
- +1 selected as first safe pilot in runway
- +1 local-only candidate
- -2 no operator decision validator
- -1 no identity envelope validator
- -1 no runtime start preflight validator
- -1 no assignable service requests
- -1 no chain integrity layer for this preflight

Interpretation: candidate is correctly chosen, but activation is still gated.

## Runtime Boundary

This preflight:

- registers no worker pools
- assigns no service requests
- starts no workers
- executes no command previews
- starts no local runtime process
- opens no browser sessions
- calls no model APIs
- calls no MCP tools
- installs no dependencies
- creates no credentials
- touches no account, wallet, payment, public, GitHub, X, marketplace, legal/KYC, or tax state
- changes no external state

## Decision

Recommended next report-only build: `local_runtime_adapter_pool_activation_contract_v1` schema and negative fixture suite, after implementation-design approval.

