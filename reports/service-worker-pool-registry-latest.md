# Service Worker Pool Registry

Generated UTC: 2026-06-15T14:17:59Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-pool-registry-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-pool-registry-validation-latest.json`

## Operating Rule

This report defines service-worker pools needed by the assignment plan. It grants no approval and does not register, assign, start, complete, enqueue, update, browse, call APIs, post, submit, register accounts, trade, spend, or contact anyone.

- Pools defined: `7`
- Missing dedicated pool registrations: `7`
- Current assignment-plan request demand: `14`
- Pool status counts: `{"missing_service_worker_pool": 7}`
- Role counts: `{"browser_action_worker": 2, "chief_risk_officer": 1, "evidence_builder": 1, "observability_worker": 2, "reputation_review_worker": 1}`
- Service requests assigned by registry: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Pools

| Pool | Worker Type | Role | Demand | Status | Active Role Agents | Next Action |
| --- | --- | --- | ---: | --- | --- | --- |
| `service-worker-browser-read-only-pool` | `browser_read_only` | `browser_action_worker` | 7 | `missing_service_worker_pool` | none | Register a concrete service-worker pool/agent before using assignment previews. |
| `service-worker-signed-in-browser-read-only-pool` | `browser_signed_in_read_only` | `browser_action_worker` | 1 | `missing_service_worker_pool` | none | Register a concrete service-worker pool/agent before using assignment previews. |
| `service-worker-legal-kyc-payment-review-pool` | `legal_kyc_tax_payment_review` | `chief_risk_officer` | 1 | `missing_service_worker_pool` | none | Register a concrete service-worker pool/agent before using assignment previews. |
| `service-worker-local-runtime-adapter-pool` | `local_runtime_adapter` | `observability_worker` | 2 | `missing_service_worker_pool` | none | Register a concrete service-worker pool/agent before using assignment previews. |
| `service-worker-model-api-execution-pool` | `model_api_execution` | `observability_worker` | 1 | `missing_service_worker_pool` | none | Register a concrete service-worker pool/agent before using assignment previews. |
| `service-worker-other-gated-work-pool` | `other_gated_worker` | `evidence_builder` | 1 | `missing_service_worker_pool` | none | Register a concrete service-worker pool/agent before using assignment previews. |
| `service-worker-public-submission-review-pool` | `public_submission` | `reputation_review_worker` | 1 | `missing_service_worker_pool` | none | Register a concrete service-worker pool/agent before using assignment previews. |

## Capabilities

### service-worker-browser-read-only-pool

- Worker type: `browser_read_only`
- Role: `browser_action_worker`
- Current lanes: `ai_ml_competitions, content_and_social_growth, digital_products_templates_plugins, money_source_discovery, paid_code_bounties, security_bounty_private_reports`
- Capabilities:
  - public browser read-only navigation
  - source URL and title capture
  - short compliant excerpt capture
  - local artifact writing

### service-worker-signed-in-browser-read-only-pool

- Worker type: `browser_signed_in_read_only`
- Role: `browser_action_worker`
- Current lanes: `platform_engineering`
- Capabilities:
  - approved signed-in read-only inspection
  - no account setting changes
  - no public X/Grok action
  - local research note capture

### service-worker-legal-kyc-payment-review-pool

- Worker type: `legal_kyc_tax_payment_review`
- Role: `chief_risk_officer`
- Current lanes: `digital_products_templates_plugins`
- Capabilities:
  - legal/KYC/tax/payment requirement review
  - commitment and account-contract gate detection
  - user/CRO question packet writing

### service-worker-local-runtime-adapter-pool

- Worker type: `local_runtime_adapter`
- Role: `observability_worker`
- Current lanes: `platform_engineering`
- Capabilities:
  - local deterministic runtime execution
  - artifact and trace emission
  - no network or account side effects

### service-worker-model-api-execution-pool

- Worker type: `model_api_execution`
- Role: `observability_worker`
- Current lanes: `platform_engineering`
- Capabilities:
  - provider/model/cost scope check
  - input/output artifact boundary check
  - cost and trace logging before any API call

### service-worker-other-gated-work-pool

- Worker type: `other_gated_worker`
- Role: `evidence_builder`
- Current lanes: `platform_engineering`
- Capabilities:
  - local evidence building
  - gate-specific checklist execution
  - artifact writing

### service-worker-public-submission-review-pool

- Worker type: `public_submission`
- Role: `reputation_review_worker`
- Current lanes: `security_bounty_private_reports`
- Capabilities:
  - public-facing draft review
  - submission route risk review
  - spam/slop and account-health check

## Next Action

Register concrete service-worker pool agents only after deciding ownership and operating boundaries. After registration, rerun the assignment plan; real assignments still require approval, compatible exact scope, and execution readiness.

