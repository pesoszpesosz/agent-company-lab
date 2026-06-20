from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_core_deck_compacts_scan_command_and_route():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "pathCoreDeckViewByLane" in app
    assert "function pathCoreDeckView" in app
    assert "function pathCoreDeckModules" in app
    assert "function renderPathRouteRail(lane, nodes, focusedNode)" in app
    assert "function renderPathCoreDeck(lane, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes)" in app
    assert "data-path-core-view" in app
    assert "pathCoreViewButton" in app
    assert "path-core-deck" in app
    assert "path-core-tabs" in app
    assert "path-core-panel" in app

    render_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert "renderPathCoreDeck(lane, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes)" in render_slice
    assert "renderPathMissionScan(lane, trail, nodes, focusedNode, mapStats, pathProgress)" not in render_slice
    assert "renderPathCommandStrip(lane, trail, focusedNode, pathNotes)" not in render_slice
    assert "class=\"path-route\"" not in render_slice

    for token in [
        ".path-core-deck",
        ".path-core-tabs",
        ".path-core-tab",
        ".path-core-panel",
        ".path-core-panel > *",
        "pathCorePanelEnter",
        "overflow-x: auto",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Core Deck" in readme
    assert "20260618-path-core-deck" in index
