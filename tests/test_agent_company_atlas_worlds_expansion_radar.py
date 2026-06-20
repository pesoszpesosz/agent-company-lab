from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "web" / "app.js"
CSS = ROOT / "web" / "styles.css"
INDEX = ROOT / "web" / "index.html"
README = ROOT / "web" / "README.md"


def test_worlds_expansion_radar_model_and_mount():
    app = APP.read_text(encoding="utf-8")

    assert "function worldsExpansionRadarModel(lanes, stats)" in app
    assert "const agents = state.snapshot?.agents ?? [];" in app
    assert "const assets = visualAssetRecords();" in app
    assert "lanes.filter((lane) => lane.visual?.minigame?.texture).length" in app
    assert "agents.filter((agent) => agent.visual?.avatar).length" in app
    assert "Math.max(stats.futureSlots, Math.ceil(lanes.length / 2), 4)" in app
    assert 'id: "live-worlds"' in app
    assert 'id: "game-seeds"' in app
    assert 'id: "bot-pods"' in app
    assert 'id: "future-slots"' in app

    assert "function renderWorldsExpansionRadar(lanes, stats)" in app
    assert 'class="worlds-expansion-radar"' in app
    assert 'data-worlds-expansion-radar-cell="${escapeHtml(cell.id)}"' in app
    assert 'style="--radar-a:${escapeHtml(cell.accent)}; --radar-b:${escapeHtml(cell.accentAlt)}; --radar-charge:${cell.charge}%; --radar-index:${cell.index};"' in app
    assert "${renderWorldsExpansionRadar(lanes, stats)}" in app


def test_worlds_expansion_radar_styles_are_compact_and_motion_safe():
    css = CSS.read_text(encoding="utf-8")

    assert "/* 20260620-worlds-expansion-radar */" in css
    assert 'body[data-atlas-deck="worlds"] .worlds-expansion-radar' in css
    assert "grid-template-columns: minmax(150px, 0.74fr) repeat(4, minmax(0, 1fr));" in css
    assert "min-height: 78px;" in css
    assert ".worlds-expansion-radar-cell" in css
    assert "animation: worldsExpansionRadarSweep 8.4s ease-in-out infinite;" in css
    assert "@keyframes worldsExpansionRadarSweep" in css
    assert "@media (max-width: 760px)" in css
    assert "grid-auto-flow: column;" in css
    assert "grid-auto-columns: minmax(128px, 156px);" in css
    assert "overflow-x: auto;" in css
    assert "body[data-atlas-deck=\"worlds\"] .worlds-expansion-radar::before," in css
    assert "body[data-atlas-deck=\"worlds\"] .worlds-expansion-radar-orbit," in css
    assert ".path-stage-signal" in css


def test_worlds_expansion_radar_documented_and_cache_busted():
    readme = README.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    assert "Worlds Expansion Radar" in readme
    assert "live worlds, game seeds, bot pods, asset coverage, and future slots" in readme
    assert "20260620-worlds-expansion-radar" in index
    assert "20260620-worlds-future-lane-socket-board-20260620-worlds-expansion-radar" in index