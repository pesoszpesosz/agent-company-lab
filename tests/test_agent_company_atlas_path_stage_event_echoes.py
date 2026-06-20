from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_event_echoes_connect_route_tokens_to_trail_events():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathStageNodeEchoEvents(lane, node)" in app
    assert "return pathNodeRelatedEvents(lane, node, 3);" in app
    assert "function renderPathStageNodeEchoes(lane, node)" in app
    assert "path-stage-node-echoes" in app
    assert "path-stage-node-echo" in app
    assert "pathEventGlyphType(item)" in app
    assert "renderPathStageNodeEchoes(lane, node)" in app

    marker = "/* 20260620-path-stage-event-echoes */"
    assert marker in styles
    echo_slice = styles[styles.index(marker) :]
    assert ".path-stage-node-echoes" in echo_slice
    assert ".path-stage-node-echo" in echo_slice
    assert ".path-stage-node-echo.outcome" in echo_slice
    assert ".path-stage-node-echo.gate" in echo_slice
    assert ".path-stage-node-echo.task" in echo_slice
    assert "@keyframes pathStageEchoPulse" in echo_slice
    assert "@keyframes pathStageEchoRing" in echo_slice
    assert "min-height: min(488px, calc(100vh - 142px));" in echo_slice
    assert "@media (max-width: 560px)" in echo_slice
    assert ".path-stage-node-echo" in styles[styles.index("@media (prefers-reduced-motion: reduce)") :]

    assert "Path Stage Event Echoes" in readme
    assert "20260620-path-stage-event-echoes" in index
