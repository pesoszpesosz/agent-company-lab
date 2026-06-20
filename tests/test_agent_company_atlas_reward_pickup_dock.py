from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_asset_route_reward_pickup_dock_stays_out_of_asset_grid():
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")

    marker = "/* 20260620-reward-pickup-dock */"
    assert marker in styles
    dock_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="library"][data-atlas-stage="assets"]'
    assert f"{scoped} .unlock-toast" in dock_slice
    assert "top: 286px;" in dock_slice
    assert "bottom: auto;" in dock_slice
    assert "width: min(318px, calc(100vw - 28px));" in dock_slice
    assert "max-height: 72px;" in dock_slice
    assert f"{scoped} .agent-roster" in dock_slice
    assert "padding-right: 340px;" in dock_slice
    assert f"{scoped} .unlock-toast-copy > p:not(.eyebrow)" in dock_slice
    assert "display: none;" in dock_slice[dock_slice.index(f"{scoped} .unlock-toast-copy > p:not(.eyebrow)") :]
    assert f"{scoped} .unlock-toast-meta" in dock_slice
    assert f"{scoped} .unlock-toast-actions .trophy-open" in dock_slice
    assert "@media (max-width: 560px)" in dock_slice
    assert "top: 224px;" in dock_slice
    assert "width: min(210px, calc(100vw - 28px));" in dock_slice
    assert "padding-right: 220px;" in dock_slice
    assert "prefers-reduced-motion: reduce" in dock_slice

    assert "20260620-reward-pickup-dock" in index
    assert "20260620-asset-vault-inventory-board-20260620-reward-pickup-dock" in index
    assert "Reward Pickup Dock" in readme