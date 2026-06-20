from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_board_first_shelf_collapses_desktop_hud_rows():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-board-first-shelf */"
    assert marker in styles
    shelf_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    assert "@media (min-width: 1040px) and (min-height: 700px)" in shelf_slice
    assert f"{scoped} .cockpit-command-stack" in shelf_slice
    assert "grid-template-columns: minmax(124px, 0.92fr) minmax(112px, 0.78fr) minmax(112px, 0.78fr) minmax(124px, 0.86fr);" in shelf_slice
    assert "grid-template-areas: \"control run crew unlock\";" in shelf_slice
    assert "margin: 0 0 5px;" in shelf_slice
    assert f"{scoped} .cockpit-command-stack > .cockpit-control-pad" in shelf_slice
    assert f"{scoped} .cockpit-command-stack > .cockpit-runway-pulse" in shelf_slice
    assert f"{scoped} .cockpit-command-stack > .cockpit-crew-handoff-rail" in shelf_slice
    assert f"{scoped} .cockpit-command-stack > .cockpit-unlock-chain" in shelf_slice
    assert "min-height: 38px;" in shelf_slice
    assert f"{scoped} .cockpit-command-stack em" in shelf_slice
    assert "display: none;" in shelf_slice
    assert f"{scoped} .command-route-minimap" in shelf_slice
    assert f"{scoped} .command-channel-dock" in shelf_slice
    assert "min-height: 44px;" in shelf_slice
    assert "margin-bottom: 4px;" in shelf_slice
    assert f"{scoped} .command-route-core em" in shelf_slice
    assert f"{scoped} .command-channel-agent em" in shelf_slice
    assert f"{scoped} .command-channel-cell em" in shelf_slice
    assert f"{scoped} .quest-board-stack" in shelf_slice
    assert "min-height: clamp(320px, calc(100vh - 396px), 520px);" in shelf_slice
    assert "@media (prefers-reduced-motion: reduce)" in shelf_slice

    assert "20260620-command-cockpit-board-first-shelf" in index
    assert "Command Cockpit Board First Shelf" in readme
    assert "collapses the command HUD into one desktop shelf" in readme