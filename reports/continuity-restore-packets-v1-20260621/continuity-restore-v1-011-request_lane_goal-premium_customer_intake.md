# Continuity Restore Packet: continuity-restore-v1-011-request_lane_goal-premium_customer_intake

Kind: `request_lane_goal`
Target: `lane:premium_customer_intake`
Assigned surface: `existing_lane_owner`
Recommended owner: `premium-customer-intake-agent-20260620`
Priority: `86`

## Required Evidence

One current lane goal artifact, or an explicit park/kill request with rationale.

## Next Action

Ask the lane owner for one current goal artifact; if no owner exists, route to AI Resources for owner repair before goal assignment.

## Prohibited Actions

- `mutate_source_snapshot`
- `create_duplicate_agent_without_overlap_review`
- `start_worker_or_thread_without_explicit_ceo_scope`
- `publish_submit_trade_spend_or_call_external_api`
