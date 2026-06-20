from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_level_tokens_turn_route_cards_into_arcade_tokens():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-level-tokens */"
    assert marker in styles
    token_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    board = f'{scoped} .path-map-board.mission-stage[data-path-stage-depth-view="stage"]'
    ribbon = f"{board} .path-stage-ribbon"
    node = f"{board} .path-stage-node"

    assert "@media (max-width: 560px)" in token_slice
    assert ribbon in token_slice
    assert "grid-auto-columns: minmax(88px, 0.58fr);" in token_slice
    assert "padding: 84px 8px 100px;" in token_slice
    assert f"{ribbon}::after" in token_slice
    assert "pathStageMobileTokenSpotlight" in token_slice
    assert node in token_slice
    assert "width: 88px;" in token_slice
    assert "height: 94px;" in token_slice
    assert "border-radius: 18px;" in token_slice
    assert f"{node} i" in token_slice
    assert "width: 38px;" in token_slice
    assert "font-size: 0.96rem;" in token_slice
    assert f"{node} strong" in token_slice
    assert "margin-top: 54px;" in token_slice
    assert f"{board} .path-stage-node-badges" in token_slice
    assert "transform: scale(0.8);" in token_slice
    assert "prefers-reduced-motion: reduce" in token_slice

    assert "Path Stage Mobile Level Tokens" in readme
    assert "20260620-path-stage-mobile-level-tokens" in index

