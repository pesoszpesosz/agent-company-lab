from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_controller_dock_promotes_level_reel_as_game_controls():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-controller-dock */"
    assert marker in styles
    dock_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    base = f"{scoped} .detail-content.detail-view-overview"
    row = f'{base} .quest-action-row[data-quest-dock-density="secondary"]'
    reel = f"{base} .quest-level-reel"
    node = f"{base} .quest-level-reel-node"

    assert "@media (max-width: 560px)" in dock_slice
    assert row in dock_slice
    assert "display: none !important;" in dock_slice
    assert reel in dock_slice
    assert "right: auto;" in dock_slice
    assert "bottom: 34px;" in dock_slice
    assert "left: 50%;" in dock_slice
    assert "width: min(236px, calc(100vw - 84px));" in dock_slice
    assert "grid-template-columns: repeat(5, minmax(0, 34px));" in dock_slice
    assert "opacity: 0.92;" in dock_slice
    assert "transform: translateX(-50%);" in dock_slice
    assert node in dock_slice
    assert "min-height: 28px;" in dock_slice
    assert f"{node} i" in dock_slice
    assert "width: 20px;" in dock_slice
    assert f"{node} span" in dock_slice
    assert "font-size: 0;" in dock_slice
    assert "Command Cockpit Mobile Controller Dock" in readme
    assert "20260620-command-cockpit-mobile-controller-dock" in index
