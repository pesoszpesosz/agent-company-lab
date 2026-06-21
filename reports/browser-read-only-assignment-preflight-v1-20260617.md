# Browser Read-Only Assignment Preflight v1

Generated UTC: 2026-06-21T15:49:33Z
Validation JSON: `E:\agent-company-lab\reports\browser-read-only-assignment-preflight-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\browser-read-only-assignment-preflight-v1-20260617.json`
Policy validation: `E:\agent-company-lab\reports\browser-read-only-worker-policy-v1-validation-20260617.json`
Adapter contract validation: `E:\agent-company-lab\reports\browser-worker-adapter-contract-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Preflight verdict: `candidates_valid_assignment_blocked_no_signed_approval`
- Candidate requests: `9`
- Assignment allowed: `0`
- Blocked without signed approval: `9`
- Browser sessions started: `0`
- Service requests assigned: `0`
- External side effects: `False`

## Candidate Requests

| Request | Lane | Packet Complete | Assignment Allowed | Blocked Reason |
| --- | --- | --- | --- | --- |
| `req-algora-opik-readonly-refresh-20260618` | `paid_code_bounties` | `True` | `False` | `no_signed_operator_approval` |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `digital_products_templates_plugins` | `True` | `False` | `no_signed_operator_approval` |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `paid_code_bounties` | `True` | `False` | `no_signed_operator_approval` |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `security_bounty_private_reports` | `True` | `False` | `no_signed_operator_approval` |
| `req-promptbase-guideline-readonly-review-20260618` | `digital_products_templates_plugins` | `True` | `False` | `no_signed_operator_approval` |
| `req-test-browser-readonly-complete-20260614` | `content_and_social_growth` | `True` | `False` | `no_signed_operator_approval` |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `ai_ml_competitions` | `True` | `False` | `no_signed_operator_approval` |
| `req-wave4-digital-products-browser-readonly-20260614` | `digital_products_templates_plugins` | `True` | `False` | `no_signed_operator_approval` |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `money_source_discovery` | `True` | `False` | `no_signed_operator_approval` |

## Boundary

- This preflight reads the queue and policy validation only.
- It does not assign service requests, start workers, open browsers, mutate queue state, or perform external actions.
