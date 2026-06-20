from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_story_rail_restores_core_path_story_without_scroll_copy():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-story-rail */"
    assert marker in styles
    rail_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    board = f'{scoped} .path-map-board.mission-stage[data-path-stage-depth-view="stage"]'
    shell = f"{board} > .path-stage-mobile-story-rail-shell"
    scanner = f"{shell} .path-stage-quest-scanner"
    grid = f"{shell} .path-stage-quest-scanner-grid"
    cell = f"{shell} .path-stage-quest-scan-cell"

    assert "const questScanner = pathStageQuestScannerModel(lane, trail, nodes, focusedNode, pathNotes, pathProgress);" in app
    assert 'class="path-stage-mobile-story-rail-shell"' in app
    assert "${renderPathStageQuestScanner(questScanner)}" in app

    assert f"{scoped} .path-stage-mobile-story-rail-shell" in rail_slice
    assert "display: none;" in rail_slice
    assert "@media (max-width: 560px)" in rail_slice
    assert shell in rail_slice
    assert "position: absolute;" in rail_slice
    assert "bottom: 118px;" in rail_slice
    assert "min-height: 42px;" in rail_slice
    assert "max-height: 48px;" in rail_slice
    assert "pointer-events: none;" in rail_slice
    assert scanner in rail_slice
    assert "position: relative;" in rail_slice
    assert "width: 100%;" in rail_slice
    assert f"{shell} .path-stage-quest-scanner-head" in rail_slice
    assert "display: none !important;" in rail_slice
    assert grid in rail_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in rail_slice
    assert cell in rail_slice
    assert "min-height: 32px;" in rail_slice
    assert f"{cell}:nth-child(n + 5)" in rail_slice
    assert f"{cell} em" in rail_slice
    assert f"{cell} b" in rail_slice

    assert "Path Stage Mobile Story Rail" in readme
    assert "20260620-path-stage-mobile-story-rail" in index
    assert "20260620-command-cockpit-mobile-cinematic-focus-20260620-path-stage-mobile-story-rail" in index
    assert "path-stage-bot-command-beacon-20260620-path-stage-mobile-story-rail" in index
