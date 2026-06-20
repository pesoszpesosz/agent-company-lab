# Control Plane Capacity Benchmark V1

Generated UTC: 2026-06-20T17:50:00Z
Lane: `platform_engineering`
Status: benchmark complete, non-destructive index upgrade applied
JSON mirror: `E:\agent-company-lab\reports\control-plane-capacity-benchmark-v1-20260620.json`
Raw benchmark JSON: `E:\agent-company-lab\work\capacity-benchmark\control_plane_capacity_benchmark_v1_20260620.raw.json`
Synthetic benchmark DB: `E:\agent-company-lab\work\capacity-benchmark\control_plane_capacity_benchmark_v1_20260620.sqlite`

## Decision

The current SQLite control plane is usable at 100,000-row scale for local single-writer operation, but report/dashboard paths need lane/task/status indexes before growth. Applied non-destructive indexes to the production schema and DB for tasks, artifacts, outcomes, and service requests.

## Production Baseline Before Benchmark

| Table | Count |
| --- | ---: |
| tasks | 582 |
| artifacts | 2444 |
| outcomes | 421 |
| trace_events | 512 |
| service_requests | 16 |
| lanes | 15 |
| agents | 16 |

Production DB size before index upgrade was about 3.89 MB (`996` pages at `4096` bytes/page).

## Synthetic Benchmark

The benchmark created a separate SQLite file under `work/capacity-benchmark`, loaded the project schema, inserted synthetic rows into tasks, artifacts, outcomes, trace events, and service requests, and timed common CEO/report queries.

| Target rows per primary table | Insert seconds | Temp DB size | Slowest query | Slowest seconds |
| ---: | ---: | ---: | --- | ---: |
| 1,000 | 0.019220 | 1.36 MB | `join_task_artifact_trace` | 0.000751 |
| 10,000 | 0.179718 | 11.98 MB | `join_task_artifact_trace` | 0.004654 |
| 100,000 | 2.398367 | 120.13 MB | `join_task_artifact_trace` | 0.056622 |

## 100,000-Row Query Timings Before Extra Indexes

| Query | Seconds |
| --- | ---: |
| `count_open_tasks` | 0.014343 |
| `recent_tasks_by_lane` | 0.013241 |
| `artifacts_by_lane` | 0.015030 |
| `outcomes_by_lane` | 0.011844 |
| `trace_by_lane_indexed` | 0.000124 |
| `trace_by_task_indexed` | 0.000028 |
| `service_requests_needs_review` | 0.002519 |
| `join_task_artifact_trace` | 0.056622 |

## 100,000-Row Query Timings After Temp Indexes

| Query | Seconds |
| --- | ---: |
| `count_open_tasks` | 0.004251 |
| `recent_tasks_by_lane` | 0.000170 |
| `artifacts_by_lane` | 0.000086 |
| `outcomes_by_lane` | 0.000069 |
| `trace_by_lane_indexed` | 0.000101 |
| `trace_by_task_indexed` | 0.000033 |
| `service_requests_needs_review` | 0.000053 |
| `join_task_artifact_trace` | 0.000246 |

The indexed temp DB was about 150.07 MB. The extra indexes cost storage but remove the slowest full-scan report paths.

## Applied Production Indexes

Applied through `python tools\agent_company.py init` after updating `tools/agent_company_core/schema.py`:

- `idx_tasks_lane_created` on `tasks(lane_id, created_at)`
- `idx_tasks_status_priority_created` on `tasks(status, priority, created_at)`
- `idx_artifacts_lane_created` on `artifacts(lane_id, created_at)`
- `idx_artifacts_task_created` on `artifacts(task_id, created_at)`
- `idx_outcomes_lane_created` on `outcomes(lane_id, created_at)`
- `idx_outcomes_task_created` on `outcomes(task_id, created_at)`
- `idx_service_requests_status_created` on `service_requests(status, created_at)`
- `idx_service_requests_lane_status` on `service_requests(lane_id, status)`

## Dashboard Feed Verification Fix

After regenerating the snapshot, `test_visual_dashboard_snapshot_keeps_recent_command_unlocks` exposed that the mission feed cap clipped traces below the expected invariant after the company grew to 15 lanes. Increased `COMPANY_FEED_EVENT_LIMIT` from `92` to `120` in `tools/visual_dashboard_snapshot_trail.py`.

Result after regeneration:

- Mission feed items: `288`
- Mission feed trace count: `127`
- Focused snapshot test: passed

## Capacity Policy

- SQLite remains the source of truth for now.
- Use SQLite confidently through 100,000-row local operation if work remains single-writer and reports use indexed lane/task/status paths.
- Re-run this benchmark at 500,000 and 1,000,000 row scales before adding durable workflow engines.
- Add report pagination and snapshot archiving before dashboard payloads become too large.
- Treat Temporal, DBOS, Hatchet, Trigger.dev, LangGraph, Prefect, Dagster, and Restate as future adapters, not current dependencies.

## Runner Follow-Up

Completed: `control_plane_capacity_benchmark_runner_v1` now exists as `python tools\agent_company.py run-control-plane-capacity-benchmark`.

- Runner module: `E:\agent-company-lab\tools\agent_company_core\control_plane_capacity_benchmark_runner.py`
- Runner report: `E:\agent-company-lab\reports\control-plane-capacity-benchmark-runner-v1-20260620.md`
- Runner JSON: `E:\agent-company-lab\reports\control-plane-capacity-benchmark-runner-v1-20260620.json`
- Synthetic runner DB: `E:\agent-company-lab\work\capacity-benchmark\control_plane_capacity_benchmark_runner_v1_20260620.sqlite`
- Verified scenario: `1,000`, `10,000`, and `100,000` synthetic rows per target table.

## Next Action

Run this reusable benchmark at `500,000` and `1,000,000` rows before adding durable workflow engines or high-volume worker queues.

## Boundary

- Production table rows inserted by benchmark: 0
- Production data deleted or rewritten: 0
- Production schema change: non-destructive indexes only
- Dashboard feed cap change: local snapshot builder only
- Runtime/workers started: 0
- Browser sessions started: 0
- Model/API/MCP calls: 0
- Service requests approved, assigned, or started: 0
- External side effects: false
