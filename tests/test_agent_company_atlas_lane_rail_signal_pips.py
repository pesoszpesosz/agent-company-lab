from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_lane_rail_cards_show_compact_signal_pips():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function laneRailSignalMarkup(lane)" in app
    assert "function orderedLaneRailLanes(lanes)" in app
    assert "const lanes = orderedLaneRailLanes(filteredLanes());" in app
    assert "lane.id === state.selectedLaneId" in app[app.index("function orderedLaneRailLanes") : app.index("function laneRailSignalMarkup")]
    assert "${laneRailSignalMarkup(lane)}" in app
    assert 'data-lane-state="${escapeHtml(lane.state)}"' in app
    assert "--lane-progress:${boundedProgress(lane.progress ?? 0)}%;" in app
    assert 'class="lane-rail-signal"' in app
    assert 'class="lane-rail-pip level"' in app
    assert 'class="lane-rail-pip progress"' in app
    assert 'class="lane-rail-pip gates"' in app

    for token in [
        ".lane-rail-signal",
        ".lane-rail-signal::before",
        ".lane-rail-pip",
        ".lane-button.active .lane-rail-pip",
        ".lane-button[data-lane-state=\"gated\"] .lane-rail-pip.gates",
        "laneRailSignalSweep",
        "laneRailPipWake",
    ]:
        assert token in styles

    reduced_motion = styles[styles.index("@media (prefers-reduced-motion: reduce)") :]
    assert ".lane-rail-signal::before" in reduced_motion
    assert ".lane-rail-pip" in reduced_motion

    assert "Lane Rail Signal Pips" in readme
    assert "20260619-lane-rail-signal-pips" in index


def test_lane_rail_cards_show_level_selector_tray():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-lane-rail-level-selector" in index
    assert "function laneRailLevelSelectorMarkup(lane)" in app
    assert "${laneRailLevelSelectorMarkup(lane)}" in app

    selector_start = app.index("function laneRailLevelSelectorMarkup(lane)")
    selector_end = app.index("function laneRailSignalMarkup(lane)", selector_start)
    selector_slice = app[selector_start:selector_end]
    assert "const gateCount = (counts.blockers ?? 0) + (counts.pendingRequests ?? 0);" in selector_slice
    assert "const rewardCount = counts.outcomes ?? 0;" in selector_slice
    assert "const activeCount = counts.activeTasks ?? 0;" in selector_slice
    assert 'class="lane-level-selector"' in selector_slice
    assert 'class="lane-level-cell level"' in selector_slice
    assert 'class="lane-level-cell gate ${gateCount ? "gated" : "clear"}"' in selector_slice
    assert 'class="lane-level-cell reward"' in selector_slice
    assert 'class="lane-level-cell active"' in selector_slice

    selector_css_start = styles.index("\n.lane-level-selector {\n")
    selector_css_end = styles.index(".lane-rail-signal", selector_css_start)
    selector_css_slice = styles[selector_css_start:selector_css_end]
    assert "grid-template-columns: 0.78fr 0.86fr 0.86fr 0.86fr;" in selector_css_slice
    assert "min-height: 42px;" in selector_css_slice
    assert ".lane-level-cell" in selector_css_slice
    assert ".lane-level-cell.gated" in selector_css_slice
    assert ".lane-button.active .lane-level-selector" in selector_css_slice

    reduced_motion = styles[styles.index("@media (prefers-reduced-motion: reduce)") :]
    assert ".lane-level-selector::before" in reduced_motion

    assert "Lane Rail Level Selector" in readme


def test_command_cockpit_lane_rail_uses_selector_without_redundant_chrome():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-lane-selector-compression" in index

    compact_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button')
    compact_end = styles.index(".lane-list", compact_start)
    compact_slice = styles[compact_start:compact_end]
    assert "min-height: 52px;" in compact_slice
    assert "padding: 5px 4px;" in compact_slice

    avatar_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button-avatar')
    avatar_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button h3',
        avatar_start,
    )
    avatar_slice = styles[avatar_start:avatar_end]
    assert "width: 24px;" in avatar_slice
    assert "height: 24px;" in avatar_slice

    selector_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-level-selector')
    selector_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-rail-signal',
        selector_start,
    )
    selector_slice = styles[selector_start:selector_end]
    assert "margin: 3px 0 0;" in selector_slice
    assert "min-height: 16px;" in selector_slice

    hidden_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button .progress-track')
    hidden_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button .small-muted',
        hidden_start,
    )
    hidden_slice = styles[hidden_start:hidden_end]
    assert "display: none;" in hidden_slice

    summary_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button .small-muted')
    summary_end = styles.index("@media", summary_start)
    summary_slice = styles[summary_start:summary_end]
    assert "display: none;" in summary_slice

    assert "Command Cockpit Lane Selector Compression" in readme


def test_command_cockpit_lane_rail_reads_as_cartridge_rack():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-lane-cartridge-rail" in index
    assert "Command Cockpit Lane Cartridge Rail" in readme

    list_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list')
    button_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button', list_start)
    list_slice = styles[list_start:button_start]
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in list_slice
    assert "gap: 4px;" in list_slice
    assert "padding: 22px 6px 6px;" in list_slice

    button_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button.active',
        button_start,
    )
    button_slice = styles[button_start:button_end]
    assert "min-height: 52px;" in button_slice
    assert "overflow: hidden;" in button_slice

    title_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button h3')
    title_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button p', title_start)
    title_slice = styles[title_start:title_end]
    assert "font-size: 0.62rem;" in title_slice
    assert "line-height: 1.05;" in title_slice
    assert "text-overflow: ellipsis;" in title_slice

    realm_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button p', title_end)
    badge_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button .badge', realm_start)
    assert "display: none;" in styles[realm_start:badge_start]

    cell_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-level-cell')
    rail_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-rail-signal', cell_start)
    cell_slice = styles[cell_start:rail_start]
    assert "min-height: 12px;" in cell_slice
    assert "font-size: 0.62rem;" in cell_slice
    assert ".lane-level-cell em" in cell_slice
    assert "display: none;" in cell_slice

    rail_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-rail-signal', cell_start)
    progress_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button .progress-track', rail_start)
    rail_slice = styles[rail_start:progress_start]
    assert "min-height: 6px;" in rail_slice
    assert ".lane-rail-pip" in rail_slice


def test_command_cockpit_lane_rail_reads_as_territory_board():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "20260619-command-cockpit-territory-board" in index
    assert "Command Cockpit Territory Board" in readme

    assert "const activeIndex = Math.max(0, lanes.findIndex((lane) => lane.id === state.selectedLaneId));" in app
    assert 'el.laneList.style.setProperty("--lane-board-active-index", activeIndex);' in app
    assert 'el.laneList.style.setProperty("--lane-board-count", Math.max(1, lanes.length));' in app
    assert 'class="lane-territory-route"' in app
    assert 'class="lane-territory-route-line"' in app
    assert 'class="lane-territory-runner"' in app
    assert 'class="lane-territory-node ${lane.id === state.selectedLaneId ? "active" : ""} ${escapeHtml(lane.state)}"' in app
    assert 'style="--lane-board-node-index:${index};"' in app

    base_start = styles.index("\n.lane-territory-route")
    base_end = styles.index(".lane-button", base_start)
    assert "display: none;" in styles[base_start:base_end]

    board_start = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list')
    board_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-territory-route',
        board_start,
    )
    board_slice = styles[board_start:board_end]
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in board_slice
    assert "padding: 22px 6px 6px;" in board_slice
    assert "overflow-x: hidden;" in board_slice

    route_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-territory-route',
        board_end,
    )
    line_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-territory-route-line',
        route_start,
    )
    route_slice = styles[route_start:line_start]
    assert "display: block;" in route_slice
    assert "height: 12px;" in route_slice

    runner_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-territory-runner',
        line_start,
    )
    node_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-territory-node',
        runner_start,
    )
    runner_slice = styles[runner_start:node_start]
    assert "left: calc(((var(--lane-board-active-index, 0) + 0.5) / max(1, var(--lane-board-count, 1))) * 100%);" in runner_slice
    assert "animation: laneTerritoryRunner 3.1s ease-in-out infinite;" in runner_slice

    active_node_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-territory-node.active',
        node_start,
    )
    active_node_end = styles.index('body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button', active_node_start)
    active_node_slice = styles[active_node_start:active_node_end]
    assert "animation: laneTerritoryNodePulse 2s ease-in-out infinite;" in active_node_slice

    assert "@keyframes laneTerritoryRunner" in styles
    assert "@keyframes laneTerritoryNodePulse" in styles

    medium_start = styles.index("@media (max-width: 1320px)")
    medium_panel_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel',
        medium_start,
    )
    medium_panel_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel .panel-head',
        medium_panel_start,
    )
    medium_panel_slice = styles[medium_panel_start:medium_panel_end]
    assert "order: -3;" in medium_panel_slice
    assert "max-height: 156px;" in medium_panel_slice

    medium_head_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list-panel .panel-head',
        medium_panel_end,
    )
    medium_head_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list {',
        medium_head_start,
    )
    assert "display: none;" in styles[medium_head_start:medium_head_end]

    medium_list_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-list {',
        medium_head_end,
    )
    medium_list_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button',
        medium_list_start,
    )
    medium_list_slice = styles[medium_list_start:medium_list_end]
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in medium_list_slice
    assert "max-height: 132px;" in medium_list_slice

    medium_selector_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-level-selector',
        medium_list_end,
    )
    medium_selector_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-rail-signal',
        medium_selector_start,
    )
    assert "display: none;" in styles[medium_selector_start:medium_selector_end]

    mobile_route_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-territory-route',
        styles.index("@media (max-width: 860px)"),
    )
    mobile_route_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button',
        mobile_route_start,
    )
    assert "display: none;" in styles[mobile_route_start:mobile_route_end]

    mobile_active_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button.active',
        mobile_route_end,
    )
    mobile_active_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-rail-signal',
        mobile_active_start,
    )
    mobile_active_slice = styles[mobile_active_start:mobile_active_end]
    assert "height: 28px;" in mobile_active_slice
    assert "min-height: 28px;" in mobile_active_slice

    mobile_signal_start = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-rail-signal',
        mobile_active_end,
    )
    mobile_signal_end = styles.index(
        'body[data-atlas-deck="command"][data-atlas-stage="cockpit"] .lane-button-top',
        mobile_signal_start,
    )
    assert "display: none;" in styles[mobile_signal_start:mobile_signal_end]
