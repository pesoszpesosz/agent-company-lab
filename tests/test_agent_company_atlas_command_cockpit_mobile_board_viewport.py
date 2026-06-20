from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_overview_uses_bounded_game_board_viewport():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-board-viewport */"
    assert marker in styles
    board_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    stage = f'{scoped} .active-lane-mounted-stage[data-active-stage-view="overview"]'
    quest = f'{scoped} .detail-content.detail-view-overview .quest-cockpit[data-quest-motion-quality="premium"]'

    assert "@media (max-width: 560px)" in board_slice
    assert f"{scoped} .detail-content.detail-view-overview" in board_slice
    assert "display: grid !important;" in board_slice
    assert "height: clamp(420px, calc(100vh - 212px), 642px) !important;" in board_slice
    assert "overflow: hidden !important;" in board_slice
    assert stage in board_slice
    assert "height: 100% !important;" in board_slice
    assert "max-height: calc(100vh - 222px) !important;" in board_slice
    assert f"{stage} .active-lane-stage-lens" in board_slice
    assert f"{stage} > .detail-section:first-of-type" in board_slice
    assert quest in board_slice
    assert "grid-template-rows: 40px minmax(0, 1fr) !important;" in board_slice
    assert "Command Cockpit Mobile Board Viewport" in readme
    assert "20260620-command-cockpit-mobile-board-viewport" in index
