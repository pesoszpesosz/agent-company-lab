# Durable Service-Worker Queue Adapter Manifests - 2026-06-15

Scope: `platform_engineering`.

This report maps the current `service_worker_request.v1` queue into durable-queue adapter contracts. It does not import DBOS, Hatchet, or Temporal; it does not start workers, open browsers, call APIs/models, approve requests, enqueue jobs, or perform external side effects.

## Source Queue

- Source queue: `E:\agent-company-lab\reports\service-worker-request-queue-latest.json`
- Service-worker rows: 14
- Status counts: `{'needs_review': 11, 'complete': 1, 'rejected': 2}`
- Worker type counts: `{'browser_signed_in_read_only': 1, 'legal_kyc_tax_payment_review': 1, 'browser_read_only': 7, 'public_submission': 1, 'model_api_execution': 1, 'local_runtime_adapter': 2, 'other_gated_worker': 1}`

## Adapter Decision

| Adapter | Family | Mode | Safe now | Route counts | Next local test |
| --- | --- | --- | --- | --- | --- |
| `sqlite_service_worker_queue_adapter` | `sqlite_local` | `local_sqlite_queue` | true | `{'hold_for_approval_do_not_enqueue': 11, 'terminal_complete_do_not_enqueue': 1, 'terminal_rejected_do_not_enqueue': 2}` | Add a deterministic dequeuer that emits result placeholders for approved local-only packets and refuses all gated packets. |
| `dbos_service_worker_queue_manifest` | `dbos` | `local_contract_only` | false | `{'hold_for_approval_do_not_enqueue': 11, 'terminal_complete_do_not_enqueue': 1, 'terminal_rejected_do_not_enqueue': 2}` | Generate DBOS transaction/workflow stubs from packets without importing DBOS, opening network connections, or executing workers. |
| `hatchet_service_worker_queue_manifest` | `hatchet` | `local_contract_only` | false | `{'hold_for_approval_do_not_enqueue': 11, 'terminal_complete_do_not_enqueue': 1, 'terminal_rejected_do_not_enqueue': 2}` | Generate Hatchet task/job manifests from packets without starting a Hatchet worker, server, or external queue. |
| `temporal_service_worker_queue_manifest` | `temporal` | `local_contract_only` | false | `{'hold_for_approval_do_not_enqueue': 11, 'terminal_complete_do_not_enqueue': 1, 'terminal_rejected_do_not_enqueue': 2}` | Generate workflow/activity boundary manifests from packets; approvals wait by signal and all side-effect activities remain disabled. |

## Validation

- Manifest count: 4
- Mapped request total: 56
- Network required: False
- Dependencies imported: False
- API calls: False
- External side effects: False
- Enqueue now: False
- Service requests approved by manifest: 0
- Service requests started by manifest: 0

## Queue Gate

All `needs_review` packets route to `hold_for_approval_do_not_enqueue`. Complete and rejected lifecycle-test packets route to terminal no-enqueue states. Even if a future packet has `approved` or `assigned` status, the adapter contract still requires exact approval-scope verification, a lease, packet validation, and side-effect boundary checks before execution.

## Files

- Schema: `E:\agent-company-lab\architecture\durable-service-worker-queue-adapter-v1.schema.json`
- Manifest set: `E:\agent-company-lab\reports\durable-queue-adapters\durable-service-worker-queue-adapter-manifests-20260615.json`
- Validation mirror: `E:\agent-company-lab\reports\durable-queue-adapters\durable-service-worker-queue-adapter-validation-20260615.json`
