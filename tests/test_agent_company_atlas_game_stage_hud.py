from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_game_stage_hud_replaces_page_chrome_with_arcade_navigation():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderGameStageHud(lane)" in app
    assert "${renderGameStageHud(lane)}" in app
    assert 'class="game-stage-hud"' in app
    assert 'class="game-stage-hud-button' in app
    assert 'data-detail-view="${escapeHtml(view.id)}"' in app
    assert "gameStepCount(lane)" in app

    assert ".detail-content.detail-view-game .detail-top" in styles
    game_top_block = styles[
        styles.index(".detail-content.detail-view-game .detail-top") : styles.index(".detail-content.detail-view-game .detail-tabs")
    ]
    assert "display: none" in game_top_block

    assert ".detail-content.detail-view-game .detail-tabs" in styles
    game_tabs_start = styles.index(".detail-content.detail-view-game .detail-tabs")
    game_tabs_end = styles.index(".game-stage-hud", game_tabs_start)
    assert "display: none" in styles[game_tabs_start:game_tabs_end]

    assert ".game-stage-hud" in styles
    assert ".game-stage-hud-button.active" in styles
    assert ".game-stage-hud-meter" in styles
    assert 'body[data-detail-view="game"] .systems-cell-grid' in styles
    compact_grid_start = styles.index('body[data-detail-view="game"] .systems-cell-grid')
    compact_grid_block = styles[compact_grid_start : styles.index("@keyframes systemsGridGlow", compact_grid_start)]
    assert "display: none" in compact_grid_block

    assert "Game Stage HUD" in readme
    assert "20260618-game-stage-hud" in index


def test_game_stage_mobile_focus_compacts_long_minigame_grids():
    styles = read("web/styles.css")

    assert "body[data-detail-view=\"game\"] .systems-cell:not(.is-current)" in styles
    assert "body[data-detail-view=\"game\"] .baseline-stage:not(.is-current)" in styles
    assert "body[data-detail-view=\"game\"] .foundry-stage:not(.is-current)" in styles
    assert "body[data-detail-view=\"game\"] .scout-card:not(.is-current)" in styles

    compact_start = styles.index("body[data-detail-view=\"game\"] .systems-cell:not(.is-current)")
    compact_block = styles[compact_start : styles.index("@media", compact_start) if "@media" in styles[compact_start:] else len(styles)]
    assert "display: none" in compact_block
    assert "@media (max-width: 860px)" in styles[:compact_start]
