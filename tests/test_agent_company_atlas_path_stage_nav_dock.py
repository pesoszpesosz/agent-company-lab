from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_nav_dock_moves_detail_navigation_inside_cockpit():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderPathStageNavDock(pathProgress)" in app
    assert "${renderPathStageNavDock(pathProgress)}" in app
    assert 'class="path-stage-nav-dock"' in app
    assert 'class="path-stage-nav-button' in app
    assert 'data-detail-view="${escapeHtml(view.id)}"' in app

    assert ".detail-content.detail-view-path .detail-tabs" in styles
    tabs_start = styles.index(".detail-content.detail-view-path .detail-tabs")
    tabs_end = styles.index(".detail-content.detail-view-path .detail-tab", tabs_start + 1)
    tabs_block = styles[tabs_start:tabs_end]
    assert "display: none" in tabs_block

    assert ".path-stage-nav-dock" in styles
    assert "position: absolute" in styles[styles.index(".path-stage-nav-dock") : styles.index(".path-stage-nav-meter")]
    assert ".path-stage-nav-button.active" in styles
    assert ".path-map-board.mission-stage" in styles
    assert "padding: 46px 10px 10px" in styles

    assert "Path Stage Nav Dock" in readme
    assert "20260618-path-stage-nav-dock" in index
