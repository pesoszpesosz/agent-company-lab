# Agent Company Atlas Milestone Runway Browser Verification

- Generated: `2026-06-18T10:26:02Z`
- Task: `task-agent-company-atlas-milestone-runway-v1-20260618`
- Status: `milestone_runway_browser_verified`
- Decision: `runway_nodes_lenses_actions_responsive_checks_passed`

## Checks

- `desktop_panel_visible`: `True`
- `desktop_has_required_node_types`: `True`
- `desktop_has_lenses_actions_and_scrolling_track`: `True`
- `path_action_opens_path_map`: `True`
- `chronicle_action_opens_chronicle`: `True`
- `trail_action_opens_trail`: `True`
- `desktop_no_overflow_or_console_errors`: `True`
- `mobile_runway_responsive`: `True`
- `wide_runway_responsive`: `True`
- `temporary_server_stopped`: `True`
- `no_external_side_effects`: `True`

## Browser Evidence

- `desktop`: `{'panel_visible': True, 'nodes': 15, 'kind_counts': {'checkpoint': 5, 'event': 5, 'future': 1, 'gate': 1, 'unlock': 3}, 'stats_text': '40%route14nodes2gates52events', 'lens_count': 5, 'actions': ['chronicle', 'path', 'trail'], 'track_scrolls': True, 'horizontal_overflow': False, 'console_errors': 0}`
- `interactions`: `{'path': {'hash': '#lane=money_source_discovery&view=path', 'visible': True}, 'chronicle': {'hash': '#lane=money_source_discovery&view=chronicle', 'visible': True}, 'trail': {'hash': '#lane=money_source_discovery&view=trail', 'visible': True}}`
- `mobile`: `{'panel_visible': True, 'nodes': 15, 'stat_columns': 2, 'actions': ['chronicle', 'path', 'trail'], 'track_scrolls': True, 'horizontal_overflow': False, 'console_errors': 0}`
- `wide`: `{'panel_visible': True, 'nodes': 15, 'stat_columns': 4, 'actions': ['chronicle', 'path', 'trail'], 'track_scrolls': True, 'horizontal_overflow': False, 'console_errors': 0}`
- `boundary`: `{'browser_sessions_started': 1, 'temporary_localhost_static_server_started': 1, 'temporary_localhost_static_server_stopped': 1, 'browser_local_hash_changes': 3, 'external_network_calls': 0, 'account_login_or_profile_actions': 0, 'wallet_payment_or_trade_actions': 0, 'public_posts_messages_or_submissions': 0, 'service_requests_mutated': 0, 'model_mcp_or_external_api_calls': 0, 'external_side_effects': 0}`

## Source Files

- `index`: `E:\agent-company-lab\web\index.html` (15465 bytes, `3a8fee2fe528b4aea399d4c625a696a1c0a31bd835febd03dd415a4b30e2c2b7`)
- `app`: `E:\agent-company-lab\web\app.js` (469167 bytes, `49fb537fd4ea17db6403d54c8139b6165138223826528d9fcb59ac3a048838c7`)
- `styles`: `E:\agent-company-lab\web\styles.css` (486022 bytes, `cc4a243ae7511dad80f58d4fd0ff8d7381fdb5c847c793ae2b62f1f894ca71a1`)
- `readme`: `E:\agent-company-lab\web\README.md` (37911 bytes, `b446b6b4b5de82fee1bd7a5e2bc53013244075d6fe0481e70d4dfea3f58ef039`)
- `snapshot`: `E:\agent-company-lab\web\data\snapshot.json` (1011383 bytes, `d3d5b6d82c9161e4c51d82a688a6c4951de598bbf85400913b570d08a3b74afe`)
- `prior_trace_metadata`: `E:\agent-company-lab\reports\agent-company-atlas-milestone-runway-trace-metadata-20260618.json` (5687 bytes, `845d82a0a1dc80d560de66bfea25f369e5c17cea3cea730fc2a3d858aa2fc550`)

## Next Action

Continue closing Atlas platform tasks, starting with Milestone Runway lens controls.
