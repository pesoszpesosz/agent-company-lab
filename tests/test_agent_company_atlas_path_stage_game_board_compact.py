from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_game_board_compact_prioritizes_map_over_nested_panel_stack():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-game-board-compact */"
    assert marker in styles
    compact_slice = styles[styles.index(marker) :]

    assert 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"] .active-lane-mounted-stage[data-active-stage-view="path"]' in compact_slice
    assert "overflow: visible;" in compact_slice
    assert ".detail-content.detail-view-path .path-viewport-header" in compact_slice
    assert "display: none;" in compact_slice

    assert ".path-map-board.mission-stage[data-path-stage-depth-view=\"stage\"]" in compact_slice
    assert "grid-template-areas:" in compact_slice
    assert '"glance core"' in compact_slice
    assert '"route route"' in compact_slice
    assert '"scanner scanner"' in compact_slice

    assert ".path-map-board.mission-stage[data-path-stage-depth-view=\"stage\"] .path-stage-ribbon" in compact_slice
    assert "grid-area: route;" in compact_slice
    assert "grid-column: 1 / -1;" in compact_slice
    assert "grid-row: 2;" in compact_slice
    assert "min-height: clamp(190px, 26vh, 270px);" in compact_slice

    assert ".path-map-board.mission-stage[data-path-stage-depth-view=\"stage\"] .path-stage-chapter-radar" in compact_slice
    assert "transform: translateY(calc(100% + 10px));" in compact_slice

    assert "Path Stage Game Board Compact" in readme
    assert "20260620-path-stage-game-board-compact" in index.split('href="./styles.css?v=', 1)[1]
