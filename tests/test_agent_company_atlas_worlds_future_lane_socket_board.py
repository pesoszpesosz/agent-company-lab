from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_worlds_future_lane_socket_board_makes_expansion_low_scroll_and_reusable():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function futureLaneSocketBlueprints(lanes, stats)" in app
    assert "function renderFutureLaneSocketBoard(lanes, stats)" in app
    assert "renderFutureLaneSocketBoard(lanes, stats)" in app
    assert 'class="future-lane-socket-board"' in app
    assert 'data-future-lane-socket="${escapeHtml(socket.id)}"' in app
    assert 'data-worlds-launch-action="${escapeHtml(socket.action)}"' in app
    assert "New Lane" in app
    assert "Bot Pod" in app
    assert "Mini Game" in app
    assert "Asset Kit" in app
    assert "Proof Trail" in app

    marker = "/* 20260620-worlds-future-lane-socket-board */"
    assert marker in styles
    socket_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="worlds"]'
    assert f"{scoped} .future-lane-socket-board" in socket_slice
    assert "grid-template-columns: minmax(112px, 0.18fr) minmax(0, 1fr);" in socket_slice
    assert "min-height: 92px;" in socket_slice
    assert f"{scoped} .future-lane-socket-track" in socket_slice
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in socket_slice
    assert f"{scoped} .future-lane-socket" in socket_slice
    assert "min-height: 70px;" in socket_slice
    assert f"{scoped} .future-lane-socket-ring" in socket_slice
    assert "@keyframes futureLaneSocketPulse" in socket_slice
    assert "@media (max-width: 560px)" in socket_slice
    assert "flex: 0 0 92px;" in socket_slice
    assert "@media (prefers-reduced-motion: reduce)" in socket_slice

    assert "Worlds Future Lane Socket Board" in readme
    assert "20260620-worlds-future-lane-socket-board" in index
    assert "20260620-path-stage-desktop-objective-bar-20260620-path-stage-realm-cartridge-20260620-worlds-future-lane-socket-board" in index