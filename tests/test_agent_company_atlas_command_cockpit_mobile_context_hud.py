from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_context_hud_reduces_competing_layers():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-context-hud */"
    assert marker in styles
    hud_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    base = f"{scoped} .detail-content.detail-view-overview"

    assert "@media (max-width: 760px)" in hud_slice
    assert f"{base} .quest-path-depth-lens" in hud_slice
    assert f"{base} .quest-cinematic-focus-plate" in hud_slice
    assert f"{base} .quest-mission-stack" in hud_slice
    assert "opacity: 0 !important;" in hud_slice
    assert "display: none !important;" in hud_slice
    assert f"{base} .quest-level-reel" in hud_slice
    assert "bottom: 34px;" in hud_slice
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in hud_slice
    assert "opacity: 0.64;" in hud_slice
    assert f"{base} .quest-board-identity-cartridge" in hud_slice
    assert "display: none !important;" in hud_slice
    assert f"{base} .quest-spotlight-camera-aperture" in hud_slice
    assert "opacity: 0.24;" in hud_slice
    assert f"{base} .quest-selected-node-lens-tray" in hud_slice
    assert "bottom: 96px;" in hud_slice
    assert "grid-template-columns: minmax(0, 1fr) 70px;" in hud_slice
    assert f"{base} .quest-selected-node-lens-depth" in hud_slice
    assert "text-overflow: ellipsis;" in hud_slice
    assert "Command Cockpit Mobile Context HUD" in readme
    assert "20260620-command-cockpit-mobile-context-hud" in index
