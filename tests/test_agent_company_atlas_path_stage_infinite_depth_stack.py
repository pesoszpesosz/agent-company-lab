from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_infinite_depth_stack_keeps_clicked_path_game_readable_without_scroll():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathStageInfiniteDepthLayers(lane, trail, nodes, focusedNode, pathProgress, mapStats, pathNotes)" in app
    assert "function renderPathStageInfiniteDepthStack(lane, trail, nodes, focusedNode, pathProgress, mapStats, pathNotes)" in app
    assert "path-stage-infinite-depth-stack" in app
    assert "path-stage-depth-layer" in app
    assert 'data-path-depth-layer="${escapeHtml(layer.id)}"' in app
    assert 'id: "happened"' in app
    assert 'id: "blocker"' in app
    assert 'id: "tests"' in app
    assert 'id: "proof"' in app
    assert 'id: "next"' in app
    assert "renderPathStageInfiniteDepthStack(lane, trail, nodes, focusedNode, pathProgress, mapStats, pathNotes)" in app

    board_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert board_slice.index("renderPathStageBotCommandBeacon") < board_slice.index("renderPathStageInfiniteDepthStack")
    assert board_slice.index("renderPathStageInfiniteDepthStack") < board_slice.index("path-stage-mobile-story-rail-shell")

    marker = "/* 20260620-path-stage-infinite-depth-stack */"
    assert marker in styles
    stack_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    stack = f"{scoped} .path-stage-infinite-depth-stack"

    assert stack in stack_slice
    assert f"{stack}::before" in stack_slice
    assert f"{stack} .path-stage-depth-layer" in stack_slice
    assert f"{stack} .path-stage-depth-layer.blocker" in stack_slice
    assert f"{stack} .path-stage-depth-layer.tests" in stack_slice
    assert f"{stack} .path-stage-depth-layer.proof" in stack_slice
    assert "position: absolute;" in stack_slice
    assert "pointer-events: none;" in stack_slice
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in stack_slice
    assert "animation: pathStageInfiniteDepthPulse" in stack_slice
    assert "@keyframes pathStageInfiniteDepthPulse" in stack_slice
    assert "@media (max-width: 560px)" in stack_slice
    assert "top: 58px;" in stack_slice
    assert "height: 38px;" in stack_slice
    assert "@media (prefers-reduced-motion: reduce)" in stack_slice

    assert "Path Stage Infinite Depth Stack" in readme
    assert "20260620-path-stage-infinite-depth-stack" in index