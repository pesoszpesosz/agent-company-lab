from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_board_first_collapses_duplicate_overview_layers():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-board-first */"
    assert marker in styles
    board_slice = styles[styles.index(marker) :]

    assert "@media (max-width: 560px)" in board_slice
    assert ".active-lane-mounted-stage[data-active-stage-view=\"path\"]" in board_slice
    assert "min-height: min(560px, calc(100svh - 158px));" in board_slice
    assert ".active-lane-holo-board" in board_slice
    assert ".active-lane-objective-beacons" in board_slice
    assert ".active-lane-bot-party-dock" in board_slice
    assert "display: none;" in board_slice
    assert "min-height: min(468px, calc(100svh - 164px));" in board_slice
    assert "min-height: clamp(210px, 29svh, 268px);" in board_slice

    assert "Path Stage Mobile Board First" in readme
    assert "20260620-path-stage-mobile-board-first" in index
