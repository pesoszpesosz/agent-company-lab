from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_quest_scanner_keeps_core_state_inside_clicked_path_stage():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-path-stage-quest-scanner" in index

    assert "function pathStageQuestScannerModel(" in app
    assert "function renderPathStageQuestScanner(model)" in app
    assert "const questScanner = pathStageQuestScannerModel(lane, trail, nodes, focusedNode, pathNotes, pathProgress);" in app
    assert "${renderPathStageQuestScanner(questScanner)}" in app
    assert 'class="path-stage-quest-scanner ' in app
    assert 'data-path-quest-scan="${escapeHtml(cell.id)}"' in app

    for signal in ["Happened", "Blocker", "Proof", "Next"]:
        assert signal in app

    marker = "/* 20260620-path-stage-quest-scanner */"
    assert marker in styles
    scanner_slice = styles[styles.index(marker) :]
    assert ".path-stage-quest-scanner" in scanner_slice
    assert ".path-stage-quest-scanner-sweep" in scanner_slice
    assert ".path-stage-quest-scanner-grid" in scanner_slice
    assert ".path-stage-quest-scan-cell.gated" in scanner_slice
    assert ".path-stage-quest-scan-cell.unlocked" in scanner_slice
    assert "pathStageQuestScannerSweep" in scanner_slice
    assert "prefers-reduced-motion: reduce" in scanner_slice
    assert ".path-map-board.mission-stage[data-path-stage-depth-view=\"stage\"] .path-stage-quest-scanner" in scanner_slice
    assert "overflow-x: auto;" in scanner_slice

    assert "Path Stage Quest Scanner" in readme
