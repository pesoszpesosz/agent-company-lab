from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "web" / "app.js"
CSS = ROOT / "web" / "styles.css"
INDEX = ROOT / "web" / "index.html"
README = ROOT / "web" / "README.md"


def test_atlas_command_ribbon_is_wired_into_global_shell():
    app = APP.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    assert 'atlasCommandRibbon: document.querySelector("#atlas-command-ribbon")' in app
    assert 'id="atlas-command-ribbon"' in index
    assert 'class="atlas-command-ribbon"' in index
    assert "function atlasCommandRibbonModel()" in app
    assert "function renderAtlasCommandRibbon()" in app
    assert "renderAtlasCommandRibbon();" in app
    assert "const atlasCommandRibbonButton = event.target.closest(\"[data-atlas-command-ribbon-action]\");" in app
    assert "activateAtlasCommandRibbon(atlasCommandRibbonButton.dataset.atlasCommandRibbonAction);" in app


def test_atlas_command_ribbon_model_uses_existing_snapshot_signals():
    app = APP.read_text(encoding="utf-8")

    assert "const totals = state.snapshot?.totals ?? {};" in app
    assert "const lanes = state.snapshot?.lanes ?? [];" in app
    assert "const agents = state.snapshot?.agents ?? [];" in app
    assert "const feedItems = state.snapshot?.missionFeed?.items ?? [];" in app
    assert "const assets = visualAssetRecords();" in app
    assert "const gateCount = (totals.blockers ?? 0) + (totals.pendingRequests ?? 0);" in app
    assert "const selected = selectedLane();" in app
    assert 'id: "lanes"' in app
    assert 'id: "gates"' in app
    assert 'id: "bots"' in app
    assert 'id: "wins"' in app
    assert 'id: "assets"' in app
    assert 'id: "next"' in app
    assert 'data-atlas-command-ribbon-cell="${escapeHtml(cell.id)}"' in app
    assert 'data-atlas-command-ribbon-action="${escapeHtml(cell.action)}"' in app


def test_atlas_command_ribbon_styles_are_compact_premium_and_motion_safe():
    styles = CSS.read_text(encoding="utf-8")

    marker = "/* 20260620-atlas-command-ribbon */"
    assert marker in styles
    ribbon = styles[styles.index(marker) :]
    assert ".atlas-command-ribbon" in ribbon
    assert "grid-template-columns: minmax(142px, 0.62fr) repeat(6, minmax(0, 1fr));" in ribbon
    assert "min-height: 62px;" in ribbon
    assert ".atlas-command-ribbon-cell" in ribbon
    assert "animation: atlasCommandRibbonSweep 8.6s ease-in-out infinite;" in ribbon
    assert "@keyframes atlasCommandRibbonSweep" in ribbon
    assert "@media (max-width: 760px)" in ribbon
    assert "grid-auto-flow: column;" in ribbon
    assert "grid-auto-columns: minmax(118px, 152px);" in ribbon
    assert "overflow-x: auto;" in ribbon
    assert ".atlas-command-ribbon::before," in ribbon
    assert ".path-stage-signal" in ribbon[ribbon.rindex("@media (prefers-reduced-motion: reduce)") :]


def test_atlas_command_ribbon_documented_and_cache_busted():
    readme = README.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    assert "Atlas Command Ribbon" in readme
    assert "lanes, gates, bots, wins, assets, and next focus" in readme
    assert "20260620-atlas-command-ribbon" in index