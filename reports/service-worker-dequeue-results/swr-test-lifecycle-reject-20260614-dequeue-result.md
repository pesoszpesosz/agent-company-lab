# Service Worker Dequeue Result - swr-test-lifecycle-reject-20260614

Generated UTC: 2026-06-19T14:16:55Z

- Source service request: `req-test-lifecycle-reject-20260614`
- Lane: `platform_engineering`
- Worker type: `local_runtime_adapter`
- Status snapshot: `rejected`
- Risk gate: test_no_external_action
- Route: `terminal_rejected_no_worker_start`
- Dequeue allowed: `False`
- Worker started: `False`
- Service request updated: `False`
- Approval granted: `False`
- API calls: `False`
- External side effects: `False`

## Reason

Source service request is rejected; do not reopen without a new service request.

## Next Action

Approve exact scope separately before any real worker execution; otherwise keep packet parked.
