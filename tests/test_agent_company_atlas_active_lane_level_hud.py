from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_active_lane_level_hud_stays_visible_above_compact_lane_views():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function renderActiveLaneLevelHud" in app
    assert "${renderActiveLaneLevelHud(lane)}" in app
    assert 'class="active-lane-level-hud"' in app
    assert 'class="active-lane-hud-meter"' in app
    assert 'class="active-lane-hud-track"' in app
    assert 'class="active-lane-hud-bot"' in app

    hud_start = styles.index(".active-lane-level-hud")
    hud_end = styles.index("@keyframes activeLaneHudSweep", hud_start)
    hud_slice = styles[hud_start:hud_end]
    assert "grid-template-columns: minmax(220px, 0.84fr) minmax(260px, 1fr) minmax(190px, 0.72fr);" in hud_slice
    assert "min-height: 118px;" in hud_slice
    assert "overflow: hidden;" in hud_slice
    assert ".active-lane-hud-track" in hud_slice
    assert ".active-lane-hud-bot" in hud_slice
    assert ".active-lane-hud-next" in hud_slice
    assert "animation: activeLaneHudSweep 5.8s ease-in-out infinite;" in hud_slice

    compact_start = styles.index(".detail-content .detail-top")
    compact_end = styles.index(".active-lane-level-hud", compact_start)
    compact_slice = styles[compact_start:compact_end]
    assert ".detail-content .detail-tabs" in compact_slice
    assert "display: none;" in compact_slice
    assert ".active-lane-level-hud" not in compact_slice

    assert "Active Lane Level HUD" in readme
    assert "20260619-active-lane-level-hud" in index


def test_command_cockpit_compresses_active_lane_hud_into_status_bar():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-hud-compression" in index

    hud_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-level-hud')
    hud_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-core',
        hud_start,
    )
    hud_slice = styles[hud_start:hud_end]
    assert "grid-template-columns: minmax(180px, 0.74fr) minmax(220px, 1fr) minmax(158px, 0.58fr);" in hud_slice
    assert "min-height: 96px;" in hud_slice
    assert "margin-bottom: 8px;" in hud_slice
    assert "padding: 8px;" in hud_slice

    core_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-core')
    core_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-avatar',
        core_start,
    )
    core_slice = styles[core_start:core_end]
    assert "grid-template-columns: 46px minmax(0, 1fr) 46px;" in core_slice
    assert "padding: 7px;" in core_slice

    avatar_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-avatar')
    avatar_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-title em',
        avatar_start,
    )
    avatar_slice = styles[avatar_start:avatar_end]
    assert "width: 46px;" in avatar_slice
    assert "height: 46px;" in avatar_slice

    hidden_copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-title em')
    hidden_copy_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-track',
        hidden_copy_start,
    )
    hidden_copy_slice = styles[hidden_copy_start:hidden_copy_end]
    assert "display: none;" in hidden_copy_slice
    assert ".active-lane-hud-next em" in hidden_copy_slice

    track_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-track')
    track_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-bot',
        track_start,
    )
    track_slice = styles[track_start:track_end]
    assert "padding: 7px;" in track_slice
    assert "min-height: 58px;" in track_slice

    assert "Command Cockpit HUD Compression" in readme


def test_command_cockpit_mobile_hud_becomes_compact_status_strip():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mobile-hud-strip" in index

    mobile_start = styles.index("@media (max-width: 860px)")

    hud_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-level-hud',
        mobile_start,
    )
    hud_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-core',
        hud_start,
    )
    hud_slice = styles[hud_start:hud_end]
    assert "grid-template-columns: 1fr;" in hud_slice
    assert "gap: 4px;" in hud_slice
    assert "padding: 4px;" in hud_slice
    assert "overflow: hidden;" in hud_slice

    core_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-core',
        hud_start,
    )
    core_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-avatar',
        core_start,
    )
    core_slice = styles[core_start:core_end]
    assert "grid-template-columns: 38px minmax(0, 1fr) 38px;" in core_slice
    assert "min-height: 46px;" in core_slice
    assert "padding: 4px;" in core_slice

    avatar_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-avatar',
        core_start,
    )
    avatar_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-track',
        avatar_start,
    )
    avatar_slice = styles[avatar_start:avatar_end]
    assert "width: 38px;" in avatar_slice
    assert "height: 38px;" in avatar_slice

    track_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-track',
        avatar_start,
    )
    track_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-signal',
        track_start,
    )
    track_slice = styles[track_start:track_end]
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in track_slice
    assert "gap: 3px;" in track_slice
    assert "padding: 3px;" in track_slice
    assert "overflow: hidden;" in track_slice

    signal_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-signal',
        track_start,
    )
    signal_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-bot',
        signal_start,
    )
    signal_slice = styles[signal_start:signal_end]
    assert "min-height: 22px;" in signal_slice
    assert "padding: 2px 3px;" in signal_slice
    assert ".active-lane-hud-signal span" in signal_slice
    assert "display: none;" in signal_slice

    bot_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-bot',
        signal_start,
    )
    bot_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-bot-avatar',
        bot_start,
    )
    bot_slice = styles[bot_start:bot_end]
    assert "grid-template-columns: 30px minmax(0, 1fr);" in bot_slice
    assert "min-height: 36px;" in bot_slice
    assert "padding: 4px;" in bot_slice

    bot_avatar_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-bot-avatar',
        bot_start,
    )
    bot_avatar_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-next',
        bot_avatar_start,
    )
    bot_avatar_slice = styles[bot_avatar_start:bot_avatar_end]
    assert "width: 30px;" in bot_avatar_slice
    assert "height: 30px;" in bot_avatar_slice

    next_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-next',
        bot_avatar_start,
    )
    arena_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-hud-arena',
        next_start,
    )
    assert "display: none;" in styles[next_start:arena_start]

    matrix_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix',
        arena_start,
    )
    matrix_end = styles.index(
        "body[data-detail-view=\"game\"]",
        matrix_start,
    )
    strip_slice = styles[arena_start:matrix_end]
    assert "display: none;" in strip_slice
    assert "Command Cockpit Mobile HUD Strip" in readme


def test_active_lane_level_hud_has_compact_animated_arena_band():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneArenaNodes" in app
    assert "const arenaNodes = activeLaneArenaNodes(lane, trail, phase, blockerPressure);" in app
    assert 'class="active-lane-hud-arena"' in app
    assert 'class="active-lane-hud-route"' in app
    assert 'class="active-lane-hud-runner"' in app
    assert 'class="active-lane-hud-node' in app

    arena_start = styles.index(".active-lane-hud-arena")
    arena_end = styles.index("@keyframes activeLaneHudSweep", arena_start)
    arena_slice = styles[arena_start:arena_end]
    assert ".active-lane-level-hud" in arena_slice
    assert "grid-column: 1 / -1;" in arena_slice
    assert "min-height: 34px;" in arena_slice
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in arena_slice
    assert ".active-lane-hud-runner" in arena_slice
    assert "animation: activeLaneRunner 4.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in arena_slice
    assert ".active-lane-hud-node::after" in arena_slice
    assert "animation: activeLaneNodePulse 2.8s ease-in-out infinite;" in arena_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-hud-arena" in mobile_slice
    assert "min-height: 30px;" in mobile_slice

    assert "@keyframes activeLaneRunner" in styles
    assert "@keyframes activeLaneNodePulse" in styles
    assert "Active Lane Arena Band" in readme
    assert "20260619-active-lane-arena-band" in index


def test_active_lane_level_hud_has_premium_depth_field_motion():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneHudSparks" in app
    assert "const sparks = activeLaneHudSparks(lane, blockerPressure);" in app
    assert 'class="active-lane-hud-depth-field"' in app
    assert 'class="active-lane-hud-spark"' in app
    assert "--spark-x" in app
    assert "--spark-delay" in app

    depth_start = styles.index(".active-lane-hud-depth-field")
    depth_end = styles.index("@keyframes activeLaneHudSweep", depth_start)
    depth_slice = styles[depth_start:depth_end]
    assert "position: absolute;" in depth_slice
    assert "pointer-events: none;" in depth_slice
    assert "animation: activeLaneDepthPan 9.6s ease-in-out infinite;" in depth_slice
    assert ".active-lane-hud-spark" in depth_slice
    assert "animation: activeLaneSparkDrift 5.4s ease-in-out infinite;" in depth_slice
    assert "transform: translate3d(var(--spark-x), var(--spark-y), 0)" in depth_slice

    assert "@keyframes activeLaneDepthPan" in styles
    assert "@keyframes activeLaneSparkDrift" in styles
    assert "Active Lane Depth Field" in readme
    assert "20260619-active-lane-depth-field" in index


def test_active_lane_level_hud_has_compact_lane_switch_deck():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneSwitchRecords" in app
    assert "const switchRecords = activeLaneSwitchRecords(lane);" in app
    assert 'class="active-lane-switch-deck"' in app
    assert 'class="active-lane-switch-chip' in app
    assert 'data-lane-id="${escapeHtml(record.id)}"' in app
    assert 'aria-pressed="${record.id === lane.id ? "true" : "false"}"' in app

    switch_start = styles.index(".active-lane-switch-deck")
    switch_end = styles.index("@keyframes activeLaneHudSweep", switch_start)
    switch_slice = styles[switch_start:switch_end]
    assert "grid-column: 1 / -1;" in switch_slice
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in switch_slice
    assert "min-height: 38px;" in switch_slice
    assert ".active-lane-switch-chip" in switch_slice
    assert ".active-lane-switch-chip.active" in switch_slice
    assert "animation: activeLaneSwitchPulse 3.6s ease-in-out infinite;" in switch_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-switch-deck" in mobile_slice
    assert "grid-auto-flow: column;" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice

    assert "@keyframes activeLaneSwitchPulse" in styles
    assert "Active Lane Switch Deck" in readme
    assert "20260619-active-lane-switch-deck" in index


def test_active_lane_level_hud_has_micro_chronicle_cards():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneMicroChronicleCards" in app
    assert "const microChronicleCards = activeLaneMicroChronicleCards(lane, trail, nextAction);" in app
    assert 'class="active-lane-micro-chronicle"' in app
    assert 'class="active-lane-micro-card' in app
    assert 'data-micro-tone="${escapeHtml(card.tone)}"' in app

    micro_start = styles.index(".active-lane-micro-chronicle")
    micro_end = styles.index("@keyframes activeLaneHudSweep", micro_start)
    micro_slice = styles[micro_start:micro_end]
    assert "grid-column: 1 / -1;" in micro_slice
    assert "grid-template-columns: repeat(3, minmax(0, 1fr));" in micro_slice
    assert "min-height: 64px;" in micro_slice
    assert ".active-lane-micro-card" in micro_slice
    assert ".active-lane-micro-card::before" in micro_slice
    assert "animation: activeLaneMicroGlow 4.2s ease-in-out infinite;" in micro_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-micro-chronicle" in mobile_slice
    assert "grid-template-columns: 1fr;" in mobile_slice
    assert "min-height: 0;" in mobile_slice

    assert "@keyframes activeLaneMicroGlow" in styles
    assert "Active Lane Micro Chronicle" in readme
    assert "20260619-active-lane-micro-chronicle" in index


def test_active_lane_level_hud_has_always_visible_view_portal_dock():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneViewPortalRecords" in app
    assert "const viewPortals = activeLaneViewPortalRecords(lane);" in app
    assert 'class="active-lane-view-portals"' in app
    assert 'class="active-lane-view-portal' in app
    assert 'data-detail-view="${escapeHtml(portal.id)}"' in app
    assert 'aria-pressed="${state.detailView === portal.id ? "true" : "false"}"' in app

    portal_start = styles.index(".active-lane-view-portals")
    portal_end = styles.index("@keyframes activeLaneHudSweep", portal_start)
    portal_slice = styles[portal_start:portal_end]
    assert "grid-column: 1 / -1;" in portal_slice
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in portal_slice
    assert "min-height: 34px;" in portal_slice
    assert ".active-lane-view-portal" in portal_slice
    assert ".active-lane-view-portal.active" in portal_slice
    assert "animation: activeLanePortalTrace 4.4s ease-in-out infinite;" in portal_slice

    hidden_tabs_start = styles.index(".detail-content .detail-tabs")
    hidden_tabs_slice = styles[hidden_tabs_start : hidden_tabs_start + 240]
    assert "display: none;" in hidden_tabs_slice
    assert ".active-lane-view-portals" not in hidden_tabs_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-view-portals" in mobile_slice
    assert "grid-auto-flow: column;" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice

    assert "@keyframes activeLanePortalTrace" in styles
    assert "Active Lane View Portal Dock" in readme
    assert "20260619-active-lane-view-portal-dock" in index


def test_active_lane_legacy_chrome_is_collapsed_for_every_mounted_view():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    chrome_start = styles.index(".detail-content .detail-top")
    chrome_end = styles.index(".active-lane-level-hud", chrome_start)
    chrome_slice = styles[chrome_start:chrome_end]
    assert ".detail-content .detail-top" in chrome_slice
    assert ".detail-content .detail-tabs" in chrome_slice
    assert "display: none;" in chrome_slice

    assert "Active Lane Legacy Chrome Collapse" in readme
    assert "20260619-active-lane-legacy-chrome-collapse" in index


def test_active_lane_level_hud_has_view_transition_meter():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneViewTransition" in app
    assert "const viewTransition = activeLaneViewTransition(lane, viewPortals);" in app
    assert 'class="active-lane-view-transition"' in app
    assert 'class="active-lane-view-transition-runner"' in app
    assert '--view-step:${viewTransition.step}; --view-count:${viewTransition.count};' in app
    assert "${escapeHtml(viewTransition.label)}" in app

    transition_start = styles.index(".active-lane-view-transition")
    transition_end = styles.index("@keyframes activeLaneHudSweep", transition_start)
    transition_slice = styles[transition_start:transition_end]
    assert "grid-column: 1 / -1;" in transition_slice
    assert "min-height: 24px;" in transition_slice
    assert "grid-template-columns: minmax(78px, auto) minmax(0, 1fr) minmax(52px, auto);" in transition_slice
    assert ".active-lane-view-transition-track" in transition_slice
    assert ".active-lane-view-transition-runner" in transition_slice
    assert "left: calc((var(--view-step) / max(1, var(--view-count) - 1)) * 100%);" in transition_slice
    assert "animation: activeLaneViewRunner 4.6s ease-in-out infinite;" in transition_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-view-transition" in mobile_slice
    assert "grid-template-columns: minmax(64px, auto) minmax(0, 1fr) minmax(42px, auto);" in mobile_slice

    assert "@keyframes activeLaneViewRunner" in styles
    assert "Active Lane View Transition Meter" in readme
    assert "20260619-active-lane-view-transition-meter" in index


def test_selected_lane_body_is_bounded_inside_mounted_stage_frame():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert 'class="active-lane-mounted-stage"' in app
    assert 'data-active-stage-view="${escapeHtml(state.detailView)}"' in app
    assert 'class="active-lane-mounted-stage-scan"' in app
    assert "${renderDetailBody(lane)}" in app

    stage_start = styles.index(".active-lane-mounted-stage")
    stage_end = styles.index("@keyframes activeLaneHudSweep", stage_start)
    stage_slice = styles[stage_start:stage_end]
    assert "max-height: min(430px, calc(100vh - 300px));" in stage_slice
    assert "overflow-y: auto;" in stage_slice
    assert "scrollbar-gutter: stable;" in stage_slice
    assert ".active-lane-mounted-stage-scan" in stage_slice
    assert "animation: activeLaneMountedStageScan 6.2s ease-in-out infinite;" in stage_slice
    assert "animation: activeLaneMountedStageIn 260ms ease both;" in stage_slice

    compact_start = styles.index('body[data-atlas-deck="command"] .active-lane-mounted-stage')
    compact_slice = styles[compact_start : compact_start + 520]
    assert "max-height: min(360px, calc(100vh - 292px));" in compact_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-mounted-stage" in mobile_slice
    assert "max-height: min(420px, calc(100vh - 240px));" in mobile_slice

    assert "@keyframes activeLaneMountedStageScan" in styles
    assert "@keyframes activeLaneMountedStageIn" in styles
    assert "Active Lane Mounted Stage Frame" in readme
    assert "20260619-active-lane-mounted-stage-frame" in index


def test_command_cockpit_expands_mounted_lane_stage_after_chrome_compression():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-mounted-stage-expansion" in index

    stage_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage')
    stage_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage::after',
        stage_start,
    )
    stage_slice = styles[stage_start:stage_end]
    assert "flex: 1 1 auto;" in stage_slice
    assert "min-height: 0;" in stage_slice
    assert "max-height: none;" in stage_slice
    assert "padding: 6px;" in stage_slice

    fade_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage::after')
    fade_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage > .detail-section:first-of-type',
        fade_start,
    )
    fade_slice = styles[fade_start:fade_end]
    assert "height: 20px;" in fade_slice
    assert "margin: -20px -6px 0;" in fade_slice

    first_section_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage > .detail-section:first-of-type')
    first_section_end = styles.index("@media", first_section_start)
    first_section_slice = styles[first_section_start:first_section_end]
    assert "padding-top: 0;" in first_section_slice
    assert "margin-top: 0;" in first_section_slice

    assert "Command Cockpit Mounted Stage Expansion" in readme


def test_active_lane_hud_compacts_controls_into_command_matrix():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert 'class="active-lane-control-matrix"' in app
    assert 'class="active-lane-control-matrix-rail"' in app
    assert 'aria-label="Active lane command matrix"' in app
    assert 'data-matrix-area="chronicle"' in app
    assert 'data-matrix-area="views"' in app
    assert 'data-matrix-area="transition"' in app
    assert 'data-matrix-area="switch"' in app

    matrix_start = styles.index(".active-lane-control-matrix")
    matrix_end = styles.index("@keyframes activeLaneViewRunner", matrix_start)
    matrix_slice = styles[matrix_start:matrix_end]
    assert "grid-column: 1 / -1;" in matrix_slice
    assert "grid-template-columns: minmax(220px, 0.9fr) minmax(280px, 1.1fr);" in matrix_slice
    assert "min-height: 124px;" in matrix_slice
    assert "overflow: hidden;" in matrix_slice
    assert ".active-lane-control-matrix-rail" in matrix_slice
    assert "animation: activeLaneControlRail 5.2s ease-in-out infinite;" in matrix_slice
    assert '.active-lane-control-matrix .active-lane-micro-chronicle[data-matrix-area="chronicle"]' in matrix_slice
    assert "grid-row: 1 / 3;" in matrix_slice
    assert '.active-lane-control-matrix .active-lane-view-portals[data-matrix-area="views"]' in matrix_slice
    assert '.active-lane-control-matrix .active-lane-view-transition[data-matrix-area="transition"]' in matrix_slice
    assert '.active-lane-control-matrix .active-lane-switch-deck[data-matrix-area="switch"]' in matrix_slice
    assert "grid-auto-flow: column;" in matrix_slice
    assert "overflow-x: auto;" in matrix_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-control-matrix" in mobile_slice
    assert "grid-template-columns: 1fr;" in mobile_slice
    assert "min-height: 0;" in mobile_slice

    assert "@keyframes activeLaneControlRail" in styles
    assert "Active Lane Control Matrix" in readme
    assert "20260619-active-lane-control-matrix" in index


def test_command_cockpit_compacts_control_matrix_into_quick_deck():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-control-matrix-quick-deck" in index

    matrix_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix')
    matrix_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-micro-chronicle',
        matrix_start,
    )
    matrix_slice = styles[matrix_start:matrix_end]
    assert "grid-template-columns: minmax(0, 1fr) minmax(150px, 0.52fr);" in matrix_slice
    assert "grid-template-rows: 28px 32px 28px;" in matrix_slice
    assert "min-height: 0;" in matrix_slice
    assert "padding: 5px;" in matrix_slice

    chronicle_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-micro-chronicle')
    chronicle_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-micro-card',
        chronicle_start,
    )
    chronicle_slice = styles[chronicle_start:chronicle_end]
    assert "grid-column: 1 / -1;" in chronicle_slice
    assert "grid-row: 1;" in chronicle_slice
    assert "grid-template-columns: repeat(3, minmax(0, 1fr));" in chronicle_slice

    card_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-micro-card')
    card_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-micro-card em',
        card_start,
    )
    card_slice = styles[card_start:card_end]
    assert "min-height: 28px;" in card_slice
    assert "padding: 4px 5px;" in card_slice

    card_body_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-micro-card em')
    card_body_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-view-portals',
        card_body_start,
    )
    assert "display: none;" in styles[card_body_start:card_body_end]

    portals_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-view-portals')
    portals_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-view-transition',
        portals_start,
    )
    portals_slice = styles[portals_start:portals_end]
    assert "grid-column: 1 / -1;" in portals_slice
    assert "grid-row: 2;" in portals_slice
    assert "min-height: 28px;" in portals_slice

    transition_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-view-transition')
    transition_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-switch-deck',
        transition_start,
    )
    transition_slice = styles[transition_start:transition_end]
    assert "grid-column: 1;" in transition_slice
    assert "grid-row: 3;" in transition_slice
    assert "min-height: 26px;" in transition_slice

    switch_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix .active-lane-switch-deck')
    switch_end = styles.index("@media", switch_start)
    switch_slice = styles[switch_start:switch_end]
    assert "grid-column: 2;" in switch_slice
    assert "grid-row: 3;" in switch_slice
    assert "min-height: 26px;" in switch_slice

    assert "Command Cockpit Control Matrix Quick Deck" in readme


def test_mounted_stage_has_sticky_stage_lens_bar():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneStageLens" in app
    assert "const stageLens = activeLaneStageLens(lane);" in app
    assert 'class="active-lane-stage-lens"' in app
    assert 'data-stage-lens-view="${escapeHtml(state.detailView)}"' in app
    assert 'class="active-lane-stage-lens-signals"' in app
    assert 'class="active-lane-stage-lens-signal ${escapeHtml(signal.tone)}"' in app
    assert "${stageLens.signals" in app

    lens_start = styles.index(".active-lane-stage-lens")
    lens_end = styles.index("@keyframes activeLaneViewRunner", lens_start)
    lens_slice = styles[lens_start:lens_end]
    assert "position: sticky;" in lens_slice
    assert "top: 0;" in lens_slice
    assert "z-index: 5;" in lens_slice
    assert "grid-template-columns: minmax(118px, 0.78fr) minmax(0, 1.22fr);" in lens_slice
    assert "min-height: 32px;" in lens_slice
    assert "margin-bottom: 8px;" in lens_slice
    assert ".active-lane-stage-lens-signals" in lens_slice
    assert ".active-lane-stage-lens-signal" in lens_slice
    assert "animation: activeLaneStageLensPulse 4.8s ease-in-out infinite;" in lens_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-stage-lens" in mobile_slice
    assert "grid-template-columns: 1fr;" in mobile_slice
    assert ".active-lane-stage-lens-signals" in mobile_slice
    assert "grid-auto-flow: column;" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice

    assert "@keyframes activeLaneStageLensPulse" in styles
    assert "Active Lane Stage Lens Bar" in readme
    assert "20260619-active-lane-stage-lens-bar" in index


def test_command_cockpit_compresses_mounted_stage_lens_bar():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-stage-lens-compression" in index

    lens_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens')
    lens_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens-copy',
        lens_start,
    )
    lens_slice = styles[lens_start:lens_end]
    assert "grid-template-columns: minmax(94px, 0.52fr) minmax(0, 1fr);" in lens_slice
    assert "min-height: 26px;" in lens_slice
    assert "margin-bottom: 6px;" in lens_slice
    assert "padding: 4px;" in lens_slice

    copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens-copy')
    copy_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens-copy em',
        copy_start,
    )
    copy_slice = styles[copy_start:copy_end]
    assert "gap: 0;" in copy_slice

    hidden_meta_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens-copy em')
    hidden_meta_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens-signals',
        hidden_meta_start,
    )
    hidden_meta_slice = styles[hidden_meta_start:hidden_meta_end]
    assert "display: none;" in hidden_meta_slice

    signals_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens-signals')
    signals_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens-signal {',
        signals_start,
    )
    signals_slice = styles[signals_start:signals_end]
    assert "gap: 4px;" in signals_slice

    signal_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-lens-signal')
    signal_end = styles.index("@media", signal_start)
    signal_slice = styles[signal_start:signal_end]
    assert "min-height: 24px;" in signal_slice
    assert "padding: 3px 5px;" in signal_slice

    assert "Command Cockpit Stage Lens Compression" in readme


def test_mounted_stage_has_state_driven_holo_board_surface():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneHoloBoardNodes" in app
    assert "const holoNodes = activeLaneHoloBoardNodes(lane);" in app
    assert 'class="active-lane-holo-board"' in app
    assert 'class="active-lane-holo-runner"' in app
    assert 'class="active-lane-holo-node ${escapeHtml(node.tone)}"' in app
    assert 'style="--holo-index:${node.index};"' in app

    board_start = styles.index(".active-lane-holo-board")
    board_end = styles.index("@keyframes activeLaneViewRunner", board_start)
    board_slice = styles[board_start:board_end]
    assert "position: sticky;" in board_slice
    assert "top: 44px;" in board_slice
    assert "min-height: 58px;" in board_slice
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in board_slice
    assert "pointer-events: none;" in board_slice
    assert ".active-lane-holo-runner" in board_slice
    assert ".active-lane-holo-node" in board_slice
    assert "animation: activeLaneHoloRunner 5.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in board_slice
    assert "animation: activeLaneHoloNodeWake 3.4s ease-in-out infinite;" in board_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-holo-board" in mobile_slice
    assert "top: 82px;" in mobile_slice
    assert "min-height: 50px;" in mobile_slice

    assert "@keyframes activeLaneHoloRunner" in styles
    assert "@keyframes activeLaneHoloNodeWake" in styles
    assert "Active Lane Holo Board" in readme
    assert "20260619-active-lane-holo-board" in index


def test_command_cockpit_turns_holo_board_into_stage_floor():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-holo-floor" in index

    board_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-holo-board')
    board_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-holo-board::before',
        board_start,
    )
    board_slice = styles[board_start:board_end]
    assert "top: 34px;" in board_slice
    assert "min-height: 42px;" in board_slice
    assert "margin-bottom: -6px;" in board_slice
    assert "transform: perspective(640px) rotateX(18deg);" in board_slice
    assert "transform-origin: center top;" in board_slice

    floor_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-holo-board::before')
    floor_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-holo-board::after',
        floor_start,
    )
    floor_slice = styles[floor_start:floor_end]
    assert "repeating-linear-gradient(90deg" in floor_slice
    assert "animation: commandHoloFloorDrift 7.2s ease-in-out infinite;" in floor_slice

    runner_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-holo-runner')
    runner_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-holo-node',
        runner_start,
    )
    runner_slice = styles[runner_start:runner_end]
    assert "height: 4px;" in runner_slice
    assert "animation: activeLaneHoloRunner 4.2s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in runner_slice

    node_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-holo-node')
    node_end = styles.index("@media", node_start)
    node_slice = styles[node_start:node_end]
    assert "min-height: 30px;" in node_slice
    assert "padding: 3px 4px;" in node_slice

    assert "@keyframes commandHoloFloorDrift" in styles
    assert "Command Cockpit Holo Floor" in readme


def test_mounted_stage_has_lane_atmosphere_engine():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneStageMotes" in app
    assert "const stageMotes = activeLaneStageMotes(lane);" in app
    assert 'class="active-lane-stage-atmosphere"' in app
    assert 'class="active-lane-stage-mote ${escapeHtml(mote.tone)}"' in app
    assert "--mote-x:${mote.x}%;" in app
    assert "--mote-delay:${mote.delay}ms;" in app
    assert "--mote-size:${mote.size}px;" in app

    atmosphere_start = styles.index(".active-lane-stage-atmosphere")
    atmosphere_end = styles.index(".active-lane-mounted-stage > .detail-section:first-of-type", atmosphere_start)
    atmosphere_slice = styles[atmosphere_start:atmosphere_end]
    assert "position: absolute;" in atmosphere_slice
    assert "z-index: 0;" in atmosphere_slice
    assert "pointer-events: none;" in atmosphere_slice
    assert ".active-lane-stage-mote" in atmosphere_slice
    assert "animation: activeLaneStageMoteDrift 7.8s ease-in-out infinite;" in atmosphere_slice
    assert "animation-delay: var(--mote-delay);" in atmosphere_slice

    layer_start = styles.index(".active-lane-mounted-stage > :not(.active-lane-mounted-stage-scan)")
    layer_slice = styles[layer_start : layer_start + 260]
    assert ":not(.active-lane-stage-atmosphere)" in layer_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-stage-mote:nth-child(n + 7)" in mobile_slice
    assert "display: none;" in mobile_slice

    assert "@keyframes activeLaneStageMoteDrift" in styles
    assert "Active Lane Atmosphere Engine" in readme
    assert "20260619-active-lane-atmosphere-engine" in index


def test_mounted_stage_has_actionable_objective_beacons():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneObjectiveBeacons" in app
    assert "const objectiveBeacons = activeLaneObjectiveBeacons(lane);" in app
    assert 'class="active-lane-objective-beacons"' in app
    assert 'class="active-lane-objective-beacon ${escapeHtml(beacon.tone)}"' in app
    assert "${escapeHtml(beacon.label)}" in app
    assert "${escapeHtml(beacon.value)}" in app
    assert "${escapeHtml(beacon.body)}" in app

    beacon_start = styles.index("\n.active-lane-objective-beacons {")
    beacon_end = styles.index(".active-lane-switch-deck", beacon_start)
    beacon_slice = styles[beacon_start:beacon_end]
    assert "position: sticky;" in beacon_slice
    assert "top: 110px;" in beacon_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in beacon_slice
    assert "min-height: 44px;" in beacon_slice
    assert "overflow: hidden;" in beacon_slice
    assert ".active-lane-objective-beacon" in beacon_slice
    assert "animation: activeLaneObjectivePulse 4.2s ease-in-out infinite;" in beacon_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-objective-beacons" in mobile_slice
    assert "top: 138px;" in mobile_slice
    assert "grid-auto-flow: column;" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice

    assert "@keyframes activeLaneObjectivePulse" in styles
    assert "Active Lane Objective Beacons" in readme
    assert "20260619-active-lane-objective-beacons" in index


def test_mounted_stage_has_compact_bot_party_dock():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "function activeLaneBotPartyRecords" in app
    assert "const botPartyRecords = activeLaneBotPartyRecords(lane);" in app
    assert 'class="active-lane-bot-party-dock"' in app
    assert 'class="active-lane-bot-party-card ${escapeHtml(record.tone)}"' in app
    assert 'agentAvatarMarkup(record.agent, lane, "active-lane-bot-party-avatar")' in app
    assert "${escapeHtml(record.callsign)}" in app
    assert "${escapeHtml(record.status)}" in app
    assert "${escapeHtml(record.action)}" in app

    dock_start = styles.index("\n.active-lane-bot-party-dock {")
    dock_end = styles.index(".active-lane-switch-deck", dock_start)
    dock_slice = styles[dock_start:dock_end]
    assert "position: sticky;" in dock_slice
    assert "top: 164px;" in dock_slice
    assert "grid-template-columns: repeat(3, minmax(0, 1fr));" in dock_slice
    assert "min-height: 52px;" in dock_slice
    assert ".active-lane-bot-party-card" in dock_slice
    assert ".active-lane-bot-party-avatar" in dock_slice
    assert "animation: activeLaneBotPartyPing 4.6s ease-in-out infinite;" in dock_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".active-lane-bot-party-dock" in mobile_slice
    assert "top: 198px;" in mobile_slice
    assert "grid-auto-flow: column;" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice

    assert "@keyframes activeLaneBotPartyPing" in styles
    assert "Active Lane Bot Party Dock" in readme
    assert "20260619-active-lane-bot-party-dock" in index


def test_command_cockpit_compacts_objective_and_bot_docks_into_signal_rails():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-signal-rails" in index

    beacon_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-objective-beacons')
    beacon_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-objective-beacon {',
        beacon_start,
    )
    beacon_slice = styles[beacon_start:beacon_end]
    assert "top: 78px;" in beacon_slice
    assert "min-height: 32px;" in beacon_slice
    assert "margin-bottom: 4px;" in beacon_slice
    assert "padding: 3px;" in beacon_slice

    beacon_card_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-objective-beacon')
    beacon_card_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-objective-beacon i',
        beacon_card_start,
    )
    beacon_card_slice = styles[beacon_card_start:beacon_card_end]
    assert "min-height: 28px;" in beacon_card_slice
    assert "padding: 3px 5px;" in beacon_card_slice

    beacon_copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-objective-beacon i')
    beacon_copy_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-bot-party-dock {',
        beacon_copy_start,
    )
    assert "display: none;" in styles[beacon_copy_start:beacon_copy_end]

    bot_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-bot-party-dock')
    bot_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-bot-party-card {',
        bot_start,
    )
    bot_slice = styles[bot_start:bot_end]
    assert "top: 116px;" in bot_slice
    assert "min-height: 34px;" in bot_slice
    assert "margin-bottom: 4px;" in bot_slice
    assert "padding: 3px;" in bot_slice

    bot_card_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-bot-party-card')
    bot_card_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-bot-party-avatar',
        bot_card_start,
    )
    bot_card_slice = styles[bot_card_start:bot_card_end]
    assert "grid-template-columns: 26px minmax(0, 1fr);" in bot_card_slice
    assert "min-height: 30px;" in bot_card_slice
    assert "padding: 3px 5px;" in bot_card_slice

    bot_avatar_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-bot-party-avatar')
    bot_avatar_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-bot-party-card i',
        bot_avatar_start,
    )
    bot_avatar_slice = styles[bot_avatar_start:bot_avatar_end]
    assert "width: 26px;" in bot_avatar_slice
    assert "height: 26px;" in bot_avatar_slice

    bot_copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-bot-party-card i')
    bot_copy_end = styles.index("@media", bot_copy_start)
    assert "display: none;" in styles[bot_copy_start:bot_copy_end]

    assert "Command Cockpit Signal Rails" in readme


def test_command_cockpit_owner_bot_uses_animated_character_frame():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")

    assert "20260619-command-cockpit-bot-character-frame" in index
    assert "styles.css?v=20260619-command-cockpit-event-lens-20260619-command-cockpit-event-pulse-20260619-command-cockpit-node-halos-20260619-command-cockpit-crew-relay-20260619-command-cockpit-focus-beam-20260619-command-cockpit-insight-ribbon-20260619-lane-expansion-portal-deck-20260619-agent-constellation-bay-20260619-command-cockpit-node-echo-rail-20260619-command-cockpit-node-signal-packets-20260619-command-cockpit-node-focus-lens-20260619-command-cockpit-stable-board-20260619-command-cockpit-path-depth-stack-20260619-command-cockpit-minigame-sigil-20260619-command-cockpit-unlock-badges-20260619-command-cockpit-footer-overlay-20260619-command-cockpit-viewport-fit-20260619-command-cockpit-quest-node-focus-20260619-command-cockpit-quest-level-map-20260619-command-cockpit-territory-board-20260619-command-cockpit-stage-compass-20260619-command-cockpit-mission-cartridge-20260619-command-cockpit-bot-character-frame" in index
    assert "app.js?v=20260619-command-cockpit-event-lens-20260619-command-cockpit-event-pulse-20260619-command-cockpit-node-halos-20260619-command-cockpit-crew-relay-20260619-command-cockpit-focus-beam-20260619-command-cockpit-insight-ribbon-20260619-lane-expansion-portal-deck-20260619-agent-constellation-bay-20260619-command-cockpit-node-echo-rail-20260619-command-cockpit-node-signal-packets-20260619-command-cockpit-node-focus-lens-20260619-command-cockpit-stable-board-20260619-command-cockpit-path-depth-stack-20260619-command-cockpit-minigame-sigil-20260619-command-cockpit-unlock-badges-20260619-command-cockpit-footer-overlay-20260619-command-cockpit-viewport-fit-20260619-command-cockpit-quest-node-focus-20260619-command-cockpit-quest-level-map-20260619-command-cockpit-territory-board-20260619-command-cockpit-stage-compass-20260619-command-cockpit-mission-cartridge-20260619-command-cockpit-bot-character-frame" in index

    assert "function agentCharacterFrame(" in app
    assert "const frameClass = `${className} agent-character-frame`;" in app
    assert 'class="agent-character-portrait"' in app
    assert 'class="agent-character-aura"' in app
    assert 'class="agent-character-sigil"' in app
    assert 'class="agent-character-scan"' in app
    assert 'agentCharacterFrame(ownerAgent, lane, "active-lane-hud-bot-avatar")' in app
    assert "agentAvatarMarkup(ownerAgent, lane, \"active-lane-hud-bot-avatar\")" not in app

    frame_start = styles.index(".active-lane-hud-bot-avatar.agent-character-frame")
    frame_end = styles.index(".active-lane-hud-bot-copy", frame_start)
    frame_slice = styles[frame_start:frame_end]
    assert "grid-row: 1 / 3;" in frame_slice
    assert ".agent-character-frame" in frame_slice
    assert "isolation: isolate;" in frame_slice
    assert ".agent-character-portrait" in frame_slice
    assert ".agent-character-aura" in frame_slice
    assert "animation: agentCharacterAura 5.6s ease-in-out infinite;" in frame_slice
    assert ".agent-character-sigil" in frame_slice
    assert ".agent-character-scan" in frame_slice
    assert "animation: agentCharacterScan 3.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in frame_slice

    assert "@keyframes agentCharacterAura" in styles
    assert "@keyframes agentCharacterScan" in styles

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert "body[data-atlas-deck=\"command\"][data-atlas-stage=\"cockpit\"][data-detail-view=\"overview\"] .active-lane-hud-bot-avatar.agent-character-frame" in mobile_slice
    assert "body[data-atlas-deck=\"command\"][data-atlas-stage=\"cockpit\"] .agent-character-sigil" in mobile_slice
    assert "width: 11px;" in mobile_slice
    assert "height: 11px;" in mobile_slice

    assert "Command Cockpit Bot Character Frame" in readme


def test_command_cockpit_uses_generated_mission_cartridge_texture():
    index = read("web/index.html")
    styles = read("web/styles.css")
    app = read("web/app.js")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/command-cockpit-mission-cartridge-20260619.png"

    assert asset.exists()
    assert asset.stat().st_size > 100_000
    assert "20260619-command-cockpit-mission-cartridge" in index
    assert "styles.css?v=20260619-command-cockpit-event-lens-20260619-command-cockpit-event-pulse-20260619-command-cockpit-node-halos-20260619-command-cockpit-crew-relay-20260619-command-cockpit-focus-beam-20260619-command-cockpit-insight-ribbon-20260619-lane-expansion-portal-deck-20260619-agent-constellation-bay-20260619-command-cockpit-node-echo-rail-20260619-command-cockpit-node-signal-packets-20260619-command-cockpit-node-focus-lens-20260619-command-cockpit-stable-board-20260619-command-cockpit-path-depth-stack-20260619-command-cockpit-minigame-sigil-20260619-command-cockpit-unlock-badges-20260619-command-cockpit-footer-overlay-20260619-command-cockpit-viewport-fit-20260619-command-cockpit-quest-node-focus-20260619-command-cockpit-quest-level-map-20260619-command-cockpit-territory-board-20260619-command-cockpit-stage-compass-20260619-command-cockpit-mission-cartridge" in index
    assert "app.js?v=20260619-command-cockpit-event-lens-20260619-command-cockpit-event-pulse-20260619-command-cockpit-node-halos-20260619-command-cockpit-crew-relay-20260619-command-cockpit-focus-beam-20260619-command-cockpit-insight-ribbon-20260619-lane-expansion-portal-deck-20260619-agent-constellation-bay-20260619-command-cockpit-node-echo-rail-20260619-command-cockpit-node-signal-packets-20260619-command-cockpit-node-focus-lens-20260619-command-cockpit-stable-board-20260619-command-cockpit-path-depth-stack-20260619-command-cockpit-minigame-sigil-20260619-command-cockpit-unlock-badges-20260619-command-cockpit-footer-overlay-20260619-command-cockpit-viewport-fit-20260619-command-cockpit-quest-node-focus-20260619-command-cockpit-quest-level-map-20260619-command-cockpit-territory-board-20260619-command-cockpit-stage-compass-20260619-command-cockpit-mission-cartridge" in index

    hud_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-level-hud')
    hud_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-bot',
        hud_start,
    )
    hud_slice = styles[hud_start:hud_end]
    assert 'url("./assets/system/command-cockpit-mission-cartridge-20260619.png") center / cover' in hud_slice
    assert "linear-gradient(180deg, rgba(3, 6, 9, 0.34), rgba(3, 6, 9, 0.82))" in hud_slice
    assert "inset 0 -18px 44px rgba(0, 0, 0, 0.38)" in hud_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    world_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-world-map',
        mobile_start,
    )
    world_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-world-map::-webkit-scrollbar',
        world_start,
    )
    world_slice = styles[world_start:world_end]
    assert "grid-auto-columns: minmax(64px, 1fr);" in world_slice
    assert "min-height: 32px;" in world_slice
    assert "padding: 3px;" in world_slice

    assert "system-command-cockpit-mission-cartridge" in app
    assert "Command Cockpit Mission Cartridge" in app
    assert "./assets/system/command-cockpit-mission-cartridge-20260619.png" in app
    assert "Command Cockpit Mission Cartridge" in readme




