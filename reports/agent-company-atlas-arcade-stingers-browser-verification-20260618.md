# Agent Company Atlas Arcade Stingers Browser Verification

- Generated: `2026-06-18T10:04:54Z`
- Task: `task-agent-company-atlas-arcade-stingers-v1-20260618`
- Status: `arcade_stingers_browser_verified`
- Decision: `animated_stinger_counts_motion_personalities_reduced_motion_and_responsive_checks_passed`

## Source Files

- `index`: `E:\agent-company-lab\web\index.html` (15465 bytes, `3a8fee2fe528b4aea399d4c625a696a1c0a31bd835febd03dd415a4b30e2c2b7`)
- `app`: `E:\agent-company-lab\web\app.js` (458453 bytes, `f4336517ee43a8a1503d43a29eab66e1d51fe39cd478193933b68fc781ec1f70`)
- `styles`: `E:\agent-company-lab\web\styles.css` (476554 bytes, `03f3fdd6d892c21cdeb5109d20b347020cc2de6a83e1d736a03fa68f2f3aad02`)
- `readme`: `E:\agent-company-lab\web\README.md` (37432 bytes, `459cd6f9f3fd61436a1f4e0ef172d64f4fb02876731b15faaae54b64df64c912`)
- `snapshot`: `E:\agent-company-lab\web\data\snapshot.json` (1012190 bytes, `b529aeea7daa1e20f3f6c347d1a1d5b04ea93691cd4e55b4ba48f942f0a7cd0b`)
- `prior_trace_metadata`: `E:\agent-company-lab\reports\agent-company-atlas-arcade-stingers-trace-metadata-20260618.json` (4696 bytes, `455e4014babf46fc2fd2465146edc2f7d4a9f00e293d672d0fc1f25df7b85137`)

## Desktop

- `viewport`: `{'width': 1280, 'height': 720}`
- `url`: `http://127.0.0.1:8771/index.html?verify=arcade-stingers-fresh-20260618#lane=platform_engineering&view=overview`
- `cards`: `12`
- `wrappers`: `12`
- `stingers`: `36`
- `distinct_types`: `['drift', 'grid', 'map', 'pulse', 'route', 'scan']`
- `type_counts`: `{'drift': 2, 'grid': 2, 'map': 2, 'pulse': 2, 'route': 2, 'scan': 2}`
- `animated_names`: `['arcadeStingerBeacon', 'arcadeStingerDrift', 'arcadeStingerDriftWide', 'arcadeStingerGrid', 'arcadeStingerPulse', 'arcadeStingerPulseWide', 'arcadeStingerRoute', 'arcadeStingerScan', 'arcadeStingerSweep']`
- `animated_name_count`: `9`
- `keyframe_count`: `9`
- `has_reduced_motion_rule`: `True`
- `transform_opacity_only_signal`: `True`
- `wrapper_aria_hidden_count`: `12`
- `badge_count`: `12`
- `loaded_textures`: `24`
- `grid_columns`: `4`
- `horizontal_overflow`: `False`
- `console_error_count`: `0`

## Mobile

- `viewport`: `{'width': 390, 'height': 844}`
- `cards`: `12`
- `wrappers`: `12`
- `stingers`: `36`
- `distinct_types`: `['drift', 'grid', 'map', 'pulse', 'route', 'scan']`
- `loaded_textures`: `24`
- `grid_columns`: `1`
- `horizontal_overflow`: `False`
- `wrapper_aria_hidden_count`: `12`
- `badge_count`: `12`
- `console_error_count`: `0`

## Wide

- `viewport`: `{'width': 1600, 'height': 1000}`
- `cards`: `12`
- `wrappers`: `12`
- `stingers`: `36`
- `distinct_types`: `['drift', 'grid', 'map', 'pulse', 'route', 'scan']`
- `loaded_textures`: `24`
- `grid_columns`: `5`
- `horizontal_overflow`: `False`
- `wrapper_aria_hidden_count`: `12`
- `badge_count`: `12`
- `console_error_count`: `0`

## Boundary

- `browser_sessions_started`: `1`
- `temporary_localhost_static_server_started`: `1`
- `temporary_localhost_static_server_stopped`: `1`
- `browser_local_hash_changes`: `0`
- `browser_local_asset_filter_changed`: `0`
- `external_network_calls`: `0`
- `account_login_or_profile_actions`: `0`
- `wallet_payment_or_trade_actions`: `0`
- `public_posts_messages_or_submissions`: `0`
- `service_requests_mutated`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Checks

- `desktop_has_12_wrappers_and_36_stingers`: `True`
- `desktop_has_six_data_driven_motion_personalities`: `True`
- `desktop_has_nine_animation_keyframes`: `True`
- `desktop_has_reduced_motion_coverage`: `True`
- `desktop_animation_uses_transform_opacity_signal`: `True`
- `desktop_stingers_are_aria_hidden`: `True`
- `desktop_loaded_textures_badges_and_grid`: `True`
- `desktop_no_overflow_or_console_errors`: `True`
- `mobile_single_column_stingers_present`: `True`
- `mobile_loaded_textures_no_overflow_or_errors`: `True`
- `wide_five_column_stingers_present`: `True`
- `wide_loaded_textures_no_overflow_or_errors`: `True`
- `temporary_server_stopped`: `True`
- `no_external_side_effects`: `True`

## Next Action

Continue closing Atlas platform tasks, starting with Motion Forge animation-audit verification.
