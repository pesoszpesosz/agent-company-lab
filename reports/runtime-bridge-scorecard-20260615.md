# Runtime Bridge Scorecard

Generated UTC: 2026-06-15T12:14:51Z

## Operating Rule

This scorecard ranks runtime bridges only. It does not approve service requests, install dependencies, enqueue work, start workers, call APIs, browse, submit, trade, pay, register accounts, or perform external actions.

## Summary

- Scorecard rows: `11`
- Chain integrity passed: `True`
- Blocked from execution: `11`
- Worker starts: `0`
- Dependency installs: `0`
- API calls: `False`
- External side effects: `False`

## Recommended Runtime Distribution

- `current_sqlite_reports`: `11` packet(s)

## Runtime Catalog

| Runtime | Role | Durability | Human Gate Fit | Local Fit | Notes |
| --- | --- | --- | --- | --- | --- |
| `current_sqlite_reports` | authoritative_control_plane | `3` | `5` | `5` | Already owns tasks, artifacts, traces, service requests, packets, review boards, and chain integrity. |
| `pydantic_ai_local` | typed_local_worker | `1` | `4` | `5` | Best first bridge for typed local artifact workers and schema-checked summaries; API/model calls stay gated. |
| `langgraph_stateful_managers` | stateful_manager_seeker_loop | `4` | `5` | `3` | Fit for long-running manager/seeker state machines with human-in-the-loop checkpoints after local gates are stable. |
| `microsoft_agent_framework` | production_multi_agent_target | `4` | `4` | `3` | Active Microsoft successor path for production multi-agent orchestration, governance, human-in-loop, MCP/A2A, Python/.NET. |
| `dbos_postgres_queue` | durable_python_queue_candidate | `5` | `4` | `2` | Good minimal Postgres-backed durable workflow/queue adapter candidate; needs Postgres proof before adoption. |
| `hatchet_durable_queue` | durable_multi_language_queue_candidate | `5` | `4` | `2` | Good self-hosted durable queue/monitoring candidate for scaled workers; needs service-worker packet adapter proof. |
| `autogen_legacy_patterns` | legacy_pattern_reference | `2` | `2` | `2` | Maintenance-mode; use only for migration or historical pattern comparison, not new core. |

## Packet Scorecard

| Request | Worker Type | Gate | Recommended Runtime | Score | Reason |
| --- | --- | --- | --- | --- | --- |
| `req-pydantic-ai-model-backed-adapter-20260614` | `model_api_execution` | `ceo_user_cro_model_api_cost_gate` | `current_sqlite_reports` | `96` | approval/cost/artifact authority first |
| `req-next-wave-digital-legal-payment-review-20260614` | `legal_kyc_tax_payment_review` | `user_cro_legal_payment_gate` | `current_sqlite_reports` | `98` | human-only gate and review packet authority |
| `req-next-wave-security-report-route-review-20260614` | `public_submission` | `user_cro_reputation_public_submission_gate` | `current_sqlite_reports` | `98` | reputation/user/CRO gate authority |
| `req-grok-research-worker-20260614` | `browser_signed_in_read_only` | `user_cro_signed_in_browser_gate` | `current_sqlite_reports` | `95` | keep as review/approval authority |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `browser_read_only` | `cro_exact_scope_readonly_gate` | `current_sqlite_reports` | `95` | keep as review/approval authority |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `browser_read_only` | `cro_exact_scope_readonly_gate` | `current_sqlite_reports` | `95` | keep as review/approval authority |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `browser_read_only` | `cro_exact_scope_readonly_gate` | `current_sqlite_reports` | `95` | keep as review/approval authority |
| `req-test-browser-readonly-complete-20260614` | `browser_read_only` | `cro_exact_scope_readonly_gate` | `current_sqlite_reports` | `95` | keep as review/approval authority |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `browser_read_only` | `cro_exact_scope_readonly_gate` | `current_sqlite_reports` | `95` | keep as review/approval authority |
| `req-wave4-digital-products-browser-readonly-20260614` | `browser_read_only` | `cro_exact_scope_readonly_gate` | `current_sqlite_reports` | `95` | keep as review/approval authority |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `browser_read_only` | `cro_exact_scope_readonly_gate` | `current_sqlite_reports` | `95` | keep as review/approval authority |

## Build Order

1. Keep `current_sqlite_reports` as the service-request and approval authority.
2. Build a Pydantic-AI-shaped dry-run local worker for artifact summarization only, with `api_calls=false` and no dependency install unless separately approved.
3. Build DBOS-vs-Hatchet packet-placeholder adapter manifests before importing either runtime.
4. Revisit LangGraph and Microsoft Agent Framework after local worker proofs and approval flow remain clean.
5. Keep AutoGen as a legacy pattern reference only.

## No-Action Statement

No approval, rejection, decision authority, service-request update, assignment, worker start, dependency install, browser/API action, account action, payment, trade, public submission, security testing, wallet action, or external side effect was performed.
