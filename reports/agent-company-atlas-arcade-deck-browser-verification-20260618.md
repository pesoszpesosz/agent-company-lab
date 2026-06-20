# Agent Company Atlas Arcade Deck Browser Verification

- Generated: `2026-06-18T10:00:40Z`
- Task: `task-agent-company-atlas-arcade-deck-v1-20260618`
- Status: `arcade_deck_browser_verified`
- Decision: `desktop_mobile_launcher_cards_textures_actions_and_responsive_checks_passed`

## Source Files

- `index`: `E:\agent-company-lab\web\index.html` (15465 bytes, `3a8fee2fe528b4aea399d4c625a696a1c0a31bd835febd03dd415a4b30e2c2b7`)
- `app`: `E:\agent-company-lab\web\app.js` (457315 bytes, `b6d44e8aacc9f7b266dbfde63f6bfd4054f263d7ca13787222e074ea94849d23`)
- `styles`: `E:\agent-company-lab\web\styles.css` (466443 bytes, `29471a68a96617e8d5b56fb01e8846adabed0067073068c76e13a6d4b0dab5d6`)
- `snapshot`: `E:\agent-company-lab\web\data\snapshot.json` (1012967 bytes, `72efe0afa73bdb956008c174c2ffe81a47f5690dcfb028935853bd34de29a3ac`)
- `prior_trace_metadata`: `E:\agent-company-lab\reports\agent-company-atlas-arcade-deck-trace-metadata-20260618.json` (5412 bytes, `7e89494c8276a6b6462ac015effd9c30e4fdc47555046a63ed2d694375cbf4db`)

## Desktop

- `viewport`: `{'width': 1280, 'height': 720}`
- `url`: `http://127.0.0.1:8770/index.html?verify=arcade-deck-fresh-20260618#lane=platform_engineering&view=overview`
- `title`: `Agent Company Atlas`
- `panel_exists`: `True`
- `panel_visible`: `True`
- `panel_width`: `1221`
- `panel_height`: `1478`
- `cards`: `12`
- `active_cards`: `1`
- `gated_cards`: `7`
- `ready_cards`: `5`
- `play_buttons`: `12`
- `path_buttons`: `12`
- `art_buttons`: `12`
- `textures`: `24`
- `loaded_textures`: `24`
- `first_texture_natural_width`: `1536`
- `first_texture_natural_height`: `1024`
- `grid_columns`: `4`
- `stinger_overlays`: `36`
- `horizontal_overflow`: `False`
- `console_error_count`: `0`

## Interactions

- `play_button_count_for_platform_engineering`: `1`
- `path_button_count_for_platform_engineering`: `1`
- `art_button_count_for_platform_engineering`: `1`
- `play_hash_after_click`: `#lane=platform_engineering&view=game`
- `play_game_contains_systems_grid`: `True`
- `play_game_action_buttons`: `3`
- `path_hash_after_click`: `#lane=platform_engineering&view=path`
- `path_view_contains_path_map`: `True`
- `path_view_contains_route_text`: `True`
- `art_hash_after_click`: `#lane=platform_engineering&view=overview`
- `art_filter_active_after_click`: `True`
- `asset_vault_count_text_after_art`: `12 / 65 game`
- `active_assets_after_art`: `1`

## Mobile

- `viewport`: `{'width': 390, 'height': 844}`
- `panel_exists`: `True`
- `panel_visible`: `True`
- `panel_width`: `347`
- `panel_height`: `5656`
- `cards`: `12`
- `active_cards`: `1`
- `play_buttons`: `12`
- `path_buttons`: `12`
- `art_buttons`: `12`
- `textures`: `24`
- `loaded_textures`: `24`
- `grid_columns`: `1`
- `horizontal_overflow`: `False`
- `console_error_count`: `0`

## Boundary

- `browser_sessions_started`: `1`
- `temporary_localhost_static_server_started`: `1`
- `temporary_localhost_static_server_stopped`: `1`
- `browser_local_hash_changes`: `3`
- `browser_local_asset_filter_changed`: `1`
- `external_network_calls`: `0`
- `account_login_or_profile_actions`: `0`
- `wallet_payment_or_trade_actions`: `0`
- `public_posts_messages_or_submissions`: `0`
- `service_requests_mutated`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Checks

- `desktop_panel_visible`: `True`
- `desktop_has_12_minigame_cards`: `True`
- `desktop_has_play_path_art_actions`: `True`
- `desktop_textures_loaded`: `True`
- `desktop_responsive_grid_and_stingers`: `True`
- `play_action_opens_game_view`: `True`
- `path_action_opens_path_view`: `True`
- `art_action_filters_game_assets`: `True`
- `desktop_no_overflow_or_console_errors`: `True`
- `mobile_panel_and_cards_visible`: `True`
- `mobile_single_column_loaded_actions`: `True`
- `mobile_no_overflow_or_console_errors`: `True`
- `temporary_server_stopped`: `True`
- `no_external_side_effects`: `True`

## Next Action

Continue closing Atlas platform tasks, starting with Arcade Deck animated stingers and Motion Forge verification.
