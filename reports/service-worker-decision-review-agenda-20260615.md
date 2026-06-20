# Service Worker Decision Review Agenda

Generated UTC: 2026-06-15T12:03:45Z

## Operating Rule

Local review board only. No approval, rejection, assignment, worker start, browser/API action, payment, trade, public submission, account action, or external side effect is granted.

## Summary

- Agenda rows: `11`
- Review-ready rows: `11`
- High-risk/user rows: `4`
- CRO required: `11`
- Human user required: `4`
- CEO required: `1`
- Reputation review required: `1`
- Blocked rows: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Agenda

| Priority | Group | Request | Lane | Authorities | Question | Packet |
| --- | --- | --- | --- | --- | --- | --- |
| `20` | `ceo_user_cro_model_api_cost_gate` | `req-pydantic-ai-model-backed-adapter-20260614` | `platform_engineering` | human_user, chief_risk_officer, ceo_orchestrator | Should user, CEO, and CRO authorize a concrete provider/model/max-cost/artifact scope, or reject this model/API request? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-pydantic-ai-model-backed-adapter-20260614.md` |
| `20` | `user_cro_legal_payment_gate` | `req-next-wave-digital-legal-payment-review-20260614` | `digital_products_templates_plugins` | human_user, chief_risk_officer | Should user personally approve legal/KYC/tax/payment review scope with no commitment, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-digital-legal-payment-review-20260614.md` |
| `20` | `user_cro_reputation_public_submission_gate` | `req-next-wave-security-report-route-review-20260614` | `security_bounty_private_reports` | human_user, chief_risk_officer, reputation_review_worker | Should user and CRO send this to reputation review for a possible submission route, or reject before any public contact? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-security-report-route-review-20260614.md` |
| `20` | `user_cro_signed_in_browser_gate` | `req-grok-research-worker-20260614` | `platform_engineering` | human_user, chief_risk_officer | Should user approve signed-in read-only browser scope with no public actions, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-grok-research-worker-20260614.md` |
| `10` | `cro_exact_scope_readonly_gate` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `digital_products_templates_plugins` | chief_risk_officer | Should CRO approve the exact-scope read-only worker packet, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-digital-marketplace-browser-readonly-20260614.md` |
| `10` | `cro_exact_scope_readonly_gate` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `paid_code_bounties` | chief_risk_officer | Should CRO approve the exact-scope read-only worker packet, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-paid-code-algora-archestra-browser-readonly-20260614.md` |
| `10` | `cro_exact_scope_readonly_gate` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `security_bounty_private_reports` | chief_risk_officer | Should CRO approve the exact-scope read-only worker packet, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-next-wave-security-google-oss-vrp-browser-readonly-20260614.md` |
| `10` | `cro_exact_scope_readonly_gate` | `req-test-browser-readonly-complete-20260614` | `content_and_social_growth` | chief_risk_officer | Should CRO approve the exact-scope read-only worker packet, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-test-browser-readonly-complete-20260614.md` |
| `10` | `cro_exact_scope_readonly_gate` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `ai_ml_competitions` | chief_risk_officer | Should CRO approve the exact-scope read-only worker packet, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-wave4-ai-ml-competitions-browser-readonly-20260614.md` |
| `10` | `cro_exact_scope_readonly_gate` | `req-wave4-digital-products-browser-readonly-20260614` | `digital_products_templates_plugins` | chief_risk_officer | Should CRO approve the exact-scope read-only worker packet, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-wave4-digital-products-browser-readonly-20260614.md` |
| `10` | `cro_exact_scope_readonly_gate` | `req-wave4-money-source-discovery-browser-readonly-20260614` | `money_source_discovery` | chief_risk_officer | Should CRO approve the exact-scope read-only worker packet, or reject/park it? | `E:\agent-company-lab\reports\service-worker-human-decision-packets\req-wave4-money-source-discovery-browser-readonly-20260614.md` |

## Next Action

Open the highest-priority packet first, review exact scope and stop conditions, then keep it parked or ask the human/CRO for an explicit approve/reject decision. Rerun preflight before any state-changing command.
