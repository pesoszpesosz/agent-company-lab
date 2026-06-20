from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_path_entry_uses_compact_mission_stage():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "detail-content detail-view-${escapeHtml(state.detailView)}" in app
    assert "path-map-board mission-stage" in app
    assert ".detail-content.detail-view-path .detail-top" in styles
    assert ".detail-content.detail-view-path h2" in styles
    assert ".detail-content.detail-view-path .detail-avatar" in styles
    assert ".detail-content.detail-view-path .detail-copy {\n  display: none;" in styles
    assert ".detail-content.detail-view-path .detail-tabs" in styles
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in styles
    assert ".path-map-board.mission-stage" in styles
    assert ".path-map-board.mission-stage .path-mission-glance" in styles
    assert ".path-map-board.mission-stage .path-core-deck" in styles
    assert ".path-map-board.mission-stage .path-glance-card" in styles
    assert ".path-map-board.mission-stage .path-core-panel" in styles
    assert "max-height: min(640px, calc(100vh - 80px));" in styles
    assert "animation: missionStageSignal" in styles
    assert "@keyframes missionStageSignal" in styles
    assert "Compact Mission Stage" in readme
    assert "20260618-compact-mission-stage" in index
