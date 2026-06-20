from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_utility_dock_replaces_lower_scroll_stack():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "pathUtilityDockViewByLane" in app
    assert "function pathUtilityDockView" in app
    assert "function pathUtilityDockModules" in app
    assert "function renderPathUtilityDock" in app
    assert "data-path-utility-view" in app
    assert "pathUtilityViewButton" in app
    assert "path-utility-dock" in app
    assert "path-utility-tabs" in app
    assert "path-utility-panel" in app
    assert app.index("renderPathChapterArchive(lane, trail)") < app.index("renderPathUtilityDock(lane")
    assert "path-bottom-grid" not in app[app.index("function renderPathMapView") : app.index("function pathCommandStripCells")]

    for token in [
        ".path-utility-dock",
        ".path-utility-tabs",
        ".path-utility-tab",
        ".path-utility-panel",
        ".path-utility-panel .path-brief-card",
        "grid-auto-flow: column",
        "overflow-x: auto",
        "pathUtilityPanelEnter",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Utility Dock" in readme
    assert "20260618-path-utility-dock" in index
