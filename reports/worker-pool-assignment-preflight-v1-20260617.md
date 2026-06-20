# Worker Pool Assignment Preflight v1

Generated UTC: 2026-06-17T18:45:35Z
Preflight: `worker-pool-preflight-agent-company-scaleout-v1-20260617`
Task: `task-worker-pool-assignment-preflight-v1-20260617`
Schema: `E:\agent-company-lab\architecture\worker-pool-assignment-preflight-v1.schema.json`
JSON: `E:\agent-company-lab\reports\worker-pool-assignment-preflight-v1-20260617.json`
Validation: `E:\agent-company-lab\reports\worker-pool-assignment-preflight-v1-validation-20260617.json`

## Summary

- Assignment rows: `14`
- Assignable now: `0`
- Worker pools required: `7`
- Missing pools: `7`
- Readiness rows: `14`
- Ready to start: `0`
- Human/CRO-gated rows: `11`
- Terminal no-execution rows: `3`
- Validation failures: `0`

## Blocking Findings

| Finding | Severity | Evidence | Required Before Start |
| --- | --- | --- | --- |
| `finding-no-assignable-requests` | `blocker` | assignment_plan.assignable_now_count=0 | `True` |
| `finding-missing-worker-pools` | `blocker` | pool_registry.missing_pool_count=7 of pool_count=7 | `True` |
| `finding-no-ready-starts` | `blocker` | readiness.ready_to_start_count=0 | `True` |
| `finding-human-cro-gate` | `blocker` | gate_map.human_cro_approval_required=11 | `True` |

## Recommended Next Actions

| Action | Type | Allowed Now | Description |
| --- | --- | --- | --- |
| `action-refresh-gate-chain` | `local_report_refresh` | `True` | Refresh service-worker gate map, pool registry, assignment plan, readiness, and chain integrity before any human decision. |
| `action-draft-pool-registration-review` | `manual_review_packet` | `True` | Use existing pool registration packets to decide whether to register local service-worker pool agents. |
| `action-assign-worker` | `service_request_assignment` | `False` | Assign any service request to a worker pool. |
| `action-start-worker` | `worker_start` | `False` | Start any browser, model/API, public-submission, wallet/payment, legal/KYC, or runtime worker. |

## Boundary

- This preflight is report-only.
- It registers no pools, assigns no service requests, starts no workers, updates no service requests, calls no APIs, and performs no external side effects.
