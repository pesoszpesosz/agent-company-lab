from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_asset_vault_assets_stage_is_bounded_inventory_board():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-asset-vault-inventory-board */"
    assert marker in styles
    board_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="library"][data-atlas-stage="assets"]'
    assert f"{scoped} .operator-roster-panel" in board_slice
    assert "max-height: 168px;" in board_slice
    assert f"{scoped} .agent-roster" in board_slice
    assert "scroll-snap-type: x proximity;" in board_slice
    assert f"{scoped} .operator-identity-bay" in board_slice
    assert f"{scoped} .agent-sprite-foundry" in board_slice
    assert f"{scoped} .asset-vault-panel" in board_slice
    assert "grid-template-rows: auto auto minmax(0, 1fr);" in board_slice
    assert "max-height: min(720px, calc(100vh - 154px));" in board_slice
    assert f"{scoped} .asset-vault" in board_slice
    assert "overflow: auto;" in board_slice
    assert "overscroll-behavior: contain;" in board_slice
    assert "grid-template-columns: repeat(auto-fill, minmax(132px, 1fr));" in board_slice
    assert f"{scoped} .asset-card" in board_slice
    assert "height: 174px;" in board_slice
    assert "@media (max-width: 560px)" in board_slice
    assert "grid-auto-flow: column;" in board_slice
    assert "grid-template-rows: repeat(2, 126px);" in board_slice
    assert "scroll-snap-type: x mandatory;" in board_slice
    assert "@keyframes assetVaultInventoryScan" in board_slice
    assert "prefers-reduced-motion: reduce" in board_slice

    assert "Asset Vault Inventory Board" in readme
    assert "20260620-asset-vault-inventory-board" in index
    assert "20260620-worlds-mobile-portal-dock-20260620-asset-vault-inventory-board" in index
