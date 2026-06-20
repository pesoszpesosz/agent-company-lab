from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_expansion_sockets_surface_future_forks_without_scroll():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathStageExpansionSocketModel(lane, focusedNode, hidden)" in app
    assert "const hasTrailSeed = eventCount || (lane.trail?.length ?? 0) ? 1 : 0;" in app
    assert "function renderPathStageExpansionSockets(lane, focusedNode, hidden)" in app
    assert "path-stage-expansion-sockets" in app
    assert "path-stage-expansion-socket" in app
    assert "pathStageNodeEchoEvents(lane, focusedNode)" in app
    assert "renderPathStageExpansionSockets(lane, focusedNode, hidden)" in app

    ribbon_slice = app[app.index("function renderPathStageRibbon") : app.index("function pathCoreDeckModules")]
    assert ribbon_slice.index("renderPathStageExpansionSockets") < ribbon_slice.index("renderPathStageFocusLens")

    marker = "/* 20260620-path-stage-expansion-sockets */"
    assert marker in styles
    socket_slice = styles[styles.index(marker) :]

    assert ".path-stage-expansion-sockets" in socket_slice
    assert ".path-stage-expansion-socket.gate" in socket_slice
    assert ".path-stage-expansion-socket.task" in socket_slice
    assert ".path-stage-expansion-socket.proof" in socket_slice
    assert ".path-stage-expansion-socket.future" in socket_slice
    assert "@keyframes pathStageExpansionSocketPulse" in socket_slice
    assert "@media (max-width: 560px)" in socket_slice
    assert "@media (prefers-reduced-motion: reduce)" in socket_slice

    assert "Path Stage Expansion Sockets" in readme
    assert "20260620-path-stage-expansion-sockets" in index
