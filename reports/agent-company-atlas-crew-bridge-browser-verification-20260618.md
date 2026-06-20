# Agent Company Atlas Crew Bridge Browser Verification

- Generated: `2026-06-18T10:14:16Z`
- Task: `task-agent-company-atlas-crew-bridge-v1-20260618`
- Status: `crew_bridge_browser_verified`
- Decision: `crew_cards_readiness_meters_queue_comms_path_responsive_checks_passed`

## Source Files

- `index`: `E:\agent-company-lab\web\index.html` (15465 bytes, `3a8fee2fe528b4aea399d4c625a696a1c0a31bd835febd03dd415a4b30e2c2b7`)
- `app`: `E:\agent-company-lab\web\app.js` (469167 bytes, `49fb537fd4ea17db6403d54c8139b6165138223826528d9fcb59ac3a048838c7`)
- `styles`: `E:\agent-company-lab\web\styles.css` (476554 bytes, `03f3fdd6d892c21cdeb5109d20b347020cc2de6a83e1d736a03fa68f2f3aad02`)
- `readme`: `E:\agent-company-lab\web\README.md` (37432 bytes, `459cd6f9f3fd61436a1f4e0ef172d64f4fb02876731b15faaae54b64df64c912`)
- `snapshot`: `E:\agent-company-lab\web\data\snapshot.json` (1011692 bytes, `f4aea045bb0fed475813be2c63261d4c0ec74b1cad6c8b6155f1ce2054abe69c`)
- `prior_trace_metadata`: `E:\agent-company-lab\reports\agent-company-atlas-crew-bridge-trace-metadata-20260618.json` (5843 bytes, `2a39d8df046fffeab6f61817a9e6de42d6872b64c28f4dfc7310218bbca77702`)

## Desktop

- `viewport`: `{'width': 1280, 'height': 720}`
- `url`: `http://127.0.0.1:8773/index.html?verify=crew-bridge-fresh-20260618#lane=platform_engineering&view=overview`
- `panel_exists`: `True`
- `panel_visible`: `True`
- `panel_width`: `1187`
- `panel_height`: `1641`
- `cards`: `11`
- `lanes`: `11`
- `meters`: `11`
- `active_cards`: `1`
- `action_types`: `['comms', 'path', 'queue']`
- `action_count`: `36`
- `queue_buttons`: `12`
- `comms_buttons`: `12`
- `path_buttons`: `12`
- `animated_signal`: `True`
- `reduced_motion_signal`: `True`
- `grid_columns`: `2`
- `horizontal_overflow`: `False`
- `console_error_count`: `0`

## Interactions

- `queue_button_count_for_money_source_discovery`: `1`
- `comms_button_count_for_money_source_discovery`: `1`
- `path_button_count_for_money_source_discovery`: `1`
- `queue_card_staged`: `True`
- `queue_outbox_has_lane`: `True`
- `queue_outbox_excerpt_contains_review_gate`: `True`
- `comms_hash_after_click`: `#lane=money_source_discovery&view=comms`
- `comms_visible_after_click`: `True`
- `comms_selected_heading`: `Money Source Discovery`
- `path_hash_after_click`: `#lane=money_source_discovery&view=path`
- `path_visible_after_click`: `True`
- `path_selected_heading`: `Money Source Discovery`
- `active_card_recheck_count`: `1`
- `active_card_recheck_lane`: `money_source_discovery`

## Mobile

- `viewport`: `{'width': 390, 'height': 844}`
- `panel_exists`: `True`
- `panel_visible`: `True`
- `panel_width`: `313`
- `panel_height`: `3474`
- `cards`: `11`
- `meters`: `11`
- `active_cards`: `1`
- `action_buttons`: `36`
- `queue_buttons`: `12`
- `comms_buttons`: `12`
- `path_buttons`: `12`
- `grid_columns`: `1`
- `horizontal_overflow`: `False`
- `console_error_count`: `0`

## Wide

- `viewport`: `{'width': 1600, 'height': 1000}`
- `panel_exists`: `True`
- `panel_visible`: `True`
- `panel_width`: `1507`
- `panel_height`: `1110`
- `cards`: `11`
- `meters`: `11`
- `active_cards`: `1`
- `action_buttons`: `36`
- `queue_buttons`: `12`
- `comms_buttons`: `12`
- `path_buttons`: `12`
- `grid_columns`: `3`
- `horizontal_overflow`: `False`
- `console_error_count`: `0`

## Boundary

- `browser_sessions_started`: `1`
- `temporary_localhost_static_server_started`: `1`
- `temporary_localhost_static_server_stopped`: `1`
- `browser_local_hash_changes`: `2`
- `browser_local_queue_draft_staged`: `1`
- `external_network_calls`: `0`
- `account_login_or_profile_actions`: `0`
- `wallet_payment_or_trade_actions`: `0`
- `public_posts_messages_or_submissions`: `0`
- `service_requests_mutated`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Checks

- `desktop_panel_visible`: `True`
- `desktop_cards_meters_and_actions_present`: `True`
- `desktop_has_comms_queue_path_actions`: `True`
- `desktop_active_state_and_motion_signals_present`: `True`
- `queue_action_stages_local_draft`: `True`
- `comms_action_opens_lane_comms`: `True`
- `path_action_opens_lane_path`: `True`
- `active_card_syncs_to_selected_lane`: `True`
- `desktop_no_overflow_or_console_errors`: `True`
- `mobile_single_column_crew_deck_present`: `True`
- `mobile_actions_no_overflow_or_errors`: `True`
- `wide_three_column_crew_deck_present`: `True`
- `wide_actions_no_overflow_or_errors`: `True`
- `temporary_server_stopped`: `True`
- `no_external_side_effects`: `True`

## Next Action

Continue closing Atlas platform tasks, starting with Milestone Runway verification.
