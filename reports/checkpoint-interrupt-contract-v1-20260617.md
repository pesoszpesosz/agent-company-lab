# Checkpoint Interrupt Contract v1

Generated UTC: 2026-06-21T15:49:35Z
Report JSON: `E:\agent-company-lab\reports\checkpoint-interrupt-contract-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\checkpoint-interrupt-contract-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `3`
- Rejected fixtures: `16`
- Resume allowed: `False`
- Apply allowed: `False`
- Worker start allowed: `False`
- External side effects: `False`

## Source State

| Source | Ready |
| --- | --- |
| `wave15_validation_ready` | `True` |
| `operator_docket_validation_ready` | `True` |
| `apply_preflight_validation_ready` | `True` |

## Fixture Results

| Fixture | Expected | Accepted | Passed | Errors |
| --- | --- | --- | --- | --- |
| `positive_service_request_gate` | `accepted` | `True` | `True` |  |
| `positive_runtime_adoption_gate` | `accepted` | `True` | `True` |  |
| `positive_lane_task_handoff` | `accepted` | `True` | `True` |  |
| `negative_wrong_schema_version` | `rejected` | `False` | `True` | schema_version_mismatch |
| `negative_unknown_source_kind` | `rejected` | `False` | `True` | source_kind_unknown |
| `negative_missing_lane` | `rejected` | `False` | `True` | lane_id_missing |
| `negative_service_request_without_id` | `rejected` | `False` | `True` | service_request_id_required_for_service_request_source |
| `negative_lane_task_without_task` | `rejected` | `False` | `True` | task_id_required_for_lane_or_runtime_source |
| `negative_manual_review_false` | `rejected` | `False` | `True` | manual_review_required_must_be_true |
| `negative_resume_allowed` | `rejected` | `False` | `True` | resume_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_missing_required_artifacts` | `rejected` | `False` | `True` | required_artifacts_must_be_non_empty_list |
| `negative_outside_required_artifact` | `rejected` | `False` | `True` | required_artifact_must_stay_inside_lab |
| `negative_missing_source_research` | `rejected` | `False` | `True` | source_research_validation_path_missing |
| `negative_resume_command_written` | `rejected` | `False` | `True` | runtime_boundary_resume_commands_written_must_equal_0 |
| `negative_service_request_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_runtime_started` | `rejected` | `False` | `True` | runtime_boundary_runtime_starts_must_equal_0 |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Checkpoint interrupts pause work; they do not resume it.
- They write no apply or resume command.
- They start no worker, runtime, browser, MCP tool, model call, public action, wallet action, or payment.
