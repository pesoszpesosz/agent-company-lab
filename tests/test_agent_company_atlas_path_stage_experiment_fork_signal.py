from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_experiment_fork_signal_surfaces_tests_without_new_scroll_panel():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-path-stage-experiment-fork-signal" in index

    model_slice = app[app.index("function pathStageQuestScannerModel") : app.index("function renderPathStageQuestScanner")]
    assert "const minigame = lane.visual?.minigame ?? {};" in model_slice
    assert "const testCount =" in model_slice
    assert "(lane.counts?.activeTasks ?? 0)" in model_slice
    assert "(lane.recentTasks?.length ?? 0)" in model_slice
    assert 'id: "tests"' in model_slice
    assert 'label: "Tests"' in model_slice
    assert "future sockets primed" in model_slice

    render_slice = app[app.index("function renderPathStageQuestScanner") : app.index("function renderPathMapView")]
    assert 'data-path-quest-scan="${escapeHtml(cell.id)}"' in render_slice
    assert "model.cells" in render_slice

    scanner_marker = "/* 20260620-path-stage-quest-scanner */"
    assert scanner_marker in styles
    scanner_slice = styles[styles.index(scanner_marker) :]
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in scanner_slice
    assert "overflow-x: auto;" in scanner_slice

    assert "Path Stage Experiment Fork Signal" in readme
