from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_node_cartridge_makes_selected_lens_read_like_game_pickup():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-node-cartridge */"
    assert marker in styles
    cartridge_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    base = f"{scoped} .detail-content.detail-view-overview"
    tray = f"{base} .quest-selected-node-lens-tray"
    copy = f"{base} .quest-selected-node-lens-copy"

    assert "@media (max-width: 560px)" in cartridge_slice
    assert tray in cartridge_slice
    assert "bottom: 92px;" in cartridge_slice
    assert "grid-template-columns: minmax(0, 1fr) 58px;" in cartridge_slice
    assert "min-height: 42px;" in cartridge_slice
    assert "max-height: 46px;" in cartridge_slice
    assert copy in cartridge_slice
    assert f"{copy} b" in cartridge_slice
    assert "display: none;" in cartridge_slice
    assert f"{base} .quest-selected-node-lens-copy strong" in cartridge_slice
    assert "font-size: 0.58rem;" in cartridge_slice
    assert f"{base} .quest-selected-node-lens-jump" in cartridge_slice
    assert "min-height: 32px;" in cartridge_slice
    assert "Command Cockpit Mobile Node Cartridge" in readme
    assert "20260620-command-cockpit-mobile-node-cartridge" in index
