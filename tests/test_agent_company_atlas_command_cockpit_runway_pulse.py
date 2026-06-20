from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_runway_pulse_models_recent_path_state():
    app = read("web/app.js")

    assert "function cockpitRunwayPulseModel(lane)" in app
    assert "const trail = chronicleTrail(lane);" in app
    assert "const suggestion = bestLaneDispatchSuggestion(lane);" in app
    assert "lane.counts?.tasks" in app
    assert "lane.counts?.blockers" in app
    assert "lane.counts?.evidence" in app
    assert "const pulses = [" in app
    assert 'id: "latest"' in app
    assert 'id: "task"' in app
    assert 'id: "blocker"' in app
    assert 'id: "proof"' in app
    assert 'id: "next"' in app
    assert "latest?.title" in app
    assert "chronicleNextAction(lane)" in app
    assert "function renderCockpitRunwayPulse(model)" in app
    assert 'class="cockpit-runway-pulse"' in app
    assert 'data-cockpit-runway-tone="${escapeHtml(model.tone)}"' in app
    assert 'data-cockpit-runway-pulse="${escapeHtml(pulse.id)}"' in app


def test_command_cockpit_runway_pulse_mounts_between_controller_and_minimap():
    app = read("web/app.js")
    render_start = app.index("function renderDetail()")
    render_end = app.index("function renderDetailBody", render_start)
    render_slice = app[render_start:render_end]

    assert "const cockpitRunwayPulse = cockpitRunwayPulseModel(lane);" in render_slice
    assert render_slice.index("const cockpitRunwayPulse = cockpitRunwayPulseModel(lane);") < render_slice.index("el.detailPanel.innerHTML")
    assert "${renderCockpitRunwayPulse(cockpitRunwayPulse)}" in render_slice
    assert render_slice.index("${renderCockpitControlPad(cockpitControlPad)}") < render_slice.index("${renderCockpitRunwayPulse(cockpitRunwayPulse)}")
    assert render_slice.index("${renderCockpitRunwayPulse(cockpitRunwayPulse)}") < render_slice.index("${renderCommandCockpitRouteMinimap(lane)}")


def test_command_cockpit_runway_pulse_is_compact_animated_and_documented():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-runway-pulse */"
    assert marker in styles
    block = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"]'

    assert f"{scoped} .cockpit-runway-pulse" in block
    assert "grid-template-columns: 44px repeat(5, minmax(0, 1fr));" in block
    assert "min-height: 46px;" in block
    assert "overflow: hidden;" in block
    assert ".cockpit-runway-pulse::before" in block
    assert "animation: cockpitRunwayPulseSweep 8.8s ease-in-out infinite;" in block
    assert "@keyframes cockpitRunwayPulseSweep" in block
    assert ".cockpit-runway-node" in block
    assert "data-cockpit-runway-tone" in read("web/app.js")
    assert "@media (max-width: 760px)" in block
    assert "grid-template-columns: 36px repeat(5, minmax(72px, 1fr));" in block
    assert "min-height: 42px;" in block
    assert "@media (prefers-reduced-motion: reduce)" in block
    assert ".cockpit-runway-pulse::before," in block
    assert ".path-stage-signal" in block
    assert "Command Cockpit Runway Pulse" in readme
    assert "latest event, task pressure, blockers, proof, and next move" in readme
    assert "20260620-command-cockpit-runway-pulse" in index