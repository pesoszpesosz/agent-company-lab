from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_view_defaults_to_stage_shell_before_deep_panels():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "pathStageDepthByLane: {}" in app
    assert 'new Set(["stage", "archive", "utility"])' in app
    assert 'return "stage";' in app
    assert "function renderPathStageDepthDock(" in app
    assert 'class="path-stage-depth-dock"' in app
    assert 'id: "stage"' in app
    assert 'id: "archive"' in app
    assert 'id: "utility"' in app
    assert 'data-path-stage-depth="${escapeHtml(card.id)}"' in app

    path_view = app[app.index("function renderPathMapView(lane) {") : app.index("function pathUtilityDockView(lane)")]
    assert "const depthView = pathStageDepthView(lane);" in path_view
    assert "${renderPathStageDepthDock(lane, trail, pathNotes, gateCount, depthView, pathProgress)}" in path_view
    assert 'depthView === "archive" ? renderPathChapterArchive(lane, trail) : ""' in path_view
    assert 'depthView === "utility" ? renderPathUtilityDock(lane, focusedNode, nodes, pathNotes, visibleTrail, trail, gateCount) : ""' in path_view
    assert "${renderPathChapterArchive(lane, trail)}" not in path_view
    assert "${renderPathUtilityDock(lane, focusedNode, nodes, pathNotes, visibleTrail, trail, gateCount)}" not in path_view

    assert "const pathStageDepthButton = event.target.closest(\"[data-path-stage-depth]\");" in app
    assert "state.pathStageDepthByLane" in app
    assert 'pathGlanceJumpButton.dataset.pathGlanceJump === "archive"' in app
    assert 'pathGlanceJumpButton.dataset.pathGlanceJump === "proof"' in app
    assert 'pathStageDepth: "utility"' in app

    for token in [
        ".path-stage-depth-dock",
        ".path-stage-depth-card",
        ".path-stage-depth-card.active",
        'body[data-detail-view="path"] .path-map-board.mission-stage',
    ]:
        assert token in styles

    stage_shell_block = styles[styles.index('body[data-detail-view="path"] .path-map-board.mission-stage') : styles.index(".path-stage-depth-dock")]
    assert "max-height: min(562px, calc(100vh - 150px));" in stage_shell_block
    assert "overflow: hidden;" in stage_shell_block

    assert "Path Stage Shell" in readme
    assert "20260618-path-stage-shell" in index
