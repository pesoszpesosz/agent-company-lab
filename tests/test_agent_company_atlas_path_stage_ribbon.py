from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_ribbon_surfaces_route_levels_before_core_deck():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderPathStageRibbon(lane, nodes, focusedNode, pathProgress)" in app
    assert "path-stage-ribbon" in app
    assert "path-stage-node" in app
    assert "data-path-node-focus" in app

    render_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert render_slice.index("renderPathMissionGlance") < render_slice.index("renderPathStageRibbon")
    assert render_slice.index("renderPathStageRibbon") < render_slice.index("renderPathCoreDeck")

    for token in [
        ".path-stage-ribbon",
        ".path-stage-ribbon::before",
        ".path-stage-progress",
        ".path-stage-node",
        ".path-stage-node.is-focused",
        ".path-stage-node.gate",
        ".path-stage-node.unlock",
        "@keyframes pathStageRunner",
    ]:
        assert token in styles

    ribbon_block = styles[styles.index(".path-stage-ribbon {") : styles.index(".path-stage-ribbon::before")]
    node_block = styles[styles.index(".path-stage-node {") : styles.index(".path-stage-node i")]
    assert "height: 74px;" in ribbon_block
    assert "min-height: 0;" in ribbon_block
    assert "height: 58px;" in node_block
    assert "min-height: 0;" in node_block

    assert "Path Stage Ribbon" in readme
    assert "20260618-path-stage-ribbon" in index
