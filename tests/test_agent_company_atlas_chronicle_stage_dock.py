from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_chronicle_stage_dock_mounts_one_log_module_at_a_time():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "chronicleStageViewByLane" in app
    assert "function renderChronicleStageDock(lane, activeStage, counts)" in app
    assert "function renderChronicleStagePanel(lane, activeStage, chronicle)" in app
    assert "function chronicleViewModel(lane)" in app
    assert "${renderChronicleStageDock(lane, activeStage, chronicle.counts)}" in app
    assert "${renderChronicleStagePanel(lane, activeStage, chronicle)}" in app
    assert 'data-chronicle-stage="${escapeHtml(stage.id)}"' in app
    assert 'event.target.closest("[data-chronicle-stage]")' in app

    chronicle_start = app.index("function renderChronicleView(lane)")
    chronicle_end = app.index("function chronicleViewModel", chronicle_start)
    chronicle_slice = app[chronicle_start:chronicle_end]
    assert "chronicle-mapline" not in chronicle_slice
    assert "chronicle-gates" not in chronicle_slice
    assert "chronicle-stream" not in chronicle_slice

    signal_start = app.index("const signalPanel =")
    signal_end = app.index("const panels =", signal_start)
    signal_slice = app[signal_start:signal_end]
    assert "chronicle-grid" not in signal_slice

    assert ".detail-content.detail-view-chronicle .detail-top" in styles
    chronicle_top_start = styles.index(".detail-content.detail-view-chronicle .detail-top")
    chronicle_top_end = styles.index(".detail-content.detail-view-game .detail-top", chronicle_top_start)
    assert "display: none" in styles[chronicle_top_start:chronicle_top_end]

    assert ".detail-content.detail-view-chronicle .detail-tabs" in styles
    chronicle_tabs_start = styles.index(".detail-content.detail-view-chronicle .detail-tabs")
    chronicle_tabs_end = styles.index(".detail-content.detail-view-overview .detail-tabs", chronicle_tabs_start)
    assert "display: none" in styles[chronicle_tabs_start:chronicle_tabs_end]

    assert ".chronicle-stage-dock" in styles
    assert ".chronicle-stage-button.active" in styles
    assert 'body[data-detail-view="chronicle"] .chronicle-board' in styles

    assert "Chronicle Stage Dock" in readme
    assert "20260619-chronicle-stage-dock" in index
