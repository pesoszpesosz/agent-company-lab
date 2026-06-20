from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_viewport_console_governor_reduces_scroll_and_tones_motion():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-viewport-console-governor */"
    assert marker in styles
    governor_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    assert "@media (min-width: 1040px) and (min-height: 700px)" in governor_slice
    assert f"{scoped} .workspace" in governor_slice
    assert "grid-template-columns: minmax(230px, 0.64fr) minmax(0, 1.76fr);" in governor_slice
    assert "height: calc(100vh - 128px);" in governor_slice
    assert "overflow: hidden;" in governor_slice
    assert f"{scoped} .lane-list" in governor_slice
    assert "max-height: calc(100vh - 250px);" in governor_slice
    assert "scrollbar-gutter: stable;" in governor_slice
    assert f"{scoped} .detail-panel" in governor_slice
    assert f"{scoped} .active-lane-mounted-stage" in governor_slice
    assert f"{scoped} .active-lane-mounted-stage-scan" in governor_slice
    assert "animation: commandViewportConsoleScan 9.6s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in governor_slice
    assert f"{scoped} .quest-cockpit" in governor_slice
    assert "grid-template-rows: minmax(0, 1fr) auto;" in governor_slice
    assert "@media (max-width: 760px)" in governor_slice
    assert "min-height: calc(100svh - 76px);" in governor_slice
    assert "@keyframes commandViewportConsoleScan" in governor_slice
    assert "prefers-reduced-motion: reduce" in governor_slice

    assert "20260620-command-cockpit-viewport-console-governor" in index
    assert "Command Cockpit Viewport Console Governor" in readme