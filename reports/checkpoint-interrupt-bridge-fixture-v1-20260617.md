# Checkpoint Interrupt Bridge Fixture v1

Generated UTC: 2026-06-21T15:49:34Z
Report JSON: `E:\agent-company-lab\reports\checkpoint-interrupt-bridge-fixture-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\checkpoint-interrupt-bridge-fixture-v1-validation-20260617.json`
Source scorecard: `E:\agent-company-lab\reports\adapter-candidate-scorecard-v1-20260617.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `1`
- Rejected fixtures: `19`
- Runtime adoption allowed: `False`
- Dependency installs: `0`
- External framework imports: `0`
- Runtime starts: `0`
- Graph nodes executed: `0`
- Resume allowed: `False`
- Worker starts: `0`
- External side effects: `False`

## Source State

| Source | Ready |
| --- | --- |
| `scorecard_validation_ready` | `True` |
| `checkpoint_validation_ready` | `True` |
| `scorecard_top_candidate_langgraph` | `True` |

## Fixture Results

| Fixture | Expected | Accepted | Passed | Errors |
| --- | --- | --- | --- | --- |
| `positive_langgraph_checkpoint_bridge_fixture` | `accepted` | `True` | `True` |  |
| `negative_wrong_candidate` | `rejected` | `False` | `True` | source_candidate_must_be_langgraph |
| `negative_wrong_rank` | `rejected` | `False` | `True` | source_candidate_rank_must_be_1 |
| `negative_runtime_mode_live` | `rejected` | `False` | `True` | bridge_mode_must_be_local_fixture_only |
| `negative_not_mapped_to_checkpoint` | `rejected` | `False` | `True` | maps_to_checkpoint_interrupt_contract_must_be_true |
| `negative_runtime_adoption_allowed` | `rejected` | `False` | `True` | runtime_adoption_allowed_must_be_false |
| `negative_dependency_install_allowed` | `rejected` | `False` | `True` | dependency_install_allowed_must_be_false |
| `negative_dependency_import_allowed` | `rejected` | `False` | `True` | dependency_import_allowed_must_be_false |
| `negative_resume_allowed` | `rejected` | `False` | `True` | resume_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_missing_checkpoint_validation` | `rejected` | `False` | `True` | checkpoint_contract_validation_path_missing |
| `negative_outside_scorecard_validation` | `rejected` | `False` | `True` | scorecard_validation_path_must_stay_inside_lab |
| `negative_external_framework_import` | `rejected` | `False` | `True` | runtime_boundary_external_framework_imports_must_equal_0 |
| `negative_runtime_started` | `rejected` | `False` | `True` | runtime_boundary_runtime_starts_must_equal_0 |
| `negative_graph_node_executed` | `rejected` | `False` | `True` | runtime_boundary_graph_nodes_executed_must_equal_0 |
| `negative_checkpoint_resumed` | `rejected` | `False` | `True` | runtime_boundary_checkpoint_resumes_must_equal_0 |
| `negative_model_api_called` | `rejected` | `False` | `True` | runtime_boundary_model_api_calls_must_equal_False |
| `negative_service_request_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- This bridge is local scaffolding only.
- It imports no LangGraph package and installs no dependency.
- It executes no graph node, resumes no checkpoint, applies no decision, and starts no worker or runtime.
