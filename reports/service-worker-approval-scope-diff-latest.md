# Service Worker Approval Scope Diff

Generated UTC: 2026-06-15T10:21:10Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-approval-scope-diff-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-approval-scope-diff-validation-latest.json`

## Operating Rule

This report compares approval-scope text against `service_worker_request.v1` packet boundaries. It grants no approval and does not assign, start, complete, enqueue, browse, call APIs, post, submit, register, trade, spend, or contact anyone.

- Requests evaluated: `14`
- Scope-compatible rows: `0`
- Route counts: `{"missing_exact_scope": 9, "scope_text_without_approval_record": 2, "terminal_complete_scope_audit_only": 1, "terminal_rejected_scope_audit_only": 2}`
- Status counts: `{"complete": 1, "needs_review": 11, "rejected": 2}`
- Worker starts: `0`
- Service requests updated: `0`
- API calls: `False`
- External side effects: `False`

## Scope Diff Rows

| Status | Compatible | Route | Source Request | Scope Failures |
| --- | --- | --- | --- | --- |
| `needs_review` | `False` | `scope_text_without_approval_record` | `req-grok-research-worker-20260614` | latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present, host_scope_ok |
| `needs_review` | `False` | `missing_exact_scope` | `req-next-wave-digital-legal-payment-review-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |
| `needs_review` | `False` | `missing_exact_scope` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present, host_scope_ok |
| `needs_review` | `False` | `missing_exact_scope` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |
| `needs_review` | `False` | `missing_exact_scope` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |
| `needs_review` | `False` | `missing_exact_scope` | `req-next-wave-security-report-route-review-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |
| `needs_review` | `False` | `scope_text_without_approval_record` | `req-pydantic-ai-model-backed-adapter-20260614` | latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |
| `needs_review` | `False` | `missing_exact_scope` | `req-test-browser-readonly-complete-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |
| `complete` | `False` | `terminal_complete_scope_audit_only` | `req-test-lifecycle-approve-20260614` | side_effect_denials_present |
| `rejected` | `False` | `terminal_rejected_scope_audit_only` | `req-test-lifecycle-reject-20260614` | latest_approval_approved, approval_scope_matches_service_scope, side_effect_denials_present |
| `rejected` | `False` | `terminal_rejected_scope_audit_only` | `req-test-service-intake-valid-20260614` | latest_approval_approved, approval_scope_matches_service_scope, side_effect_denials_present |
| `needs_review` | `False` | `missing_exact_scope` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |
| `needs_review` | `False` | `missing_exact_scope` | `req-wave4-digital-products-browser-readonly-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |
| `needs_review` | `False` | `missing_exact_scope` | `req-wave4-money-source-discovery-browser-readonly-20260614` | scope_present, latest_approval_exists, latest_approval_approved, latest_approval_not_expired, approval_scope_matches_service_scope, side_effect_denials_present |

## Next Action

Use this report before approving or starting any service-worker request. A compatible scope is still not a start command; it must be followed by the execution-readiness verifier and explicit human approval.

