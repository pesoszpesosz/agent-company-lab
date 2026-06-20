# Service Worker Decision Preflight

Generated UTC: 2026-06-17T20:41:28Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-decision-preflight-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-decision-preflight-validation-latest.json`

## Operating Rule

This report rolls up decision drift, command safety, and authority classification before a human uses a decision packet. It can mark a packet ready for human review, but it does not grant authority, approve or reject requests, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.

- Preflight rows: `11`
- Ready for human review: `11`
- Blocked rows: `0`
- Execution allowed: `0`
- Assignment allowed: `0`
- Worker starts allowed: `0`
- Validation failures: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Preflight Rows

| Request | Ready | Authorities | Route | Blockers |
| --- | --- | --- | --- | --- |
| `req-grok-research-worker-20260614` | `True` | human_user, chief_risk_officer | human_user_and_cro_required_signed_in_browser | none |
| `req-next-wave-digital-legal-payment-review-20260614` | `True` | human_user, chief_risk_officer | human_user_and_cro_required_legal_payment | none |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `True` | chief_risk_officer | cro_can_approve_after_exact_scope_review | none |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `True` | chief_risk_officer | cro_can_approve_after_exact_scope_review | none |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `True` | chief_risk_officer | cro_can_approve_after_exact_scope_review | none |
| `req-next-wave-security-report-route-review-20260614` | `True` | human_user, chief_risk_officer, reputation_review_worker | human_user_cro_and_reputation_review_required | none |
| `req-pydantic-ai-model-backed-adapter-20260614` | `True` | human_user, chief_risk_officer, ceo_orchestrator | human_user_cro_and_ceo_required_model_api_cost | none |
| `req-test-browser-readonly-complete-20260614` | `True` | chief_risk_officer | cro_can_approve_after_exact_scope_review | none |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `True` | chief_risk_officer | cro_can_approve_after_exact_scope_review | none |
| `req-wave4-digital-products-browser-readonly-20260614` | `True` | chief_risk_officer | cro_can_approve_after_exact_scope_review | none |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `True` | chief_risk_officer | cro_can_approve_after_exact_scope_review | none |

## Next Action

A human/CRO can use this report as the final local checklist before reviewing a decision packet. Replace exact-scope placeholders and rerun drift/command/authority checks before any state-changing command.

