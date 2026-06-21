# Lane Manager Checkpoint Handoff v1

Generated UTC: 2026-06-21T15:49:37Z
Report JSON: `E:\agent-company-lab\reports\lane-manager-checkpoint-handoff-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\lane-manager-checkpoint-handoff-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Expected lane handoffs: `14`
- Accepted fixtures: `1`
- Rejected fixtures: `12`
- Handoff allowed: `False`
- Worker start allowed: `False`
- Service request mutation allowed: `False`
- External side effects: `False`

## Covered Lanes

- `ai_ml_competitions`
- `ai_resources_lab`
- `content_and_social_growth`
- `digital_products_templates_plugins`
- `lead_generation_and_sales`
- `local_trading_strategy_research`
- `money_source_discovery`
- `paid_code_bounties`
- `platform_engineering`
- `prediction_market_research`
- `premium_customer_intake`
- `security_bounty_private_reports`
- `web3_airdrops_grants_hackathons`
- `youtube_content_channels`

## Fixture Results

| Fixture | Expected | Accepted | Rows | Passed | Errors |
| --- | --- | --- | ---: | --- | --- |
| `positive_all_owned_active_lane_handoffs` | `accepted` | `True` | `14` | `True` |  |
| `negative_missing_lane` | `rejected` | `False` | `13` | `True` | handoff_lane_set_must_equal_owned_active_lanes_excluding_read_only_payouts |
| `negative_submitted_payout_lane_included` | `rejected` | `False` | `15` | `True` | handoff_lane_set_must_equal_owned_active_lanes_excluding_read_only_payouts, excluded_read_only_lane_must_not_be_handoff_row, manager_agent_id_must_match_lane_owner |
| `negative_missing_manager` | `rejected` | `False` | `14` | `True` | manager_agent_id_must_match_lane_owner, manager_agent_id_missing |
| `negative_checkpoint_not_required` | `rejected` | `False` | `14` | `True` | checkpoint_interrupt_required_must_be_true |
| `negative_handoff_allowed` | `rejected` | `False` | `14` | `True` | handoff_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `14` | `True` | worker_start_allowed_must_be_false |
| `negative_service_request_mutation_allowed` | `rejected` | `False` | `14` | `True` | service_request_mutation_allowed_must_be_false |
| `negative_outside_bridge_validation` | `rejected` | `False` | `14` | `True` | checkpoint_bridge_validation_path_must_stay_inside_lab, checkpoint_bridge_validation_not_ready |
| `negative_task_created_side_effect` | `rejected` | `False` | `14` | `True` | runtime_boundary_tasks_created_must_equal_0 |
| `negative_service_request_assigned` | `rejected` | `False` | `14` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_runtime_started` | `rejected` | `False` | `14` | `True` | runtime_boundary_runtime_starts_must_equal_0 |
| `negative_external_side_effect` | `rejected` | `False` | `14` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Handoff rows are checkpoint pause packets only.
- They create no tasks, acquire no tasks, mutate no service requests, and start no workers.
- The submitted payout lane remains read-only and excluded from handoff rows.
