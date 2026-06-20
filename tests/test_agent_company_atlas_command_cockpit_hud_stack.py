from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_hud_stack_groups_existing_instruments_before_route():
    app = read("web/app.js")
    render_start = app.index("function renderDetail()")
    render_end = app.index("function renderDetailBody", render_start)
    render_slice = app[render_start:render_end]

    assert 'class="cockpit-command-stack"' in render_slice
    assert 'data-cockpit-command-stack="${escapeHtml(state.detailView)}"' in render_slice
    assert 'aria-label="Cockpit command HUD stack"' in render_slice
    assert render_slice.index('class="cockpit-command-stack"') < render_slice.index("${renderCommandCockpitRouteMinimap(lane)}")
    assert render_slice.index("${renderCockpitControlPad(cockpitControlPad)}") < render_slice.index("${renderCockpitRunwayPulse(cockpitRunwayPulse)}")
    assert render_slice.index("${renderCockpitRunwayPulse(cockpitRunwayPulse)}") < render_slice.index("${renderCockpitCrewHandoffRail(cockpitCrewHandoffRail)}")
    assert render_slice.index("${renderCockpitCrewHandoffRail(cockpitCrewHandoffRail)}") < render_slice.index("${renderCockpitUnlockChain(cockpitUnlockChain)}")
    assert render_slice.index("${renderCockpitUnlockChain(cockpitUnlockChain)}") < render_slice.index("${renderCommandCockpitRouteMinimap(lane)}")


def test_command_cockpit_hud_stack_compresses_vertical_cockpit_chrome():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-hud-stack */"
    assert marker in styles
    block = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"]'

    assert f"{scoped} .cockpit-command-stack" in block
    assert "display: grid;" in block
    assert "grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);" in block
    assert 'grid-template-areas:' in block
    assert '"control control"' in block
    assert '"run crew"' in block
    assert '"unlock unlock"' in block
    assert "gap: 6px;" in block
    assert "margin: 0 0 7px;" in block
    assert ".cockpit-command-stack > .cockpit-control-pad" in block
    assert ".cockpit-command-stack > .cockpit-runway-pulse" in block
    assert ".cockpit-command-stack > .cockpit-crew-handoff-rail" in block
    assert ".cockpit-command-stack > .cockpit-unlock-chain" in block
    assert "margin: 0;" in block
    assert "min-height: 44px;" in block
    assert ".cockpit-command-stack > .cockpit-control-pad {" in block
    assert "grid-area: control;" in block
    assert ".cockpit-command-stack > .cockpit-runway-pulse {" in block
    assert "grid-area: run;" in block
    assert ".cockpit-command-stack > .cockpit-crew-handoff-rail {" in block
    assert "grid-area: crew;" in block
    assert ".cockpit-command-stack > .cockpit-unlock-chain {" in block
    assert "grid-area: unlock;" in block
    assert "@media (max-width: 760px)" in block
    assert "grid-template-columns: 1fr;" in block
    assert '"control"' in block
    assert '"run"' in block
    assert '"crew"' in block
    assert '"unlock"' in block
    assert "Command Cockpit HUD Stack" in readme
    assert "compresses the controller, run pulse, crew handoff, and unlock chain" in readme
    assert "20260620-command-cockpit-hud-stack" in index