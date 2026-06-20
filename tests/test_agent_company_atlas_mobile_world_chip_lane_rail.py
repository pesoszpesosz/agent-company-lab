from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_mobile_world_chip_lane_rail_turns_paths_into_compact_world_slots():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-world-chip-rail */"
    assert marker in styles
    rail_slice = styles[styles.index(marker) :]

    assert "@media (max-width: 560px)" in rail_slice
    assert ".lane-list[data-lane-selector-mode=\"gate\"]" in rail_slice
    assert "height: 42px !important;" in rail_slice
    assert ".lane-list-panel::after" in rail_slice
    assert ".lane-button-top" in rail_slice
    assert "display: none !important;" in rail_slice
    assert ".lane-button::after" in rail_slice
    assert "var(--lane-progress, 0%)" in rail_slice
    assert ".lane-button.active" in rail_slice
    assert "flex-basis: 64px;" in rail_slice
    assert ".lane-world-signal" in rail_slice
    assert "display: grid !important;" in rail_slice
    assert ".lane-world-signal em" in rail_slice

    assert "Mobile World Chip Lane Rail" in readme
    assert "future lanes read as compact playable worlds" in readme
    assert "20260620-command-cockpit-mobile-world-chip-rail" in index
