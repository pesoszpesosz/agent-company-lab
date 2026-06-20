from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_bot_relay_capsule_embeds_local_bot_handoff_in_scanner():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-path-stage-bot-relay-capsule" in index

    model_slice = app[app.index("function pathStageQuestScannerModel") : app.index("function renderPathStageQuestScanner")]
    assert "const owner = laneAgents(lane)[0];" in model_slice
    assert "const suggestion = bestLaneDispatchSuggestion(lane);" in model_slice
    assert "state.stagedDispatches.some" in model_slice
    assert 'id: "bot"' in model_slice
    assert "thread: lane.ownerThreadId ?? owner?.thread_id ?? \"No thread\"" in model_slice

    render_slice = app[app.index("function renderPathStageQuestScanner") : app.index("function renderPathMapView")]
    assert 'class="path-stage-quest-scanner-relay ${model.relay.staged ? "staged" : ""}"' in render_slice
    assert 'class="path-stage-quest-scanner-avatar"' in render_slice
    assert 'data-path-handoff-stage="${escapeHtml(model.relay.laneId)}"' in render_slice
    assert 'data-detail-view="comms"' in render_slice

    marker = "/* 20260620-path-stage-bot-relay-capsule */"
    assert marker in styles
    relay_slice = styles[styles.index(marker) :]
    assert ".path-stage-quest-scanner-relay" in relay_slice
    assert ".path-stage-quest-scanner-relay.staged" in relay_slice
    assert ".path-stage-quest-scanner-avatar" in relay_slice
    assert ".path-stage-quest-scanner-relay .tool-button" in relay_slice
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in relay_slice
    assert ".path-stage-quest-scanner-relay {\n    display: none;" in relay_slice

    assert "Path Stage Bot Relay Capsule" in readme
