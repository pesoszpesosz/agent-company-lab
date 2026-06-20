from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_reward_medal_dock_stops_toast_from_owning_the_screen():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-reward-medal-dock */"
    assert marker in styles
    dock_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    toast = f"{scoped} .unlock-toast"

    assert "@media (max-width: 560px)" in dock_slice
    assert toast in dock_slice
    assert "left: 10px;" in dock_slice
    assert "right: auto;" in dock_slice
    assert "width: min(214px, calc(100vw - 20px));" in dock_slice
    assert "grid-template-columns: 34px minmax(0, 1fr);" in dock_slice
    assert "min-height: 52px;" in dock_slice
    assert "max-height: 56px;" in dock_slice
    assert f"{toast}-art" in dock_slice
    assert "min-height: 38px;" in dock_slice
    assert f"{toast}-copy" in dock_slice
    assert "padding-right: 28px;" in dock_slice
    assert f"{toast}-meta" in dock_slice
    assert "display: none;" in dock_slice[dock_slice.index(f"{toast}-meta") :]
    assert f"{toast}-actions .trophy-open" in dock_slice
    assert "display: none;" in dock_slice[dock_slice.index(f"{toast}-actions .trophy-open") :]
    assert "Command Cockpit Mobile Reward Medal Dock" in readme
    assert "20260620-command-cockpit-mobile-reward-medal-dock" in index
