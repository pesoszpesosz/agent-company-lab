from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_desktop_scanner_collapse_lets_depth_stack_replace_duplicate_panel():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-desktop-scanner-collapse */"
    assert marker in styles
    collapse_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    board = f'{scoped} .path-map-board.mission-stage[data-path-stage-depth-view="stage"]'

    assert "@media (min-width: 1121px)" in collapse_slice
    assert f"{board} .path-core-deck" in collapse_slice
    assert "display: none;" in collapse_slice
    assert f"{scoped} .path-stage-infinite-depth-stack" in collapse_slice
    assert "right: 18px;" in collapse_slice
    assert "width: min(360px, calc(100% - 36px));" in collapse_slice
    assert "Path Stage Desktop Scanner Collapse" in readme
    assert "20260620-path-stage-desktop-scanner-collapse" in index