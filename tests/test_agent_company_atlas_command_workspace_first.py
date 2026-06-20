from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_deck_prioritizes_active_workspace_before_global_boards():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    workspace = index.index('<section class="workspace" data-atlas-deck-section="command all"')
    system_relay = index.index('<section class="system-relay-panel"')
    dispatch_console = index.index('<section class="dispatch-console-panel"')
    command_relay = index.index('<section class="command-relay-deck-panel"')
    company_quest = index.index('<section class="company-quest-board-panel"')
    operator_roster = index.index('<section class="operator-roster-panel"')

    assert workspace < system_relay
    assert workspace < dispatch_console
    assert workspace < command_relay
    assert workspace < company_quest
    assert workspace < operator_roster

    assert "Command Workspace First" in readme
    assert ".detail-panel {\n    order: -2;" in styles
    assert "20260618-command-workspace-first" in index


def test_command_workspace_uses_wide_detail_stage_on_desktop():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    workspace_start = styles.index(".workspace {\n  display: grid;")
    workspace_end = styles.index(".lane-list-panel,", workspace_start)
    workspace_slice = styles[workspace_start:workspace_end]
    assert "grid-template-columns: minmax(168px, 0.46fr) minmax(680px, 1.72fr) minmax(286px, 0.72fr);" in workspace_slice
    assert "min-height: 640px;" in workspace_slice

    assert ".lane-list-panel {\n  grid-column: 1;" in styles
    assert ".detail-panel {\n  grid-column: 2;" in styles
    assert ".map-stage {\n  grid-column: 3;" in styles
    assert ".detail-panel::before" in styles
    assert "animation: detailStageScan 6.6s ease-in-out infinite;" in styles
    assert "@keyframes detailStageScan" in styles

    map_start = styles.index(".map-stage {")
    map_end = styles.index(".map-playback-hud", map_start)
    map_slice = styles[map_start:map_end]
    assert "height: min(640px, calc(100vh - 80px));" in map_slice
    assert "min-height: 0;" in map_slice

    map_viewport_start = styles.index(".map-viewport {")
    map_viewport_end = styles.index(".map-viewport.dragging", map_viewport_start)
    map_viewport_slice = styles[map_viewport_start:map_viewport_end]
    assert "min-height: 100%;" in map_viewport_slice

    lane_list_start = styles.index("\n.lane-list {\n")
    lane_list_end = styles.index(".lane-button {", lane_list_start)
    lane_list_slice = styles[lane_list_start:lane_list_end]
    assert "max-height: 544px;" in lane_list_slice

    responsive_start = styles.index("@media (max-width: 1320px)")
    responsive_end = styles.index("@media (max-width: 1120px)", responsive_start)
    responsive_slice = styles[responsive_start:responsive_end]
    assert ".map-stage {\n    height: auto;" in responsive_slice
    assert ".lane-list {\n    max-height: 360px;" in responsive_slice

    assert "Command Stage Wide Focus" in readme
    assert "20260619-command-stage-wide-focus" in index


def test_command_cockpit_stage_hides_map_as_separate_level():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-stage-gate" in index

    cockpit_workspace_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .workspace')
    cockpit_workspace_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .map-stage',
        cockpit_workspace_start,
    )
    cockpit_workspace_slice = styles[cockpit_workspace_start:cockpit_workspace_end]
    assert "grid-template-columns: minmax(150px, 0.34fr) minmax(0, 1fr);" in cockpit_workspace_slice
    assert "min-height: min(660px, calc(100vh - 150px));" in cockpit_workspace_slice

    cockpit_map_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .map-stage')
    cockpit_map_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel',
        cockpit_map_start,
    )
    cockpit_map_slice = styles[cockpit_map_start:cockpit_map_end]
    assert "display: none;" in cockpit_map_slice

    cockpit_lane_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel')
    cockpit_lane_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list {',
        cockpit_lane_start,
    )
    cockpit_lane_slice = styles[cockpit_lane_start:cockpit_lane_end]
    assert "max-height: min(660px, calc(100vh - 150px));" in cockpit_lane_slice

    cockpit_detail_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-panel')
    cockpit_detail_end = styles.index("@media (max-width: 860px)", cockpit_detail_start)
    cockpit_detail_slice = styles[cockpit_detail_start:cockpit_detail_end]
    assert "grid-column: 2;" in cockpit_detail_slice
    assert "max-height: min(660px, calc(100vh - 150px));" in cockpit_detail_slice
    assert "overflow-y: auto;" in cockpit_detail_slice

    assert "Command Cockpit Stage Gate" in readme


def test_command_deck_uses_compact_top_hud():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert 'body[data-atlas-deck="command"] .app-shell' in styles
    assert 'body[data-atlas-deck="command"] .topbar' in styles
    assert 'body[data-atlas-deck="command"] .atlas-deck-dock' in styles
    assert 'body[data-atlas-deck="command"] .atlas-deck-button' in styles

    command_shell_start = styles.index('body[data-atlas-deck="command"] .app-shell')
    command_shell_end = styles.index('body[data-atlas-deck="command"] .topbar', command_shell_start)
    command_shell_slice = styles[command_shell_start:command_shell_end]
    assert "padding-top: 12px;" in command_shell_slice

    command_topbar_start = styles.index('body[data-atlas-deck="command"] .topbar')
    command_topbar_end = styles.index('body[data-atlas-deck="command"] .brand-block', command_topbar_start)
    command_topbar_slice = styles[command_topbar_start:command_topbar_end]
    assert "min-height: 42px;" in command_topbar_slice
    assert "padding: 0 4px 6px;" in command_topbar_slice

    command_dock_start = styles.index('body[data-atlas-deck="command"] .atlas-deck-dock')
    command_dock_end = styles.index('body[data-atlas-deck="command"] .atlas-deck-button', command_dock_start)
    command_dock_slice = styles[command_dock_start:command_dock_end]
    assert "grid-template-columns: repeat(6, minmax(90px, 1fr));" in command_dock_slice
    assert "margin: 0 0 8px;" in command_dock_slice
    assert "padding: 5px;" in command_dock_slice

    command_button_start = styles.index('body[data-atlas-deck="command"] .atlas-deck-button')
    command_button_end = styles.index('body[data-atlas-deck="command"] .atlas-deck-button span', command_button_start)
    command_button_slice = styles[command_button_start:command_button_end]
    assert "min-height: 36px;" in command_button_slice
    assert "padding: 5px 7px;" in command_button_slice

    assert 'body[data-atlas-deck="command"] .atlas-deck-button em' in styles
    assert 'body[data-atlas-deck="command"] .atlas-deck-button em {\n  display: none;' in styles

    assert "Command Top HUD Compact" in readme
    assert "20260619-command-top-hud-compact" in index


def test_command_deck_bounds_lower_archive_boards():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    archive_start = styles.index("body[data-atlas-deck=\"command\"] .system-relay-panel")
    archive_end = styles.index("body[data-atlas-deck=\"command\"] .command-relay-visual", archive_start)
    archive_slice = styles[archive_start:archive_end]

    for selector in [
        'body[data-atlas-deck="command"] .system-relay-panel',
        'body[data-atlas-deck="command"] .dispatch-console-panel',
        'body[data-atlas-deck="command"] .command-relay-deck-panel',
        'body[data-atlas-deck="command"] .company-quest-board-panel',
        'body[data-atlas-deck="command"] .crew-bridge-panel',
        'body[data-atlas-deck="command"] .thread-nexus-panel',
        'body[data-atlas-deck="command"] .bot-command-panel',
        'body[data-atlas-deck="command"] .operator-roster-panel',
    ]:
        assert selector in archive_slice

    assert "max-height: 282px;" in archive_slice
    assert "min-height: 0;" in archive_slice
    assert "overflow-y: auto;" in archive_slice
    assert "scrollbar-gutter: stable;" in archive_slice

    assert "body[data-atlas-deck=\"command\"] .system-relay-panel::after" in styles
    assert "body[data-atlas-deck=\"command\"] .operator-roster-panel::after" in styles
    assert "body[data-atlas-deck=\"command\"] .thread-nexus-panel::after" in styles
    assert "body[data-atlas-deck=\"command\"] .bot-command-panel::after" in styles
    assert "commandArchiveGlow" in styles
    assert "body[data-atlas-deck=\"command\"] .command-relay-visual,\nbody[data-atlas-deck=\"command\"] .company-quest-visual" in styles
    assert "min-height: 180px;" in styles

    assert "Command Archive Shelf" in readme
    assert "20260619-command-archive-shelf" in index


def test_command_mobile_workspace_uses_bounded_stage_stack():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]

    assert 'body[data-atlas-deck="command"] .workspace' in mobile_slice
    assert "gap: 10px;" in mobile_slice
    assert "min-height: 0;" in mobile_slice

    assert 'body[data-atlas-deck="command"] .detail-panel' in mobile_slice
    assert "max-height: min(430px, calc(100vh - 214px));" in mobile_slice

    assert 'body[data-atlas-deck="command"] .lane-list-panel' in mobile_slice
    assert 'body[data-atlas-deck="command"] .lane-list' in mobile_slice
    assert "max-height: 202px;" in mobile_slice

    assert 'body[data-atlas-deck="command"] .map-stage' in mobile_slice
    assert 'body[data-atlas-deck="command"] .map-viewport' in mobile_slice
    assert "height: 220px;" in mobile_slice
    assert "min-height: 220px;" in mobile_slice

    assert "Command Mobile Stage Stack" in readme
    assert "20260619-command-mobile-stage-stack" in index


def test_command_cockpit_mobile_uses_launch_frame_instead_of_tall_chrome():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mobile-launch-frame" in index

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]

    shell_start = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .app-shell')
    shell_end = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .topbar', shell_start)
    shell_slice = mobile_slice[shell_start:shell_end]
    assert "padding: 8px 14px 76px;" in shell_slice

    topbar_start = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .topbar')
    topbar_end = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .brand-block', topbar_start)
    topbar_slice = mobile_slice[topbar_start:topbar_end]
    assert "flex-direction: row;" in topbar_slice
    assert "min-height: 40px;" in topbar_slice
    assert "padding: 0 0 5px;" in topbar_slice

    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .brand-block .eyebrow' in mobile_slice
    snapshot_start = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .top-actions .snapshot-pill')
    snapshot_end = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .icon-button', snapshot_start)
    assert "display: none;" in mobile_slice[snapshot_start:snapshot_end]

    dock_start = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .atlas-deck-dock')
    dock_end = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .atlas-deck-button', dock_start)
    dock_slice = mobile_slice[dock_start:dock_end]
    assert "grid-auto-columns: minmax(86px, 28%);" in dock_slice
    assert "margin: 0 0 5px;" in dock_slice
    assert "padding: 4px;" in dock_slice

    lane_panel_start = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel', dock_end)
    lane_panel_end = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list {', lane_panel_start)
    lane_panel_slice = mobile_slice[lane_panel_start:lane_panel_end]
    assert "order: -3;" in lane_panel_slice
    assert "max-height: 38px;" in lane_panel_slice
    assert "padding: 3px;" in lane_panel_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel .panel-head' in mobile_slice

    lane_list_start = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list {', lane_panel_end)
    lane_list_end = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button', lane_list_start)
    lane_list_slice = mobile_slice[lane_list_start:lane_list_end]
    assert "display: flex;" in lane_list_slice
    assert "max-height: 30px;" in lane_list_slice
    assert "overflow-y: hidden;" in lane_list_slice
    assert "padding: 0 0 2px;" in lane_list_slice

    lane_button_start = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button', lane_list_end)
    lane_button_end = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button-top', lane_button_start)
    lane_button_slice = mobile_slice[lane_button_start:lane_button_end]
    assert "flex: 0 0 84px;" in lane_button_slice
    assert "min-height: 28px;" in lane_button_slice

    detail_start = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-panel')
    detail_end = mobile_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-body', detail_start)
    detail_slice = mobile_slice[detail_start:detail_end]
    assert "max-height: min(610px, calc(100vh - 126px));" in detail_slice

    assert "Command Cockpit Mobile Launch Frame" in readme


def test_command_deck_uses_cinematic_motion_layers():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    command_motion_start = styles.index('body[data-atlas-deck="command"] .workspace')
    command_motion_end = styles.index('body[data-atlas-deck="command"] .system-relay-panel', command_motion_start)
    command_motion_slice = styles[command_motion_start:command_motion_end]

    assert "perspective: 1600px;" in command_motion_slice
    assert 'body[data-atlas-deck="command"] .detail-panel' in command_motion_slice
    assert 'body[data-atlas-deck="command"] .map-stage::before' in command_motion_slice
    assert 'body[data-atlas-deck="command"] .map-stage::after' in command_motion_slice
    assert "animation: commandMapGlide 8.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in command_motion_slice
    assert "animation: commandMapDepthDrift 12s ease-in-out infinite;" in command_motion_slice

    assert 'body[data-atlas-deck="command"] .detail-panel::before' in styles
    assert 'body[data-atlas-deck="command"] .detail-panel::after' in styles
    assert "animation: commandCinematicSweep 8.4s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles
    assert "animation: commandDepthGrid 10.6s ease-in-out infinite;" in styles
    assert 'body[data-atlas-deck="command"] .lane-button.active .lane-rail-signal' in styles
    assert 'body[data-atlas-deck="command"] .lane-button.active .lane-rail-pip::after' in styles
    assert "@keyframes commandRailBreathe" in styles
    assert "@keyframes commandPipGlint" in styles

    assert "Command Cinematic Motion" in readme
    assert "20260619-command-cinematic-motion" in index


def test_command_deck_uses_single_archive_focus_dock():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    workspace = index.index('<section class="workspace" data-atlas-deck-section="command all"')
    archive_dock = index.index('<section class="command-archive-dock"')
    system_relay = index.index('<section class="system-relay-panel"')
    assert workspace < archive_dock < system_relay

    for panel in [
        "relay",
        "dispatch",
        "command",
        "quest",
        "crew",
        "threads",
        "bots",
        "operators",
    ]:
        assert f'data-command-archive-button="{panel}"' in index
        assert f'data-command-archive-panel="{panel}"' in index

    archive_start = styles.index('body[data-atlas-deck="command"] [data-command-archive-panel]')
    archive_end = styles.index("@keyframes commandArchiveDockSweep", archive_start)
    archive_slice = styles[archive_start:archive_end]
    assert 'body[data-atlas-deck="command"][data-command-archive-panel="relay"] [data-command-archive-panel="relay"]' in archive_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="bots"] [data-command-archive-panel]:not([data-command-archive-panel="bots"])' in archive_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="bots"] [data-command-archive-panel="bots"]' in archive_slice
    assert "display: none;" in archive_slice
    assert "display: grid;" in archive_slice
    assert "max-height: min(318px, calc(100vh - 186px));" in archive_slice

    assert 'commandArchivePanel: "relay"' in app
    assert "function setCommandArchivePanel" in app
    assert "function applyCommandArchivePanel" in app
    assert "data-command-archive-button" in app

    assert "Command Archive Focus Dock" in readme
    assert "20260619-command-archive-focus-dock" in index


def test_command_map_stage_opens_as_solo_map_surface():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-map-stage-solo" in index
    assert 'data-atlas-stage="cockpit map"' in index

    solo_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .workspace')
    solo_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-stage', solo_start)
    solo_slice = styles[solo_start:solo_end]
    assert "grid-template-columns: minmax(0, 1fr);" in solo_slice
    assert "min-height: min(640px, calc(100vh - 150px));" in solo_slice

    map_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-stage')
    map_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-viewport', map_start)
    map_slice = styles[map_start:map_end]
    assert "grid-column: 1;" in map_slice
    assert "height: min(640px, calc(100vh - 150px));" in map_slice
    assert "min-height: min(640px, calc(100vh - 150px));" in map_slice

    hidden_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .lane-list-panel')
    hidden_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-stage', hidden_start)
    hidden_slice = styles[hidden_start:hidden_end]
    assert 'body[data-atlas-deck="command"][data-atlas-stage="map"] .detail-panel' in hidden_slice
    assert "display: none;" in hidden_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert 'body[data-atlas-deck="command"][data-atlas-stage="map"] .map-stage' in mobile_slice
    assert "height: min(520px, calc(100vh - 142px));" in mobile_slice

    assert "Command Map Stage Solo" in readme


def test_command_map_stage_fills_solo_board_with_depth_motion():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "20260619-command-map-solo-fill" in index

    reset_start = app.index("function resetView")
    reset_end = app.index("function applyTransform", reset_start)
    reset_slice = app[reset_start:reset_end]
    assert 'document.body.dataset.atlasDeck === "command" && document.body.dataset.atlasStage === "map"' in reset_slice
    assert "const minScale = isSoloMapStage ? 0.52 : 0.42;" in reset_slice
    assert "const scaleBoost = isSoloMapStage ? 1.32 : 1.08;" in reset_slice
    assert "const maxScale = isSoloMapStage ? 0.96 : 0.82;" in reset_slice

    deck_start = app.index("function setAtlasDeck")
    deck_end = app.index("function setCommandArchivePanel", deck_start)
    deck_slice = app[deck_start:deck_end]
    assert 'if (nextDeck === "command" && state.activeAtlasStage === "map") {' in deck_slice
    assert "window.requestAnimationFrame(() => resetView());" in deck_slice

    solo_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-viewport')
    solo_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-world', solo_start)
    viewport_slice = styles[solo_start:solo_end]
    assert "position: relative;" in viewport_slice
    assert "background:" in viewport_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="map"] .map-viewport::before' in viewport_slice
    assert "animation: mapSoloGridPulse 7.4s ease-in-out infinite;" in viewport_slice

    world_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-world')
    world_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .route-line', world_start)
    world_slice = styles[world_start:world_end]
    assert "filter: drop-shadow(0 22px 36px rgba(0, 0, 0, 0.36)) saturate(1.08);" in world_slice

    route_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .route-line')
    route_end = styles.index("@keyframes mapSoloGridPulse", route_start)
    route_slice = styles[route_start:route_end]
    assert "stroke-width: 0.42;" in route_slice
    assert "filter: drop-shadow(0 0 6px rgba(68, 215, 201, 0.42));" in route_slice

    assert "@keyframes mapSoloGridPulse" in styles
    assert "Command Map Solo Fill" in readme


def test_command_map_stage_uses_compact_overlay_dock():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-map-overlay-dock" in index

    playback_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-playback-hud')
    playback_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-playback-hud .eyebrow', playback_start)
    playback_slice = styles[playback_start:playback_end]
    assert "left: 12px;" in playback_slice
    assert "right: 170px;" in playback_slice
    assert "top: 12px;" in playback_slice
    assert "max-width: none;" in playback_slice
    assert "min-height: 44px;" in playback_slice
    assert "padding: 8px 10px;" in playback_slice

    compact_playback_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-playback-hud .eyebrow')
    compact_playback_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-playback-hud h3', compact_playback_start)
    compact_playback_slice = styles[compact_playback_start:compact_playback_end]
    assert "display: none;" in compact_playback_slice

    playback_title_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-playback-hud h3')
    playback_title_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-playback-hud span', playback_title_start)
    playback_title_slice = styles[playback_title_start:playback_title_end]
    assert "white-space: nowrap;" in playback_title_slice
    assert "text-overflow: ellipsis;" in playback_title_slice

    focus_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-focus-panel')
    focus_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-focus-panel:not([hidden])', focus_start)
    focus_slice = styles[focus_start:focus_end]
    assert "left: 12px;" in focus_slice
    assert "right: 12px;" in focus_slice
    assert "bottom: 12px;" in focus_slice
    assert "width: auto;" in focus_slice
    assert "min-height: 0;" in focus_slice
    assert "padding: 10px 12px;" in focus_slice

    focus_visible_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-focus-panel:not([hidden])')
    focus_visible_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-focus-panel p:last-child', focus_visible_start)
    focus_visible_slice = styles[focus_visible_start:focus_visible_end]
    assert "display: grid;" in focus_visible_slice
    assert "grid-template-columns: minmax(0, 1fr) auto;" in focus_visible_slice

    focus_body_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-focus-panel p:last-child')
    focus_body_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="map"] .map-focus-stats', focus_body_start)
    focus_body_slice = styles[focus_body_start:focus_body_end]
    assert "display: none;" in focus_body_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert 'body[data-atlas-deck="command"][data-atlas-stage="map"] .map-playback-hud' in mobile_slice
    assert "right: 170px;" in mobile_slice

    assert "Command Map Overlay Dock" in readme


def test_command_bots_stage_opens_as_command_room():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "20260619-command-bot-command-room" in index
    assert '{ id: "bots", label: "Bots", note: "crew", deck: "command", stage: "bots", panel: "bots", target: ".bot-command-panel" }' in app
    assert 'data-command-archive-panel="bots"' in index

    dock_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .command-archive-dock')
    dock_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .command-archive-dock h2', dock_start)
    dock_slice = styles[dock_start:dock_end]
    assert "grid-template-columns: minmax(118px, 0.2fr) minmax(0, 1fr);" in dock_slice
    assert "margin: 0 0 8px;" in dock_slice
    assert "padding: 8px;" in dock_slice

    h2_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .command-archive-dock h2')
    h2_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .command-archive-buttons', h2_start)
    h2_slice = styles[h2_start:h2_end]
    assert "font-size: 0.78rem;" in h2_slice

    panel_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-panel')
    panel_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-summary', panel_start)
    panel_slice = styles[panel_start:panel_end]
    assert "max-height: min(620px, calc(100vh - 188px));" in panel_slice
    assert "padding: 14px;" in panel_slice
    assert "border-color: color-mix(in srgb, var(--teal) 30%, rgba(255, 255, 255, 0.14));" in panel_slice

    summary_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-summary')
    summary_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-matrix', summary_start)
    summary_slice = styles[summary_start:summary_end]
    assert "grid-template-columns: repeat(4, minmax(84px, 1fr));" in summary_slice
    assert "position: sticky;" in summary_slice
    assert "top: 0;" in summary_slice

    matrix_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-matrix')
    matrix_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-card-rail', matrix_start)
    matrix_slice = styles[matrix_start:matrix_end]
    assert "grid-template-columns: 1fr;" in matrix_slice

    rail_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-card-rail')
    rail_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-card {', rail_start)
    rail_slice = styles[rail_start:rail_end]
    assert "grid-template-columns: repeat(auto-fit, minmax(184px, 1fr));" in rail_slice
    assert "gap: 8px;" in rail_slice

    card_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-card')
    card_end = styles.index("@media (max-width: 860px)", card_start)
    card_slice = styles[card_start:card_end]
    assert "min-height: 166px;" in card_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert 'body[data-atlas-deck="command"][data-atlas-stage="bots"] .command-archive-dock' in mobile_slice
    assert "grid-template-columns: 1fr;" in mobile_slice

    assert "Command Bot Command Room" in readme


def test_command_bots_stage_uses_compact_card_deck():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-bot-card-deck" in index
    assert "20260620-command-bot-low-scroll-squadron-board" in index

    summary_chip_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-summary span')
    summary_chip_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-top', summary_chip_start)
    summary_chip_slice = styles[summary_chip_start:summary_chip_end]
    assert "min-height: 42px;" in summary_chip_slice
    assert "padding: 7px;" in summary_chip_slice

    top_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-top')
    top_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-top .operator-avatar', top_start)
    top_slice = styles[top_start:top_end]
    assert "grid-template-columns: 40px minmax(0, 1fr) auto;" in top_slice
    assert "gap: 6px;" in top_slice

    title_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-top h3')
    title_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-top p:not(.eyebrow)', title_start)
    title_slice = styles[title_start:title_end]
    assert "white-space: nowrap;" in title_slice
    assert "text-overflow: ellipsis;" in title_slice

    specialty_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-top p:not(.eyebrow)')
    specialty_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-lane', specialty_start)
    specialty_slice = styles[specialty_start:specialty_end]
    assert "display: none;" in specialty_slice

    avatar_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-top .operator-avatar')
    avatar_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-lane', avatar_start)
    avatar_slice = styles[avatar_start:avatar_end]
    assert "width: 40px;" in avatar_slice
    assert "height: 40px;" in avatar_slice

    lane_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-lane')
    lane_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-stats span', lane_start)
    lane_slice = styles[lane_start:lane_end]
    assert "grid-template-columns: minmax(0, 1fr) auto;" in lane_slice
    assert "align-items: center;" in lane_slice

    stats_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-stats span')
    stats_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-ask', stats_start)
    stats_slice = styles[stats_start:stats_end]
    assert "min-height: 30px;" in stats_slice
    assert "padding: 4px;" in stats_slice

    ask_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-ask')
    ask_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-thread', ask_start)
    ask_slice = styles[ask_start:ask_end]
    assert "display: none;" in ask_slice

    thread_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-thread')
    thread_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-actions', thread_start)
    thread_slice = styles[thread_start:thread_end]
    assert "display: none;" in thread_slice

    actions_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-actions')
    actions_end = styles.index("@media (max-width: 860px)", actions_start)
    actions_slice = styles[actions_start:actions_end]
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in actions_slice
    assert "margin-top: 0;" in actions_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert 'body[data-atlas-deck="command"][data-atlas-stage="bots"] .bot-command-card-rail' in mobile_slice
    assert "grid-auto-flow: column;" in mobile_slice
    assert "grid-auto-columns: minmax(214px, 238px);" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice

    assert "Command Bot Card Deck" in readme


def test_command_bots_stage_squadron_hud_makes_bot_crew_scannable():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-bot-squadron-hud" in index
    assert "20260620-command-bot-squadron-hud" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-bot-squadron-hud" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function botSquadronHudModel(records)" in app
    assert "function renderBotSquadronHud(model)" in app
    assert "const squadronHud = botSquadronHudModel(records);" in app
    assert "el.botCommandMatrix.innerHTML = `${renderBotSquadronHud(squadronHud)}${renderBotCommandSwitchboard(records)}<div class=\"bot-command-card-rail\">${records.map(renderBotCommandCard).join(\"\")}</div>`;" in app
    assert "crewReadiness(record)" in app
    assert "crewMode(record)" in app
    assert "agentRosterAvatar(record.agent)" in app
    assert 'class="bot-squadron-hud"' in app
    assert 'class="bot-squadron-orbit"' in app
    assert 'class="bot-squadron-beacon ${escapeHtml(mode)} ${record.lane?.id === state.selectedLaneId ? "active" : ""}"' in app
    assert 'data-bot-squadron-mode="${escapeHtml(model.mode)}"' in app
    assert "--bot-squadron-ready:${model.readiness}%" in app

    marker = "/* 20260620-command-bot-squadron-hud */"
    assert marker in styles
    hud_slice = styles[styles.index(marker):]
    assert ".bot-squadron-hud" in hud_slice
    assert ".bot-squadron-hud::before" in hud_slice
    assert ".bot-squadron-orbit" in hud_slice
    assert ".bot-squadron-beacon" in hud_slice
    assert ".bot-squadron-stats" in hud_slice
    assert ".bot-squadron-hud[data-bot-squadron-mode=\"gated\"]" in hud_slice
    assert ".bot-squadron-beacon.gated" in hud_slice
    assert ".bot-squadron-beacon.active" in hud_slice
    assert "grid-column: 1 / -1;" in hud_slice
    assert "animation: botSquadronOrbit" in hud_slice
    assert "@keyframes botSquadronOrbit" in hud_slice
    assert "@media (max-width: 860px)" in hud_slice
    assert "@media (prefers-reduced-motion: reduce)" in hud_slice

    assert "Command Bot Squadron HUD" in readme
    assert "avatar cluster" in readme


def test_command_cockpit_low_scroll_premium_pass_prioritizes_one_screen_board():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-low-scroll-premium-pass" in index
    assert "styles.css?v=" in index
    assert "20260619-command-cockpit-low-scroll-premium-pass" in index.split('href="./styles.css?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-low-scroll-premium-pass */"
    assert marker in styles
    pass_start = styles.index(marker)
    pass_slice = styles[pass_start:]

    assert "--cockpit-shell-height: min(516px, calc(100vh - 204px));" in pass_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .workspace' in pass_slice
    assert "grid-template-columns: minmax(0, 174px) minmax(0, 1fr);" in pass_slice
    assert "height: var(--cockpit-shell-height) !important;" in pass_slice
    assert "max-height: var(--cockpit-shell-height) !important;" in pass_slice

    lane_start = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list')
    lane_end = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button', lane_start)
    lane_slice = pass_slice[lane_start:lane_end]
    assert "grid-template-columns: 1fr;" in lane_slice
    assert "max-height: calc(var(--cockpit-shell-height) - 48px);" in lane_slice

    quest_start = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-cockpit')
    quest_end = pass_slice.index('@media (max-width: 1120px)', quest_start)
    quest_slice = pass_slice[quest_start:quest_end]
    assert "grid-template-columns: minmax(0, 0.78fr) minmax(0, 1.5fr) minmax(0, 0.78fr);" in quest_slice
    assert "flex: 1 1 auto;" in quest_slice
    assert "height: auto;" in quest_slice
    assert "overflow: hidden;" in quest_slice

    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-level-hud' in pass_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens' in pass_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-dock' in pass_slice
    old_chrome_start = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-level-hud')
    old_chrome_end = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage', old_chrome_start)
    old_chrome_slice = pass_slice[old_chrome_start:old_chrome_end]
    assert "display: none;" in old_chrome_slice

    mounted_start = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage')
    mounted_end = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage::after', mounted_start)
    mounted_slice = pass_slice[mounted_start:mounted_end]
    assert "height: 100%;" in mounted_slice
    assert "max-height: none;" in mounted_slice

    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .command-archive-dock' in pass_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .live-ops-pulse-panel' in pass_slice
    support_start = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .command-archive-dock')
    support_end = pass_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-panel::before', support_start)
    support_slice = pass_slice[support_start:support_end]
    assert "display: none;" in support_slice

    assert "Command Cockpit Low-Scroll Premium Pass" in readme
    assert "tighter first-screen game board" in readme


def test_command_cockpit_mission_director_makes_current_objective_obvious():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mission-director" in index
    assert "20260619-command-cockpit-mission-director" in index.split('href="./styles.css?v=', 1)[1]
    assert "function renderQuestMissionDirector(" in app
    assert "${renderQuestMissionDirector(lane, data, gateTitle, gateBody)}" in app
    assert 'class="quest-mission-director' in app
    assert 'data-quest-director-tone="' in app
    assert "Mission Director" in app
    assert "Owner" in app
    assert "Queue" in app
    assert "Gate" in app
    assert "Reward" in app

    marker = "/* 20260619-command-cockpit-mission-director */"
    assert marker in styles
    director_start = styles.index(marker)
    director_end = styles.index("/* 20260619-command-cockpit-low-scroll-premium-pass */", director_start)
    director_slice = styles[director_start:director_end]
    assert ".quest-mission-director" in director_slice
    assert ".quest-director-current" in director_slice
    assert ".quest-director-chips" in director_slice
    assert "@keyframes questDirectorSweep" in director_slice

    cockpit_start = styles.index("/* 20260619-command-cockpit-low-scroll-premium-pass */")
    cockpit_slice = styles[cockpit_start:]
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-mission-director' in cockpit_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-command-grid' in cockpit_slice
    command_grid_start = cockpit_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-command-grid')
    command_grid_end = cockpit_slice.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-event-chain', command_grid_start)
    command_grid_slice = cockpit_slice[command_grid_start:command_grid_end]
    assert "display: none;" in command_grid_slice

    assert "Command Cockpit Mission Director" in readme
    assert "one obvious current objective" in readme


def test_command_cockpit_mission_director_chips_are_action_sockets():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-command-socket" in index
    assert "20260619-command-cockpit-relay-braid" in index
    assert "20260619-command-cockpit-relay-braid" in index.split('href="./styles.css?v=', 1)[1]
    assert "function questCommandSocket(" in app
    assert "function renderQuestRelayBraid(" in app
    assert "${renderQuestRelayBraid(lane, crew, commandSocket)}" in app
    assert 'class="quest-relay-braid' in app
    assert 'data-detail-view="comms"' in app
    assert 'data-copy-command="${escapeHtml(lane.id)}"' in app
    assert "bestLaneDispatchSuggestion(lane)" in app
    assert "dispatchTone(suggestion.kind)" in app
    assert 'label: "Queue"' in app
    assert "queue: true" in app
    assert 'data-stage-lane-command="${escapeHtml(lane.id)}"' in app
    assert "stageDispatch(bestLaneDispatchSuggestion(lane))" in app
    assert "data-quest-director-action" in app
    assert 'view: "comms"' in app
    assert 'view: "path"' in app
    assert 'view: "trail"' in app
    assert 'class="quest-director-chip ${escapeHtml(chip.tone)} ${chip.queue ? "queue" : ""}"' in app
    assert 'type="button"' in app
    assert 'data-detail-view="${escapeHtml(chip.view)}"' in app
    assert 'Stage lane command' in app

    marker = "/* 20260619-command-cockpit-mission-director */"
    director_start = styles.index(marker)
    director_end = styles.index("/* 20260619-command-cockpit-low-scroll-premium-pass */", director_start)
    director_slice = styles[director_start:director_end]
    assert ".quest-director-chip:hover" in director_slice
    assert ".quest-director-chip:focus-visible" in director_slice
    assert "cursor: pointer;" in director_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in director_slice
    assert "/* 20260619-command-cockpit-command-socket */" in director_slice
    assert ".quest-director-chip.queue" in director_slice
    assert "/* 20260619-command-cockpit-relay-braid */" in director_slice
    assert ".quest-relay-braid" in director_slice
    assert ".quest-relay-actions button" in director_slice
    assert "@keyframes questRelayBraidSweep" in director_slice

    assert "Command Cockpit Command Socket" in readme
    assert "stages the best lane dispatch from the cockpit" in readme
    assert "Command Cockpit Relay Braid" in readme
    assert "COM/Q/COPY controls" in readme
    assert "Mission Director Action Sockets" in readme
    assert "Owner, Gate, and Reward chips jump" in readme


def test_command_cockpit_mobile_run_board_reduces_scroll_and_clarifies_purpose():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mobile-run-board" in index
    assert "20260619-command-cockpit-mobile-run-board" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-mobile-command-fold-cascade" in index
    assert "20260619-command-cockpit-mobile-command-fold-cascade" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-mobile-signal-glass" in index.split('href="./styles.css?v=', 1)[1]
    assert "Money Path Run" in app
    assert "Latest Discovery" in app
    assert "${escapeHtml(compactText(lane.name, 78))}" in app

    marker = "/* 20260619-command-cockpit-mobile-run-board */"
    assert marker in styles
    board_slice = styles[styles.index(marker):]
    assert "@media (max-width: 760px)" in board_slice
    assert "overflow-x: clip !important;" in board_slice
    assert "overflow: hidden !important;" in board_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage' in board_slice
    assert "grid-auto-flow: column;" in board_slice
    assert "min-height: calc(100vh - 12px);" in board_slice
    assert "min-height: calc(100vh - 109px) !important;" in board_slice
    assert "min-height: min(566px, calc(100vh - 178px)) !important;" in board_slice
    assert "min-height: min(520px, calc(100vh - 238px)) !important;" in board_slice
    assert "height: 74px;" in board_slice
    assert "min-height: 108px;" in board_slice
    assert "height: clamp(218px, 34vh, 292px) !important;" in board_slice
    assert "body[data-atlas-deck=\"command\"][data-atlas-stage=\"cockpit\"] .detail-content.detail-view-overview .quest-board-stack" in board_slice
    assert "min-height: clamp(218px, 34vh, 292px);" in board_slice
    assert "body[data-atlas-deck=\"command\"][data-atlas-stage=\"cockpit\"] .detail-content.detail-view-overview .quest-action-row" in board_slice
    assert "order: 3;" in board_slice
    assert "order: 4;" in board_slice
    assert "position: static !important;" in board_slice
    assert "body[data-atlas-deck=\"command\"][data-atlas-stage=\"cockpit\"] .quest-stage-grid" in board_slice
    assert "body[data-atlas-deck=\"command\"][data-atlas-stage=\"cockpit\"] .quest-event-chain" in board_slice
    assert "display: none !important;" in board_slice

    fold_marker = "/* 20260619-command-cockpit-mobile-command-fold-cascade */"
    assert fold_marker in styles
    fold_slice = styles[styles.index(fold_marker):]
    assert "height: auto !important;" in fold_slice
    assert "overflow: visible !important;" in fold_slice
    assert "height: clamp(154px, 22vh, 184px) !important;" in fold_slice
    assert "/* 20260619-command-cockpit-mobile-signal-glass */" in styles
    glass_slice = styles[styles.index("/* 20260619-command-cockpit-mobile-signal-glass */"):]
    assert "opacity: 0.24;" in glass_slice
    assert "backdrop-filter: blur(12px) saturate(1.08);" in glass_slice

    assert "Command Cockpit Mobile Run Board" in readme
    assert "playable board instead of a long page" in readme
    assert "Command Cockpit Mobile Command Fold" in readme
    assert "no longer collapses to a clipped blank field" in readme
    assert "Command Cockpit Mobile Signal Glass" in readme
    assert "premium control surface instead of visual noise" in readme


def test_command_cockpit_run_spine_embeds_history_gate_and_next_in_map():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-run-spine" in index
    assert "function renderQuestRunSpine(" in app
    assert "${renderQuestRunSpine(lane, data, gateTitle, gateBody)}" in app
    assert 'class="quest-run-spine"' in app
    assert "data-quest-run-spine" in app
    assert 'data-detail-view="${escapeHtml(node.view)}"' in app
    assert 'label: "Proof"' in app
    assert 'label: "Gate"' in app
    assert 'label: "Next"' in app

    marker = "/* 20260619-command-cockpit-run-spine */"
    assert marker in styles
    spine_start = styles.index(marker)
    spine_end = styles.index("/* 20260619-command-cockpit-low-scroll-premium-pass */", spine_start)
    spine_slice = styles[spine_start:spine_end]
    assert ".quest-run-spine" in spine_slice
    assert ".quest-run-spine-node" in spine_slice
    assert "@keyframes questRunSpineSweep" in spine_slice
    assert "cursor: pointer;" in spine_slice

    mobile_marker = "/* 20260619-command-cockpit-mobile-run-board */"
    mobile_slice = styles[styles.index(mobile_marker):]
    assert ".quest-run-spine-node em" in mobile_slice
    assert "display: none;" in mobile_slice

    assert "Command Cockpit Run Spine" in readme
    assert "what has been proven, what is blocking progress, and what move is queued" in readme


def test_command_cockpit_realm_skin_cartridge_makes_lane_game_identity_visible():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-realm-skin-cartridge" in index
    assert "function renderQuestRealmSkinCartridge(" in app
    assert "${renderQuestRealmSkinCartridge(lane, data)}" in app
    assert 'class="quest-realm-skin-cartridge' in app
    assert "data-quest-realm-skin" in app
    assert 'data-detail-view="game"' in app
    assert "lane.visual?.minigame" in app
    assert "arcadeStingerType(lane)" in app
    assert "minigameDefinition(lane)" in app

    marker = "/* 20260619-command-cockpit-realm-skin-cartridge */"
    assert marker in styles
    cartridge_start = styles.index(marker)
    cartridge_end = styles.index("/* 20260619-command-cockpit-low-scroll-premium-pass */", cartridge_start)
    cartridge_slice = styles[cartridge_start:cartridge_end]
    assert ".quest-realm-skin-cartridge" in cartridge_slice
    assert ".quest-realm-skin-thumb" in cartridge_slice
    assert "@keyframes questRealmSkinSweep" in cartridge_slice
    assert "cursor: pointer;" in cartridge_slice

    mobile_marker = "/* 20260619-command-cockpit-mobile-run-board */"
    mobile_slice = styles[styles.index(mobile_marker):]
    assert ".quest-realm-skin-copy em" in mobile_slice
    assert "display: none;" in mobile_slice

    assert "Command Cockpit Realm Skin Cartridge" in readme
    assert "lane.visual.minigame" in readme


def test_command_cockpit_crew_presence_dock_brings_bots_into_map():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-crew-presence-dock" in index
    assert "function renderQuestCrewPresenceDock(" in app
    assert "${renderQuestCrewPresenceDock(lane)}" in app
    assert "agentPartyRecords(lane)" in app
    assert 'class="quest-crew-presence-dock' in app
    assert "data-quest-crew-presence" in app
    assert 'data-detail-view="comms"' in app
    assert 'agentAvatarMarkup(record.agent, lane, "quest-crew-presence-avatar")' in app
    assert "crewReadiness(record)" in app
    assert "crewMode(record)" in app

    marker = "/* 20260619-command-cockpit-crew-presence-dock */"
    assert marker in styles
    dock_start = styles.index(marker)
    dock_end = styles.index("/* 20260619-command-cockpit-lane-world-signal */", dock_start)
    dock_slice = styles[dock_start:dock_end]
    assert ".quest-crew-presence-dock" in dock_slice
    assert ".quest-crew-presence-agent" in dock_slice
    assert ".quest-crew-presence-avatar" in dock_slice
    assert "@keyframes questCrewPresenceSweep" in dock_slice
    assert "cursor: pointer;" in dock_slice

    mobile_marker = "/* 20260619-command-cockpit-mobile-run-board */"
    mobile_slice = styles[styles.index(mobile_marker):]
    assert ".quest-crew-presence-dock" in mobile_slice
    assert "top: 50px;" in mobile_slice
    assert ".quest-crew-presence-copy em" in mobile_slice
    assert "display: none;" in mobile_slice

    assert "Command Cockpit Crew Presence Dock" in readme
    assert "opens Comms without adding another scrolling panel" in readme


def test_command_cockpit_unlock_ladder_shows_checkpoint_progress_in_map():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-unlock-ladder-strip" in index
    assert "function renderQuestUnlockLadder(" in app
    assert "${renderQuestUnlockLadder(lane, data)}" in app
    assert "lane.quest?.checkpoints" in app
    assert "data-quest-unlock-ladder" in app
    assert 'data-detail-view="path"' in app
    assert "data-unlock-state" in app
    assert "data-unlock-current" in app
    assert "lane.counts?.outcomes" in app

    marker = "/* 20260619-command-cockpit-unlock-ladder-strip */"
    assert marker in styles
    ladder_start = styles.index(marker)
    ladder_end = styles.index("/* 20260619-command-cockpit-lane-world-signal */", ladder_start)
    ladder_slice = styles[ladder_start:ladder_end]
    assert ".quest-unlock-ladder" in ladder_slice
    assert ".quest-unlock-ladder-pips" in ladder_slice
    assert "@keyframes questUnlockLadderSweep" in ladder_slice
    assert "@keyframes questUnlockCurrentPulse" in ladder_slice
    assert "cursor: pointer;" in ladder_slice

    mobile_marker = "/* 20260619-command-cockpit-mobile-run-board */"
    mobile_slice = styles[styles.index(mobile_marker):]
    assert ".quest-unlock-ladder" in mobile_slice
    assert "top: 94px;" in mobile_slice
    assert ".quest-unlock-ladder > em" in mobile_slice
    assert "display: none;" in mobile_slice

    assert "Command Cockpit Unlock Ladder Strip" in readme
    assert "cleared levels, current gate/next unlock, and win count" in readme


def test_command_cockpit_signal_convoy_animates_real_event_packets():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-signal-convoy" in index
    assert "function renderQuestSignalConvoy(" in app
    assert "${renderQuestSignalConvoy(packets)}" in app
    assert 'class="quest-event-convoy"' in app
    assert "quest-event-convoy-trail" in app
    assert "data-convoy-tone" in app
    assert "--event-pulse-x" in app
    assert "--event-pulse-y" in app
    assert "--event-pulse-delay" in app

    marker = "/* 20260619-command-cockpit-signal-convoy */"
    assert marker in styles
    convoy_start = styles.index(marker)
    convoy_end = styles.index("@keyframes questEventLensSweep", convoy_start)
    convoy_slice = styles[convoy_start:convoy_end]
    assert ".quest-event-convoy" in convoy_slice
    assert ".quest-event-convoy-trail" in convoy_slice
    assert 'data-convoy-tone="gated"' in convoy_slice
    assert 'data-convoy-tone="earned"' in convoy_slice
    assert "@keyframes questSignalConvoyRun" in convoy_slice
    assert "pointer-events: none;" in convoy_slice

    assert "Command Cockpit Signal Convoy" in readme
    assert "proof, gates, wins, and live work visibly travel through the quest map" in readme


def test_command_cockpit_quest_camera_rail_adds_dense_in_board_motion():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-quest-camera-rail" in index
    assert "20260619-command-cockpit-quest-camera-rail" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-quest-camera-rail" in index.split('<script src="./app.js?v=', 1)[1]
    assert "function questCameraRailSignals(" in app
    assert "function renderQuestCameraRail(" in app
    assert "const cameraRail = questCameraRailSignals(lane, data, focusedCell);" in app
    assert "${renderQuestCameraRail(cameraRail, focusedCell)}" in app
    assert 'class="quest-camera-rail"' in app
    assert "lane.quest?.checkpoints" in app
    assert "lane.counts?.blockers" in app
    assert "lane.counts?.evidence" in app
    assert "questCrewRelayRecord(lane)" in app
    assert "data-camera-tone" in app
    assert "--quest-camera-focus-x" in app
    assert "--camera-x" in app
    assert "--camera-y" in app

    marker = "/* 20260619-command-cockpit-quest-camera-rail */"
    assert marker in styles
    rail_start = styles.index(marker)
    rail_end = styles.index(".quest-event-pulse", rail_start)
    rail_slice = styles[rail_start:rail_end]
    assert ".quest-camera-rail" in rail_slice
    assert ".quest-camera-sweep" in rail_slice
    assert ".quest-camera-orbit" in rail_slice
    assert ".quest-camera-blip" in rail_slice
    assert "@keyframes questCameraRailSweep" in rail_slice
    assert "@keyframes questCameraRailOrbit" in rail_slice
    assert "@keyframes questCameraRailBlip" in rail_slice
    assert "@keyframes questCameraRailPing" in rail_slice
    assert "pointer-events: none;" in rail_slice

    cockpit_slice = styles[styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-camera-rail'):]
    assert ".quest-camera-blip strong" in cockpit_slice
    assert "@media (max-width: 860px)" in cockpit_slice
    assert ".quest-camera-blip i" in cockpit_slice
    assert "display: none;" in cockpit_slice

    assert "Command Cockpit Quest Camera Rail" in readme
    assert "milestone, blocker, proof, bot, and next-move blips" in readme


def test_command_cockpit_route_capsule_shows_unlock_path_without_scroll():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-route-capsule" in index
    assert "20260619-command-cockpit-route-capsule" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-route-capsule" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questRouteCapsules(fieldCells, focusedRole)" in app
    assert "function renderQuestRouteCapsule(routeCapsules, focusedCell)" in app
    assert "const routeCapsules = questRouteCapsules(focusedFieldCells, focusedRole);" in app
    assert "${renderQuestRouteCapsule(routeCapsules, focusedCell)}" in app
    assert 'class="quest-route-capsule"' in app
    assert 'class="quest-route-capsule-node"' in app
    assert 'data-route-role="${escapeHtml(node.role)}"' in app
    assert 'data-route-current="${node.current ? "true" : "false"}"' in app
    assert 'data-route-focused="${node.focused ? "true" : "false"}"' in app
    assert "--route-node-index" in app

    marker = "/* 20260619-command-cockpit-route-capsule */"
    assert marker in styles
    route_slice = styles[styles.index(marker):]
    assert ".quest-route-capsule" in route_slice
    assert "pointer-events: none;" in route_slice
    assert ".quest-route-capsule-node" in route_slice
    assert ".quest-route-capsule-beam" in route_slice
    assert "@keyframes questRouteCapsuleBeam" in route_slice
    assert "@media (max-width: 760px)" in route_slice
    assert "@media (prefers-reduced-motion: reduce)" in route_slice

    assert "Command Cockpit Route Capsule" in readme
    assert "world, level, checkpoint, gate, and next nodes" in readme


def test_command_cockpit_board_atmosphere_adds_data_driven_premium_motion():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-board-atmosphere" in index
    assert "20260619-command-cockpit-board-atmosphere" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-board-atmosphere" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestBoardAtmosphere(lane, data, focusedCell)" in app
    assert "${renderQuestBoardAtmosphere(lane, data, focusedCell)}" in app
    assert 'class="quest-board-atmosphere"' in app
    assert 'data-board-atmosphere-tone="${escapeHtml(focusedCell?.tone ?? data.phase.tone)}"' in app
    assert 'data-board-atmosphere-focus="${escapeHtml(focusedCell?.role ?? "checkpoint")}"' in app
    assert "--board-atmosphere-progress:${data.checkpointProgress}%" in app
    assert "--board-atmosphere-pressure:${Math.min(1, blockerPressure / 6).toFixed(2)}" in app
    assert "--board-atmosphere-proof:${Math.min(1, proofCount / 18).toFixed(2)}" in app
    assert "command-cockpit-event-pulse-20260619.png" in app
    assert 'class="quest-board-atmosphere-spark"' in app

    marker = "/* 20260619-command-cockpit-board-atmosphere */"
    assert marker in styles
    atmosphere_slice = styles[styles.index(marker):]
    assert ".quest-board-atmosphere" in atmosphere_slice
    assert "pointer-events: none;" in atmosphere_slice
    assert ".quest-board-atmosphere-grid" in atmosphere_slice
    assert ".quest-board-atmosphere-sheen" in atmosphere_slice
    assert ".quest-board-atmosphere-spark" in atmosphere_slice
    assert "@keyframes questBoardAtmosphereDrift" in atmosphere_slice
    assert "@keyframes questBoardAtmosphereSpark" in atmosphere_slice
    assert "@media (prefers-reduced-motion: reduce)" in atmosphere_slice
    assert "@media (max-width: 760px)" in atmosphere_slice

    assert "Command Cockpit Board Atmosphere" in readme
    assert "data-driven texture and motion layer" in readme


def test_command_cockpit_lane_constellation_keeps_many_paths_in_board():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-lane-constellation" in index
    assert "20260619-command-cockpit-lane-constellation" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-lane-constellation" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questLaneConstellationLanes(activeLane)" in app
    assert "function renderQuestLaneConstellation(activeLane)" in app
    assert "orderedLaneRailLanes(state.snapshot?.lanes ?? [])" in app
    assert "const lanes = questLaneConstellationLanes(activeLane);" in app
    assert "${renderQuestLaneConstellation(lane)}" in app
    assert 'class="quest-lane-constellation"' in app
    assert 'class="quest-lane-constellation-chip' in app
    assert 'data-lane-id="${escapeHtml(item.id)}"' in app
    assert 'data-constellation-role="${item.id === activeLane.id ? "active" : "neighbor"}"' in app
    assert 'aria-pressed="${item.id === activeLane.id ? "true" : "false"}"' in app
    assert 'class="quest-lane-constellation-more"' in app

    marker = "/* 20260619-command-cockpit-lane-constellation */"
    assert marker in styles
    constellation_slice = styles[styles.index(marker):]
    assert ".quest-lane-constellation" in constellation_slice
    assert "pointer-events: none;" in constellation_slice
    assert ".quest-lane-constellation-chip" in constellation_slice
    assert "pointer-events: auto;" in constellation_slice
    assert ".quest-lane-constellation-more" in constellation_slice
    assert "@keyframes questLaneConstellationPulse" in constellation_slice
    assert "@media (max-width: 760px)" in constellation_slice
    assert "@media (prefers-reduced-motion: reduce)" in constellation_slice

    assert "Command Cockpit Lane Constellation" in readme
    assert "active lane and neighboring money paths" in readme


def test_command_cockpit_mission_stack_turns_node_context_into_board_stages():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-mission-stack" in index
    assert "20260620-command-cockpit-mission-stack" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-mission-stack" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestMissionStack(model)" in app
    assert "const missionStackRows = rows.slice(0, 4);" in app
    assert "${renderQuestMissionStack(model)}" in app
    assert 'class="quest-mission-stack' in app
    assert 'data-mission-stack-role="${escapeHtml(model.role)}"' in app
    assert 'class="quest-mission-stack-stage' in app
    assert 'data-mission-stage-active="${row.label.toLowerCase() === activeLens ? "true" : "false"}"' in app
    assert 'data-mission-stack-view="${escapeHtml(row.view)}"' in app
    assert 'class="quest-mission-stack-link"' in app
    assert "const questExpansionLaneId = state.selectedLaneId ?? selectedLane()?.id;" in app
    assert "[questExpansionLaneId]: questExpansionLens.dataset.questExpansionLens" in app

    marker = "/* 20260620-command-cockpit-mission-stack */"
    assert marker in styles
    stack_slice = styles[styles.index(marker):]
    assert ".quest-mission-stack" in stack_slice
    assert "pointer-events: none;" in stack_slice
    assert ".quest-mission-stack-stage" in stack_slice
    assert "pointer-events: auto;" in stack_slice
    assert ".quest-mission-stack-link" in stack_slice
    assert ".quest-mission-stack ~ .quest-run-spine" in stack_slice
    assert "@keyframes questMissionStackTrace" in stack_slice
    assert "@media (max-width: 760px)" in stack_slice
    assert "@media (prefers-reduced-motion: reduce)" in stack_slice

    assert "Command Cockpit Mission Stack" in readme
    assert "Timeline, Blocker, Proof, and Next" in readme


def test_command_cockpit_mission_dossier_makes_active_lens_visible_in_board():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-mission-dossier" in index
    assert "20260620-command-cockpit-mission-dossier" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-mission-dossier" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestMissionDossier(model)" in app
    assert "const rows = model.lensRows ?? model.expansionRows ?? [];" in app
    assert "const activeRow = rows.find((row) => row.label.toLowerCase() === activeLens) ?? rows[0];" in app
    assert "const depthCards = (model.lensDepthCards ?? []).slice(0, 3);" in app
    assert "${renderQuestMissionDossier(model)}" in app
    assert 'class="quest-mission-dossier' in app
    assert 'data-mission-dossier-lens="${escapeHtml(activeRow.label.toLowerCase())}"' in app
    assert 'data-mission-dossier-role="${escapeHtml(model.role)}"' in app
    assert 'class="quest-mission-dossier-card"' in app
    assert 'data-dossier-card-tone="${escapeHtml(card.tone)}"' in app

    marker = "/* 20260620-command-cockpit-mission-dossier */"
    assert marker in styles
    dossier_slice = styles[styles.index(marker):]
    assert ".quest-mission-dossier" in dossier_slice
    assert "pointer-events: none;" in dossier_slice
    assert ".quest-mission-dossier-card" in dossier_slice
    assert ".quest-mission-dossier ~ .quest-selected-node-lens-tray" in dossier_slice
    assert "opacity: 0.01 !important;" in dossier_slice
    assert "pointer-events: none !important;" in dossier_slice
    assert "@keyframes questMissionDossierReveal" in dossier_slice
    assert "@media (max-width: 760px)" in dossier_slice
    assert "@media (prefers-reduced-motion: reduce)" in dossier_slice

    assert "Command Cockpit Mission Dossier" in readme
    assert "active Timeline, Blocker, Proof, or Next lens" in readme


def test_command_cockpit_level_reel_shows_unlock_progress_inside_board():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-level-reel" in index
    assert "20260620-command-cockpit-level-reel" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-level-reel" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questLevelReelNodes(lane, data, cells, focusedIndex)" in app
    assert "function renderQuestLevelReel(lane, data, cells, focusedIndex)" in app
    assert "const reelNodes = questLevelReelNodes(lane, data, cells, focusedIndex);" in app
    assert "${renderQuestLevelReel(lane, data, focusedFieldCells, focusedIndex)}" in app
    assert 'class="quest-level-reel"' in app
    assert 'data-level-reel-focus="${escapeHtml(reelNodes[1]?.role ?? "checkpoint")}"' in app
    assert "--level-reel-progress:${data.checkpointProgress}%" in app
    assert 'class="quest-level-reel-node' in app
    assert 'data-quest-focus-node="${escapeHtml(node.role)}"' in app
    assert 'data-level-reel-current="${node.current ? "true" : "false"}"' in app
    assert 'data-level-reel-focused="${node.focused ? "true" : "false"}"' in app
    assert 'aria-pressed="${node.focused ? "true" : "false"}"' in app

    marker = "/* 20260620-command-cockpit-level-reel */"
    assert marker in styles
    reel_slice = styles[styles.index(marker):]
    assert ".quest-level-reel" in reel_slice
    assert "pointer-events: none;" in reel_slice
    assert ".quest-level-reel-node" in reel_slice
    assert "pointer-events: auto;" in reel_slice
    assert ".quest-level-reel-progress" in reel_slice
    assert "@keyframes questLevelReelScan" in reel_slice
    assert "@media (max-width: 760px)" in reel_slice
    assert "@media (prefers-reduced-motion: reduce)" in reel_slice

    assert "Command Cockpit Level Reel" in readme
    assert "World, Level, Checkpoint, Gate, and Next" in readme


def test_command_cockpit_unlock_pulse_turns_progress_into_board_feedback():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-unlock-pulse" in index
    assert "20260620-command-cockpit-unlock-pulse" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-unlock-pulse" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestUnlockPulse(lane, data, focusedCell)" in app
    assert "${renderQuestUnlockPulse(lane, data, focusedCell)}" in app
    assert "const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);" in app
    assert "const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);" in app
    assert 'class="quest-unlock-pulse"' in app
    assert 'data-unlock-pulse-focus="${escapeHtml(focusedCell?.role ?? "checkpoint")}"' in app
    assert 'data-unlock-pulse-gate="${blockerPressure ? "locked" : "open"}"' in app
    assert "--unlock-pulse-progress:${data.checkpointProgress}%" in app
    assert "--unlock-pulse-pressure:${Math.min(1, blockerPressure / 6).toFixed(2)}" in app
    assert "--unlock-pulse-proof:${Math.min(1, proofCount / 24).toFixed(2)}" in app
    assert 'class="quest-unlock-pulse-orb' in app
    assert 'data-unlock-orb-tone="${escapeHtml(orb.tone)}"' in app

    marker = "/* 20260620-command-cockpit-unlock-pulse */"
    assert marker in styles
    pulse_slice = styles[styles.index(marker):]
    assert ".quest-unlock-pulse" in pulse_slice
    assert "pointer-events: none;" in pulse_slice
    assert ".quest-unlock-pulse-ring" in pulse_slice
    assert ".quest-unlock-pulse-orb" in pulse_slice
    assert "@keyframes questUnlockPulseSweep" in pulse_slice
    assert "@keyframes questUnlockPulseOrb" in pulse_slice
    assert "@media (max-width: 760px)" in pulse_slice
    assert "@media (prefers-reduced-motion: reduce)" in pulse_slice

    assert "Command Cockpit Unlock Pulse" in readme
    assert "progress, gate pressure, and proof volume" in readme


def test_command_cockpit_focus_director_reduces_overlay_noise():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-focus-director" in index
    assert "20260620-command-cockpit-focus-director" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-focus-director" in index.split('<script src="./app.js?v=', 1)[1]

    assert 'data-quest-board-director="camera"' in app

    marker = "/* 20260620-command-cockpit-focus-director */"
    assert marker in styles
    director_slice = styles[styles.index(marker):]
    assert '.quest-field[data-quest-board-director="camera"]' in director_slice
    assert ".quest-cinematic-focus-plate" in director_slice
    assert ".quest-board-signal-overlay" in director_slice
    assert ".quest-camera-rail" in director_slice
    assert ".quest-route-capsule-node b" in director_slice
    assert ".quest-mission-stack" in director_slice
    assert ".quest-mission-dossier" in director_slice
    assert "pointer-events: none;" in director_slice
    assert "@media (max-width: 760px)" in director_slice
    assert "@media (prefers-reduced-motion: reduce)" in director_slice

    assert "Command Cockpit Focus Director" in readme
    assert "secondary telemetry recedes" in readme


def test_command_cockpit_lane_gate_selector_compresses_many_paths():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-lane-gate-selector" in index
    assert "20260620-command-cockpit-lane-gate-selector" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-lane-gate-selector" in index.split('<script src="./app.js?v=', 1)[1]

    assert 'el.laneList.dataset.laneSelectorMode = "gate";' in app
    assert 'el.laneList.dataset.laneOverflowCount = String(Math.max(0, lanes.length - 7));' in app
    assert 'data-lane-gate-rank="${index}"' in app
    assert '${index > 6 ? "reserve" : ""}' in app

    marker = "/* 20260620-command-cockpit-lane-gate-selector */"
    assert marker in styles
    selector_slice = styles[styles.index(marker):]
    assert '.lane-list[data-lane-selector-mode="gate"]' in selector_slice
    assert '.lane-list[data-lane-selector-mode="gate"] .lane-button:not(.active)' in selector_slice
    assert '.lane-list[data-lane-selector-mode="gate"] .lane-button.reserve' in selector_slice
    assert '.lane-list[data-lane-selector-mode="gate"] .lane-button.active' in selector_slice
    assert ".lane-list-panel::after" in selector_slice
    assert "attr(data-lane-overflow-count)" in selector_slice
    assert "grid-template-columns: 28px minmax(0, 1fr);" in selector_slice
    assert "@media (max-width: 1120px)" in selector_slice
    assert "@media (prefers-reduced-motion: reduce)" in selector_slice

    assert "Command Cockpit Lane Gate Selector" in readme
    assert "many money paths" in readme


def test_command_cockpit_lane_expansion_slots_reserve_future_paths():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-lane-expansion-slots" in index
    assert "20260620-command-cockpit-lane-expansion-slots" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-lane-expansion-slots" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function laneExpansionSlots(lanes)" in app
    assert "const expansionSlots = laneExpansionSlots(lanes);" in app
    assert 'el.laneList.dataset.laneExpansionSlots = String(expansionSlots.length);' in app
    assert 'setAttribute("data-lane-expansion-slots", String(expansionSlots.length))' in app
    assert 'class="lane-expansion-slots"' in app
    assert 'data-lane-expansion-slot="${escapeHtml(slot.id)}"' in app
    assert 'data-lane-expansion-rank="${index}"' in app
    assert "--lane-expansion-count" in app

    marker = "/* 20260620-command-cockpit-lane-expansion-slots */"
    assert marker in styles
    slots_slice = styles[styles.index(marker):]
    assert ".lane-expansion-slots" in slots_slice
    assert ".lane-expansion-slot" in slots_slice
    assert ".lane-expansion-slot::before" in slots_slice
    assert ".lane-expansion-slot[data-lane-expansion-slot=\"minigame\"]" in slots_slice
    assert "pointer-events: none;" in slots_slice
    assert "@media (max-width: 1120px)" in slots_slice
    assert "@media (prefers-reduced-motion: reduce)" in slots_slice

    assert "Command Cockpit Lane Expansion Slots" in readme
    assert "future money paths" in readme


def test_command_cockpit_lane_expansion_mobile_dock_keeps_future_slots_visible():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-lane-expansion-mobile-dock" in index
    assert "20260620-command-cockpit-lane-expansion-mobile-dock" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-lane-expansion-mobile-dock" in index.split('<script src="./app.js?v=', 1)[1]

    marker = "/* 20260620-command-cockpit-lane-expansion-mobile-dock */"
    assert marker in styles
    dock_start = styles.index(marker)
    dock_slice = styles[dock_start:styles.index("@media (prefers-reduced-motion: reduce)", dock_start)]
    assert "@media (max-width: 760px)" in dock_slice
    assert ".lane-list[data-lane-selector-mode=\"gate\"] {" in dock_slice
    assert "padding-right: 68px;" in dock_slice
    assert ".lane-expansion-slots" in dock_slice
    assert "position: sticky;" in dock_slice
    assert "right: 0;" in dock_slice
    assert "grid-column: auto;" in dock_slice
    assert "grid-template-columns: repeat(4, 11px);" in dock_slice
    assert "justify-self: end;" in dock_slice
    assert "width: 62px;" in dock_slice
    assert "margin: 0;" in dock_slice
    assert "backdrop-filter: blur(8px);" in dock_slice
    assert ".lane-expansion-slot i," in dock_slice
    assert "display: none;" in dock_slice

    assert "Command Cockpit Lane Expansion Mobile Dock" in readme
    assert "first mobile rail" in readme


def test_command_cockpit_path_depth_lens_fuses_happened_blocker_proof_next():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-path-depth-lens" in index
    assert "20260620-command-cockpit-path-depth-lens" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-path-depth-lens" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questPathDepthLensModel(lane, data, focusedCell, gateTitle, gateBody)" in app
    assert "function renderQuestPathDepthLens(model)" in app
    assert "const pathDepthLens = questPathDepthLensModel(lane, data, focusedCell, gateTitle, gateBody);" in app
    assert "${renderQuestPathDepthLens(pathDepthLens)}" in app
    assert 'class="quest-path-depth-lens"' in app
    assert 'data-path-depth-focus="${escapeHtml(model.focus)}"' in app
    assert 'data-path-depth-cell="${escapeHtml(cell.id)}"' in app
    assert '"happened", "Happened"' in app
    assert '"blocker", "Blocker"' in app
    assert '"proof", "Proof"' in app
    assert '"next", "Next"' in app

    marker = "/* 20260620-command-cockpit-path-depth-lens */"
    assert marker in styles
    lens_slice = styles[styles.index(marker):]
    assert ".quest-path-depth-lens" in lens_slice
    assert ".quest-path-depth-lens::before" in lens_slice
    assert ".quest-path-depth-cell" in lens_slice
    assert ".quest-path-depth-cell[data-path-depth-tone=\"gated\"]" in lens_slice
    assert "pointer-events: none;" in lens_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in lens_slice
    assert "animation: questPathDepthLensSweep" in lens_slice
    assert "@keyframes questPathDepthLensSweep" in lens_slice
    assert "@media (max-width: 760px)" in lens_slice
    assert "@media (prefers-reduced-motion: reduce)" in lens_slice

    assert "Command Cockpit Path Depth Lens" in readme
    assert "what happened, what blocks it, proof, and next move" in readme


def test_command_cockpit_realm_mood_layer_gives_each_path_a_world_vibe():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-realm-mood-layer" in index
    assert "20260620-command-cockpit-realm-mood-layer" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-realm-mood-layer" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questRealmMoodModel(lane, data)" in app
    assert "function renderQuestRealmMoodLayer(model)" in app
    assert "const realmMood = questRealmMoodModel(lane, data);" in app
    assert "${renderQuestRealmMoodLayer(realmMood)}" in app
    assert "lane.visual?.minigame ?? {}" in app
    assert "minigameDefinition(lane)" in app
    assert "arcadeStingerType(lane)" in app
    assert 'data-realm-mood="${escapeHtml(model.mood)}"' in app
    assert 'data-realm-custom="${model.custom ? "true" : "false"}"' in app
    assert "--realm-mood-charge:${model.charge}%" in app
    assert 'class="quest-realm-mood-layer"' in app
    assert 'class="quest-realm-mood-orbit"' in app

    marker = "/* 20260620-command-cockpit-realm-mood-layer */"
    assert marker in styles
    mood_slice = styles[styles.index(marker):]
    assert ".quest-realm-mood-layer" in mood_slice
    assert ".quest-realm-mood-layer::before" in mood_slice
    assert ".quest-realm-mood-orbit" in mood_slice
    assert ".quest-realm-mood-chip" in mood_slice
    assert '.quest-realm-mood-layer[data-realm-custom="true"]' in mood_slice
    assert "top: 132px;" in mood_slice
    assert "pointer-events: none;" in mood_slice
    assert "animation: questRealmMoodOrbit" in mood_slice
    assert "@keyframes questRealmMoodOrbit" in mood_slice
    assert "@media (max-width: 760px)" in mood_slice
    mobile_mood_slice = mood_slice[mood_slice.index("@media (max-width: 760px)"):]
    assert "top: 178px;" in mobile_mood_slice
    assert "width: 148px;" in mobile_mood_slice
    assert "display: none;" in mobile_mood_slice
    assert "@media (prefers-reduced-motion: reduce)" in mood_slice

    assert "Command Cockpit Realm Mood Layer" in readme
    assert "different game worlds" in readme


def test_command_cockpit_premium_motion_governor_promotes_one_game_board():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-premium-motion-governor" in index
    assert "20260620-command-cockpit-premium-motion-governor" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-premium-motion-governor" in index.split('<script src="./app.js?v=', 1)[1]

    assert 'class="quest-cockpit" data-quest-motion-quality="premium"' in app
    assert 'data-quest-motion-quality="premium" aria-label="Quest level map"' in app

    marker = "/* 20260620-command-cockpit-premium-motion-governor */"
    assert marker in styles
    governor_slice = styles[styles.index(marker):]
    assert '.quest-cockpit[data-quest-motion-quality="premium"]' in governor_slice
    assert '.quest-field[data-quest-motion-quality="premium"]' in governor_slice
    assert ".quest-cockpit-hero" in governor_slice
    assert ".quest-stage-grid" in governor_slice
    assert ".quest-signal-row" in governor_slice
    assert ".quest-command-grid" in governor_slice
    assert ".quest-event-chain" in governor_slice
    assert "display: none !important;" in governor_slice
    assert "animation-duration: 12s !important;" in governor_slice
    assert "animation-duration: 18s !important;" in governor_slice
    assert "@media (max-width: 760px)" in governor_slice
    assert "@media (prefers-reduced-motion: reduce)" in governor_slice

    assert "Command Cockpit Premium Motion Governor" in readme
    assert "one premium game board" in readme


def test_command_cockpit_mission_readout_summarizes_run_without_scroll():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-mission-readout" in index
    assert "20260620-command-cockpit-mission-readout" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-mission-readout" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestMissionReadout(lane, data, focusedCell, gateTitle)" in app
    assert "${renderQuestMissionReadout(lane, data, focusedCell, gateTitle)}" in app
    assert 'class="quest-mission-readout"' in app
    assert 'data-quest-readout-tone="${escapeHtml(focusedCell?.tone ?? data.phase.tone)}"' in app
    assert "data.checkpointProgress" in app
    assert "blockerPressure" in app
    assert "data.nextAction" in app
    assert "focusedCell?.label" in app

    marker = "/* 20260620-command-cockpit-mission-readout */"
    assert marker in styles
    readout_slice = styles[styles.index(marker):]
    assert ".quest-mission-readout" in readout_slice
    assert ".quest-mission-readout::before" in readout_slice
    assert ".quest-mission-readout-cell" in readout_slice
    assert ".quest-mission-readout-core" in readout_slice
    assert ".quest-field[data-quest-motion-quality=\"premium\"] .quest-mission-readout" in readout_slice
    assert "pointer-events: none;" in readout_slice
    assert "grid-template-columns: minmax(82px, 0.7fr) minmax(0, 1.45fr) minmax(78px, 0.85fr);" in readout_slice
    assert "@media (max-width: 760px)" in readout_slice
    assert "@media (prefers-reduced-motion: reduce)" in readout_slice

    assert "Command Cockpit Mission Readout" in readme
    assert "without adding scroll" in readme


def test_command_cockpit_unlock_trail_makes_level_progress_readable():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-command-cockpit-unlock-trail" in index
    assert "20260620-command-cockpit-unlock-trail" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-command-cockpit-unlock-trail" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestUnlockTrail(lane, data, reelNodes, focusedIndex)" in app
    assert "const levelReelNodes = questLevelReelNodes(lane, data, focusedFieldCells, focusedIndex);" in app
    assert "${renderQuestUnlockTrail(lane, data, levelReelNodes, focusedIndex)}" in app
    assert "${renderQuestLevelReel(lane, data, focusedFieldCells, focusedIndex)}" in app
    assert 'class="quest-unlock-trail"' in app
    assert 'data-unlock-trail-gate="${blockerPressure ? "locked" : "open"}"' in app
    assert 'data-unlock-trail-node="${escapeHtml(node.role)}"' in app
    assert "--unlock-trail-progress:${data.checkpointProgress}%" in app

    marker = "/* 20260620-command-cockpit-unlock-trail */"
    assert marker in styles
    trail_slice = styles[styles.index(marker):]
    assert ".quest-unlock-trail" in trail_slice
    assert ".quest-unlock-trail-beam" in trail_slice
    assert ".quest-unlock-trail-node" in trail_slice
    assert ".quest-unlock-trail-node[data-unlock-trail-current=\"true\"]" in trail_slice
    assert ".quest-unlock-trail[data-unlock-trail-gate=\"locked\"]" in trail_slice
    assert "pointer-events: none;" in trail_slice
    assert "animation: questUnlockTrailScan" in trail_slice
    assert "@keyframes questUnlockTrailScan" in trail_slice
    assert "@media (max-width: 760px)" in trail_slice
    assert "@media (prefers-reduced-motion: reduce)" in trail_slice

    assert "Command Cockpit Unlock Trail" in readme
    assert "level progress" in readme


def test_command_cockpit_board_bot_badge_marks_lane_owner_in_game_surface():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-board-bot-badge" in index
    assert "20260619-command-cockpit-board-bot-badge" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-board-bot-badge" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestBoardBotBadge(crew, lane, focusedCell)" in app
    assert "${renderQuestBoardBotBadge(crew, lane, focusedCell)}" in app
    assert 'class="quest-board-bot-badge' in app
    assert 'data-board-bot-tone="${escapeHtml(tone)}"' in app
    assert 'data-board-bot-focus="${escapeHtml(focusedCell?.role ?? "checkpoint")}"' in app
    assert 'data-detail-view="comms"' in app
    assert 'agentAvatarMarkup(crew.agent, lane, "quest-board-bot-avatar")' in app
    assert "crewReadiness" in app

    marker = "/* 20260619-command-cockpit-board-bot-badge */"
    assert marker in styles
    badge_slice = styles[styles.index(marker):]
    assert ".quest-board-bot-badge" in badge_slice
    assert ".quest-board-bot-avatar" in badge_slice
    assert ".quest-board-bot-link" in badge_slice
    assert "cursor: pointer;" in badge_slice
    assert "@keyframes questBoardBotBadgePing" in badge_slice
    assert "@media (max-width: 760px)" in badge_slice
    assert "@media (prefers-reduced-motion: reduce)" in badge_slice

    assert "Command Cockpit Board Bot Badge" in readme
    assert "lane owner directly inside the Quest board" in readme


def test_command_cockpit_boss_board_reduces_stacked_report_chrome():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-boss-board" in index
    assert "20260619-command-cockpit-boss-board" in index.split('href="./styles.css?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-boss-board */"
    assert marker in styles
    boss_start = styles.index(marker)
    boss_slice = styles[boss_start:]

    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .detail-content.detail-view-overview .quest-cockpit' in boss_slice
    assert "grid-template-columns: minmax(0, 0.6fr) minmax(270px, 0.4fr) !important;" in boss_slice
    assert "grid-template-rows: minmax(62px, auto) minmax(0, 1fr) !important;" in boss_slice
    assert ".quest-cockpit-hero" in boss_slice
    assert ".quest-mission-director" in boss_slice
    assert "grid-column: 2;" in boss_slice
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in boss_slice
    assert ".quest-board-stack" in boss_slice
    assert "grid-column: 1 / 5 !important;" in boss_slice
    assert "min-height: clamp(224px, calc(var(--cockpit-shell-height) - 220px), 302px);" in boss_slice
    assert "animation: questBossBoardScan" in boss_slice
    assert "@keyframes questBossBoardScan" in boss_slice
    assert ".quest-event-chain" in boss_slice
    assert ".quest-stage-grid" in boss_slice
    assert ".quest-command-grid" in boss_slice
    assert "display: none !important;" in boss_slice
    assert "@media (max-width: 1120px)" in boss_slice
    assert "@media (max-width: 760px)" in boss_slice
    assert "min-height: 50px;" in boss_slice
    assert "display: none;" in boss_slice

    assert "Command Cockpit Boss Board" in readme
    assert "compact hero/director top HUD plus enlarged animated Quest map" in readme


def test_command_cockpit_icon_command_dock_replaces_text_buttons_with_symbols():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-icon-command-dock" in index
    assert "20260619-command-cockpit-icon-command-dock" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-icon-command-dock" in index.split('<script src="./app.js?v=', 1)[1]
    assert "function renderQuestActionDock(" in app
    assert "${renderQuestActionDock()}" in app
    assert 'class="tool-button quest-action-button"' in app
    assert 'class="quest-action-icon"' in app
    assert "data-action-icon" in app
    assert 'aria-label="${escapeHtml(action.title)}"' in app
    assert 'icon: "map"' in app
    assert 'icon: "log"' in app
    assert 'icon: "game"' in app
    assert 'icon: "comms"' in app
    assert 'icon: "trail"' in app

    marker = "/* 20260619-command-cockpit-icon-command-dock */"
    assert marker in styles
    dock_slice = styles[styles.index(marker):]
    assert ".quest-action-button" in dock_slice
    assert ".quest-action-icon" in dock_slice
    assert 'data-action-icon="map"' in dock_slice
    assert 'data-action-icon="log"' in dock_slice
    assert 'data-action-icon="game"' in dock_slice
    assert 'data-action-icon="comms"' in dock_slice
    assert 'data-action-icon="trail"' in dock_slice
    assert "@keyframes questIconCommandDockSweep" in dock_slice
    assert "clip: rect(0 0 0 0);" in dock_slice

    assert "Command Cockpit Icon Command Dock" in readme
    assert "icon-first CSS-drawn map/log/game/comms/trail controls" in readme


def test_command_cockpit_arcade_board_fit_reclaims_mobile_dead_space():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-arcade-board-fit" in index
    assert "20260619-command-cockpit-arcade-board-fit" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-arcade-board-fit" in index.split('<script src="./app.js?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-arcade-board-fit */"
    assert marker in styles
    fit_slice = styles[styles.index(marker):]
    assert ".quest-board-stack::after" in fit_slice
    assert ".quest-field::after" in fit_slice
    assert "animation: questArcadeBoardAurora" in fit_slice
    assert "animation: questArcadeBoardScan" in fit_slice
    assert "@keyframes questArcadeBoardAurora" in fit_slice
    assert "@keyframes questArcadeBoardScan" in fit_slice
    assert "height: clamp(300px, calc(100vh - 408px), 380px) !important;" in fit_slice
    assert ".quest-action-row" in fit_slice
    assert "position: fixed !important;" in fit_slice
    assert "top: calc(100vh - 344px);" in fit_slice
    assert "bottom: auto;" in fit_slice
    assert "width: min(330px, calc(100vw - 60px));" in fit_slice
    assert "backdrop-filter: blur(13px);" in fit_slice

    assert "Command Cockpit Arcade Board Fit" in readme
    assert "pins the mobile icon dock back into the board" in readme


def test_command_cockpit_mobile_immersive_stack_starts_board_sooner():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mobile-immersive-stack" in index
    assert "20260619-command-cockpit-mobile-immersive-stack" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-mobile-immersive-stack" in index.split('<script src="./app.js?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-mobile-immersive-stack */"
    assert marker in styles
    mobile_slice = styles[styles.index(marker):]
    assert "@media (max-width: 760px)" in mobile_slice
    assert ".topbar" in mobile_slice
    assert "min-height: 32px;" in mobile_slice
    assert ".atlas-deck-dock" in mobile_slice
    assert "min-height: 29px;" in mobile_slice
    assert ".atlas-deck-button em" in mobile_slice
    assert "display: none;" in mobile_slice
    assert ".lane-list-panel" in mobile_slice
    assert "height: 46px;" in mobile_slice
    assert ".lane-list" in mobile_slice
    assert "height: 38px;" in mobile_slice
    assert ".quest-cockpit-hero" in mobile_slice
    assert "min-height: 48px;" in mobile_slice
    assert ".quest-board-stack" in mobile_slice
    assert "height: clamp(348px, calc(100vh - 336px), 430px) !important;" in mobile_slice

    assert "Command Cockpit Mobile Immersive Stack" in readme
    assert "selected path board starts sooner" in readme


def test_command_cockpit_mobile_launch_chrome_squeeze_starts_board_even_sooner():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mobile-launch-chrome-squeeze" in index
    assert "20260619-command-cockpit-mobile-launch-chrome-squeeze" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-mobile-launch-chrome-squeeze" in index.split('<script src="./app.js?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-mobile-launch-chrome-squeeze */"
    assert marker in styles
    squeeze_slice = styles[styles.index(marker):]
    assert "@media (max-width: 760px)" in squeeze_slice
    assert ".atlas-deck-dock" in squeeze_slice
    assert "min-height: 24px;" in squeeze_slice
    assert ".atlas-deck-button" in squeeze_slice
    assert "height: 20px;" in squeeze_slice
    assert ".lane-list-panel" in squeeze_slice
    assert "height: 38px;" in squeeze_slice
    assert ".lane-button" in squeeze_slice
    assert "height: 24px;" in squeeze_slice
    assert ".active-lane-mounted-stage[data-active-stage-view=\"overview\"]" in squeeze_slice
    assert "margin-top: -8px;" in squeeze_slice
    assert ".quest-board-stack" in squeeze_slice
    assert "height: clamp(360px, calc(100vh - 318px), 444px) !important;" in squeeze_slice

    assert "Command Cockpit Mobile Launch Chrome Squeeze" in readme
    assert "pulls the Quest board closer to the top of the phone viewport" in readme


def test_command_cockpit_mobile_director_readout_preserves_blocker_context():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mobile-director-readout" in index
    assert "20260619-command-cockpit-mobile-director-readout" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-mobile-director-readout" in index.split('<script src="./app.js?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-mobile-director-readout */"
    assert marker in styles
    readout_slice = styles[styles.index(marker):]
    assert "@media (max-width: 760px)" in readout_slice
    assert ".quest-mission-director" in readout_slice
    assert "min-height: 42px;" in readout_slice
    assert ".quest-director-current" in readout_slice
    assert "grid-template-columns: minmax(0, 1fr) auto;" in readout_slice
    assert ".quest-director-current .eyebrow" in readout_slice
    assert "display: none;" in readout_slice
    assert ".quest-director-current h3" in readout_slice
    assert "font-size: 0.58rem;" in readout_slice
    assert ".quest-director-current p:not(.eyebrow)" in readout_slice
    assert "display: block !important;" in readout_slice
    assert "max-width: 98px;" in readout_slice
    assert "border-radius: 999px;" in readout_slice
    assert ".quest-relay-braid" in readout_slice
    assert "display: none;" in readout_slice

    assert "Command Cockpit Mobile Director Readout" in readme
    assert "keeps the current blocker visible as a compact chip" in readme


def test_command_cockpit_desktop_board_first_lift_prioritizes_play_surface():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-desktop-board-first-lift" in index
    assert "20260619-command-cockpit-desktop-board-first-lift" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-desktop-board-first-lift" in index.split('<script src="./app.js?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-desktop-board-first-lift */"
    assert marker in styles
    lift_slice = styles[styles.index(marker):]
    assert "@media (min-width: 761px)" in lift_slice
    assert ".quest-cockpit" in lift_slice
    assert "grid-template-rows: 46px minmax(0, 1fr) !important;" in lift_slice
    assert ".quest-mission-director" in lift_slice
    assert "min-height: 48px;" in lift_slice
    assert "max-height: 54px;" in lift_slice
    assert ".quest-director-chips" in lift_slice
    assert "display: none;" in lift_slice
    assert ".quest-relay-braid" in lift_slice
    assert "display: none;" in lift_slice
    assert ".quest-board-stack" in lift_slice
    assert "margin-top: -10px;" in lift_slice
    assert ".quest-field" in lift_slice
    assert "min-height: clamp(260px, calc(var(--cockpit-shell-height) - 170px), 360px);" in lift_slice

    assert "Command Cockpit Desktop Board First Lift" in readme
    assert "pulls the desktop Quest board upward" in readme


def test_command_cockpit_desktop_stage_chrome_collapse_removes_duplicate_preboard_bands():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-desktop-stage-chrome-collapse" in index
    assert "20260619-command-cockpit-desktop-stage-chrome-collapse" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-desktop-stage-chrome-collapse" in index.split('<script src="./app.js?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-desktop-stage-chrome-collapse */"
    assert marker in styles
    collapse_slice = styles[styles.index(marker):]
    assert "@media (min-width: 761px)" in collapse_slice
    assert ".active-lane-stage-event-ribbon" in collapse_slice
    assert ".active-lane-stage-footer-rail" in collapse_slice
    assert "display: none;" in collapse_slice
    assert ".active-lane-mounted-stage[data-active-stage-view=\"overview\"]" in collapse_slice
    assert "padding-top: 2px;" in collapse_slice
    assert ".detail-section" in collapse_slice
    assert "padding-top: 4px;" in collapse_slice
    assert ".quest-cockpit" in collapse_slice
    assert "margin-top: -8px;" in collapse_slice

    assert "Command Cockpit Desktop Stage Chrome Collapse" in readme
    assert "removes duplicated desktop pre-board ribbons" in readme


def test_command_cockpit_node_drill_stack_adds_selected_node_depth():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-node-drill-stack" in index
    assert "20260619-command-cockpit-node-drill-stack" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-node-drill-stack" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questNodeDrillCards(lane, data, cell, gateTitle, gateBody)" in app
    assert "function renderQuestNodeDrillStack(cards, cell)" in app
    assert "const focusedDrillCards = questNodeDrillCards(lane, data, focusedCell, gateTitle, gateBody);" in app
    assert "${renderQuestNodeDrillStack(focusedDrillCards, focusedCell)}" in app
    assert 'class="quest-node-drill-stack"' in app
    assert 'class="quest-node-drill-card"' in app
    assert 'data-quest-drill-role="${escapeHtml(cell?.role ?? "checkpoint")}"' in app
    assert 'label: "Focus"' in app
    assert 'label: "Milestone"' in app
    assert 'label: "Blocker"' in app
    assert 'label: "Trail"' in app
    assert 'label: "Next"' in app
    assert 'label: "Proof"' in app

    marker = "/* 20260619-command-cockpit-node-drill-stack */"
    assert marker in styles
    drill_slice = styles[styles.index(marker):]
    assert ".quest-node-drill-stack" in drill_slice
    assert ".quest-node-drill-card" in drill_slice
    assert "@keyframes questNodeDrillSweep" in drill_slice
    assert "animation: questNodeDrillSweep 6.6s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in drill_slice
    assert 'data-drill-tone="gated"' in drill_slice
    assert 'data-drill-tone="clear"' in drill_slice
    assert "right: 354px;" in drill_slice
    assert "grid-template-columns: repeat(3, minmax(0, 1fr));" in drill_slice
    assert "@media (max-width: 760px)" in drill_slice
    assert "bottom: 96px;" in drill_slice

    assert "Command Cockpit Node Drill Stack" in readme
    assert "selected-node focus/milestone/blocker/trail/next/proof cards" in readme


def test_command_cockpit_clarity_mode_reduces_board_noise():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-clarity-mode" in index
    assert "20260619-command-cockpit-clarity-mode" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-clarity-mode" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questNodeDrillPriority(card)" in app
    assert 'const criticalLabels = new Set(["Focus", "Blocker", "Next"]);' in app
    assert 'data-quest-clarity-mode="focus"' in app
    assert 'data-drill-priority="${escapeHtml(questNodeDrillPriority(card))}"' in app

    marker = "/* 20260619-command-cockpit-clarity-mode */"
    assert marker in styles
    clarity_slice = styles[styles.index(marker):]
    assert '[data-quest-clarity-mode="focus"] .quest-field-cell:not([data-quest-focused="true"])' in clarity_slice
    assert '.quest-node-drill-card[data-drill-priority="archive"]' in clarity_slice
    assert '.quest-node-drill-card[data-drill-priority="primary"]' in clarity_slice
    assert "display: none;" in clarity_slice
    assert "filter: saturate(0.72);" in clarity_slice
    assert "opacity: 1 !important;" in clarity_slice
    assert "@media (max-width: 760px)" in clarity_slice

    assert "Command Cockpit Clarity Mode" in readme
    assert "fades secondary board noise" in readme


def test_command_cockpit_cinematic_focus_plate_replaces_tiny_drill_rail():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-cinematic-focus-plate" in index
    assert "20260619-command-cockpit-cinematic-focus-plate" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-cinematic-focus-plate" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questCinematicFocusPlateModel(lane, data, cell, cards, focusIndex, focusCount, crew)" in app
    assert "function renderQuestCinematicFocusPlate(model)" in app
    assert "const cinematicFocus = questCinematicFocusPlateModel(lane, data, focusedCell, focusedDrillCards, focusedIndex, focusedFieldCells.length, crew);" in app
    assert "${renderQuestCinematicFocusPlate(cinematicFocus)}" in app
    assert 'class="quest-cinematic-focus-plate ${escapeHtml(model.tone)}"' in app
    assert 'data-quest-cinematic-role="${escapeHtml(model.role)}"' in app
    assert "Node Lock" in app
    assert "Blocker" in app
    assert "Next" in app

    marker = "/* 20260619-command-cockpit-cinematic-focus-plate */"
    assert marker in styles
    plate_slice = styles[styles.index(marker):]
    assert ".quest-cinematic-focus-plate" in plate_slice
    assert ".quest-cinematic-focus-plate::before" in plate_slice
    assert ".quest-cinematic-focus-stats" in plate_slice
    assert "@keyframes questCinematicFocusSweep" in plate_slice
    assert ".quest-node-drill-stack" in plate_slice
    assert "display: none;" in plate_slice
    assert "bottom: 96px;" in plate_slice
    assert "@media (max-width: 760px)" in plate_slice

    assert "Command Cockpit Cinematic Focus Plate" in readme
    assert "single mission plate" in readme


def test_command_cockpit_selected_node_expansion_console_adds_in_board_depth():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-selected-node-expansion-console" in index
    assert "20260619-command-cockpit-selected-node-expansion-console" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-selected-node-expansion-console" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questSelectedNodeExpansionRows(lane, data, cell, cards)" in app
    assert "function renderQuestSelectedNodeExpansionConsole(model)" in app
    assert "expansionRows: questSelectedNodeExpansionRows(lane, data, cell, cards)," in app
    assert "${renderQuestSelectedNodeExpansionConsole(cinematicFocus)}" in app
    assert 'class="quest-selected-node-expansion-console ${escapeHtml(model.tone)}"' in app
    assert 'data-quest-expansion-role="${escapeHtml(model.role)}"' in app
    assert 'class="quest-selected-node-expansion-row"' in app
    assert 'label: "Timeline"' in app
    assert 'label: "Blocker"' in app
    assert 'label: "Proof"' in app
    assert 'label: "Next"' in app

    marker = "/* 20260619-command-cockpit-selected-node-expansion-console */"
    assert marker in styles
    expansion_slice = styles[styles.index(marker):]
    assert ".quest-selected-node-expansion-console" in expansion_slice
    assert ".quest-selected-node-expansion-console::before" in expansion_slice
    assert ".quest-selected-node-expansion-row" in expansion_slice
    assert "right: 12px;" in expansion_slice
    assert "bottom: 13px;" in expansion_slice
    assert "width: 332px;" in expansion_slice
    assert ".quest-selected-node-expansion-console ~ .quest-run-spine" in expansion_slice
    assert "display: none !important;" in expansion_slice
    assert "@keyframes questSelectedNodeExpansionSweep" in expansion_slice
    assert "@media (max-width: 760px)" in expansion_slice
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in expansion_slice

    assert "Command Cockpit Selected Node Expansion Console" in readme
    assert "timeline, blocker, proof, and next-move rows" in readme


def test_command_cockpit_selected_node_expansion_actions_open_deep_views():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-selected-node-expansion-actions" in index
    assert "20260619-command-cockpit-selected-node-expansion-actions" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-selected-node-expansion-actions" in index.split('<script src="./app.js?v=', 1)[1]

    assert 'view: "trail"' in app
    assert 'view: "path"' in app
    assert 'view: "comms"' in app
    assert '<button class="quest-selected-node-expansion-row"' in app
    assert 'type="button" data-expansion-tone="${escapeHtml(row.tone)}"' in app
    assert 'data-detail-view="${escapeHtml(row.view)}"' in app
    assert 'data-quest-expansion-action="${escapeHtml(row.label.toLowerCase())}"' in app
    assert 'aria-label="Open ${escapeHtml(row.label)} for ${escapeHtml(model.title)}"' in app

    marker = "/* 20260619-command-cockpit-selected-node-expansion-actions */"
    assert marker in styles
    actions_slice = styles[styles.index(marker):]
    assert "pointer-events: auto;" in actions_slice
    assert "appearance: none;" in actions_slice
    assert "cursor: pointer;" in actions_slice
    assert ".quest-selected-node-expansion-row:hover" in actions_slice
    assert ".quest-selected-node-expansion-row:focus-visible" in actions_slice
    assert "@media (prefers-reduced-motion: reduce)" in actions_slice

    assert "Command Cockpit Selected Node Expansion Actions" in readme
    assert "drill-in controls" in readme


def test_command_cockpit_selected_node_lens_tray_keeps_drilldown_in_board():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-selected-node-lens-tray" in index
    assert "20260619-command-cockpit-selected-node-lens-tray" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-selected-node-lens-tray" in index.split('<script src="./app.js?v=', 1)[1]
    assert "20260619-command-cockpit-selected-node-lens-tray-layer" in index
    assert "20260619-command-cockpit-selected-node-lens-tray-mobile-fit" in index

    assert "questExpansionLensByLane: {}" in app
    assert "function renderQuestSelectedNodeLensTray(model)" in app
    assert "const activeExpansionLens = state.questExpansionLensByLane[lane.id] ?? \"timeline\";" in app
    assert "lensRows: cinematicFocus.expansionRows," in app
    assert "activeLens: activeExpansionLens," in app
    assert "${renderQuestSelectedNodeLensTray(cinematicFocus)}" in app
    assert 'class="quest-selected-node-lens-tray ${escapeHtml(model.tone)}"' in app
    assert 'data-quest-active-lens="${escapeHtml(activeRow.label.toLowerCase())}"' in app
    assert 'data-detail-view="${escapeHtml(activeRow.view)}"' in app
    assert 'data-quest-expansion-lens="${escapeHtml(row.label.toLowerCase())}"' in app

    handler_slice = app[app.index('const questExpansionLens = event.target.closest("[data-quest-expansion-lens]");'):]
    assert "state.questExpansionLensByLane = { ...state.questExpansionLensByLane" in handler_slice
    assert "renderDetail();" in handler_slice
    assert "return;" in handler_slice.split('const viewButton = event.target.closest("[data-detail-view]");', 1)[0]

    marker = "/* 20260619-command-cockpit-selected-node-lens-tray */"
    assert marker in styles
    lens_slice = styles[styles.index(marker):]
    assert ".quest-selected-node-lens-tray" in lens_slice
    assert "grid-template-columns: minmax(0, 1fr) auto;" in lens_slice
    assert "pointer-events: auto;" in lens_slice
    assert "z-index: 18;" in lens_slice
    assert "@keyframes questSelectedNodeLensEnter" in lens_slice
    assert "@media (max-width: 760px)" in lens_slice
    assert "top: 64px;" in lens_slice

    assert "Command Cockpit Selected Node Lens Tray" in readme
    assert "keeps the first drilldown inside the board" in readme


def test_command_cockpit_selected_node_lens_depth_cards_expand_context_locally():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-selected-node-lens-depth-cards" in index
    assert "20260619-command-cockpit-selected-node-lens-depth-cards" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-selected-node-lens-depth-cards" in index.split('<script src="./app.js?v=', 1)[1]
    assert "20260619-command-cockpit-selected-node-lens-depth-mobile-fit" in index

    assert "function questSelectedNodeLensDepthCards(lane, data, activeLens, gateTitle, gateBody)" in app
    assert "lensDepthCards: questSelectedNodeLensDepthCards(lane, data, activeExpansionLens, gateTitle, gateBody)," in app
    assert "const depthCards = model.lensDepthCards ?? [];" in app
    assert 'class="quest-selected-node-lens-depth"' in app
    assert 'class="quest-selected-node-lens-card"' in app
    assert 'data-lens-card-tone="${escapeHtml(card.tone)}"' in app
    assert 'data-lens-card-kind="${escapeHtml(card.kind)}"' in app
    assert 'Timeline' in app
    assert 'Blocker' in app
    assert 'Proof' in app
    assert 'Next' in app

    marker = "/* 20260619-command-cockpit-selected-node-lens-depth-cards */"
    assert marker in styles
    depth_slice = styles[styles.index(marker):]
    assert ".quest-selected-node-lens-depth" in depth_slice
    assert "grid-template-columns: repeat(3, minmax(0, 1fr));" in depth_slice
    assert ".quest-selected-node-lens-card" in depth_slice
    assert "animation: questSelectedNodeLensCardIn" in depth_slice
    assert "@keyframes questSelectedNodeLensCardIn" in depth_slice
    assert "@media (max-width: 760px)" in depth_slice
    assert "top: 64px;" in depth_slice

    assert "Command Cockpit Selected Node Lens Depth Cards" in readme
    assert "three compact depth cards" in readme


def test_command_cockpit_selected_node_lens_reactor_energizes_local_dossier():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-selected-node-lens-reactor" in index
    assert "20260619-command-cockpit-selected-node-lens-reactor" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-selected-node-lens-reactor" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestSelectedNodeLensReactor(activeRow, depthCards)" in app
    assert "${renderQuestSelectedNodeLensReactor(activeRow, depthCards)}" in app
    assert 'class="quest-selected-node-lens-reactor"' in app
    assert 'data-lens-reactor="${escapeHtml(activeRow.label.toLowerCase())}"' in app
    assert 'class="quest-selected-node-lens-rail"' in app
    assert 'class="quest-selected-node-lens-pip"' in app
    assert 'data-lens-pip-tone="${escapeHtml(card.tone)}"' in app

    marker = "/* 20260619-command-cockpit-selected-node-lens-reactor */"
    assert marker in styles
    reactor_slice = styles[styles.index(marker):]
    assert ".quest-selected-node-lens-reactor" in reactor_slice
    assert "pointer-events: none;" in reactor_slice
    assert ".quest-selected-node-lens-rail" in reactor_slice
    assert ".quest-selected-node-lens-pip" in reactor_slice
    assert "@keyframes questSelectedNodeLensRailFlow" in reactor_slice
    assert "@keyframes questSelectedNodeLensCorePulse" in reactor_slice
    assert "@media (prefers-reduced-motion: reduce)" in reactor_slice

    assert readme.count("Command Cockpit Selected Node Lens Depth Cards") == 1
    assert "Command Cockpit Selected Node Lens Reactor" in readme
    assert "active-lens reactor rail" in readme


def test_command_cockpit_cinematic_focus_tether_connects_node_to_plate():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-cinematic-focus-tether" in index
    assert "20260619-command-cockpit-cinematic-focus-tether" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-cinematic-focus-tether" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questCinematicFocusPlateModel(lane, data, cell, cards, focusIndex, focusCount, crew)" in app
    assert "focusIndex: Math.max(0, focusIndex)," in app
    assert "focusCount: Math.max(1, focusCount)," in app
    assert "questCinematicFocusPlateModel(lane, data, focusedCell, focusedDrillCards, focusedIndex, focusedFieldCells.length, crew)" in app
    assert "--quest-cinematic-lock-index:${model.focusIndex}; --quest-cinematic-lock-count:${model.focusCount};" in app

    marker = "/* 20260619-command-cockpit-cinematic-focus-tether */"
    assert marker in styles
    tether_slice = styles[styles.index(marker):]
    assert ".quest-cinematic-focus-plate::after" in tether_slice
    assert "--quest-cinematic-lock-x" in tether_slice
    assert "calc(((var(--quest-cinematic-lock-index) + 0.5) / var(--quest-cinematic-lock-count)) * 100%)" in tether_slice
    assert "@keyframes questCinematicTetherPulse" in tether_slice
    assert "animation: questCinematicTetherPulse 3.8s ease-in-out infinite;" in tether_slice
    assert "@media (max-width: 760px)" in tether_slice

    assert "Command Cockpit Cinematic Focus Tether" in readme
    assert "animated lock line" in readme


def test_command_cockpit_cinematic_bot_relay_keeps_comms_in_focus_plate():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-cinematic-bot-relay" in index
    assert "20260619-command-cockpit-cinematic-bot-relay" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-cinematic-bot-relay" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questCinematicFocusPlateModel(lane, data, cell, cards, focusIndex, focusCount, crew)" in app
    assert "botAvatar: crew ? agentAvatarMarkup(crew.agent, lane, \"quest-cinematic-bot-avatar\") : avatarMarkup(lane, \"quest-cinematic-bot-avatar\")," in app
    assert "botCallsign: crew?.callsign ?? lane.ownerAgentId ?? \"Unassigned\"," in app
    assert "botStatus: crew ? `${formatNumber(crew.readiness)}% ready` : \"open seat\"," in app
    assert "botSpecialty: crew?.specialty ?? lane.visual?.realm ?? \"bot socket\"," in app
    assert "const crew = questCrewRelayRecord(lane);" in app
    assert "questCinematicFocusPlateModel(lane, data, focusedCell, focusedDrillCards, focusedIndex, focusedFieldCells.length, crew)" in app
    assert 'class="quest-cinematic-bot-relay ${escapeHtml(model.botTone)}"' in app
    assert 'data-detail-view="comms"' in app
    assert "COM" in app

    marker = "/* 20260619-command-cockpit-cinematic-bot-relay */"
    assert marker in styles
    relay_slice = styles[styles.index(marker):]
    assert ".quest-cinematic-bot-relay" in relay_slice
    assert ".quest-cinematic-bot-avatar" in relay_slice
    assert "@keyframes questCinematicBotRelaySweep" in relay_slice
    assert "animation: questCinematicBotRelaySweep 4.6s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in relay_slice
    assert "grid-template-columns: 48px minmax(0, 1fr) minmax(122px, 0.44fr) minmax(168px, 0.68fr);" in relay_slice
    assert "@media (max-width: 760px)" in relay_slice

    assert "Command Cockpit Cinematic Bot Relay" in readme
    assert "responsible bot" in readme


def test_command_cockpit_cinematic_reward_rail_surfaces_proof_and_unlocks():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-cinematic-reward-rail" in index
    assert "20260619-command-cockpit-cinematic-reward-rail" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-cinematic-reward-rail" in index.split('<script src="./app.js?v=', 1)[1]

    assert 'const proof = byLabel.get("Proof");' in app
    assert 'const milestone = byLabel.get("Milestone");' in app
    assert 'rewardProof: proof?.value ?? "0 proof",' in app
    assert 'rewardMilestone: milestone?.value ?? `${formatNumber(data.checkpointProgress)}% quest`,' in app
    assert 'class="quest-cinematic-reward-rail"' in app
    assert 'aria-label="Selected node proof and unlock progress"' in app
    assert "<em>Proof</em>" in app
    assert "<em>Unlock</em>" in app

    marker = "/* 20260619-command-cockpit-cinematic-reward-rail */"
    assert marker in styles
    reward_slice = styles[styles.index(marker):]
    assert ".quest-cinematic-reward-rail" in reward_slice
    assert "@keyframes questCinematicRewardPulse" in reward_slice
    assert "animation: questCinematicRewardPulse 3.6s ease-in-out infinite;" in reward_slice
    assert "@media (max-width: 760px)" in reward_slice

    assert "Command Cockpit Cinematic Reward Rail" in readme
    assert "proof and unlock" in readme


def test_command_cockpit_cinematic_event_heartbeat_surfaces_recent_activity():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-cinematic-event-heartbeat" in index
    assert "20260619-command-cockpit-cinematic-event-heartbeat" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-cinematic-event-heartbeat" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questCinematicHeartbeatPackets(lane, data, cell)" in app
    assert "questEventPulsePackets(lane, data, cell)" in app
    assert "eventHeartbeat: questCinematicHeartbeatPackets(lane, data, cell)," in app
    assert 'class="quest-cinematic-event-heartbeat"' in app
    assert 'aria-label="Selected node recent activity heartbeat"' in app
    assert 'data-heartbeat-tone="${escapeHtml(packet.tone)}"' in app
    assert "--heartbeat-index:${index}" in app
    assert "--heartbeat-delay:${packet.delay}ms" in app

    marker = "/* 20260619-command-cockpit-cinematic-event-heartbeat */"
    assert marker in styles
    heartbeat_slice = styles[styles.index(marker):]
    assert ".quest-cinematic-event-heartbeat" in heartbeat_slice
    assert "@keyframes questCinematicHeartbeatTravel" in heartbeat_slice
    assert "animation: questCinematicHeartbeatTravel 4.2s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in heartbeat_slice
    assert "@media (max-width: 760px)" in heartbeat_slice

    assert "Command Cockpit Cinematic Event Heartbeat" in readme
    assert "recent activity" in readme


def test_command_cockpit_cinematic_action_sockets_make_focus_plate_operational():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-cinematic-action-sockets" in index
    assert "20260619-command-cockpit-cinematic-action-sockets" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-cinematic-action-sockets" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function questCinematicActionSockets()" in app
    assert 'view: "path", label: "Path", icon: "map"' in app
    assert 'view: "trail", label: "Trail", icon: "trail"' in app
    assert 'view: "game", label: "Game", icon: "game"' in app
    assert 'view: "comms", label: "Comms", icon: "comms"' in app
    assert 'class="quest-cinematic-action-sockets"' in app
    assert 'aria-label="Selected node quick view sockets"' in app
    assert 'data-detail-view="${escapeHtml(socket.view)}"' in app
    assert 'data-action-icon="${escapeHtml(socket.icon)}"' in app
    assert "${questCinematicActionSockets()}" in app

    marker = "/* 20260619-command-cockpit-cinematic-action-sockets */"
    assert marker in styles
    socket_slice = styles[styles.index(marker):]
    assert ".quest-cinematic-action-sockets" in socket_slice
    assert ".quest-cinematic-action-socket" in socket_slice
    assert ".quest-action-icon" in socket_slice
    assert "@keyframes questCinematicActionSocketPulse" in socket_slice
    assert "animation: questCinematicActionSocketPulse 3.9s ease-in-out infinite;" in socket_slice
    assert "@media (max-width: 760px)" in socket_slice

    assert "Command Cockpit Cinematic Action Sockets" in readme
    assert "Path, Trail, Game, and Comms" in readme


def test_command_cockpit_secondary_action_dock_yields_to_focus_plate_sockets():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-secondary-action-dock" in index
    assert "20260619-command-cockpit-secondary-action-dock" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-secondary-action-dock" in index.split('<script src="./app.js?v=', 1)[1]

    assert 'priority: "plate"' in app
    assert 'priority: "archive"' in app
    assert 'class="quest-action-row" data-quest-dock-density="secondary"' in app
    assert 'data-quest-action-priority="${escapeHtml(action.priority)}"' in app

    marker = "/* 20260619-command-cockpit-secondary-action-dock */"
    assert marker in styles
    dock_slice = styles[styles.index(marker):]
    assert '.quest-action-row[data-quest-dock-density="secondary"]' in dock_slice
    assert 'grid-template-columns: repeat(5, 24px);' in dock_slice
    assert 'min-height: 0;' in dock_slice
    assert 'opacity: 0.68;' in dock_slice
    assert 'animation: questSecondaryActionDockBreathe 5.6s ease-in-out infinite;' in dock_slice
    assert '@keyframes questSecondaryActionDockBreathe' in dock_slice
    assert 'data-quest-action-priority="plate"' in dock_slice
    assert '@media (max-width: 760px)' in dock_slice

    assert "Command Cockpit Secondary Action Dock" in readme
    assert "fallback rail" in readme


def test_command_cockpit_board_signal_overlay_moves_status_into_game_surface():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-board-signal-overlay" in index
    assert "20260619-command-cockpit-board-signal-overlay" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-board-signal-overlay" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestBoardSignalOverlay(signals)" in app
    assert 'class="quest-board-signal-overlay"' in app
    assert 'aria-label="Quest board score and pressure overlay"' in app
    assert 'data-quest-board-signal-state="${escapeHtml(signal.state)}"' in app
    assert "--board-signal-index:${index}" in app
    assert "${renderQuestBoardSignalOverlay(signals)}" in app
    assert 'class="quest-signal-row" data-quest-signal-density="ghost"' in app

    marker = "/* 20260619-command-cockpit-board-signal-overlay */"
    assert marker in styles
    overlay_slice = styles[styles.index(marker):]
    assert ".quest-board-signal-overlay" in overlay_slice
    assert ".quest-board-signal-chip" in overlay_slice
    assert 'data-quest-signal-density="ghost"' in overlay_slice
    assert "height: 0;" in overlay_slice
    assert "opacity: 0;" in overlay_slice
    assert "animation: questBoardSignalOverlayPulse 4.8s ease-in-out infinite;" in overlay_slice
    assert "@keyframes questBoardSignalOverlayPulse" in overlay_slice
    assert "@media (max-width: 760px)" in overlay_slice

    assert "Command Cockpit Board Signal Overlay" in readme
    assert "moves asks, unlocks, events, and score into the Quest board" in readme


def test_command_cockpit_board_identity_cartridge_moves_hero_into_game_surface():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-board-identity-cartridge" in index
    assert "20260619-command-cockpit-board-identity-cartridge" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-board-identity-cartridge" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestBoardIdentityCartridge(lane, data, minigameSigil)" in app
    assert 'class="quest-board-identity-cartridge"' in app
    assert 'aria-label="Quest board lane identity cartridge"' in app
    assert 'class="quest-board-identity-avatar"' in app
    assert 'class="quest-board-identity-copy"' in app
    assert 'class="quest-board-identity-meter"' in app
    assert 'data-quest-hero-density="ghost"' in app
    assert "${renderQuestBoardIdentityCartridge(lane, data, minigameSigil)}" in app

    marker = "/* 20260619-command-cockpit-board-identity-cartridge */"
    assert marker in styles
    cartridge_slice = styles[styles.index(marker):]
    assert ".quest-board-identity-cartridge" in cartridge_slice
    assert ".quest-board-identity-avatar" in cartridge_slice
    assert ".quest-board-identity-copy" in cartridge_slice
    assert ".quest-board-identity-meter" in cartridge_slice
    assert '.quest-cockpit-hero[data-quest-hero-density="ghost"]' in cartridge_slice
    assert "height: 0;" in cartridge_slice
    assert "opacity: 0;" in cartridge_slice
    assert "animation: questBoardIdentityCartridgeBreathe 5.2s ease-in-out infinite;" in cartridge_slice
    assert "@keyframes questBoardIdentityCartridgeBreathe" in cartridge_slice
    assert "@media (max-width: 760px)" in cartridge_slice

    assert "Command Cockpit Board Identity Cartridge" in readme
    assert "moves lane identity and quest progress into the Quest board" in readme


def test_command_cockpit_ambient_overlay_hierarchy_quiets_legacy_board_chrome():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-ambient-overlay-hierarchy" in index
    assert "20260619-command-cockpit-ambient-overlay-hierarchy" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-ambient-overlay-hierarchy" in index.split('<script src="./app.js?v=', 1)[1]

    assert 'data-quest-overlay-density="ambient-realm"' in app
    assert 'data-quest-overlay-density="ambient-crew"' in app
    assert 'data-quest-overlay-density="ambient-unlock"' in app
    assert 'class="quest-board-identity-cartridge"' in app
    assert 'class="quest-cinematic-focus-plate ' in app

    marker = "/* 20260619-command-cockpit-ambient-overlay-hierarchy */"
    assert marker in styles
    hierarchy_slice = styles[styles.index(marker):]
    assert '.quest-realm-skin-cartridge[data-quest-overlay-density="ambient-realm"]' in hierarchy_slice
    assert '.quest-crew-presence-dock[data-quest-overlay-density="ambient-crew"]' in hierarchy_slice
    assert '.quest-unlock-ladder[data-quest-overlay-density="ambient-unlock"]' in hierarchy_slice
    assert "opacity: 0.46;" in hierarchy_slice
    assert "filter: saturate(0.72) contrast(0.92);" in hierarchy_slice
    assert "z-index: 9;" in hierarchy_slice
    assert "animation-duration: 11s;" in hierarchy_slice
    assert "opacity: 0.9;" in hierarchy_slice
    assert "@media (max-width: 760px)" in hierarchy_slice

    assert "Command Cockpit Ambient Overlay Hierarchy" in readme
    assert "quiets older realm, crew, and unlock overlays" in readme


def test_command_cockpit_spotlight_node_hierarchy_turns_unselected_nodes_into_map_pips():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-spotlight-node-hierarchy" in index
    assert "20260619-command-cockpit-spotlight-node-hierarchy" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-spotlight-node-hierarchy" in index.split('<script src="./app.js?v=', 1)[1]

    assert 'data-quest-board-focus-mode="spotlight"' in app
    assert 'data-quest-clarity-mode="focus"' in app
    assert 'data-quest-focused="${cell.focused ? "true" : "false"}"' in app

    marker = "/* 20260619-command-cockpit-spotlight-node-hierarchy */"
    assert marker in styles
    spotlight_slice = styles[styles.index(marker):]
    assert '.quest-field[data-quest-board-focus-mode="spotlight"]' in spotlight_slice
    assert '.quest-field-cell:not([data-quest-focused="true"])' in spotlight_slice
    assert "opacity: 0.18;" in spotlight_slice
    assert "filter: saturate(0.46) blur(0.1px);" in spotlight_slice
    assert "height: 42px;" in spotlight_slice
    assert "align-self: center;" in spotlight_slice
    assert "transform: translateY(0) scale(0.78);" in spotlight_slice
    assert ".quest-field-cell:not([data-quest-focused=\"true\"]) span" in spotlight_slice
    assert ".quest-field-cell:not([data-quest-focused=\"true\"]) strong" in spotlight_slice
    assert ".quest-field-cell:not([data-quest-focused=\"true\"]) em" in spotlight_slice
    assert "opacity: 0;" in spotlight_slice
    assert ".quest-field-cell[data-quest-focused=\"true\"]" in spotlight_slice
    assert "height: 72px;" in spotlight_slice
    assert "z-index: 14;" in spotlight_slice
    assert "animation: questSpotlightNodePulse 3.8s ease-in-out infinite;" in spotlight_slice
    assert "@keyframes questSpotlightNodePulse" in spotlight_slice
    assert "@media (max-width: 760px)" in spotlight_slice

    assert "Command Cockpit Spotlight Node Hierarchy" in readme
    assert "turns unselected Quest nodes into quiet map pips" in readme


def test_command_cockpit_spotlight_camera_aperture_locks_selected_node():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-spotlight-camera-aperture" in index
    assert "20260619-command-cockpit-spotlight-camera-aperture" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-spotlight-camera-aperture" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function renderQuestSpotlightCameraAperture(cell, index, count)" in app
    assert 'class="quest-spotlight-camera-aperture"' in app
    assert 'data-quest-aperture-role="${escapeHtml(cell?.role ?? "checkpoint")}"' in app
    assert "--quest-aperture-x:${focusX.toFixed(2)}%;" in app
    assert "${renderQuestSpotlightCameraAperture(focusedCell, focusedIndex, focusedFieldCells.length)}" in app

    marker = "/* 20260619-command-cockpit-spotlight-camera-aperture */"
    assert marker in styles
    aperture_slice = styles[styles.index(marker):]
    assert ".quest-spotlight-camera-aperture" in aperture_slice
    assert "pointer-events: none;" in aperture_slice
    assert "left: clamp(18px, var(--quest-aperture-x, 50%), calc(100% - 18px));" in aperture_slice
    assert "animation: questSpotlightApertureBreathe 5.8s ease-in-out infinite;" in aperture_slice
    assert "@keyframes questSpotlightApertureBreathe" in aperture_slice
    assert "@keyframes questSpotlightApertureSweep" in aperture_slice
    assert "@media (max-width: 760px)" in aperture_slice

    assert "Command Cockpit Spotlight Camera Aperture" in readme
    assert "adds a subtle camera-lock aperture over the selected Quest node" in readme


def test_command_cockpit_mobile_footer_layering_quiets_echo_rail_under_run_spine():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mobile-footer-layering" in index
    assert "20260619-command-cockpit-mobile-footer-layering" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260619-command-cockpit-mobile-footer-layering" in index.split('<script src="./app.js?v=', 1)[1]

    marker = "/* 20260619-command-cockpit-mobile-footer-layering */"
    assert marker in styles
    footer_slice = styles[styles.index(marker):]
    assert "@media (max-width: 760px)" in footer_slice
    assert ".quest-node-echo-rail" in footer_slice
    assert ".quest-action-row" in footer_slice
    assert "opacity: 0 !important;" in footer_slice
    assert "visibility: hidden;" in footer_slice
    assert "pointer-events: none;" in footer_slice
    assert "transform: translateY(8px) scale(0.94);" in footer_slice
    assert ".quest-run-spine" in footer_slice
    assert "z-index: 26;" in footer_slice

    assert "Command Cockpit Mobile Footer Layering" in readme
    assert "lets the mobile Run Spine own the bottom Proof/Gate/Next band" in readme
    assert "older fallback action dock recede" in readme


def test_command_cockpit_lane_world_signal_makes_rail_feel_expandable():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-lane-world-signal" in index
    assert "20260619-command-cockpit-lane-unlock-lens" in index
    assert "20260619-command-cockpit-lane-unlock-lens" in index.split('href="./styles.css?v=', 1)[1]
    assert "function laneRailWorldSignalMarkup(" in app
    assert "function laneRailUnlockLensMarkup(" in app
    assert "${laneRailWorldSignalMarkup(lane, index, lanes.length)}" in app
    assert "${laneRailUnlockLensMarkup(lane)}" in app
    assert "data-lane-world-signal" in app
    assert "minigameDefinition(lane)" in app
    assert "minigame.id ?? lane.id" in app
    assert 'custom ? "play" : "seed"' in app
    assert 'class="lane-unlock-lens' in app
    assert "gameStepCount(lane)" in app
    assert "--lane-unlock-ready" in app
    assert 'custom ? "GAME" : "SEED"' in app

    marker = "/* 20260619-command-cockpit-lane-world-signal */"
    assert marker in styles
    signal_start = styles.index(marker)
    signal_end = styles.index("/* 20260619-command-cockpit-low-scroll-premium-pass */", signal_start)
    signal_slice = styles[signal_start:signal_end]
    assert ".lane-world-signal" in signal_slice
    assert "@keyframes laneWorldSignalSweep" in signal_slice
    assert "pointer-events: none;" in signal_slice
    assert "var(--game-texture)" in signal_slice
    assert "/* 20260619-command-cockpit-lane-unlock-lens */" in styles
    lens_slice = styles[styles.index("/* 20260619-command-cockpit-lane-unlock-lens */"):signal_start]
    assert ".lane-unlock-lens" in lens_slice
    assert "--lane-unlock-ready" in lens_slice
    assert "@keyframes laneUnlockLensSweep" in lens_slice

    cockpit_start = styles.index("/* 20260619-command-cockpit-low-scroll-premium-pass */")
    cockpit_slice = styles[cockpit_start:]
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-world-signal' in cockpit_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-world-signal em' in cockpit_slice
    assert "display: none;" in cockpit_slice
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button-top' in cockpit_slice
    assert "padding-right: 52px;" in styles
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-unlock-lens' in styles
    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-unlock-lens em' in styles

    assert "Command Cockpit Lane World Signal" in readme
    assert "future lane slots read as playable worlds" in readme
    assert "Command Cockpit Lane Unlock Lens" in readme
    assert "GAME/SEED state, stage count, gate pressure, and readiness fill" in readme
