from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


def test_command_bots_stage_is_bounded_viewport_board():
    styles = (WEB / "styles.css").read_text(encoding="utf-8")
    index = (WEB / "index.html").read_text(encoding="utf-8")
    readme = (WEB / "README.md").read_text(encoding="utf-8")

    marker = "/* 20260620-command-bot-viewport-board */"
    assert marker in styles
    board_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="bots"]'
    assert f"{scoped} .app-shell" in board_slice
    assert "height: 100svh;" in board_slice
    assert "grid-template-rows: auto auto auto minmax(0, 1fr);" in board_slice
    assert "overflow: hidden;" in board_slice

    assert f"{scoped} .command-archive-dock" in board_slice
    assert "max-height: 48px;" in board_slice

    assert f"{scoped} .bot-command-panel" in board_slice
    assert "height: min(100%, calc(100svh - 176px));" in board_slice
    assert "grid-template-rows: auto auto minmax(0, 1fr);" in board_slice
    assert "max-height: none;" in board_slice

    assert f"{scoped} .bot-command-matrix" in board_slice
    assert "grid-template-rows: auto auto minmax(0, 1fr);" in board_slice
    assert f"{scoped} .bot-command-card-rail" in board_slice
    assert "overflow: auto;" in board_slice
    assert "scrollbar-gutter: stable;" in board_slice
    assert "max-height: calc(100svh - 392px);" in board_slice

    assert "@media (max-width: 760px)" in board_slice
    mobile_slice = board_slice[board_slice.index("@media (max-width: 760px)") :]
    assert f"{scoped} .bot-command-panel" in mobile_slice
    assert "height: calc(100svh - 132px);" in mobile_slice
    assert "grid-auto-flow: column;" in mobile_slice
    assert "max-height: 214px;" in mobile_slice

    assert "@media (prefers-reduced-motion: reduce)" in board_slice
    assert "Command Bot Viewport Board" in readme
    assert "20260620-command-bot-viewport-board" in index