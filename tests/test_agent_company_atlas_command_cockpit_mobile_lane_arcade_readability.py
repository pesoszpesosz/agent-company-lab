from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_mobile_lane_arcade_uses_readable_avatar_chips_without_blank_label_plaque():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-lane-arcade-readability */"
    assert marker in styles
    mobile_slice = styles[styles.index(marker) :]

    overview = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'

    assert "@media (max-width: 560px)" in mobile_slice
    assert f"{overview} .lane-list::before" in mobile_slice
    assert "display: none !important;" in mobile_slice
    assert f"{overview} .lane-list::after" in mobile_slice
    assert "display: none !important;" in mobile_slice
    assert f"{overview} .lane-list" in mobile_slice
    assert "grid-auto-columns: 58px !important;" in mobile_slice
    assert "padding: 6px 7px !important;" in mobile_slice
    assert f"{overview} .lane-button" in mobile_slice
    assert f"{overview} .lane-list[data-lane-selector-mode=\"gate\"] .lane-button" in mobile_slice
    assert "flex: 0 0 58px !important;" in mobile_slice
    assert "min-width: 58px !important;" in mobile_slice
    assert "max-width: 58px !important;" in mobile_slice
    assert "height: 40px !important;" in mobile_slice
    assert "place-items: center;" in mobile_slice
    assert f"{overview} .lane-button::before" in mobile_slice
    assert 'content: "L" attr(data-lane-gate-rank);' in mobile_slice
    assert f"{overview} .lane-button.active::before" in mobile_slice
    assert 'content: "LIVE";' in mobile_slice
    assert f"{overview} .lane-button-avatar" in mobile_slice
    assert f"{overview} .lane-list[data-lane-selector-mode=\"gate\"] .lane-button-avatar" in mobile_slice
    assert "display: grid !important;" in mobile_slice
    assert "width: 26px;" in mobile_slice
    assert "height: 26px;" in mobile_slice
    assert f"{overview} .lane-list[data-lane-selector-mode=\"gate\"] .lane-button-top" in mobile_slice
    assert f"{overview} .lane-button-identity > div" in mobile_slice
    assert f"{overview} .lane-expansion-slot" in mobile_slice
    assert "width: 50px;" in mobile_slice
    assert "Command Cockpit Mobile Lane Arcade Readability" in readme
    assert "20260620-command-cockpit-mobile-lane-arcade-readability" in index