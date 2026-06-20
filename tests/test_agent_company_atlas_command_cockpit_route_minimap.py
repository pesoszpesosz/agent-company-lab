from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_route_minimap_adds_low_scroll_lane_state():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function commandCockpitRouteMinimap(lane)" in app
    assert "function renderCommandCockpitRouteMinimap(lane)" in app
    assert "commandCockpitRouteMinimap(lane)" in app
    assert "${renderCommandCockpitRouteMinimap(lane)}" in app
    assert 'class="command-route-minimap"' in app
    assert 'data-command-route-node="${escapeHtml(node.id)}"' in app
    assert "Gate" in app
    assert "Tasks" in app
    assert "Proof" in app
    assert "Bot" in app
    assert "Game" in app
    assert "Next" in app

    marker = "/* 20260620-command-cockpit-route-minimap */"
    assert marker in styles
    minimap_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    assert f"{scoped} .command-route-minimap" in minimap_slice
    assert "grid-template-columns: minmax(86px, 0.52fr) repeat(6, minmax(0, 1fr));" in minimap_slice
    assert "min-height: 54px;" in minimap_slice
    assert "overflow: hidden;" in minimap_slice
    assert f"{scoped} .command-route-node" in minimap_slice
    assert "animation: commandRouteMinimapPulse 7.4s ease-in-out infinite;" in minimap_slice
    assert "@media (max-width: 760px)" in minimap_slice
    assert "grid-auto-flow: column;" in minimap_slice
    assert "grid-auto-columns: minmax(104px, 126px);" in minimap_slice
    assert "@keyframes commandRouteMinimapPulse" in minimap_slice
    assert "prefers-reduced-motion: reduce" in minimap_slice

    assert "20260620-command-cockpit-route-minimap" in index
    assert "Command Cockpit Route Minimap" in readme