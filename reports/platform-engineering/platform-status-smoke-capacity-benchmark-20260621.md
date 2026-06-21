# Control Plane Capacity Benchmark Runner V1

Generated: `2026-06-21T12:43:27Z`
Status: `benchmark_complete_non_destructive`
JSON mirror: `reports\platform-engineering\platform-status-smoke-capacity-benchmark-20260621.json`
Synthetic DB: `work\platform-engineering-status-smoke\control_plane_capacity_benchmark_runner_v1_platform_status_smoke_20260621.sqlite`

## Non-Destructive Contract

- Production database rows inserted by benchmark: `0`
- External network/API calls: `false`
- Accounts created: `0`
- Input data: deterministic synthetic rows only

## Scenario Timings

| Rows per table | Total insert | Slowest query | Slowest seconds | DB MB |
| ---: | ---: | --- | ---: | ---: |
| 1000 | 0.027076s | task_artifact_outcome_join | 0.000277s | 2.38 |

## Applied Index Check

- `tasks`: `ok` (idx_tasks_duplicate_key, idx_tasks_lane_created, idx_tasks_status_priority_created)
- `artifacts`: `ok` (idx_artifacts_lane_created, idx_artifacts_task_created)
- `outcomes`: `ok` (idx_outcomes_lane_created, idx_outcomes_task_created)
- `service_requests`: `ok` (idx_service_requests_lane_status, idx_service_requests_status_created)

## Query Plans

### 1000 Rows Per Table

- `count_open_tasks`: `0.000081s`; plan: SCAN tasks USING COVERING INDEX idx_tasks_status_priority_created
- `lane_recent_tasks`: `0.000132s`; plan: SEARCH tasks USING INDEX idx_tasks_lane_created (lane_id=?)
- `status_priority_backlog`: `0.000104s`; plan: SEARCH tasks USING INDEX idx_tasks_status_priority_created (status=?) / USE TEMP B-TREE FOR LAST TERM OF ORDER BY
- `lane_recent_artifacts`: `0.000119s`; plan: SEARCH artifacts USING INDEX idx_artifacts_lane_created (lane_id=?)
- `task_artifact_outcome_join`: `0.000277s`; plan: SEARCH t USING INDEX idx_tasks_lane_created (lane_id=?) / SEARCH a USING INDEX idx_artifacts_task_created (task_id=?) LEFT-JOIN / SEARCH o USING INDEX idx_outcomes_task_created (task_id=?) LEFT-JOIN
- `service_request_status_queue`: `0.000052s`; plan: SEARCH service_requests USING INDEX idx_service_requests_status_created (status=?)

## Next Action

Use this runner after material schema/report changes and before adding durable workflow engines. Escalate to 500,000 and 1,000,000 rows when the control plane starts queueing real worker volume.
