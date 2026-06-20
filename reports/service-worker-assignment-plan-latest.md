# Service Worker Assignment Plan

Generated UTC: 2026-06-15T10:21:36Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-assignment-plan-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-assignment-plan-validation-latest.json`

## Operating Rule

This report plans service-worker assignment after approval. It grants no approval and does not assign, start, complete, enqueue, update, browse, call APIs, post, submit, register, trade, spend, or contact anyone.

- Requests planned: `14`
- Assignable now: `0`
- Assign command previews: `11`
- Route counts: `{"blocked_until_human_cro_approval": 11, "terminal_complete_no_assignment": 1, "terminal_rejected_no_assignment": 2}`
- Worker role counts: `{"browser_action_worker": 8, "chief_risk_officer": 1, "evidence_builder": 1, "observability_worker": 3, "reputation_review_worker": 1}`
- Service requests assigned by plan: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Assignment Queue

| Status | Route | Request | Lane Manager | Worker Type | Worker Role | Worker Pool | Missing Checks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `needs_review` | `blocked_until_human_cro_approval` | `req-grok-research-worker-20260614` | `recovered-profitable-edge-infra` | `browser_signed_in_read_only` | `browser_action_worker` | `service-worker-signed-in-browser-read-only-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-next-wave-digital-legal-payment-review-20260614` | `lane-manager-digital_products_templates_plugins-019ec69a` | `legal_kyc_tax_payment_review` | `chief_risk_officer` | `service-worker-legal-kyc-payment-review-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `lane-manager-digital_products_templates_plugins-019ec69a` | `browser_read_only` | `browser_action_worker` | `service-worker-browser-read-only-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `lane-manager-paid_code_bounties-019ec612` | `browser_read_only` | `browser_action_worker` | `service-worker-browser-read-only-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `lane-manager-security_bounty_private_reports-019ec612` | `browser_read_only` | `browser_action_worker` | `service-worker-browser-read-only-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-next-wave-security-report-route-review-20260614` | `lane-manager-security_bounty_private_reports-019ec612` | `public_submission` | `reputation_review_worker` | `service-worker-public-submission-review-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-pydantic-ai-model-backed-adapter-20260614` | `recovered-profitable-edge-infra` | `model_api_execution` | `observability_worker` | `service-worker-model-api-execution-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-test-browser-readonly-complete-20260614` | `lane-manager-content_and_social_growth-019ec613` | `browser_read_only` | `browser_action_worker` | `service-worker-browser-read-only-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `complete` | `terminal_complete_no_assignment` | `req-test-lifecycle-approve-20260614` | `recovered-profitable-edge-infra` | `local_runtime_adapter` | `observability_worker` | `service-worker-local-runtime-adapter-pool` | service_status_approved_or_assigned, not_terminal, human_cro_review_candidate, exact_scope_compatible, execution_readiness_ready |
| `rejected` | `terminal_rejected_no_assignment` | `req-test-lifecycle-reject-20260614` | `recovered-profitable-edge-infra` | `local_runtime_adapter` | `observability_worker` | `service-worker-local-runtime-adapter-pool` | service_status_approved_or_assigned, not_terminal, human_cro_review_candidate, exact_scope_compatible, execution_readiness_ready |
| `rejected` | `terminal_rejected_no_assignment` | `req-test-service-intake-valid-20260614` | `recovered-profitable-edge-infra` | `other_gated_worker` | `evidence_builder` | `service-worker-other-gated-work-pool` | service_status_approved_or_assigned, not_terminal, human_cro_review_candidate, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `lane-manager-ai_ml_competitions-019ec69a` | `browser_read_only` | `browser_action_worker` | `service-worker-browser-read-only-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-wave4-digital-products-browser-readonly-20260614` | `lane-manager-digital_products_templates_plugins-019ec69a` | `browser_read_only` | `browser_action_worker` | `service-worker-browser-read-only-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |
| `needs_review` | `blocked_until_human_cro_approval` | `req-wave4-money-source-discovery-browser-readonly-20260614` | `lane-manager-money_source_discovery-019ec699` | `browser_read_only` | `browser_action_worker` | `service-worker-browser-read-only-pool` | service_status_approved_or_assigned, exact_scope_compatible, execution_readiness_ready |

## Assign Preview Notes

### req-grok-research-worker-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: approved signed-in read-only inspection; no account setting changes; no public X/Grok action; local research note capture

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-grok-research-worker-20260614",
  "--agent-id",
  "service-worker-signed-in-browser-read-only-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-next-wave-digital-legal-payment-review-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: legal/KYC/tax/payment requirement review; commitment and account-contract gate detection; user/CRO question packet writing

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-next-wave-digital-legal-payment-review-20260614",
  "--agent-id",
  "service-worker-legal-kyc-payment-review-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-next-wave-digital-marketplace-browser-readonly-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: public browser read-only navigation; source URL and title capture; short compliant excerpt capture; local artifact writing

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-next-wave-digital-marketplace-browser-readonly-20260614",
  "--agent-id",
  "service-worker-browser-read-only-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-next-wave-paid-code-algora-archestra-browser-readonly-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: public browser read-only navigation; source URL and title capture; short compliant excerpt capture; local artifact writing

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-next-wave-paid-code-algora-archestra-browser-readonly-20260614",
  "--agent-id",
  "service-worker-browser-read-only-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-next-wave-security-google-oss-vrp-browser-readonly-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: public browser read-only navigation; source URL and title capture; short compliant excerpt capture; local artifact writing

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-next-wave-security-google-oss-vrp-browser-readonly-20260614",
  "--agent-id",
  "service-worker-browser-read-only-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-next-wave-security-report-route-review-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: public-facing draft review; submission route risk review; spam/slop and account-health check

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-next-wave-security-report-route-review-20260614",
  "--agent-id",
  "service-worker-public-submission-review-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-pydantic-ai-model-backed-adapter-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: provider/model/cost scope check; input/output artifact boundary check; cost and trace logging before any API call

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-pydantic-ai-model-backed-adapter-20260614",
  "--agent-id",
  "service-worker-model-api-execution-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-test-browser-readonly-complete-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: public browser read-only navigation; source URL and title capture; short compliant excerpt capture; local artifact writing

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-test-browser-readonly-complete-20260614",
  "--agent-id",
  "service-worker-browser-read-only-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-test-lifecycle-approve-20260614

- Assignment route: `terminal_complete_no_assignment`
- Can assign now: `False`
- Required capabilities: local deterministic runtime execution; artifact and trace emission; no network or account side effects

Assign preview argv: `[]`

### req-test-lifecycle-reject-20260614

- Assignment route: `terminal_rejected_no_assignment`
- Can assign now: `False`
- Required capabilities: local deterministic runtime execution; artifact and trace emission; no network or account side effects

Assign preview argv: `[]`

### req-test-service-intake-valid-20260614

- Assignment route: `terminal_rejected_no_assignment`
- Can assign now: `False`
- Required capabilities: local evidence building; gate-specific checklist execution; artifact writing

Assign preview argv: `[]`

### req-wave4-ai-ml-competitions-browser-readonly-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: public browser read-only navigation; source URL and title capture; short compliant excerpt capture; local artifact writing

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-wave4-ai-ml-competitions-browser-readonly-20260614",
  "--agent-id",
  "service-worker-browser-read-only-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-wave4-digital-products-browser-readonly-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: public browser read-only navigation; source URL and title capture; short compliant excerpt capture; local artifact writing

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-wave4-digital-products-browser-readonly-20260614",
  "--agent-id",
  "service-worker-browser-read-only-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

### req-wave4-money-source-discovery-browser-readonly-20260614

- Assignment route: `blocked_until_human_cro_approval`
- Can assign now: `False`
- Required capabilities: public browser read-only navigation; source URL and title capture; short compliant excerpt capture; local artifact writing

Assign preview argv:

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "assign-service-request",
  "--request-id",
  "req-wave4-money-source-discovery-browser-readonly-20260614",
  "--agent-id",
  "service-worker-browser-read-only-pool",
  "--decision-note",
  "Manual assignment after approval, exact scope compatibility, worker registration, and readiness verification."
]
```

## Next Action

Register concrete service-worker agents or pools before using any assign preview. A real assignment still requires separate approval, compatible exact scope, and a passing execution-readiness report.

