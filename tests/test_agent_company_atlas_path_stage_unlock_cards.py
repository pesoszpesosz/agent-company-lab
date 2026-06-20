from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_unlock_cards_make_route_nodes_read_as_game_levels():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    stage_slice = app[app.index("function renderPathStageRibbon") : app.index("function pathCoreDeckModules")]
    assert "path-stage-node-frame" in stage_slice
    assert "path-stage-node-status" in stage_slice
    assert "path-stage-node-meter" in stage_slice
    assert "stateLabel(node.status)" in stage_slice
    assert "stateLabel(node.kind)" in stage_slice
    assert "--stage-charge:" in stage_slice

    marker = "/* 20260620-path-stage-unlock-cards */"
    assert marker in styles
    card_slice = styles[styles.index(marker) :]
    assert ".path-stage-node-frame" in card_slice
    assert ".path-stage-node-status" in card_slice
    assert ".path-stage-node-meter" in card_slice
    assert ".path-stage-node.is-focused .path-stage-node-frame" in card_slice
    assert ".path-stage-node.gated .path-stage-node-status" in card_slice
    assert ".path-stage-node.unlocked .path-stage-node-status" in card_slice
    assert ".path-stage-node.future .path-stage-node-meter" in card_slice
    assert "linear-gradient(180deg, color-mix(in srgb, var(--node-a, var(--teal)) 30%, transparent) 0 var(--stage-charge, 34%)" in card_slice

    assert "Path Stage Unlock Cards" in readme
    assert "20260620-path-stage-unlock-cards" in index.split('href="./styles.css?v=', 1)[1]
