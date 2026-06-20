from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_asset_production_board_tracks_visual_database_coverage():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")

    assert "assetProductionBoard: document.querySelector(\"#asset-production-board\")" in app
    assert "function assetProductionBoardModel(assets)" in app
    assert "function renderAssetProductionBoard(assets)" in app
    assert "renderAssetProductionBoard(assets);" in app
    assert 'id="asset-production-board"' in index
    assert 'class="asset-production-board"' in index
    assert 'class="asset-production-cell ${escapeHtml(cell.tone)}"' in app
    assert 'data-asset-production-cell="${escapeHtml(cell.id)}"' in app
    assert "Lane Avatars" in app
    assert "Bot Portraits" in app
    assert "Game Textures" in app
    assert "System Art" in app
    assert "Future Slots" in app
    assert "assets.filter((asset) => asset.kind === \"lane\").length" in app
    assert "assets.filter((asset) => asset.kind === \"agent\").length" in app
    assert "assets.filter((asset) => asset.kind === \"game\").length" in app
    assert "assets.filter((asset) => asset.kind === \"system\").length" in app
    assert "Math.max(4, (state.snapshot?.lanes?.length ?? 0) + 4 - assets.filter((asset) => asset.kind === \"game\").length)" in app

    marker = "/* 20260620-asset-production-board */"
    assert marker in styles
    board_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="library"][data-atlas-stage="assets"]'
    assert f"{scoped} .asset-production-board" in board_slice
    assert "grid-template-columns: minmax(180px, 0.82fr) repeat(5, minmax(0, 1fr));" in board_slice
    assert "min-height: 94px;" in board_slice
    assert f"{scoped} .asset-production-cell" in board_slice
    assert "animation: assetProductionScan 8.2s ease-in-out infinite;" in board_slice
    assert "@keyframes assetProductionScan" in board_slice
    assert "@media (max-width: 760px)" in board_slice
    mobile_slice = board_slice[board_slice.index("@media (max-width: 760px)") :]
    assert "grid-auto-flow: column;" in mobile_slice
    assert "grid-auto-columns: minmax(132px, 156px);" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice
    assert "@media (prefers-reduced-motion: reduce)" in board_slice

    assert "20260620-asset-production-board" in index
    assert "Asset Production Board" in readme