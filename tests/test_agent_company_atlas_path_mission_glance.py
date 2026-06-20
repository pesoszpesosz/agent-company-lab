from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_mission_glance_replaces_scroll_heavy_hero():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathMissionGlanceCards(lane, trail, focusedNode, pathNotes, pathProgress)" in app
    assert "function renderPathMissionGlance(lane, trail, focusedNode, pathNotes, pathProgress)" in app
    assert "renderPathMissionGlance(lane, trail, focusedNode, pathNotes, pathProgress)" in app
    assert "path-mission-glance" in app
    assert "path-glance-card" in app
    assert "path-glance-actions" in app
    assert "data-path-glance-jump" in app
    assert "pathGlanceJumpButton" in app

    render_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert "path-map-hero" not in render_slice
    assert render_slice.index("renderPathMissionGlance") < render_slice.index("renderPathCoreDeck")

    for token in [
        ".path-mission-glance",
        ".path-glance-main",
        ".path-glance-cards",
        ".path-glance-card",
        ".path-glance-actions",
        ".path-glance-pulse",
        "pathGlancePulse",
        "grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr) auto",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Mission Glance" in readme
    assert "20260618-path-mission-glance" in index
