# Service Worker Decision Command Safety

Generated UTC: 2026-06-15T11:33:32Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-decision-command-safety-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-decision-command-safety-validation-latest.json`

## Operating Rule

This report reviews approve/reject command previews for human decision packets. It marks approve previews as not directly runnable while they contain the exact-scope placeholder, and marks all decision commands as requiring manual review. It does not run approve/reject commands, grant approvals or rejections, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.

- Command reviews: `11`
- Decision command previews: `22`
- Approve placeholders requiring replacement: `11`
- Directly runnable approve commands: `0`
- Directly runnable reject commands: `0`
- Validation failures: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Command Safety Rows

| Request | Approve Needs Scope | Reject Needs Review | Directly Runnable | Findings |
| --- | --- | --- | --- | --- |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-test-browser-readonly-complete-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-wave4-digital-products-browser-readonly-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-grok-research-worker-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-next-wave-digital-legal-payment-review-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-next-wave-security-report-route-review-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |
| `req-pydantic-ai-model-backed-adapter-20260614` | `True` | `True` | `False` | approve_exact_scope_placeholder_present, reject_reason_requires_manual_review |

## Next Action

Before any human/CRO runs an approve command, replace the exact-scope placeholder with a reviewed scope from the packet and rerun drift guard. Reject commands also require manual reason review. This report itself is only a safety review.

