from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_crew_handoff_rail_models_agents_and_queue_state():
    app = read("web/app.js")

    assert "function cockpitCrewHandoffRailModel(lane)" in app
    assert "const agents = laneAgents(lane).slice(0, 3);" in app
    assert "const suggestion = bestLaneDispatchSuggestion(lane);" in app
    assert "state.stagedDispatches.some" in app
    assert "sourceId === suggestion.id" in app
    assert "const fallback = agents.length" in app
    assert "handoffs:" in app
    assert "callsign:" in app
    assert "status:" in app
    assert "action:" in app
    assert "function renderCockpitCrewHandoffRail(model)" in app
    assert 'class="cockpit-crew-handoff-rail"' in app
    assert 'data-cockpit-crew-handoff-tone="${escapeHtml(model.tone)}"' in app
    assert 'data-cockpit-crew-handoff="${escapeHtml(record.id)}"' in app
    assert 'agentAvatarMarkup(record.agent, model.lane, "cockpit-crew-handoff-avatar")' in app


def test_command_cockpit_crew_handoff_rail_mounts_inside_cockpit_before_minimap():
    app = read("web/app.js")
    render_start = app.index("function renderDetail()")
    render_end = app.index("function renderDetailBody", render_start)
    render_slice = app[render_start:render_end]

    assert "const cockpitCrewHandoffRail = cockpitCrewHandoffRailModel(lane);" in render_slice
    assert render_slice.index("const cockpitCrewHandoffRail = cockpitCrewHandoffRailModel(lane);") < render_slice.index("el.detailPanel.innerHTML")
    assert "${renderCockpitCrewHandoffRail(cockpitCrewHandoffRail)}" in render_slice
    assert render_slice.index("${renderCockpitRunwayPulse(cockpitRunwayPulse)}") < render_slice.index("${renderCockpitCrewHandoffRail(cockpitCrewHandoffRail)}")
    assert render_slice.index("${renderCockpitCrewHandoffRail(cockpitCrewHandoffRail)}") < render_slice.index("${renderCommandCockpitRouteMinimap(lane)}")


def test_command_cockpit_crew_handoff_rail_is_compact_visual_and_documented():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-crew-handoff-rail */"
    assert marker in styles
    block = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"]'

    assert f"{scoped} .cockpit-crew-handoff-rail" in block
    assert "grid-template-columns: minmax(110px, 0.72fr) repeat(3, minmax(0, 1fr));" in block
    assert "min-height: 50px;" in block
    assert "overflow: hidden;" in block
    assert ".cockpit-crew-handoff-rail::before" in block
    assert "animation: cockpitCrewHandoffSweep 9.6s ease-in-out infinite;" in block
    assert "@keyframes cockpitCrewHandoffSweep" in block
    assert ".cockpit-crew-handoff-card" in block
    assert ".cockpit-crew-handoff-avatar" in block
    assert "@media (max-width: 760px)" in block
    assert "grid-auto-columns: minmax(128px, 156px);" in block
    assert "overflow-x: auto;" in block
    assert "@media (prefers-reduced-motion: reduce)" in block
    assert ".cockpit-crew-handoff-rail::before," in block
    assert ".path-stage-signal" in block
    assert "Command Cockpit Crew Handoff Rail" in readme
    assert "owner and support bots, staged queue state, and next command" in readme
    assert "20260620-command-cockpit-crew-handoff-rail" in index