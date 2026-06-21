# Continuity Restore Response: continuity-restore-response-v1-011-continuity-restore-v1-011-request_lane_goal-local_trading_strategy_research

Response type: `lane_goal_response_required`
Restore packet: `continuity-restore-v1-011-request_lane_goal-local_trading_strategy_research`
Target: `lane:local_trading_strategy_research`
Assigned surface: `existing_lane_owner`
Recommended owner: `lane-manager-local_trading_strategy_research-019ec613`

## Next Action

Lane owner must submit one current goal artifact, a park/revisit condition, or an owner-repair request.

## Response Contract

Allowed responses:
- `submit_current_goal_artifact`
- `park_lane_with_revisit_condition`
- `request_owner_repair`

Required fields:
- `selected_response_option`
- `lane_id`
- `restore_packet_id`
- `owner_agent_id`
- `goal_artifact_path_or_revisit_condition`

Prohibited actions:
- `mutate_source_restore_packet`
- `mutate_source_task_or_lane`
- `create_duplicate_agent_without_overlap_review`
- `start_worker_or_thread_without_explicit_ceo_scope`
- `publish_submit_trade_spend_or_call_external_api`
