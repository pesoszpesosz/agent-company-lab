# Service Worker Decision Drift Guard

Generated UTC: 2026-06-15T11:28:28Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-decision-drift-guard-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-decision-drift-guard-validation-latest.json`

## Operating Rule

This report compares human/CRO decision packets with live SQLite service-request state. It flags stale packets after status, approval, assignment, start, completion, or update drift. It does not repair drift, approve or reject requests, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.

- Drift checks: `11`
- Stale packets: `0`
- Approval/rejection records found: `0`
- Assigned rows: `0`
- Updated after packet: `0`
- Recovery command previews: `55`
- Validation failures: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Drift Rows

| Request | Packet Status | Current Status | Stale | Reasons |
| --- | --- | --- | --- | --- |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-test-browser-readonly-complete-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-wave4-digital-products-browser-readonly-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-grok-research-worker-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-next-wave-digital-legal-payment-review-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-next-wave-security-report-route-review-20260614` | `needs_review` | `needs_review` | `False` | none |
| `req-pydantic-ai-model-backed-adapter-20260614` | `needs_review` | `needs_review` | `False` | none |

## Next Action

If any packet becomes stale, do not use its approve/reject preview. Refresh the gate map, human decision packets, post-decision simulation, post-decision refresh plan, and chain integrity before any manual decision or worker step.

