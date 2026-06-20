from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_viewport_stage_removes_redundant_scroll_chrome():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert 'class="detail-section path-viewport-section"' in app
    assert 'class="lane-button-top path-viewport-header"' in app
    assert "renderPathMissionGlance" in app
    assert "renderPathStageRibbon" in app
    assert "renderPathCoreDeck" in app

    render_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert render_slice.index("path-viewport-header") < render_slice.index("path-map-board mission-stage")
    assert render_slice.index("renderPathMissionGlance") < render_slice.index("renderPathStageRibbon")
    assert render_slice.index("renderPathStageRibbon") < render_slice.index("renderPathCoreDeck")

    for token in [
        ".detail-content.detail-view-path {",
        ".detail-content.detail-view-path .path-viewport-section",
        ".detail-content.detail-view-path .path-viewport-header",
        "display: none;",
        "padding: 12px;",
        "padding: 4px 0 0;",
        "Path Viewport Stage",
        "20260618-path-viewport-stage",
    ]:
        target = readme if token == "Path Viewport Stage" else index if token == "20260618-path-viewport-stage" else styles
        assert token in target
