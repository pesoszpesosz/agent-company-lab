from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_lane_arcade_rail_reduces_selector_scroll_and_reads_like_game_launch_rail():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-lane-arcade-rail */"
    assert marker in styles
    arcade_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"]'
    overview = f'{scoped}[data-detail-view="overview"]'

    assert f"{scoped} .lane-list-panel" in arcade_slice
    assert "max-height: clamp(106px, 16vh, 138px);" in arcade_slice
    assert "height: clamp(106px, 16vh, 138px) !important;" in arcade_slice
    assert "max-height: clamp(106px, 16vh, 138px) !important;" in arcade_slice
    assert "overflow: hidden;" in arcade_slice
    assert f"{scoped} .lane-list" in arcade_slice
    assert "grid-auto-flow: column;" in arcade_slice
    assert "overflow-x: auto;" in arcade_slice
    assert "scroll-snap-type: x proximity;" in arcade_slice
    assert f"{scoped} .lane-list::before" in arcade_slice
    assert "LANE ARCADE" in arcade_slice
    assert f"{scoped} .lane-button" in arcade_slice
    assert "scroll-snap-align: center;" in arcade_slice
    assert "min-width: 132px;" in arcade_slice
    assert f"{scoped} .lane-button.active::after" in arcade_slice
    assert "animation: laneArcadeActiveSweep" in arcade_slice
    assert f"{scoped} .lane-button.reserve" in arcade_slice
    assert f"{scoped} .lane-expansion-slots" in arcade_slice
    assert "grid-auto-flow: column;" in arcade_slice
    assert f"{overview} .workspace" in arcade_slice
    assert "grid-template-columns: minmax(0, 1fr);" in arcade_slice
    assert "grid-template-rows: auto minmax(0, 1fr);" in arcade_slice
    assert f"{overview} .lane-list-panel" in arcade_slice
    assert "grid-column: 1;" in arcade_slice
    assert "grid-row: 1;" in arcade_slice
    assert f"{overview} .detail-panel" in arcade_slice
    assert "grid-row: 2;" in arcade_slice
    assert "@media (max-width: 560px)" in arcade_slice
    assert arcade_slice.rindex("@media (max-width: 560px)") > arcade_slice.rindex("height: clamp(106px, 16vh, 138px) !important;")
    assert f"{overview} .lane-list-panel" in arcade_slice
    assert "height: 56px !important;" in arcade_slice
    assert "max-height: 56px !important;" in arcade_slice
    assert "height: 44px !important;" in arcade_slice
    assert f"{overview} .lane-button" in arcade_slice
    assert "min-width: 52px !important;" in arcade_slice
    assert "Command Cockpit Lane Arcade Rail" in readme
    assert "20260620-command-cockpit-lane-arcade-rail" in index