from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_board_fill_uses_viewport_without_restoring_scroll():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-board-fill */"
    assert marker in styles
    fill_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    board = f'{scoped} .path-map-board.mission-stage[data-path-stage-depth-view="stage"]'
    assert "@media (max-width: 560px)" in fill_slice
    assert board in fill_slice
    assert "grid-template-rows: minmax(394px, 1fr) 32px;" in fill_slice
    assert "min-height: min(540px, calc(100svh - 196px));" in fill_slice
    assert "max-height: min(540px, calc(100svh - 196px));" in fill_slice
    assert f"{board} .path-stage-ribbon" in fill_slice
    assert "min-height: clamp(382px, 50svh, 474px);" in fill_slice
    assert f"{board} .path-stage-node" in fill_slice
    assert "height: clamp(116px, 42%, 146px);" in fill_slice
    assert "min-height: 116px;" in fill_slice
    assert f"{board} .path-stage-depth-dock" in fill_slice
    assert "align-self: end;" in fill_slice

    assert "Path Stage Mobile Board Fill" in readme
    assert "20260620-path-stage-mobile-board-fill" in index
