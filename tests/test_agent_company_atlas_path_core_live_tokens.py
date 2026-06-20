from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_core_motion_rail_adds_data_driven_live_tokens():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathCoreLiveTokens(lane, trail, nodes, pathNotes)" in app
    assert "const liveTokens = pathCoreLiveTokens(lane, trail, nodes, pathNotes);" in app
    assert "class=\"path-core-live-token" in app
    assert "data-path-core-live-token" in app
    assert "--path-core-live-count:" in app
    assert "--path-core-live-index:" in app

    core_slice = app[app.index("function renderPathCoreDeck") : app.index("function pathStageDepthView")]
    assert "liveTokens.map" in core_slice
    assert "pathCoreLiveTokens(lane, trail, nodes, pathNotes)" in core_slice
    assert "renderPathCoreSnapshot(lane, modules, activeModule, liveTokens, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes)" in core_slice

    for token in [
        ".path-core-live-token",
        ".path-core-live-token.blocker",
        ".path-core-live-token.proof",
        ".path-core-live-token.work",
        "pathCoreLiveTokenDrift",
        "animation-delay: calc",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Core Live Tokens" in readme
    assert "20260618-path-core-live-tokens" in index
