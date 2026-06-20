from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_core_deck_uses_compact_snapshot_instead_of_scroll_box():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderPathCoreSnapshot(" in app
    assert "pathCoreSnapshotItems(" in app
    assert "class=\"path-core-snapshot " in app
    assert "class=\"path-core-snapshot-arc\"" in app
    assert "class=\"path-core-snapshot-grid\"" in app

    core_deck = app[app.index("function renderPathCoreDeck") : app.index("function pathStageDepthView")]
    assert "renderPathCoreSnapshot(lane, modules, activeModule, liveTokens, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes)" in core_deck
    assert "${activeModule.content()}" not in core_deck

    stage_panel = styles[
        styles.index(".path-map-board.mission-stage .path-core-panel")
        : styles.index("body[data-detail-view=\"path\"] .path-map-board.mission-stage")
    ]
    assert "max-height: none;" in stage_panel
    assert "overflow: hidden;" in stage_panel

    for token in [
        ".path-core-snapshot",
        ".path-core-snapshot-arc",
        ".path-core-snapshot-grid",
        ".path-core-snapshot-card",
        ".path-core-snapshot-actions",
        '.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-core-panel',
        "pathCoreSnapshotSweep",
    ]:
        assert token in styles

    assert "padding-bottom: 7px;" in styles
    assert ".path-map-board.mission-stage[data-path-stage-depth-view=\"stage\"] .path-core-panel {\n    display: none;" in styles

    assert "Path Core Snapshot" in readme
    assert "20260618-path-core-snapshot" in index
