# Service Worker Pool Registration Plan

Generated UTC: 2026-06-15T10:21:36Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-pool-registration-plan-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-pool-registration-plan-validation-latest.json`

## Operating Rule

This report writes manual registration packets for service-worker pools. It grants no approval and does not register, assign, start, complete, enqueue, update, browse, call APIs, post, submit, register accounts, trade, spend, or contact anyone.

- Registration packets: `7`
- Register command previews: `7`
- Current assignment-plan request demand: `14`
- Route counts: `{"registration_packet_ready_manual_review": 7}`
- Pools registered by plan: `0`
- Service requests assigned by plan: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Registration Packets

| Pool | Role | Department | Demand | Route | Next Action |
| --- | --- | --- | ---: | --- | --- |
| `service-worker-browser-read-only-pool` | `browser_action_worker` | `service_worker_browser_operations` | 7 | `registration_packet_ready_manual_review` | Review ownership and boundaries, then run register-agent manually only if the pool should exist. |
| `service-worker-signed-in-browser-read-only-pool` | `browser_action_worker` | `service_worker_browser_operations` | 1 | `registration_packet_ready_manual_review` | Review ownership and boundaries, then run register-agent manually only if the pool should exist. |
| `service-worker-legal-kyc-payment-review-pool` | `chief_risk_officer` | `service_worker_risk_review` | 1 | `registration_packet_ready_manual_review` | Review ownership and boundaries, then run register-agent manually only if the pool should exist. |
| `service-worker-local-runtime-adapter-pool` | `observability_worker` | `service_worker_observability` | 2 | `registration_packet_ready_manual_review` | Review ownership and boundaries, then run register-agent manually only if the pool should exist. |
| `service-worker-model-api-execution-pool` | `observability_worker` | `service_worker_observability` | 1 | `registration_packet_ready_manual_review` | Review ownership and boundaries, then run register-agent manually only if the pool should exist. |
| `service-worker-other-gated-work-pool` | `evidence_builder` | `service_worker_evidence_building` | 1 | `registration_packet_ready_manual_review` | Review ownership and boundaries, then run register-agent manually only if the pool should exist. |
| `service-worker-public-submission-review-pool` | `reputation_review_worker` | `service_worker_reputation_review` | 1 | `registration_packet_ready_manual_review` | Review ownership and boundaries, then run register-agent manually only if the pool should exist. |

## Command Previews

### service-worker-browser-read-only-pool

- Worker type: `browser_read_only`
- Current lanes: `ai_ml_competitions, content_and_social_growth, digital_products_templates_plugins, money_source_discovery, paid_code_bounties, security_bounty_private_reports`
- Boundaries:
  - requires separate human/CRO approval before any service request assignment
  - requires compatible exact approval scope before assignment
  - requires execution-readiness verifier before any start
  - must write local artifacts and trace evidence for any allowed work
  - must stop at credentials, private data, account, public-action, payment, wallet, legal, model/API cost, or unclear scope gates
  - no login or signed-in surface unless the exact approved scope names it
  - no clicks that post, submit, message, upload, buy, sell, accept terms, or change settings

Register-agent preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "register-agent",
  "--agent-id",
  "service-worker-browser-read-only-pool",
  "--role-id",
  "browser_action_worker",
  "--department-id",
  "service_worker_browser_operations"
]
```

### service-worker-signed-in-browser-read-only-pool

- Worker type: `browser_signed_in_read_only`
- Current lanes: `platform_engineering`
- Boundaries:
  - requires separate human/CRO approval before any service request assignment
  - requires compatible exact approval scope before assignment
  - requires execution-readiness verifier before any start
  - must write local artifacts and trace evidence for any allowed work
  - must stop at credentials, private data, account, public-action, payment, wallet, legal, model/API cost, or unclear scope gates
  - no login or signed-in surface unless the exact approved scope names it
  - no clicks that post, submit, message, upload, buy, sell, accept terms, or change settings

Register-agent preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "register-agent",
  "--agent-id",
  "service-worker-signed-in-browser-read-only-pool",
  "--role-id",
  "browser_action_worker",
  "--department-id",
  "service_worker_browser_operations"
]
```

### service-worker-legal-kyc-payment-review-pool

- Worker type: `legal_kyc_tax_payment_review`
- Current lanes: `digital_products_templates_plugins`
- Boundaries:
  - requires separate human/CRO approval before any service request assignment
  - requires compatible exact approval scope before assignment
  - requires execution-readiness verifier before any start
  - must write local artifacts and trace evidence for any allowed work
  - must stop at credentials, private data, account, public-action, payment, wallet, legal, model/API cost, or unclear scope gates
  - no legal, KYC, tax, payment, seller, or account commitment; prepare review packets only

Register-agent preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "register-agent",
  "--agent-id",
  "service-worker-legal-kyc-payment-review-pool",
  "--role-id",
  "chief_risk_officer",
  "--department-id",
  "service_worker_risk_review"
]
```

### service-worker-local-runtime-adapter-pool

- Worker type: `local_runtime_adapter`
- Current lanes: `platform_engineering`
- Boundaries:
  - requires separate human/CRO approval before any service request assignment
  - requires compatible exact approval scope before assignment
  - requires execution-readiness verifier before any start
  - must write local artifacts and trace evidence for any allowed work
  - must stop at credentials, private data, account, public-action, payment, wallet, legal, model/API cost, or unclear scope gates

Register-agent preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "register-agent",
  "--agent-id",
  "service-worker-local-runtime-adapter-pool",
  "--role-id",
  "observability_worker",
  "--department-id",
  "service_worker_observability"
]
```

### service-worker-model-api-execution-pool

- Worker type: `model_api_execution`
- Current lanes: `platform_engineering`
- Boundaries:
  - requires separate human/CRO approval before any service request assignment
  - requires compatible exact approval scope before assignment
  - requires execution-readiness verifier before any start
  - must write local artifacts and trace evidence for any allowed work
  - must stop at credentials, private data, account, public-action, payment, wallet, legal, model/API cost, or unclear scope gates
  - no provider/model/API call until provider, model, max cost, data scope, and output artifact path are explicitly approved

Register-agent preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "register-agent",
  "--agent-id",
  "service-worker-model-api-execution-pool",
  "--role-id",
  "observability_worker",
  "--department-id",
  "service_worker_observability"
]
```

### service-worker-other-gated-work-pool

- Worker type: `other_gated_worker`
- Current lanes: `platform_engineering`
- Boundaries:
  - requires separate human/CRO approval before any service request assignment
  - requires compatible exact approval scope before assignment
  - requires execution-readiness verifier before any start
  - must write local artifacts and trace evidence for any allowed work
  - must stop at credentials, private data, account, public-action, payment, wallet, legal, model/API cost, or unclear scope gates

Register-agent preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "register-agent",
  "--agent-id",
  "service-worker-other-gated-work-pool",
  "--role-id",
  "evidence_builder",
  "--department-id",
  "service_worker_evidence_building"
]
```

### service-worker-public-submission-review-pool

- Worker type: `public_submission`
- Current lanes: `security_bounty_private_reports`
- Boundaries:
  - requires separate human/CRO approval before any service request assignment
  - requires compatible exact approval scope before assignment
  - requires execution-readiness verifier before any start
  - must write local artifacts and trace evidence for any allowed work
  - must stop at credentials, private data, account, public-action, payment, wallet, legal, model/API cost, or unclear scope gates
  - no public submission or contact; review route and draft quality only

Register-agent preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "register-agent",
  "--agent-id",
  "service-worker-public-submission-review-pool",
  "--role-id",
  "reputation_review_worker",
  "--department-id",
  "service_worker_reputation_review"
]
```

## Next Action

Review ownership and boundaries before registering any pool. After manual registration, rerun the pool registry and assignment plan; real assignments still require approval, compatible exact scope, and execution readiness.

