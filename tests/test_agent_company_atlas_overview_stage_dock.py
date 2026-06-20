from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_overview_stage_dock_mounts_one_mission_module_at_a_time():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "overviewStageViewByLane" in app
    assert "function renderOverviewStageDock(lane, activeStage)" in app
    assert "function renderOverviewStagePanel(lane, activeStage)" in app
    assert "function renderOverviewIntelPanel(lane)" in app
    assert "const owner = laneAgents(lane)[0]" in app
    assert "laneOwnerAgent" not in app
    assert "${renderOverviewStageDock(lane, activeStage)}" in app
    assert "${renderOverviewStagePanel(lane, activeStage)}" in app
    assert 'data-overview-stage="${escapeHtml(stage.id)}"' in app
    assert 'event.target.closest("[data-overview-stage]")' in app

    overview_start = app.index("function renderOverviewView(lane)")
    overview_end = app.index("function renderOverviewStageDock", overview_start)
    overview_slice = app[overview_start:overview_end]
    assert "renderQuestCockpit(lane)" not in overview_slice
    assert "renderMilestoneRunway(lane)" not in overview_slice
    assert "renderAgentParty(lane)" not in overview_slice
    assert "renderMinigameForge(lane)" not in overview_slice
    assert "renderGateRadar(lane)" not in overview_slice

    assert ".detail-content.detail-view-overview .detail-top" in styles
    overview_top_block = styles[
        styles.index(".detail-content.detail-view-overview .detail-top") : styles.index(".detail-content.detail-view-path .detail-top")
    ]
    assert "display: none" in overview_top_block

    assert ".detail-content.detail-view-overview .detail-tabs" in styles
    overview_tabs_start = styles.index(".detail-content.detail-view-overview .detail-tabs")
    overview_tabs_end = styles.index(".detail-content.detail-view-path {", overview_tabs_start)
    assert "display: none" in styles[overview_tabs_start:overview_tabs_end]

    assert ".overview-stage-dock" in styles
    assert ".overview-stage-button.active" in styles
    assert ".overview-intel-panel" in styles
    assert 'body[data-detail-view="overview"] .quest-cockpit-hero' in styles
    assert 'body[data-detail-view="overview"] .quest-stage-grid' in styles
    quest_stage_start = styles.index('body[data-detail-view="overview"] .quest-stage-grid')
    quest_stage_end = styles.index('body[data-detail-view="overview"] .quest-stage,', quest_stage_start)
    assert "display: none" in styles[quest_stage_start:quest_stage_end]
    assert ".overview-stage-buttons {\n    grid-template-columns: repeat(6, minmax(0, 1fr));" in styles
    assert 'body[data-detail-view="overview"] .quest-command-grid' in styles
    mobile_command_start = styles.index('body[data-detail-view="overview"] .quest-command-grid')
    mobile_command_end = styles.index('body[data-detail-view="overview"] .quest-action-row', mobile_command_start)
    assert "display: none" in styles[mobile_command_start:mobile_command_end]

    assert "Overview Stage Dock" in readme
    assert "20260618-overview-stage-dock" in index


def test_command_cockpit_compacts_overview_stage_modules_inside_mounted_stage():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-overview-module-compression" in index

    dock_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-dock')
    dock_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-meter',
        dock_start,
    )
    dock_slice = styles[dock_start:dock_end]
    assert "grid-template-columns: minmax(78px, 0.48fr) minmax(0, 1fr);" in dock_slice
    assert "margin-bottom: 6px;" in dock_slice
    assert "padding: 4px;" in dock_slice

    meter_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-meter')
    meter_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button',
        meter_start,
    )
    meter_slice = styles[meter_start:meter_end]
    assert "padding: 5px 6px;" in meter_slice

    button_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button')
    button_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .detail-section',
        button_start,
    )
    button_slice = styles[button_start:button_end]
    assert "min-height: 30px;" in button_slice
    assert "padding: 3px 4px;" in button_slice

    section_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .detail-section')
    section_end = styles.index("@media", section_start)
    section_slice = styles[section_start:section_end]
    assert "padding: 10px 0;" in section_slice

    assert "Command Cockpit Overview Module Compression" in readme


def test_command_cockpit_compacts_quest_cockpit_hero_tile():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-quest-tile-compression" in index

    quest_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-cockpit')
    quest_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-cockpit-hero',
        quest_start,
    )
    quest_slice = styles[quest_start:quest_end]
    assert "gap: 6px;" in quest_slice
    assert "padding: 8px;" in quest_slice

    hero_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-cockpit-hero')
    hero_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-avatar',
        hero_start,
    )
    hero_slice = styles[hero_start:hero_end]
    assert "grid-template-columns: 40px minmax(0, 1fr) 40px 44px;" in hero_slice
    assert "min-height: 64px;" in hero_slice
    assert "padding: 6px;" in hero_slice

    avatar_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-avatar')
    avatar_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-meter',
        avatar_start,
    )
    avatar_slice = styles[avatar_start:avatar_end]
    assert "width: 40px;" in avatar_slice
    assert "height: 40px;" in avatar_slice

    meter_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-meter')
    meter_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-cockpit-hero p',
        meter_start,
    )
    meter_slice = styles[meter_start:meter_end]
    assert "width: 44px;" in meter_slice
    assert "height: 44px;" in meter_slice

    copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-cockpit-hero p')
    copy_end = styles.index("@media", copy_start)
    copy_slice = styles[copy_start:copy_end]
    assert "-webkit-line-clamp: 1;" in copy_slice

    assert "Command Cockpit Quest Tile Compression" in readme


def test_command_cockpit_turns_quest_support_cards_into_command_strips():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-quest-command-strips" in index

    signal_row_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-signal-row')
    signal_row_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-signal {',
        signal_row_start,
    )
    signal_row_slice = styles[signal_row_start:signal_row_end]
    assert "gap: 4px;" in signal_row_slice

    signal_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-signal')
    signal_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-command-grid',
        signal_start,
    )
    signal_slice = styles[signal_start:signal_end]
    assert "min-height: 32px;" in signal_slice
    assert "padding: 5px 6px;" in signal_slice

    command_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-command-grid')
    command_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-next-card,',
        command_start,
    )
    command_slice = styles[command_start:command_end]
    assert "gap: 5px;" in command_slice
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in command_slice

    card_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-next-card')
    card_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-next-card p:not(.eyebrow)',
        card_start,
    )
    card_slice = styles[card_start:card_end]
    assert "min-height: 54px;" in card_slice
    assert "padding: 6px;" in card_slice

    copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-next-card p:not(.eyebrow)')
    copy_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-action-row',
        copy_start,
    )
    copy_slice = styles[copy_start:copy_end]
    assert "display: none;" in copy_slice

    action_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-action-row')
    action_end = styles.index("@media", action_start)
    action_slice = styles[action_start:action_end]
    assert "gap: 4px;" in action_slice
    assert "min-height: 26px;" in action_slice

    assert "Command Cockpit Quest Command Strips" in readme


def test_command_cockpit_overview_quest_reads_as_mission_console():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-mission-console" in index

    section_chrome_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .detail-section > .lane-button-top'
    )
    section_chrome_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit',
        section_chrome_start,
    )
    assert "display: none;" in styles[section_chrome_start:section_chrome_end]

    floor_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-holo-board'
    )
    floor_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-objective-beacons',
        floor_start,
    )
    assert "display: none;" in styles[floor_start:floor_end]

    objective_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-objective-beacons'
    )
    objective_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-bot-party-dock',
        objective_start,
    )
    assert "display: none;" in styles[objective_start:objective_end]

    bot_dock_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-bot-party-dock'
    )
    bot_dock_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit',
        bot_dock_start,
    )
    assert "display: none;" in styles[bot_dock_start:bot_dock_end]

    console_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit'
    )
    console_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero',
        console_start,
    )
    console_slice = styles[console_start:console_end]
    assert "grid-template-columns: minmax(0, 1.04fr) minmax(260px, 0.62fr);" in console_slice
    assert 'grid-template-areas:\n    "hero command"\n    "signals actions";' in console_slice
    assert "align-items: stretch;" in console_slice
    assert "gap: 5px;" in console_slice

    hero_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero'
    )
    hero_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-row',
        hero_start,
    )
    assert "grid-area: hero;" in styles[hero_start:hero_end]

    signal_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-row'
    )
    signal_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-command-grid',
        signal_start,
    )
    signal_slice = styles[signal_start:signal_end]
    assert "grid-area: hero;" in signal_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in signal_slice
    assert "margin: 0 106px 6px 54px;" in signal_slice

    command_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field'
    )
    command_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field::before',
        command_start,
    )
    assert "grid-area: command;" in styles[command_start:command_end]

    hidden_command_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-command-grid'
    )
    hidden_command_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row',
        hidden_command_start,
    )
    assert "display: none;" in styles[hidden_command_start:hidden_command_end]

    action_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row'
    )
    action_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row .tool-button',
        action_start,
    )
    action_slice = styles[action_start:action_end]
    assert "grid-area: actions;" in action_slice
    assert "display: grid;" in action_slice
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in action_slice

    button_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row .tool-button'
    )
    button_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-event-chain',
        button_start,
    )
    assert "width: 100%;" in styles[button_start:button_end]

    event_chain_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-event-chain'
    )
    event_chain_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway',
        event_chain_start,
    )
    assert "display: none;" in styles[event_chain_start:event_chain_end]

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_console_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit',
        mobile_start,
    )
    mobile_console_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-row',
        mobile_console_start,
    )
    mobile_console_slice = styles[mobile_console_start:mobile_console_end]
    assert "grid-template-columns: 1fr;" in mobile_console_slice
    assert 'grid-template-areas:\n      "hero"\n      "signals"\n      "command"\n      "actions";' in mobile_console_slice
    assert "width: 100%;" in mobile_console_slice
    assert "min-width: 0;" in mobile_console_slice
    assert "overflow: hidden;" in mobile_console_slice

    mobile_signal_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-row',
        mobile_console_start,
    )
    mobile_signal_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row',
        mobile_signal_start,
    )
    mobile_signal_slice = styles[mobile_signal_start:mobile_signal_end]
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in mobile_signal_slice
    assert "min-width: 0;" in mobile_signal_slice

    mobile_action_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row',
        mobile_signal_start,
    )
    mobile_action_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row .tool-button',
        mobile_action_start,
    )
    mobile_action_slice = styles[mobile_action_start:mobile_action_end]
    assert "flex-direction: row;" in mobile_action_slice
    assert "min-width: 0;" in mobile_action_slice

    responsive_shell_start = styles.index("@media (max-width: 1320px)")
    responsive_workspace_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .workspace',
        responsive_shell_start,
    )
    responsive_workspace_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel',
        responsive_workspace_start,
    )
    responsive_workspace_slice = styles[responsive_workspace_start:responsive_workspace_end]
    assert "grid-template-columns: minmax(0, 1fr);" in responsive_workspace_slice
    assert "min-width: 0;" in responsive_workspace_slice

    responsive_panel_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel',
        responsive_workspace_end,
    )
    responsive_panel_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-panel',
        responsive_panel_start + 1,
    )
    responsive_panel_slice = styles[responsive_panel_start:responsive_panel_end]
    assert "grid-column: auto;" in responsive_panel_slice
    assert "min-width: 0;" in responsive_panel_slice

    responsive_detail_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-panel',
        responsive_panel_end,
    )
    responsive_detail_end = styles.index(
        "@media (max-width: 1120px)",
        responsive_detail_start,
    )
    responsive_detail_slice = styles[responsive_detail_start:responsive_detail_end]
    assert "grid-column: auto;" in responsive_detail_slice
    assert "width: 100%;" in responsive_detail_slice
    assert "min-width: 0;" in responsive_detail_slice

    responsive_content_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content',
        responsive_detail_start,
    )
    responsive_content_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-level-hud',
        responsive_content_start,
    )
    responsive_content_slice = styles[responsive_content_start:responsive_content_end]
    assert "width: 100%;" in responsive_content_slice
    assert "min-width: 0;" in responsive_content_slice
    assert "overflow-x: hidden;" in responsive_content_slice

    responsive_hud_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-level-hud',
        responsive_content_end,
    )
    responsive_hud_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage',
        responsive_hud_start,
    )
    responsive_hud_slice = styles[responsive_hud_start:responsive_hud_end]
    assert "width: 100%;" in responsive_hud_slice
    assert "min-width: 0;" in responsive_hud_slice

    responsive_stage_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage',
        responsive_hud_end,
    )
    responsive_stage_end = styles.index(
        "@media (max-width: 1120px)",
        responsive_stage_start,
    )
    responsive_stage_slice = styles[responsive_stage_start:responsive_stage_end]
    assert "width: 100%;" in responsive_stage_slice
    assert "min-width: 0;" in responsive_stage_slice
    assert "overflow-x: hidden;" in responsive_stage_slice

    assert "Command Cockpit Mission Console" in readme


def test_command_cockpit_mobile_quest_uses_boss_bar_card():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-mobile-quest-boss-bar" in index

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]

    console_start = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit'
    )
    console_end = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero',
        console_start,
    )
    console_slice = mobile_slice[console_start:console_end]
    assert "gap: 4px;" in console_slice
    assert "padding: 6px;" in console_slice

    hero_start = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero'
    )
    hero_end = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero::after',
        hero_start,
    )
    hero_slice = mobile_slice[hero_start:hero_end]
    assert "grid-template-columns: 32px minmax(0, 1fr) 32px 38px;" in hero_slice
    assert "min-height: 48px;" in hero_slice
    assert "overflow: hidden;" in hero_slice

    runner_start = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero::after',
        hero_start,
    )
    runner_end = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-avatar',
        runner_start,
    )
    runner_slice = mobile_slice[runner_start:runner_end]
    assert 'content: "";' in runner_slice
    assert "animation: commandOverviewModuleRunner 2.4s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in runner_slice

    avatar_start = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-avatar',
        runner_start,
    )
    avatar_end = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-meter',
        avatar_start,
    )
    avatar_slice = mobile_slice[avatar_start:avatar_end]
    assert "width: 32px;" in avatar_slice
    assert "height: 32px;" in avatar_slice

    copy_start = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero p:not(.eyebrow)',
        avatar_end,
    )
    copy_end = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal',
        copy_start,
    )
    assert "display: none;" in mobile_slice[copy_start:copy_end]

    signal_start = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal {',
        copy_end,
    )
    signal_end = mobile_slice.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row',
        signal_start,
    )
    signal_slice = mobile_slice[signal_start:signal_end]
    assert "min-height: 24px;" in signal_slice
    assert "padding: 2px 3px;" in signal_slice

    assert "Command Cockpit Mobile Quest Boss Bar" in readme


def test_command_cockpit_overview_stage_uses_footer_status_rail():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    app = read("web/app.js")

    assert "20260619-command-cockpit-footer-overlay" in index
    assert "20260619-command-cockpit-stage-footer-rail" in index
    assert "function activeLaneStageFooterRail" in app
    assert "const stageFooterRail = activeLaneStageFooterRail(lane);" in app
    assert 'class="active-lane-stage-footer-rail"' in app
    assert 'class="active-lane-stage-footer-cell ${escapeHtml(cell.tone)}"' in app
    assert "${stageFooterRail}" in app

    stage_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"]'
    )
    stage_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit',
        stage_start,
    )
    stage_slice = styles[stage_start:stage_end]
    assert "display: flex;" in stage_slice
    assert "flex-direction: column;" in stage_slice
    assert "position: relative;" in stage_slice
    assert "padding-bottom: 46px;" in stage_slice

    rail_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-rail'
    )
    rail_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-rail::before',
        rail_start,
    )
    rail_slice = styles[rail_start:rail_end]
    assert "position: absolute;" in rail_slice
    assert "top: 4px;" in rail_slice
    assert "right: 8px;" in rail_slice
    assert "bottom: auto;" in rail_slice
    assert "left: 8px;" in rail_slice
    assert "z-index: 5;" in rail_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in rail_slice
    assert "min-height: 32px;" in rail_slice
    assert "margin-top: 0;" in rail_slice
    assert "backdrop-filter: blur(12px);" in rail_slice

    sweep_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-rail::before',
        rail_start,
    )
    sweep_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-cell',
        sweep_start,
    )
    sweep_slice = styles[sweep_start:sweep_end]
    assert 'content: "";' in sweep_slice
    assert "animation: commandStageFooterRailSweep 3.2s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in sweep_slice

    cell_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-cell',
        sweep_end,
    )
    cell_end = styles.index("@keyframes commandStageFooterRailSweep", cell_start)
    cell_slice = styles[cell_start:cell_end]
    assert "grid-template-columns: auto minmax(0, 1fr);" in cell_slice
    assert "min-height: 28px;" in cell_slice
    assert "text-overflow: ellipsis;" in cell_slice
    assert "grid-column: 1 / -1;" in cell_slice
    assert "display: none;" in cell_slice
    assert ".active-lane-stage-footer-cell.gated" in cell_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_rail_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-rail',
        mobile_start,
    )
    mobile_rail_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-cell',
        mobile_rail_start,
    )
    mobile_rail_slice = styles[mobile_rail_start:mobile_rail_end]
    assert "top: 4px;" in mobile_rail_slice
    assert "right: 5px;" in mobile_rail_slice
    assert "bottom: auto;" in mobile_rail_slice
    assert "left: 5px;" in mobile_rail_slice
    assert "min-height: 30px;" in mobile_rail_slice
    assert "margin-top: 0;" in mobile_rail_slice
    assert "padding: 3px;" in mobile_rail_slice

    mobile_cell_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-cell',
        mobile_rail_end,
    )
    mobile_cell_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-cell i',
        mobile_cell_start,
    )
    mobile_cell_slice = styles[mobile_cell_start:mobile_cell_end]
    assert "min-height: 26px;" in mobile_cell_slice
    assert "padding: 2px 3px;" in mobile_cell_slice

    assert "@keyframes commandStageFooterRailSweep" in styles
    assert "Command Cockpit Stage Footer Rail" in readme
    assert "Command Cockpit Footer Overlay" in readme


def test_command_cockpit_desktop_keeps_footer_rail_pinned_in_stage():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-desktop-footer-pin" in index
    assert "20260619-command-cockpit-footer-overlay" in index

    rail_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-rail'
    )
    rail_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-rail::before',
        rail_start,
    )
    rail_slice = styles[rail_start:rail_end]
    assert "position: absolute;" in rail_slice
    assert "top: 4px;" in rail_slice
    assert "bottom: auto;" in rail_slice
    assert "margin-top: 0;" in rail_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_rail_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-rail',
        mobile_start,
    )
    mobile_rail_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-footer-cell',
        mobile_rail_start,
    )
    mobile_rail_slice = styles[mobile_rail_start:mobile_rail_end]
    assert "margin-top: 0;" in mobile_rail_slice


def test_command_cockpit_overview_slimlines_desktop_hud():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-overview-hud-slimline" in index
    assert "Command Cockpit Overview HUD Slimline" in readme

    hud_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-level-hud'
    )
    bot_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-bot',
        hud_start,
    )
    hud_slice = styles[hud_start:bot_start]
    assert "min-height: 0;" in hud_slice
    assert "margin-bottom: 6px;" in hud_slice
    assert "padding: 7px;" in hud_slice

    next_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-next',
        bot_start,
    )
    arena_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-arena',
        next_start,
    )
    assert "display: none;" in styles[next_start:arena_start]

    matrix_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-control-matrix',
        arena_start,
    )
    matrix_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix',
        matrix_start,
    )
    assert "display: none;" in styles[matrix_start:matrix_end]

    assert "Command Cockpit Desktop Footer Pin" in readme


def test_command_cockpit_overview_uses_quest_field_board():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-quest-field-board" in index
    assert "Command Cockpit Quest Field Board" in readme
    assert "function questFieldCells(lane, data, gateTitle, gateBody)" in app
    assert "function renderQuestFieldCell(cell, index)" in app
    assert 'class="quest-field"' in app
    assert 'class="quest-field-runner"' in app
    assert 'class="quest-field-cell ${escapeHtml(cell.tone)}"' in app

    base_start = styles.index("\n.quest-field {")
    base_end = styles.index(".quest-field::before", base_start)
    base_slice = styles[base_start:base_end]
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in base_slice
    assert "min-height: 76px;" in base_slice

    runner_start = styles.index("\n.quest-field-runner")
    runner_end = styles.index(".quest-field-cell", runner_start)
    runner_slice = styles[runner_start:runner_end]
    assert "left: clamp(18px, var(--quest-progress), calc(100% - 18px));" in runner_slice
    assert "animation: questFieldRunnerPulse 1.8s ease-in-out infinite;" in runner_slice

    cockpit_field_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field'
    )
    cockpit_field_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-command-grid',
        cockpit_field_start,
    )
    cockpit_field_slice = styles[cockpit_field_start:cockpit_field_end]
    assert "grid-area: command;" in cockpit_field_slice
    assert "align-self: start;" in cockpit_field_slice
    assert "min-height: 64px;" in cockpit_field_slice

    command_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-command-grid',
        cockpit_field_end,
    )
    command_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-action-row',
        command_start,
    )
    assert "display: none;" in styles[command_start:command_end]

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_cockpit_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit',
        mobile_start,
    )
    mobile_cockpit_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field',
        mobile_cockpit_start,
    )
    assert '"command"' in styles[mobile_cockpit_start:mobile_cockpit_end]


def test_command_cockpit_overview_projects_stage_holo_floor():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-stage-holo-floor" in index
    assert "Command Cockpit Stage Holo Floor" in readme
    assert "function activeLaneStageHoloFloor(lane)" in app
    assert "const stageHoloFloor = activeLaneStageHoloFloor(lane);" in app
    assert 'class="active-lane-stage-holo-floor"' in app
    assert 'class="active-lane-stage-holo-runner"' in app
    assert 'class="active-lane-stage-holo-pad ${escapeHtml(pad.tone)}"' in app

    base_start = styles.index(".active-lane-stage-holo-floor")
    base_end = styles.index(".active-lane-stage-mote", base_start)
    assert "display: none;" in styles[base_start:base_end]

    floor_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-holo-floor'
    )
    floor_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-holo-floor::before',
        floor_start,
    )
    floor_slice = styles[floor_start:floor_end]
    assert "display: grid;" in floor_slice
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in floor_slice
    assert "bottom: 76px;" in floor_slice
    assert "height: 112px;" in floor_slice

    runner_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-holo-runner'
    )
    runner_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-holo-pad',
        runner_start,
    )
    runner_slice = styles[runner_start:runner_end]
    assert "left: clamp(18px, var(--floor-progress), calc(100% - 18px));" in runner_slice
    assert "animation: commandStageHoloRunnerPulse 1.7s ease-in-out infinite;" in runner_slice

    assert "@keyframes commandStageHoloFloorDrift" in styles
    assert "@keyframes commandStageHoloFloorSweep" in styles
    assert "@keyframes commandStageHoloPadWake" in styles

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_floor_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-holo-floor',
        mobile_start,
    )
    mobile_floor_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-holo-pad',
        mobile_floor_start,
    )
    mobile_floor_slice = styles[mobile_floor_start:mobile_floor_end]
    assert "bottom: 58px;" in mobile_floor_slice
    assert "display: none;" in mobile_floor_slice
    assert "height: 64px;" in mobile_floor_slice
    assert "opacity: 0.5;" in mobile_floor_slice


def test_command_cockpit_overview_uses_crew_chip_focus():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-crew-chip-focus" in index
    assert "Command Cockpit Crew Chip Focus" in readme

    chip_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-bot {\n  grid-template-columns: 38px minmax(0, 1fr);'
    )
    chip_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-bot-avatar',
        chip_start,
    )
    chip_slice = styles[chip_start:chip_end]
    assert "min-height: 50px;" in chip_slice
    assert "padding: 6px;" in chip_slice
    assert "overflow: hidden;" in chip_slice

    avatar_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-bot-avatar',
        chip_end,
    )
    avatar_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-bot-copy',
        avatar_start,
    )
    avatar_slice = styles[avatar_start:avatar_end]
    assert "width: 38px;" in avatar_slice
    assert "height: 38px;" in avatar_slice

    media_start = styles.index("@media (min-width: 861px)")
    fade_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .detail-content::after'
        ,
        media_start,
    )
    fade_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-control-matrix',
        fade_start,
    )
    fade_slice = styles[fade_start:fade_end]
    assert 'content: "";' in fade_slice
    assert "width: 54px;" in fade_slice
    assert "pointer-events: none;" in fade_slice


def test_command_cockpit_compacts_milestone_runway_into_level_strip():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-runway-level-strip" in index

    runway_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway')
    runway_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway-head',
        runway_start,
    )
    runway_slice = styles[runway_start:runway_end]
    assert "gap: 6px;" in runway_slice
    assert "padding: 7px;" in runway_slice

    head_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway-head')
    head_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway-head p:not(.eyebrow)',
        head_start,
    )
    head_slice = styles[head_start:head_end]
    assert "grid-template-columns: minmax(0, 1fr) minmax(154px, 0.48fr);" in head_slice
    assert "gap: 6px;" in head_slice

    head_copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway-head p:not(.eyebrow)')
    head_copy_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway-stats',
        head_copy_start,
    )
    assert "display: none;" in styles[head_copy_start:head_copy_end]

    stats_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway-stats span')
    stats_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-lens-row',
        stats_start,
    )
    stats_slice = styles[stats_start:stats_end]
    assert "min-height: 30px;" in stats_slice
    assert "padding: 4px 5px;" in stats_slice

    lens_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-lens-row')
    lens_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-lens {',
        lens_start,
    )
    lens_slice = styles[lens_start:lens_end]
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in lens_slice
    assert "gap: 4px;" in lens_slice

    lens_button_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-lens')
    lens_button_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-lens em',
        lens_button_start,
    )
    lens_button_slice = styles[lens_button_start:lens_button_end]
    assert "min-height: 30px;" in lens_button_slice
    assert "padding: 3px 5px;" in lens_button_slice

    lens_hint_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-lens em')
    lens_hint_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-track',
        lens_hint_start,
    )
    assert "display: none;" in styles[lens_hint_start:lens_hint_end]

    track_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-track')
    track_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-node',
        track_start,
    )
    track_slice = styles[track_start:track_end]
    assert "grid-auto-columns: minmax(112px, 132px);" in track_slice
    assert "min-height: 116px;" in track_slice
    assert "padding: 3px 1px 7px;" in track_slice

    node_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-node')
    node_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-node p',
        node_start,
    )
    node_slice = styles[node_start:node_end]
    assert "grid-template-rows: 24px minmax(0, 1fr);" in node_slice
    assert "min-height: 106px;" in node_slice
    assert "padding: 6px;" in node_slice

    node_copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-node p')
    node_copy_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway-actions',
        node_copy_start,
    )
    assert "-webkit-line-clamp: 2;" in styles[node_copy_start:node_copy_end]

    actions_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .milestone-runway-actions')
    actions_end = styles.index("@media", actions_start)
    actions_slice = styles[actions_start:actions_end]
    assert "gap: 4px;" in actions_slice
    assert "min-height: 26px;" in actions_slice

    assert "Command Cockpit Runway Level Strip" in readme


def test_command_cockpit_compacts_agent_party_into_crew_deck():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-crew-deck" in index

    board_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-board')
    board_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-summary',
        board_start,
    )
    board_slice = styles[board_start:board_end]
    assert "gap: 6px;" in board_slice
    assert "padding: 7px;" in board_slice

    summary_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-summary')
    summary_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-summary span',
        summary_start,
    )
    summary_slice = styles[summary_start:summary_end]
    assert "gap: 4px;" in summary_slice

    summary_chip_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-summary span')
    summary_chip_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-grid',
        summary_chip_start,
    )
    summary_chip_slice = styles[summary_chip_start:summary_chip_end]
    assert "min-height: 30px;" in summary_chip_slice
    assert "padding: 4px 5px;" in summary_chip_slice

    grid_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-grid')
    grid_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-card',
        grid_start,
    )
    grid_slice = styles[grid_start:grid_end]
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in grid_slice
    assert "gap: 6px;" in grid_slice

    card_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-card')
    card_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-top',
        card_start,
    )
    card_slice = styles[card_start:card_end]
    assert "gap: 6px;" in card_slice
    assert "padding: 7px;" in card_slice

    top_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-top')
    top_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-top .operator-avatar',
        top_start,
    )
    top_slice = styles[top_start:top_end]
    assert "grid-template-columns: 38px minmax(0, 1fr) 30px;" in top_slice
    assert "gap: 6px;" in top_slice

    avatar_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-top .operator-avatar')
    avatar_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-stats span',
        avatar_start,
    )
    avatar_slice = styles[avatar_start:avatar_end]
    assert "width: 38px;" in avatar_slice
    assert "height: 38px;" in avatar_slice

    stats_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-stats span')
    stats_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-card p',
        stats_start,
    )
    stats_slice = styles[stats_start:stats_end]
    assert "min-height: 28px;" in stats_slice
    assert "padding: 4px;" in stats_slice

    copy_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-card p')
    copy_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-thread',
        copy_start,
    )
    assert "display: none;" in styles[copy_start:copy_end]

    thread_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-thread')
    thread_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-actions',
        thread_start,
    )
    thread_slice = styles[thread_start:thread_end]
    assert "padding: 4px 6px;" in thread_slice

    actions_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .agent-party-actions')
    actions_end = styles.index("@media", actions_start)
    actions_slice = styles[actions_start:actions_end]
    assert "gap: 4px;" in actions_slice
    assert "min-height: 26px;" in actions_slice

    assert "Command Cockpit Crew Deck" in readme


def test_command_cockpit_locks_overview_stage_into_one_screen_stack():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-viewport-lock" in index
    assert "@keyframes commandOverviewModuleRunner" in styles

    panel_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-panel')
    panel_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content',
        panel_start,
    )
    panel_slice = styles[panel_start:panel_end]
    assert "display: grid;" in panel_slice
    assert "grid-template-rows: minmax(0, 1fr);" in panel_slice
    assert "height: min(660px, calc(100vh - 150px));" in panel_slice
    assert "overflow: hidden;" in panel_slice

    content_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content')
    content_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-level-hud',
        content_start,
    )
    content_slice = styles[content_start:content_end]
    assert "display: flex;" in content_slice
    assert "flex-direction: column;" in content_slice
    assert "min-height: 0;" in content_slice
    assert "height: 100%;" in content_slice

    stage_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage')
    stage_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage::after',
        stage_start,
    )
    stage_slice = styles[stage_start:stage_end]
    assert "flex: 1 1 auto;" in stage_slice
    assert "min-height: 0;" in stage_slice
    assert "max-height: none;" in stage_slice

    runner_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button.active::after')
    runner_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .detail-section',
        runner_start,
    )
    runner_slice = styles[runner_start:runner_end]
    assert "height: 2px;" in runner_slice
    assert "animation: commandOverviewModuleRunner 2.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in runner_slice

    assert "Command Cockpit Viewport Lock" in readme


def test_command_cockpit_overview_stage_dock_reads_as_level_compass():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-stage-compass" in index
    assert "Command Cockpit Stage Compass" in readme

    assert "const activeIndex = Math.max(0, stages.findIndex((stage) => stage.id === activeStage));" in app
    assert "--overview-stage-index:${activeIndex}; --overview-stage-count:${stages.length};" in app
    assert 'class="overview-stage-compass-runner"' in app
    assert 'style="--overview-stage-button-index:${index};"' in app

    dock_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-dock::after')
    dock_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-compass-runner',
        dock_start,
    )
    dock_slice = styles[dock_start:dock_end]
    assert "height: 2px;" in dock_slice
    assert "bottom: 5px;" in dock_slice

    runner_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-compass-runner')
    runner_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-meter',
        runner_start,
    )
    runner_slice = styles[runner_start:runner_end]
    assert "left: calc(((var(--overview-stage-index, 0) + 0.5) / max(1, var(--overview-stage-count, 1))) * 100%);" in runner_slice
    assert "animation: commandOverviewStageCompass 2.9s ease-in-out infinite;" in runner_slice

    buttons_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-buttons')
    buttons_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-buttons::after',
        buttons_start,
    )
    assert "position: relative;" in styles[buttons_start:buttons_end]

    buttons_rail_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-buttons::after',
        buttons_end,
    )
    buttons_rail_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-meter',
        buttons_rail_start,
    )
    buttons_rail_slice = styles[buttons_rail_start:buttons_rail_end]
    assert "height: 2px;" in buttons_rail_slice
    assert "bottom: 5px;" in buttons_rail_slice

    socket_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button::before')
    socket_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button.active::before',
        socket_start,
    )
    socket_slice = styles[socket_start:socket_end]
    assert "width: 5px;" in socket_slice
    assert "height: 5px;" in socket_slice

    active_socket_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button.active::before',
        socket_end,
    )
    active_socket_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button.active::after',
        active_socket_start,
    )
    assert "opacity: 1;" in styles[active_socket_start:active_socket_end]
    assert "@keyframes commandOverviewStageCompass" in styles

    mobile_runner_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-compass-runner',
        styles.index("@media (max-width: 860px)"),
    )
    mobile_runner_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button',
        mobile_runner_start,
    )
    mobile_runner_slice = styles[mobile_runner_start:mobile_runner_end]
    assert "width: 12px;" in mobile_runner_slice
    assert "height: 5px;" in mobile_runner_slice

    mobile_socket_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .overview-stage-button::before',
        mobile_runner_end,
    )
    mobile_socket_end = styles.index("}", mobile_socket_start)
    mobile_socket_slice = styles[mobile_socket_start:mobile_socket_end]
    assert "width: 4px;" in mobile_socket_slice
    assert "height: 4px;" in mobile_socket_slice


def test_command_cockpit_adds_bounded_stage_depth_rings():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-stage-depth-rings" in index
    assert "Command Cockpit Stage Depth Rings" in readme

    assert 'class="active-lane-stage-depth-rings"' in app
    assert 'style="--stage-depth-progress:${stageHoloFloor.progress}%;"' in app
    assert 'class="active-lane-stage-depth-ring primary"' in app
    assert 'class="active-lane-stage-depth-ring secondary"' in app
    assert 'class="active-lane-stage-depth-ring signal"' in app

    base_start = styles.index(".active-lane-stage-depth-rings")
    base_end = styles.index(".active-lane-stage-mote", base_start)
    base_slice = styles[base_start:base_end]
    assert "display: none;" in base_slice

    rings_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-depth-rings'
    )
    rings_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-holo-floor',
        rings_start,
    )
    rings_slice = styles[rings_start:rings_end]
    assert "inset: 42px 18px 76px;" in rings_slice
    assert "display: block;" in rings_slice
    assert "opacity: 0.44;" in rings_slice
    assert "mix-blend-mode: screen;" in rings_slice
    assert "rotateZ(calc(var(--stage-depth-progress) * 0.22deg))" in rings_slice
    assert "animation: commandStageDepthRingDrift" in rings_slice

    assert "@keyframes commandStageDepthRingDrift" in styles
    assert "@keyframes commandStageDepthRingPulse" in styles

    mobile_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-depth-rings',
        styles.index("@media (max-width: 860px)"),
    )
    mobile_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-depth-ring.secondary',
        mobile_start,
    )
    mobile_slice = styles[mobile_start:mobile_end]
    assert "inset: 50px 8px 62px;" in mobile_slice
    assert "opacity: 0.24;" in mobile_slice

    secondary_mobile_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-depth-ring.secondary',
        mobile_end,
    )
    secondary_mobile_end = styles.index("}", secondary_mobile_start)
    assert "display: none;" in styles[secondary_mobile_start:secondary_mobile_end]


def test_command_cockpit_overview_uses_world_map_strip():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-world-map-strip" in index
    assert "Command Cockpit World Map Strip" in readme

    assert "function activeLaneWorldMapNodes(" in app
    assert "const worldMapNodes = activeLaneWorldMapNodes" in app
    assert 'class="active-lane-world-map"' in app
    assert 'style="--world-progress:${laneXp}%;"' in app
    assert 'class="active-lane-world-runner"' in app
    assert 'class="active-lane-world-node ${escapeHtml(node.tone)}"' in app
    assert 'label: "World"' in app
    assert 'label: "Level"' in app
    assert 'label: "Quest"' in app
    assert 'label: "Proof"' in app
    assert 'label: "Gate"' in app
    assert 'label: "Bot"' in app

    base_start = styles.index(".active-lane-world-map")
    base_end = styles.index(".active-lane-world-map::before", base_start)
    assert "display: none;" in styles[base_start:base_end]

    arena_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-arena:is(.active-lane-level-hud *)'
    )
    arena_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-world-map',
        arena_start,
    )
    assert "display: none;" in styles[arena_start:arena_end]

    map_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-world-map',
        arena_end,
    )
    map_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-control-matrix',
        map_start,
    )
    map_slice = styles[map_start:map_end]
    assert "display: grid;" in map_slice
    assert "grid-column: 1 / -1;" in map_slice
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in map_slice
    assert "min-height: 42px;" in map_slice

    assert "@keyframes activeLaneWorldRunner" in styles
    assert "@keyframes activeLaneWorldNodeWake" in styles

    mobile_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-world-map',
        styles.index("@media (max-width: 860px)"),
    )
    mobile_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-world-map::-webkit-scrollbar',
        mobile_start,
    )
    mobile_slice = styles[mobile_start:mobile_end]
    assert "grid-auto-flow: column;" in mobile_slice
    assert "grid-auto-columns: minmax(64px, 1fr);" in mobile_slice
    assert "min-height: 32px;" in mobile_slice
    assert "padding: 3px;" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice
    assert "scrollbar-width: none;" in mobile_slice


def test_command_cockpit_overview_uses_stage_event_ribbon():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-stage-event-ribbon" in index
    assert "Command Cockpit Stage Event Ribbon" in readme

    assert "function activeLaneStageEventRibbon(lane)" in app
    assert "const stageEventRibbon = activeLaneStageEventRibbon(lane);" in app
    assert "${stageEventRibbon}" in app
    assert 'class="active-lane-stage-event-ribbon"' in app
    assert 'class="active-lane-stage-event-runner"' in app
    assert 'class="active-lane-stage-event-cell ${escapeHtml(cell.tone)}"' in app
    assert 'label: "event"' in app
    assert 'label: "proof"' in app
    assert 'label: "gate"' in app
    assert 'label: "next"' in app

    base_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-event-ribbon'
    )
    base_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-event-ribbon',
        base_start,
    )
    assert "display: none;" in styles[base_start:base_end]

    ribbon_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-event-ribbon'
    )
    runner_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-event-runner',
        ribbon_start,
    )
    ribbon_slice = styles[ribbon_start:runner_start]
    assert "position: sticky;" in ribbon_slice
    assert "display: grid;" in ribbon_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in ribbon_slice
    assert "min-height: 32px;" in ribbon_slice
    assert "margin-bottom: 5px;" in ribbon_slice

    runner_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-stage-event-cell',
        runner_start,
    )
    assert "animation: commandStageEventRibbonSweep 3.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles[runner_start:runner_end]
    assert "@keyframes commandStageEventRibbonSweep" in styles

    mobile_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-event-ribbon',
        styles.index("@media (max-width: 860px)"),
    )
    mobile_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] .active-lane-stage-event-ribbon::-webkit-scrollbar',
        mobile_start,
    )
    mobile_slice = styles[mobile_start:mobile_end]
    assert "grid-auto-flow: column;" in mobile_slice
    assert "grid-auto-columns: minmax(82px, 1fr);" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice
    assert "scrollbar-width: none;" in mobile_slice


def test_command_cockpit_overview_quest_field_reads_as_level_map():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-viewport-fit" in index
    assert "Command Cockpit Viewport Fit" in readme
    assert "20260619-command-cockpit-quest-node-focus" in index
    assert "Command Cockpit Quest Node Focus" in readme
    assert "20260619-command-cockpit-node-focus-lens" in index
    assert "Command Cockpit Node Focus Lens" in readme
    assert "20260619-command-cockpit-node-signal-packets" in index
    assert "Command Cockpit Node Signal Packets" in readme
    assert "20260619-command-cockpit-node-echo-rail" in index
    assert "Command Cockpit Node Echo Rail" in readme
    assert "20260619-command-cockpit-quest-level-map" in index
    assert "Command Cockpit Quest Level Map" in readme

    assert "questNodeFocusByLane" in app
    assert "function questFocusedRole(lane, fieldCells)" in app
    assert "function questFocusPackets(lane, data, cell)" in app
    assert "function questNodeEchoes(lane, data, cell, gateTitle, gateBody)" in app
    assert "function renderQuestNodeEchoRail(echoes, cell)" in app
    assert "function renderQuestFocusLens(cell, lane, data)" in app
    assert "const packets = questFocusPackets(lane, data, cell);" in app
    assert "const focusedEchoes = questNodeEchoes(lane, data, focusedCell, gateTitle, gateBody);" in app
    assert 'class="quest-board-stack"' in app
    assert 'class="quest-focus-lens ${escapeHtml(cell.tone)}"' in app
    assert 'class="quest-focus-packets"' in app
    assert 'class="quest-focus-packet"' in app
    assert 'data-packet-tone="${escapeHtml(packet.tone)}"' in app
    assert 'class="quest-node-echo-rail"' in app
    assert 'class="quest-node-echo"' in app
    assert 'data-quest-echo-role="${escapeHtml(cell?.role ?? "checkpoint")}"' in app
    assert 'data-echo-tone="${escapeHtml(echo.tone)}"' in app
    assert "${renderQuestNodeEchoRail(focusedEchoes, focusedCell)}" in app
    assert "world: [" in app
    assert "level: [" in app
    assert "checkpoint: [" in app
    assert "gate: [" in app
    assert "next: [" in app
    assert '{ label: "state", value: data.gate ? "review" : "clear"' in app
    assert '{ label: "brief", value: gateBody, tone: data.gate ? "gated" : "clear" }' in app
    assert 'data-quest-focus-node="${escapeHtml(cell.role)}"' in app
    assert 'data-quest-focused="${cell.focused ? "true" : "false"}"' in app
    assert 'aria-pressed="${cell.focused ? "true" : "false"}"' in app
    assert 'const questFocusNode = event.target.closest("[data-quest-focus-node]");' in app
    assert "state.questNodeFocusByLane = { ...state.questNodeFocusByLane, [state.selectedLaneId]: questFocusNode.dataset.questFocusNode };" in app

    assert 'aria-label="Quest level map"' in app
    assert 'style="--quest-field-count:${fieldCells.length};"' in app
    assert 'class="quest-field-map-route"' in app
    assert 'class="quest-field-socket"' in app
    assert 'class="quest-field-glyph"' in app
    assert 'role: stage.label.toLowerCase(),' in app
    assert 'glyph: stage.label === "Checkpoint" ? "ACT" : stage.label === "Level" ? "XP" : "MAP",' in app
    assert 'current: stage.label === "Checkpoint",' in app
    assert 'role: "gate",' in app
    assert 'glyph: data.gate ? "LOCK" : "OK",' in app
    assert 'current: Boolean(data.gate),' in app
    assert 'role: "next",' in app
    assert 'glyph: "GO",' in app
    assert 'data-quest-node="${escapeHtml(cell.role)}"' in app
    assert 'data-quest-current="${cell.current ? "true" : "false"}"' in app
    assert 'style="--quest-cell-index:${index}; --quest-cell-depth:${index % 2};"' in app

    base_route_start = styles.index(".quest-field-map-route")
    base_route_end = styles.index(".quest-field::after", base_route_start)
    base_route_slice = styles[base_route_start:base_route_end]
    assert "height: 22px;" in base_route_slice
    assert "transform: translateY(-50%) skewX(-7deg);" in base_route_slice
    assert ".quest-field-map-route::before" in base_route_slice

    socket_start = styles.index(".quest-field-socket")
    socket_end = styles.index(".quest-field-cell span", socket_start)
    socket_slice = styles[socket_start:socket_end]
    assert "width: 7px;" in socket_slice
    assert "height: 7px;" in socket_slice

    cockpit_field_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field'
    )
    cockpit_field_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field::before',
        cockpit_field_start,
    )
    cockpit_field_slice = styles[cockpit_field_start:cockpit_field_end]
    assert "isolation: isolate;" in cockpit_field_slice
    assert "perspective: 520px;" in cockpit_field_slice

    assert ".quest-board-stack" in styles
    assert ".quest-focus-lens" in styles
    assert ".quest-focus-rune" in styles
    assert ".quest-focus-packets" in styles
    assert ".quest-focus-packet" in styles
    assert '.quest-focus-packet[data-packet-tone="gated"]' in styles
    assert '.quest-focus-packet[data-packet-tone="clear"],' in styles
    assert ".quest-node-echo-rail" in styles
    assert ".quest-node-echo" in styles
    assert '.quest-node-echo[data-echo-tone="gated"]' in styles
    assert '.quest-node-echo[data-echo-tone="clear"],' in styles
    assert "@keyframes questNodeEchoSweep" in styles
    assert '.quest-field-cell[data-quest-focused="true"]' in styles
    assert '.quest-focus-lens[data-quest-focus-tone="gated"]' in styles
    assert "animation: questSignalBadgeSweep 4.4s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles

    cockpit_grid_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit'
    )
    cockpit_grid_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero',
        cockpit_grid_start,
    )
    cockpit_grid_slice = styles[cockpit_grid_start:cockpit_grid_end]
    assert "grid-template-columns: minmax(0, 1.04fr) minmax(260px, 0.62fr);" in cockpit_grid_slice
    assert "gap: 5px;" in cockpit_grid_slice

    stage_grid_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-stage-grid',
        cockpit_grid_end,
    )
    stage_grid_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-row',
        stage_grid_start,
    )
    assert "display: none;" in styles[stage_grid_start:stage_grid_end]

    signal_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal {',
        stage_grid_end,
    )
    signal_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal strong',
        signal_start,
    )
    signal_slice = styles[signal_start:signal_end]
    assert "grid-template-columns: auto minmax(0, 1fr);" in signal_slice
    assert "min-height: 28px;" in signal_slice
    assert "backdrop-filter: blur(10px);" in signal_slice

    cockpit_route_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-map-route',
        cockpit_field_end,
    )
    cockpit_route_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-runner',
        cockpit_route_start,
    )
    cockpit_route_slice = styles[cockpit_route_start:cockpit_route_end]
    assert "height: 28px;" in cockpit_route_slice
    assert "rotateX(54deg)" in cockpit_route_slice

    cockpit_stack_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-board-stack',
        cockpit_field_start,
    )
    cockpit_stack_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-board-stack > .quest-field',
        cockpit_stack_start,
    )
    cockpit_stack_slice = styles[cockpit_stack_start:cockpit_stack_end]
    assert "grid-area: command;" in cockpit_stack_slice
    assert "grid-template-rows: minmax(0, 1fr) auto;" in cockpit_stack_slice

    cockpit_echo_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-node-echo-rail',
        cockpit_stack_start,
    )
    cockpit_echo_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field::before',
        cockpit_echo_start,
    )
    cockpit_echo_slice = styles[cockpit_echo_start:cockpit_echo_end]
    assert "bottom: 4px;" in cockpit_echo_slice
    assert "min-height: 16px;" in cockpit_echo_slice
    assert "font-size: 0.44rem;" in cockpit_echo_slice

    cockpit_cell_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell',
        cockpit_route_end,
    )
    cockpit_cell_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell:nth-of-type(3)',
        cockpit_cell_start,
    )
    cockpit_cell_slice = styles[cockpit_cell_start:cockpit_cell_end]
    assert "transform: translateY(calc((var(--quest-cell-depth, 0) * 6px) - 3px));" in cockpit_cell_slice

    cockpit_lens_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-lens',
        cockpit_cell_end,
    )
    cockpit_lens_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-rune',
        cockpit_lens_start,
    )
    cockpit_lens_slice = styles[cockpit_lens_start:cockpit_lens_end]
    assert "grid-template-columns: 28px minmax(0, 1fr) minmax(110px, 0.44fr) minmax(118px, 0.52fr);" in cockpit_lens_slice
    assert "min-height: 34px;" in cockpit_lens_slice

    assert ".quest-field-glyph" in styles
    assert '.quest-field-cell[data-quest-current="true"]' in styles
    assert '.quest-field-cell[data-quest-current="true"] .quest-field-socket' in styles
    assert "animation: questFieldSocketPulse 2.1s ease-in-out infinite;" in styles
    assert '.quest-field-cell[data-quest-node="gate"] .quest-field-socket' in styles
    assert '.quest-field-cell[data-quest-node="next"] .quest-field-socket' in styles
    assert "@keyframes questFieldSocketPulse" in styles
    assert "font-size: 0.42rem;" in styles

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_route_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-map-route',
        mobile_start,
    )
    mobile_cell_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell',
        mobile_route_start,
    )
    mobile_route_slice = styles[mobile_route_start:mobile_cell_start]
    assert "height: 18px;" in mobile_route_slice
    assert "skewX(-5deg)" in mobile_route_slice

    mobile_stack_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-board-stack',
        mobile_start,
    )
    mobile_stack_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-depth-stack',
        mobile_stack_start,
    )
    assert "gap: 3px;" in styles[mobile_stack_start:mobile_stack_end]

    mobile_socket_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-socket',
        mobile_cell_start,
    )
    mobile_socket_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage',
        mobile_socket_start,
    )
    assert "display: none;" in styles[mobile_socket_start:mobile_socket_end]

    mobile_glyph_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-glyph',
        mobile_cell_start,
    )
    mobile_glyph_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage',
        mobile_glyph_start,
    )
    assert "display: none;" in styles[mobile_glyph_start:mobile_glyph_end]

    mobile_lens_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-lens',
        mobile_start,
    )
    mobile_lens_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-rune',
        mobile_lens_start,
    )
    mobile_lens_slice = styles[mobile_lens_start:mobile_lens_end]
    assert "grid-template-columns: 22px minmax(0, 1fr) minmax(68px, 0.36fr) minmax(76px, 0.44fr);" in mobile_lens_slice
    assert "min-height: 30px;" in mobile_lens_slice
    mobile_packet_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-packets',
        mobile_lens_start,
    )
    mobile_packet_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage',
        mobile_packet_start,
    )
    mobile_packet_slice = styles[mobile_packet_start:mobile_packet_end]
    assert "gap: 2px;" in mobile_packet_slice
    assert "min-height: 18px;" in mobile_packet_slice
    assert "display: none;" in mobile_packet_slice
    assert ".quest-node-echo-rail" in mobile_packet_slice
    assert "min-height: 14px;" in mobile_packet_slice
    assert "font-size: 0.38rem;" in mobile_packet_slice


def test_command_cockpit_overview_signal_strip_reads_as_unlock_badges():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-unlock-badges" in index
    assert "Command Cockpit Unlock Badges" in readme

    assert 'glyph: blockerPressure ? "GATE" : "OPEN"' in app
    assert 'glyph: "WIN"' in app
    assert 'glyph: "RUN"' in app
    assert 'glyph: "XP"' in app
    assert 'data-quest-signal-state="${escapeHtml(signal.state)}"' in app
    assert 'style="--quest-signal-index:${index};"' in app
    assert 'class="quest-signal-glyph"' in app
    assert 'class="quest-signal-shine"' in app

    signal_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-glyph'
    )
    signal_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-shine',
        signal_start,
    )
    signal_slice = styles[signal_start:signal_end]
    assert "width: 28px;" in signal_slice
    assert "height: 20px;" in signal_slice
    assert "font-size: 0.44rem;" in signal_slice

    shine_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-shine',
        signal_end,
    )
    shine_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal[data-quest-signal-state="locked"]',
        shine_start,
    )
    shine_slice = styles[shine_start:shine_end]
    assert "animation: questSignalBadgeSweep 3.6s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in shine_slice
    assert "animation-delay: calc(var(--quest-signal-index, 0) * -0.42s);" in shine_slice
    assert "@keyframes questSignalBadgeSweep" in styles

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_badge_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-glyph',
        mobile_start,
    )
    mobile_badge_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal strong',
        mobile_badge_start,
    )
    mobile_badge_slice = styles[mobile_badge_start:mobile_badge_end]
    assert "width: 22px;" in mobile_badge_slice
    assert "height: 17px;" in mobile_badge_slice


def test_command_cockpit_hero_has_lane_minigame_sigil():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-minigame-sigil" in index
    assert "Command Cockpit Minigame Sigil" in readme

    assert "function questMinigameSigil(lane)" in app
    assert "const minigame = lane.visual?.minigame ?? {};" in app
    assert 'const stinger = arcadeStingerType(lane);' in app
    assert 'const minigameSigil = questMinigameSigil(lane);' in app
    assert '${minigameSigil}' in app
    assert 'class="quest-minigame-sigil"' in app
    assert 'data-quest-minigame="${escapeHtml(stinger)}"' in app
    assert 'class="quest-minigame-orbit"' in app

    assert ".quest-minigame-sigil" in styles
    assert ".quest-minigame-orbit" in styles
    assert "animation: questMinigameSigilOrbit 4.2s linear infinite;" in styles
    assert "animation: questMinigameSigilGlint 3.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles
    assert '@keyframes questMinigameSigilOrbit' in styles
    assert '@keyframes questMinigameSigilGlint' in styles
    assert '.quest-minigame-sigil[data-quest-minigame="route"]' in styles
    assert '.quest-minigame-sigil[data-quest-minigame="scan"]' in styles

    hero_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-cockpit-hero')
    hero_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-avatar', hero_start)
    hero_slice = styles[hero_start:hero_end]
    assert "grid-template-columns: 40px minmax(0, 1fr) 40px 44px;" in hero_slice

    sigil_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-minigame-sigil')
    sigil_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .quest-minigame-sigil em', sigil_start)
    sigil_slice = styles[sigil_start:sigil_end]
    assert "width: 40px;" in sigil_slice
    assert "height: 40px;" in sigil_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_hero_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero',
        mobile_start,
    )
    mobile_hero_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit-hero::after',
        mobile_hero_start,
    )
    mobile_hero_slice = styles[mobile_hero_start:mobile_hero_end]
    assert "grid-template-columns: 32px minmax(0, 1fr) 32px 38px;" in mobile_hero_slice

    mobile_sigil_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-minigame-sigil',
        mobile_start,
    )
    mobile_sigil_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-minigame-sigil strong',
        mobile_sigil_start,
    )
    mobile_sigil_slice = styles[mobile_sigil_start:mobile_sigil_end]
    assert "width: 32px;" in mobile_sigil_slice
    assert "height: 32px;" in mobile_sigil_slice

    mobile_sigil_em_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-minigame-sigil em',
        mobile_sigil_end,
    )
    mobile_sigil_em_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-minigame-orbit',
        mobile_sigil_em_start,
    )
    assert "display: none;" in styles[mobile_sigil_em_start:mobile_sigil_em_end]

    mobile_signal_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal-row',
        mobile_start,
    )
    mobile_signal_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-signal {',
        mobile_signal_start,
    )
    mobile_signal_slice = styles[mobile_signal_start:mobile_signal_end]
    assert "grid-area: signals;" in mobile_signal_slice
    assert "margin: 0;" in mobile_signal_slice


def test_command_cockpit_quest_field_has_path_depth_stack():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-path-depth-stack" in index
    assert "Command Cockpit Path Depth Stack" in readme

    assert "function questDepthLayers(lane, data, gateTitle)" in app
    assert "function renderQuestDepthStack(layers)" in app
    assert 'class="quest-depth-stack"' in app
    assert 'class="quest-depth-layer"' in app
    assert 'data-depth-tone="${escapeHtml(layer.tone)}"' in app
    assert 'style="--quest-depth-index:${index};"' in app
    assert '${renderQuestDepthStack(depthLayers)}' in app
    assert '{ label: "latest"' in app
    assert '{ label: "levels"' in app
    assert '{ label: "gates"' in app
    assert '{ label: "next"' in app

    assert ".quest-depth-stack" in styles
    assert ".quest-depth-layer" in styles
    assert "@keyframes questDepthLayerSweep" in styles
    assert "animation: questDepthLayerSweep 4.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles
    assert '.quest-depth-layer[data-depth-tone="gated"]' in styles
    assert '.quest-depth-layer[data-depth-tone="earned"],' in styles

    depth_start = styles.index("\n.quest-depth-stack {")
    depth_end = styles.index(".quest-depth-layer", depth_start)
    depth_slice = styles[depth_start:depth_end]
    assert "position: absolute;" in depth_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in depth_slice
    assert "pointer-events: none;" in depth_slice

    cockpit_depth_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-depth-stack'
    )
    cockpit_depth_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-depth-layer',
        cockpit_depth_start,
    )
    cockpit_depth_slice = styles[cockpit_depth_start:cockpit_depth_end]
    assert "top: 4px;" in cockpit_depth_slice
    assert "gap: 3px;" in cockpit_depth_slice

    cockpit_cell_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell'
    )
    cockpit_cell_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell:nth-of-type(3)',
        cockpit_cell_start,
    )
    assert "padding: 18px 6px 17px;" in styles[cockpit_cell_start:cockpit_cell_end]

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_depth_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-depth-stack',
        mobile_start,
    )
    mobile_depth_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-depth-layer',
        mobile_depth_start,
    )
    mobile_depth_slice = styles[mobile_depth_start:mobile_depth_end]
    assert "grid-template-columns: repeat(4, minmax(34px, 1fr));" in mobile_depth_slice
    assert "gap: 2px;" in mobile_depth_slice

    mobile_depth_label_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-depth-layer i',
        mobile_depth_end,
    )
    mobile_depth_label_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-depth-layer strong',
        mobile_depth_label_start,
    )
    assert "display: none;" in styles[mobile_depth_label_start:mobile_depth_label_end]


def test_command_cockpit_quest_field_has_focus_beam():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    focus_asset = ROOT / "web/assets/system/command-cockpit-focus-beam-20260619.png"

    assert "20260619-command-cockpit-focus-beam" in index
    assert "Command Cockpit Focus Beam" in readme
    assert focus_asset.exists()
    assert focus_asset.stat().st_size > 200_000

    assert "function renderQuestFocusBeam(cell, index, count)" in app
    assert "const focusX = count ? ((index + 0.5) / count) * 100 : 50;" in app
    assert "const focusedIndex = Math.max(0, focusedFieldCells.findIndex((cell) => cell.role === focusedCell?.role));" in app
    assert "${renderQuestFocusBeam(focusedCell, focusedIndex, focusedFieldCells.length)}" in app
    assert 'class="quest-focus-beam"' in app
    assert 'data-quest-focus-beam="${escapeHtml(cell?.role ?? "checkpoint")}"' in app
    assert 'data-quest-focus-tone="${escapeHtml(cell?.tone ?? "live")}"' in app
    assert "--quest-focus-x:${focusX.toFixed(2)}%;" in app
    assert "--quest-focus-w:${focusW.toFixed(2)}%;" in app
    assert "command-cockpit-focus-beam-20260619.png" in app
    assert "system-command-cockpit-focus-beam" in app

    assert ".quest-focus-beam" in styles
    assert ".quest-focus-beam::before," in styles
    assert "@keyframes questFocusBeamScan" in styles
    assert "@keyframes questFocusBeamPulse" in styles
    assert "animation: questFocusBeamScan 4.6s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles
    assert "animation: questFocusBeamPulse 2.8s ease-in-out infinite;" in styles
    assert '.quest-focus-beam[data-quest-focus-beam="gate"],' in styles
    assert '.quest-focus-beam[data-quest-focus-beam="next"],' in styles

    beam_start = styles.index("\n.quest-focus-beam {")
    beam_end = styles.index(".quest-focus-beam::before,", beam_start)
    beam_slice = styles[beam_start:beam_end]
    assert "position: absolute;" in beam_slice
    assert "left: var(--quest-focus-x, 50%);" in beam_slice
    assert "width: calc(var(--quest-focus-w, 20%) - 8px);" in beam_slice
    assert "pointer-events: none;" in beam_slice

    cockpit_beam_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-beam'
    )
    cockpit_beam_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell',
        cockpit_beam_start,
    )
    cockpit_beam_slice = styles[cockpit_beam_start:cockpit_beam_end]
    assert "top: 5px;" in cockpit_beam_slice
    assert "width: calc(var(--quest-focus-w, 20%) - 6px);" in cockpit_beam_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_beam_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-beam',
        mobile_start,
    )
    mobile_beam_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell',
        mobile_beam_start,
    )
    mobile_beam_slice = styles[mobile_beam_start:mobile_beam_end]
    assert "top: 4px;" in mobile_beam_slice
    assert "width: calc(var(--quest-focus-w, 20%) - 5px);" in mobile_beam_slice
    assert "opacity: 0.5;" in mobile_beam_slice


def test_command_cockpit_focus_lens_has_crew_relay():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    crew_asset = ROOT / "web/assets/system/command-cockpit-crew-relay-20260619.png"

    assert "20260619-command-cockpit-crew-relay" in index
    assert "Command Cockpit Crew Relay" in readme
    assert crew_asset.exists()
    assert crew_asset.stat().st_size > 50_000

    assert "function questCrewRelayRecord(lane)" in app
    assert "const records = agentPartyRecords(lane);" in app
    assert "const readiness = crewReadiness(record);" in app
    assert "function renderQuestCrewRelay(record, lane)" in app
    assert "const crew = questCrewRelayRecord(lane);" in app
    assert "${renderQuestCrewRelay(crew, lane)}" in app
    assert 'class="quest-crew-relay ${escapeHtml(tone)}"' in app
    assert "quest-crew-relay-avatar" in app
    assert 'class="quest-crew-relay-action"' in app
    assert 'data-detail-view="comms"' in app
    assert "command-cockpit-crew-relay-20260619.png" in app
    assert "system-command-cockpit-crew-relay" in app

    assert ".quest-crew-relay" in styles
    assert ".quest-crew-relay::after" in styles
    assert ".quest-crew-relay-avatar" in styles
    assert ".quest-crew-relay-action" in styles
    assert "@keyframes questCrewRelaySweep" in styles
    assert "animation: questCrewRelaySweep 4.9s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles
    assert ".quest-crew-relay.gated" in styles
    assert ".quest-crew-relay.ready," in styles

    lens_start = styles.index("\n.quest-focus-lens {")
    lens_end = styles.index(".quest-focus-lens::after", lens_start)
    lens_slice = styles[lens_start:lens_end]
    assert "grid-template-columns: 34px minmax(0, 1fr) minmax(132px, 0.5fr) minmax(132px, 0.58fr);" in lens_slice

    relay_start = styles.index("\n.quest-crew-relay {")
    relay_end = styles.index(".quest-crew-relay::after", relay_start)
    relay_slice = styles[relay_start:relay_end]
    assert "grid-template-columns: 25px minmax(0, 1fr) 34px;" in relay_slice
    assert "min-height: 28px;" in relay_slice
    assert "command-cockpit-crew-relay-20260619.png" in relay_slice

    cockpit_relay_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-crew-relay'
    )
    cockpit_relay_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-packet',
        cockpit_relay_start,
    )
    cockpit_relay_slice = styles[cockpit_relay_start:cockpit_relay_end]
    assert "grid-template-columns: 22px minmax(0, 1fr) 30px;" in cockpit_relay_slice
    assert "display: none;" in cockpit_relay_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_lens_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-lens',
        mobile_start,
    )
    mobile_lens_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-rune',
        mobile_lens_start,
    )
    mobile_lens_slice = styles[mobile_lens_start:mobile_lens_end]
    assert "grid-template-columns: 22px minmax(0, 1fr) minmax(68px, 0.36fr) minmax(76px, 0.44fr);" in mobile_lens_slice

    mobile_relay_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-crew-relay',
        mobile_lens_end,
    )
    mobile_relay_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-packets',
        mobile_relay_start,
    )
    mobile_relay_slice = styles[mobile_relay_start:mobile_relay_end]
    assert "grid-template-columns: 18px minmax(0, 1fr) 24px;" in mobile_relay_slice
    assert "min-height: 22px;" in mobile_relay_slice
    assert "font-size: 0.32rem;" in mobile_relay_slice


def test_command_cockpit_quest_nodes_have_status_halos():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    halo_asset = ROOT / "web/assets/system/command-cockpit-node-halos-20260619.png"

    assert "20260619-command-cockpit-node-halos" in index
    assert "Command Cockpit Node Halos" in readme
    assert halo_asset.exists()
    assert halo_asset.stat().st_size > 100_000

    assert "function questNodeHalos(lane, data, role)" in app
    assert "const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);" in app
    assert "function questFieldCells(lane, data, gateTitle, gateBody)" in app
    assert "const fieldCells = questFieldCells(lane, data, gateTitle, gateBody);" in app
    assert "halos: questNodeHalos(lane, data, stage.label.toLowerCase())," in app
    assert "halos: questNodeHalos(lane, data, \"gate\")," in app
    assert "halos: questNodeHalos(lane, data, \"next\")," in app
    assert 'class="quest-node-halos"' in app
    assert 'class="quest-node-halo"' in app
    assert 'data-node-halo-tone="${escapeHtml(halo.tone)}"' in app
    assert "--quest-node-halo-art:url('./assets/system/command-cockpit-node-halos-20260619.png');" in app
    assert "system-command-cockpit-node-halos" in app

    assert ".quest-node-halos" in styles
    assert ".quest-node-halo" in styles
    assert ".quest-node-halo::after" in styles
    assert "@keyframes questNodeHaloSweep" in styles
    assert "animation: questNodeHaloSweep 4.7s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles
    assert '.quest-node-halo[data-node-halo-tone="gated"]' in styles
    assert '.quest-node-halo[data-node-halo-tone="earned"],' in styles
    assert "command-cockpit-node-halos-20260619.png" in styles

    halo_start = styles.index("\n.quest-node-halos {")
    halo_end = styles.index(".quest-node-halo {", halo_start)
    halo_slice = styles[halo_start:halo_end]
    assert "position: absolute;" in halo_slice
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in halo_slice
    assert "pointer-events: none;" in halo_slice

    cockpit_cell_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell'
    )
    cockpit_cell_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell:hover',
        cockpit_cell_start,
    )
    cockpit_cell_slice = styles[cockpit_cell_start:cockpit_cell_end]
    assert "padding: 18px 6px 17px;" in cockpit_cell_slice

    cockpit_halo_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-node-halos'
    )
    cockpit_halo_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-lens',
        cockpit_halo_start,
    )
    cockpit_halo_slice = styles[cockpit_halo_start:cockpit_halo_end]
    assert "bottom: 4px;" in cockpit_halo_slice
    assert "min-height: 13px;" in cockpit_halo_slice
    assert "display: none;" in cockpit_halo_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_cell_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell',
        mobile_start,
    )
    mobile_cell_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-field-cell:hover',
        mobile_cell_start,
    )
    mobile_cell_slice = styles[mobile_cell_start:mobile_cell_end]
    assert "padding: 14px 5px 16px;" in mobile_cell_slice

    mobile_halo_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-node-halos',
        mobile_start,
    )
    mobile_halo_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-focus-lens',
        mobile_halo_start,
    )
    mobile_halo_slice = styles[mobile_halo_start:mobile_halo_end]
    assert "bottom: 3px;" in mobile_halo_slice
    assert "min-height: 12px;" in mobile_halo_slice
    assert "font-size: 0.3rem;" in mobile_halo_slice


def test_command_cockpit_quest_field_has_event_pulse_packets():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    pulse_asset = ROOT / "web/assets/system/command-cockpit-event-pulse-20260619.png"

    assert "20260619-command-cockpit-event-pulse" in index
    assert "Command Cockpit Event Pulse" in readme
    assert pulse_asset.exists()
    assert pulse_asset.stat().st_size > 100_000

    assert "function questEventPulseTone(item)" in app
    assert "function questEventPulsePackets(lane, data, focusedCell)" in app
    assert "function renderQuestEventPulse(packets, cell, activeIndex = 0)" in app
    assert "questEventFocusByLane: {}" in app
    assert "const eventPulsePackets = questEventPulsePackets(lane, data, focusedCell);" in app
    assert "const eventPulseIndex = Math.max(0, Math.min(eventPulsePackets.length - 1, state.questEventFocusByLane[lane.id] ?? 0));" in app
    assert "${renderQuestEventPulse(eventPulsePackets, focusedCell, eventPulseIndex)}" in app
    assert 'class="quest-event-pulse"' in app
    assert 'class="quest-event-lens"' in app
    assert 'class="quest-event-packet"' in app
    assert 'data-quest-event-focus="${index}"' in app
    assert 'data-event-pulse-active="${index === activeIndex ? "true" : "false"}"' in app
    assert 'data-event-pulse-tone="${escapeHtml(packet.tone)}"' in app
    assert 'const questEventFocus = event.target.closest("[data-quest-event-focus]");' in app
    assert "state.questEventFocusByLane = { ...state.questEventFocusByLane, [state.selectedLaneId]: Number.isFinite(focusIndex) ? focusIndex : 0 };" in app
    assert "--quest-event-pulse-art:url('./assets/system/command-cockpit-event-pulse-20260619.png');" in app
    assert "system-command-cockpit-event-pulse" in app

    assert ".quest-event-pulse" in styles
    assert ".quest-event-lens" in styles
    assert ".quest-event-packet" in styles
    assert ".quest-event-packet::after" in styles
    assert "@keyframes questEventLensSweep" in styles
    assert "@keyframes questEventPulseScan" in styles
    assert "@keyframes questEventPacketPulse" in styles
    assert "@keyframes questEventPacketDrift" in styles
    assert '.quest-event-packet[data-event-pulse-active="true"]' in styles
    assert '.quest-event-packet[data-event-pulse-tone="gated"]' in styles
    assert '.quest-event-packet[data-event-pulse-tone="earned"]' in styles
    assert "command-cockpit-event-pulse-20260619.png" in styles

    pulse_start = styles.index("\n.quest-event-pulse {")
    pulse_end = styles.index(".quest-event-pulse::after", pulse_start)
    pulse_slice = styles[pulse_start:pulse_end]
    assert "position: absolute;" in pulse_slice
    assert "pointer-events: none;" in pulse_slice
    assert "mix-blend-mode: screen;" in pulse_slice

    lens_start = styles.index("\n.quest-event-lens {")
    lens_end = styles.index(".quest-event-lens::after", lens_start)
    lens_slice = styles[lens_start:lens_end]
    assert "position: absolute;" in lens_slice
    assert "left: min(max(var(--event-pulse-x, 50%), 18%), 82%);" in lens_slice
    assert "width: min(138px, 48%);" in lens_slice

    packet_start = styles.index("\n.quest-event-packet {")
    packet_end = styles.index(".quest-event-packet::after", packet_start)
    packet_slice = styles[packet_start:packet_end]
    assert "left: var(--event-pulse-x, 50%);" in packet_slice
    assert "top: var(--event-pulse-y, 50%);" in packet_slice
    assert "pointer-events: auto;" in packet_slice
    assert "cursor: pointer;" in packet_slice
    assert "animation:" in packet_slice

    cockpit_pulse_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-event-pulse'
    )
    cockpit_pulse_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-event-packet',
        cockpit_pulse_start,
    )
    cockpit_pulse_slice = styles[cockpit_pulse_start:cockpit_pulse_end]
    assert "opacity: 0.38;" in cockpit_pulse_slice
    assert "transform: rotateX(42deg);" in cockpit_pulse_slice
    assert "width: min(116px, 42%);" in cockpit_pulse_slice
    assert "display: none;" in cockpit_pulse_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_pulse_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-event-pulse',
        mobile_start,
    )
    mobile_pulse_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-event-packet',
        mobile_pulse_start,
    )
    mobile_pulse_slice = styles[mobile_pulse_start:mobile_pulse_end]
    assert "opacity: 0.28;" in mobile_pulse_slice
    assert "transform: none;" in mobile_pulse_slice
    assert "left: 50%;" in mobile_pulse_slice
    assert "width: min(104px, 56%);" in mobile_pulse_slice


def test_command_cockpit_quest_field_has_insight_ribbon():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    insight_asset = ROOT / "web/assets/system/command-cockpit-insight-ribbon-20260619.png"

    assert "20260619-command-cockpit-insight-ribbon" in index
    assert "Command Cockpit Insight Ribbon" in readme
    assert insight_asset.exists()
    assert insight_asset.stat().st_size > 100_000

    assert "function questInsightRibbonSignals(lane, data, cell, gateTitle, gateBody)" in app
    assert "function renderQuestInsightRibbon(signals, cell)" in app
    assert "const focusedInsights = questInsightRibbonSignals(lane, data, focusedCell, gateTitle, gateBody);" in app
    assert "${renderQuestInsightRibbon(focusedInsights, focusedCell)}" in app
    assert 'class="quest-insight-ribbon"' in app
    assert 'class="quest-insight-chip"' in app
    assert 'data-quest-insight-role="${escapeHtml(cell?.role ?? "checkpoint")}"' in app
    assert 'data-insight-tone="${escapeHtml(signal.tone)}"' in app
    assert "system-command-cockpit-insight-ribbon" in app
    assert "command-cockpit-insight-ribbon-20260619.png" in app
    assert "command-cockpit-insight-ribbon-20260619.png" in readme

    assert ".quest-insight-ribbon" in styles
    assert ".quest-insight-chip" in styles
    assert "@keyframes questInsightRibbonSweep" in styles
    assert "animation: questInsightRibbonSweep 5.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles
    assert '.quest-insight-chip[data-insight-tone="gated"]' in styles
    assert '.quest-insight-chip[data-insight-tone="clear"],' in styles

    ribbon_start = styles.index("\n.quest-insight-ribbon {")
    ribbon_end = styles.index(".quest-insight-ribbon::after", ribbon_start)
    ribbon_slice = styles[ribbon_start:ribbon_end]
    assert "position: absolute;" in ribbon_slice
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in ribbon_slice
    assert "pointer-events: none;" in ribbon_slice

    cockpit_ribbon_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-insight-ribbon'
    )
    cockpit_ribbon_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-insight-chip',
        cockpit_ribbon_start,
    )
    cockpit_ribbon_slice = styles[cockpit_ribbon_start:cockpit_ribbon_end]
    assert "top: 26px;" in cockpit_ribbon_slice
    assert "min-height: 22px;" in cockpit_ribbon_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_ribbon_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-insight-ribbon',
        mobile_start,
    )
    mobile_ribbon_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-insight-chip',
        mobile_ribbon_start,
    )
    mobile_ribbon_slice = styles[mobile_ribbon_start:mobile_ribbon_end]
    assert "top: 23px;" in mobile_ribbon_slice
    assert "grid-template-columns: repeat(6, minmax(32px, 1fr));" in mobile_ribbon_slice

    mobile_chip_text_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-insight-chip strong',
        mobile_ribbon_end,
    )
    mobile_chip_text_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"]',
        mobile_chip_text_start,
    )
    assert "display: none;" in styles[mobile_chip_text_start:mobile_chip_text_end]


def test_command_cockpit_stable_board_reduces_jumps_and_scroll_height():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-stable-board" in index
    assert "Command Cockpit Stable Board" in readme
    assert "function cockpitKeepsViewportStable()" in app
    assert 'state.activeAtlasDeck === "command" && state.activeAtlasStage === "cockpit"' in app
    assert "function settleDetailPanelIntoView()" in app
    assert "if (cockpitKeepsViewportStable()) return;" in app
    assert "settleDetailPanelIntoView();" in app

    assert "@keyframes commandCockpitBoardScan" in styles
    assert "animation: commandCockpitBoardScan 6.4s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles

    workspace_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .workspace'
    )
    workspace_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .lane-list-panel',
        workspace_start,
    )
    workspace_slice = styles[workspace_start:workspace_end]
    assert "grid-template-columns: minmax(128px, 0.26fr) minmax(0, 1fr);" in workspace_slice
    assert "min-height: min(616px, calc(100vh - 206px));" in workspace_slice

    hud_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-level-hud'
    )
    hud_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-hud-core',
        hud_start,
    )
    hud_slice = styles[hud_start:hud_end]
    assert "height: 72px;" in hud_slice
    assert "min-height: 72px;" in hud_slice
    assert "margin-bottom: 4px;" in hud_slice

    stage_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] {',
        hud_end,
    )
    stage_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] > .detail-section:first-of-type',
        stage_start,
    )
    stage_slice = styles[stage_start:stage_end]
    assert "flex: 1 1 0;" in stage_slice
    assert "overflow: hidden;" in stage_slice

    section_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .active-lane-mounted-stage[data-active-stage-view="overview"] > .detail-section:first-of-type'
    )
    section_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .overview-stage-dock',
        section_start,
    )
    section_slice = styles[section_start:section_end]
    assert "display: flex;" in section_slice
    assert "border-bottom: 0;" in section_slice

    board_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit {',
        section_end,
    )
    board_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .detail-content.detail-view-overview .quest-cockpit::after',
        board_start,
    )
    board_slice = styles[board_start:board_end]
    assert "flex: 1 1 0;" in board_slice
    assert "overflow: hidden;" in board_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_shell_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .app-shell',
        mobile_start,
    )
    mobile_shell_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .topbar',
        mobile_shell_start,
    )
    assert "padding-bottom: 12px;" in styles[mobile_shell_start:mobile_shell_end]

    mobile_stable_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .workspace',
        mobile_start,
    )
    mobile_stable_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .lane-list-panel',
        mobile_stable_start,
    )
    mobile_workspace_slice = styles[mobile_stable_start:mobile_stable_end]
    assert "grid-template-columns: 1fr;" in mobile_workspace_slice
    assert "min-height: min(632px, calc(100vh - 104px));" in mobile_workspace_slice

    mobile_panel_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .detail-panel',
        mobile_stable_start,
    )
    mobile_panel_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"] .active-lane-level-hud',
        mobile_panel_start,
    )
    mobile_panel_slice = styles[mobile_panel_start:mobile_panel_end]
    assert "grid-column: 1;" in mobile_panel_slice
    assert "height: min(540px, calc(100vh - 230px));" in mobile_panel_slice
