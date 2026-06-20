# Service Worker Decision Authority Matrix

Generated UTC: 2026-06-15T11:46:59Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-decision-authority-matrix-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-decision-authority-matrix-validation-latest.json`

## Operating Rule

This report maps each pending human/CRO decision packet to required decision authority. It does not grant approval authority, approve or reject requests, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.

- Authority reviews: `11`
- CRO-required rows: `11`
- Human-user-required rows: `4`
- CEO-required rows: `1`
- Reputation-review-required rows: `1`
- Missing internal roles: `0`
- Validation failures: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Authority Rows

| Request | Risk Gate | Required Authorities | Route |
| --- | --- | --- | --- |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `catalog_required_approval_no_external_action` | chief_risk_officer | cro_can_approve_after_exact_scope_review |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `catalog_required_approval_no_external_action` | chief_risk_officer | cro_can_approve_after_exact_scope_review |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `catalog_required_approval_no_external_action` | chief_risk_officer | cro_can_approve_after_exact_scope_review |
| `req-test-browser-readonly-complete-20260614` | `catalog_required_approval_no_external_action` | chief_risk_officer | cro_can_approve_after_exact_scope_review |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `catalog_required_approval_no_external_action` | chief_risk_officer | cro_can_approve_after_exact_scope_review |
| `req-wave4-digital-products-browser-readonly-20260614` | `catalog_required_approval_no_external_action` | chief_risk_officer | cro_can_approve_after_exact_scope_review |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `catalog_required_approval_no_external_action` | chief_risk_officer | cro_can_approve_after_exact_scope_review |
| `req-grok-research-worker-20260614` | `browser_grok_or_x_requires_signed_in_browser_and_no_public_actions` | human_user, chief_risk_officer | human_user_and_cro_required_signed_in_browser |
| `req-next-wave-digital-legal-payment-review-20260614` | `legal_kyc_tax_payment_requires_user_decision_no_commitment` | human_user, chief_risk_officer | human_user_and_cro_required_legal_payment |
| `req-next-wave-security-report-route-review-20260614` | `security_report_submission_requires_user_and_cro_approval_no_submission` | human_user, chief_risk_officer, reputation_review_worker | human_user_cro_and_reputation_review_required |
| `req-pydantic-ai-model-backed-adapter-20260614` | `model_api_call_requires_provider_model_cost_lane_and_artifact_scope` | human_user, chief_risk_officer, ceo_orchestrator | human_user_cro_and_ceo_required_model_api_cost |

## Next Action

Before any human decision command is run, confirm the required authority route for that packet and re-run command safety plus drift guard. This matrix itself grants no authority.

