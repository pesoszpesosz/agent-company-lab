# Agent Company Trace Events

Generated UTC: 2026-06-15T14:17:59Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
Rows shown: 6

## Boundary

- Trace events are local audit records for agent/company operations.
- A trace event is not approval to perform account, wallet, browser, public, legal/KYC/billing, or real-money actions.

## Counts By Event Type

| Event Type | Count |
| --- | ---: |
| `ceo_cro_model_api_gate_checklist` | 1 |
| `model_api_gate_human_review_form` | 1 |
| `model_api_worker_pool_registration_packet` | 1 |
| `pydantic_ai_local_dry_run_packet_summary` | 1 |
| `pydantic_ai_local_dry_run_worker_manifest` | 1 |
| `runtime_bridge_scorecard` | 1 |

## Counts By Lane

| Lane | Count |
| --- | ---: |
| `platform_engineering` | 6 |

## Events

| Time | Type | Trace | Lane | Task | Agent | Event | Source | Artifact | Metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-15T14:17:42Z | model_api_worker_pool_registration_packet | `trace-agent-company-runtime-bridge-20260615` | `platform_engineering` | `task-model-api-worker-pool-registration-packet-20260615` | recovered-profitable-edge-infra | `trace-event-model-api-worker-pool-registration-packet-20260615` - Registered manual-review packet for model/API execution worker pool; no pool registration, approval, service mutation, assignment, start, API call, or external effect. | codex-local-artifact | E:\agent-company-lab\reports\service-worker-model-api-review\model-api-worker-pool-registration-packet-20260615.json | {"api_calls": false, "approvals_granted": 0, "dependency_imports": 0, "dependency_installs": 0, "external_side_effects": false, "markdown_path": "E:\\agent-company-lab\\reports\\service-worker-model-api-review\\model-api |
| 2026-06-15T12:30:42Z | model_api_gate_human_review_form | `trace-agent-company-runtime-bridge-20260615` | `platform_engineering` | `task-model-api-gate-human-review-form-20260615` | recovered-profitable-edge-infra | `trace-event-model-api-gate-human-review-form-20260615` - Registered local human review form for model/API service gate; default decision park, no approval, rejection, API call, service mutation, assignment, start, or external effect. | codex-local-artifact | E:\agent-company-lab\reports\service-worker-model-api-review\model-api-gate-human-review-form-20260615.json | {"api_calls": false, "approvals_granted": 0, "default_decision": "park", "dependency_imports": 0, "dependency_installs": 0, "external_side_effects": false, "form_path": "E:\\agent-company-lab\\reports\\service-worker-mod |
| 2026-06-15T12:27:55Z | ceo_cro_model_api_gate_checklist | `trace-agent-company-runtime-bridge-20260615` | `platform_engineering` | `task-ceo-cro-model-api-gate-checklist-20260615` | recovered-profitable-edge-infra | `trace-event-ceo-cro-model-api-gate-checklist-20260615` - Registered CEO/CRO checklist for model/API gate; recommends park until provider/model/cost/artifact scope and worker pool exist; no approval, API call, service mutation, assignment, start, or external effect. | codex-local-artifact | E:\agent-company-lab\reports\service-worker-model-api-review\ceo-cro-model-api-gate-checklist-20260615.json | {"api_calls": false, "approvals_granted": 0, "checklist_path": "E:\\agent-company-lab\\reports\\service-worker-model-api-review\\ceo-cro-model-api-gate-checklist-20260615.json", "dependency_imports": 0, "dependency_insta |
| 2026-06-15T12:24:05Z | pydantic_ai_local_dry_run_packet_summary | `trace-agent-company-runtime-bridge-20260615` | `platform_engineering` | `task-pydantic-ai-local-dry-run-packet-summary-20260615` | recovered-profitable-edge-infra | `trace-event-pydantic-ai-local-dry-run-packet-summary-20260615` - Registered first local-only per-packet summary for the model/API service request; no approval, runtime import, API call, service mutation, assignment, start, or external side effect. | codex-local-artifact | E:\agent-company-lab\reports\worker-runtime\pydantic-ai-local-dry-run-summaries\req-pydantic-ai-model-backed-adapter-20260614.json | {"api_calls": false, "approvals_granted": 0, "dependency_imports": 0, "dependency_installs": 0, "external_side_effects": false, "schema_version": "trace_metadata.pydantic_ai_local_dry_run_packet_summary.v1", "service_req |
| 2026-06-15T12:20:36Z | pydantic_ai_local_dry_run_worker_manifest | `trace-agent-company-runtime-bridge-20260615` | `platform_engineering` | `task-pydantic-ai-local-dry-run-worker-manifest-20260615` | recovered-profitable-edge-infra | `trace-event-pydantic-ai-local-dry-run-worker-manifest-20260615` - Registered manifest-only Pydantic-AI local dry-run worker shape for 11 gated service-worker packets; no execution or side effects. | codex-local-artifact | E:\agent-company-lab\reports\worker-runtime\pydantic-ai-local-dry-run-worker-manifest-20260615.json | {"api_calls": false, "dependency_imports": 0, "dependency_installs": 0, "executable_rows": 0, "external_side_effects": false, "manifest_path": "E:\\agent-company-lab\\reports\\worker-runtime\\pydantic-ai-local-dry-run-wo |
| 2026-06-15T12:15:15Z | runtime_bridge_scorecard | `trace-agent-company-runtime-bridge-20260615` | `platform_engineering` | `task-runtime-bridge-scorecard-20260615` | recovered-profitable-edge-infra | `trace-event-runtime-bridge-scorecard-20260615` - Generated report-only runtime bridge scorecard for 11 review-ready service-worker packets; current SQLite remains authority and Pydantic AI dry-run local worker is the next proof, with zero installs, starts, API calls, u | local_reports | E:\agent-company-lab\reports\runtime-bridge-scorecard-20260615.json | {} |
