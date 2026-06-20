from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_bot_command_beacon_promotes_lane_owner_to_board_overlay():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathStageBotCommandBeaconModel(lane)" in app
    assert "const records = pathMissionCrewTokens(lane);" in app
    assert "readiness: record ? crewReadiness(record) : lane.progress ?? 0" in app
    assert "function renderPathStageBotCommandBeacon(lane)" in app
    assert 'class="path-stage-bot-command-beacon ${escapeHtml(model.mode)} ${model.staged ? "staged" : ""}"' in app
    assert 'data-path-handoff-stage="${escapeHtml(model.laneId)}"' in app
    assert 'data-detail-view="comms"' in app
    assert "agentRosterAvatar(model.agent)" in app

    map_view_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert "${renderPathStageBotCommandBeacon(lane)}" in map_view_slice
    assert map_view_slice.index("${renderPathStageBotCommandBeacon(lane)}") < map_view_slice.index("${renderPathStageFocusLens(lane, focusedNode, pathProgress)}")

    marker = "/* 20260620-path-stage-bot-command-beacon */"
    assert marker in styles
    beacon_slice = styles[styles.index(marker) :]

    assert ".path-stage-bot-command-beacon" in beacon_slice
    assert ".path-stage-bot-command-beacon::before" in beacon_slice
    assert ".path-stage-bot-command-beacon .operator-avatar" in beacon_slice
    assert ".path-stage-bot-command-beacon .tool-button" in beacon_slice
    assert "--path-stage-bot-ready" in beacon_slice
    assert "pathStageBotCommandPing" in beacon_slice
    assert "pointer-events: auto;" in beacon_slice
    assert "@media (max-width: 560px)" in beacon_slice
    assert "@media (prefers-reduced-motion: reduce)" in beacon_slice

    assert "Path Stage Bot Command Beacon" in readme
    assert "20260620-path-stage-bot-command-beacon" in index
