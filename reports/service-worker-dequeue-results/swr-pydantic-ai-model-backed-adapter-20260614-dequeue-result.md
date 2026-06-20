# Service Worker Dequeue Result - swr-pydantic-ai-model-backed-adapter-20260614

Generated UTC: 2026-06-19T14:16:55Z

- Source service request: `req-pydantic-ai-model-backed-adapter-20260614`
- Lane: `platform_engineering`
- Worker type: `model_api_execution`
- Status snapshot: `needs_review`
- Risk gate: model_api_call_requires_provider_model_cost_lane_and_artifact_scope
- Route: `hold_for_approval_no_worker_start`
- Dequeue allowed: `False`
- Worker started: `False`
- Service request updated: `False`
- Approval granted: `False`
- API calls: `False`
- External side effects: `False`

## Reason

Source service request is needs_review; no approval or worker start is granted by this dry-run.

## Next Action

Approve exact scope separately before any real worker execution; otherwise keep packet parked.
