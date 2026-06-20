# Service Worker Operator Decision Docket v1

Generated UTC: 2026-06-20T21:07:38Z
Docket JSON: `E:\agent-company-lab\reports\service-worker-operator-decision-docket-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\service-worker-operator-decision-docket-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Docket status: `ready_for_manual_operator_review`
- Docket rows: `11`
- Ready for manual review: `11`
- Approval granted by docket: `False`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `False`

## Ranked Docket

| Rank | Score | Lane | Request | Decision Mode | Authorities | Review Question |
| ---: | ---: | --- | --- | --- | --- | --- |
| 1 | 126 | `security_bounty_private_reports` | `req-next-wave-security-report-route-review-20260614` | `approve_review_packet_only` | human_user, chief_risk_officer, reputation_review_worker | Is the report route in-scope, safe-harbor covered, non-duplicative, and approved for private submission review only? |
| 2 | 108 | `digital_products_templates_plugins` | `req-next-wave-digital-legal-payment-review-20260614` | `approve_review_packet_only` | human_user, chief_risk_officer | Are the marketplace, payout, tax, KYC, refund, and account-contract obligations acceptable before any seller action? |
| 3 | 87 | `security_bounty_private_reports` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `approve_assignment_preflight_only` | chief_risk_officer | Which public program rules and scope facts are needed before any report/submission decision? |
| 4 | 84 | `paid_code_bounties` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `approve_assignment_preflight_only` | chief_risk_officer | Is the issue still open, unclaimed, non-duplicative, and worth a later gated public-action request? |
| 5 | 84 | `platform_engineering` | `req-pydantic-ai-model-backed-adapter-20260614` | `approve_review_packet_only` | human_user, chief_risk_officer, ceo_orchestrator | Are provider, model, max cost, credential route, allowed lane, and output artifact path explicit enough for a dry run? |
| 6 | 78 | `digital_products_templates_plugins` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `approve_assignment_preflight_only` | chief_risk_officer | Which public marketplace facts are needed before seller account, listing, payment, or legal commitments? |
| 7 | 78 | `digital_products_templates_plugins` | `req-wave4-digital-products-browser-readonly-20260614` | `approve_assignment_preflight_only` | chief_risk_officer | Which public marketplace facts are needed before seller account, listing, payment, or legal commitments? |
| 8 | 73 | `money_source_discovery` | `req-wave4-money-source-discovery-browser-readonly-20260614` | `approve_assignment_preflight_only` | chief_risk_officer | Is the exact read-only scope narrow, current, and worth approving for evidence capture? |
| 9 | 70 | `platform_engineering` | `req-grok-research-worker-20260614` | `approve_review_packet_only` | human_user, chief_risk_officer | Is signed-in read-only X/Grok research allowed without posting, following, liking, replying, or changing settings? |
| 10 | 69 | `ai_ml_competitions` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `approve_assignment_preflight_only` | chief_risk_officer | Is the exact read-only scope narrow, current, and worth approving for evidence capture? |
| 11 | 63 | `content_and_social_growth` | `req-test-browser-readonly-complete-20260614` | `approve_assignment_preflight_only` | chief_risk_officer | Is the exact read-only scope narrow, current, and worth approving for evidence capture? |

## Boundary

- This docket is a ranked manual review surface only.
- It does not approve, reject, assign, update, start, browse, call APIs, post, pay, trade, connect wallets, or submit security reports.
- Command previews in source packets remain placeholders requiring separate human/CRO action.
