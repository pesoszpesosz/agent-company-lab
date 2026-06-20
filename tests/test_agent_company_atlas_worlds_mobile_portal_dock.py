from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_worlds_mobile_portal_dock_makes_future_slots_icon_first():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-worlds-mobile-portal-dock */"
    assert marker in styles
    dock_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="worlds"]'
    assert "@media (max-width: 560px)" in dock_slice
    assert f"{scoped} .world-seed-cartridge-rail" in dock_slice
    assert "grid-template-columns: 76px minmax(0, 1fr);" in dock_slice
    assert "min-height: 64px;" in dock_slice
    assert f"{scoped} .world-seed-cartridge" in dock_slice
    assert "flex: 0 0 112px;" in dock_slice
    assert "min-height: 42px;" in dock_slice
    assert f"{scoped} .world-seed-cartridge em" in dock_slice
    assert f"{scoped} .worlds-expansion-deck" in dock_slice
    assert "min-height: 104px;" in dock_slice
    assert f"{scoped} .worlds-expansion-portal" in dock_slice
    assert "flex: 0 0 70px;" in dock_slice
    assert "place-items: center;" in dock_slice
    assert f"{scoped} .worlds-expansion-ring" in dock_slice
    assert "width: 30px;" in dock_slice
    assert f"{scoped} .worlds-expansion-portal strong" in dock_slice
    assert "-webkit-line-clamp: 2;" in dock_slice
    assert f"{scoped} .worlds-expansion-portal em" in dock_slice

    assert "Worlds Mobile Portal Dock" in readme
    assert "20260620-worlds-mobile-portal-dock" in index
    assert "20260620-path-stage-mobile-level-tokens-20260620-worlds-mobile-portal-dock" in index
