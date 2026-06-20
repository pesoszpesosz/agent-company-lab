# Service Worker Human Decision Packets

Generated UTC: 2026-06-17T20:41:28Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
Packet directory: `E:\agent-company-lab\reports\service-worker-human-decision-packets`
JSON mirror: `E:\agent-company-lab\reports\service-worker-human-decision-packets-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-human-decision-packets-validation-latest.json`

## Operating Rule

This report writes local human/CRO decision packets only. It does not approve, reject, register, assign, update, start, browse, call APIs, post, submit, pay, trade, or contact anyone.

- Decision packets: `11`
- Terminal do-not-approve rows: `3`
- Approve previews: `11`
- Reject previews: `11`
- Validation failures: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Packets

| Request | Lane | Worker Type | Gate | Pool | Packet |
| --- | --- | --- | --- | --- | --- |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `digital_products_templates_plugins` | `browser_read_only` | `human_cro_approval_required` | `service-worker-browser-read-only-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-digital-marketplace-browser-readonly-20260614.md` |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `paid_code_bounties` | `browser_read_only` | `human_cro_approval_required` | `service-worker-browser-read-only-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-paid-code-algora-archestra-browser-readonly-20260614.md` |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `security_bounty_private_reports` | `browser_read_only` | `human_cro_approval_required` | `service-worker-browser-read-only-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-security-google-oss-vrp-browser-readonly-20260614.md` |
| `req-test-browser-readonly-complete-20260614` | `content_and_social_growth` | `browser_read_only` | `human_cro_approval_required` | `service-worker-browser-read-only-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-test-browser-readonly-complete-20260614.md` |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `ai_ml_competitions` | `browser_read_only` | `human_cro_approval_required` | `service-worker-browser-read-only-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-wave4-ai-ml-competitions-browser-readonly-20260614.md` |
| `req-wave4-digital-products-browser-readonly-20260614` | `digital_products_templates_plugins` | `browser_read_only` | `human_cro_approval_required` | `service-worker-browser-read-only-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-wave4-digital-products-browser-readonly-20260614.md` |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `money_source_discovery` | `browser_read_only` | `human_cro_approval_required` | `service-worker-browser-read-only-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-wave4-money-source-discovery-browser-readonly-20260614.md` |
| `req-grok-research-worker-20260614` | `platform_engineering` | `browser_signed_in_read_only` | `human_cro_approval_required` | `service-worker-signed-in-browser-read-only-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-grok-research-worker-20260614.md` |
| `req-next-wave-digital-legal-payment-review-20260614` | `digital_products_templates_plugins` | `legal_kyc_tax_payment_review` | `human_cro_approval_required` | `service-worker-legal-kyc-payment-review-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-digital-legal-payment-review-20260614.md` |
| `req-next-wave-security-report-route-review-20260614` | `security_bounty_private_reports` | `public_submission` | `human_cro_approval_required` | `service-worker-public-submission-review-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-security-report-route-review-20260614.md` |
| `req-pydantic-ai-model-backed-adapter-20260614` | `platform_engineering` | `model_api_execution` | `human_cro_approval_required` | `service-worker-model-api-execution-pool` | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-pydantic-ai-model-backed-adapter-20260614.md` |

## Next Action

A human/CRO can open a packet, revise the suggested exact scope if needed, and manually run either the approve or reject preview. Pool registration, assignment, readiness, and worker start remain separate later gates.

