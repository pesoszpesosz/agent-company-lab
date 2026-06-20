from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_control_pad_models_lane_actions_without_new_scroll():
    app = read("web/app.js")

    assert "function cockpitControlPadModel(lane)" in app
    assert "const actions = [" in app
    assert 'id: "path"' in app
    assert 'id: "gate"' in app
    assert 'id: "proof"' in app
    assert 'id: "bot"' in app
    assert 'id: "game"' in app
    assert 'id: "queue"' in app
    assert "lane.counts?.blockers" in app
    assert "lane.counts?.evidence" in app
    assert "gameStepCount(lane)" in app
    assert "bestLaneDispatchSuggestion(lane)" in app
    assert "function renderCockpitControlPad(model)" in app
    assert 'class="cockpit-control-pad"' in app
    assert 'data-cockpit-control-action="${escapeHtml(action.id)}"' in app
    assert 'data-cockpit-control-lane="${escapeHtml(model.laneId)}"' in app


def test_command_cockpit_control_pad_mounts_and_routes_inside_stage():
    app = read("web/app.js")

    render_start = app.index("function renderDetail()")
    render_end = app.index("function renderDetailBody", render_start)
    render_slice = app[render_start:render_end]

    assert "const cockpitControlPad = cockpitControlPadModel(lane);" in render_slice
    assert render_slice.index("const cockpitControlPad = cockpitControlPadModel(lane);") < render_slice.index("el.detailPanel.innerHTML")
    assert "${renderCockpitControlPad(cockpitControlPad)}" in render_slice
    assert render_slice.index("${renderCockpitControlPad(cockpitControlPad)}") < render_slice.index("${renderCommandCockpitRouteMinimap(lane)}")

    assert "function activateCockpitControlPad(action, laneId)" in app
    assert 'event.target.closest("[data-cockpit-control-action]")' in app
    assert 'activateCockpitControlPad(cockpitControlButton.dataset.cockpitControlAction, cockpitControlButton.dataset.cockpitControlLane);' in app
    assert 'if (action === "queue") {' in app
    assert "stageDispatch(bestLaneDispatchSuggestion(lane));" in app
    assert 'selectLane(lane.id, "path");' in app
    assert 'selectLane(lane.id, "trail");' in app
    assert 'selectLane(lane.id, "chronicle");' in app
    assert 'selectLane(lane.id, "comms");' in app
    assert 'selectLane(lane.id, "game");' in app


def test_command_cockpit_control_pad_is_compact_premium_and_documented():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-control-pad */"
    assert marker in styles
    block = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"]'

    assert f"{scoped} .cockpit-control-pad" in block
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in block
    assert "min-height: 48px;" in block
    assert "position: sticky;" in block
    assert "top: 0;" in block
    assert "backdrop-filter: blur(18px);" in block
    assert ".cockpit-control-pad::before" in block
    assert "animation: cockpitControlPadSweep 9.2s ease-in-out infinite;" in block
    assert "@keyframes cockpitControlPadSweep" in block
    assert ".cockpit-control-action" in block
    assert "data-cockpit-control-tone" in read("web/app.js")
    assert "@media (max-width: 760px)" in block
    assert "grid-auto-columns: minmax(74px, 92px);" in block
    assert "overflow-x: auto;" in block
    assert "@media (prefers-reduced-motion: reduce)" in block
    assert ".cockpit-control-pad::before," in block
    assert ".path-stage-signal" in block
    assert "Command Cockpit Control Pad" in readme
    assert "compact in-stage game controller" in readme
    assert "20260620-command-cockpit-control-pad" in index