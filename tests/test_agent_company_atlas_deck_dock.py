from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_atlas_deck_dock_contract_is_wired():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert 'atlasDeckDock: document.querySelector("#atlas-deck-dock")' in app
    assert "activeAtlasDeck" in app
    assert "ATLAS_DECK_KEY" in app
    assert "ATLAS_DECKS" in app
    assert "function renderAtlasDeckDock()" in app
    assert "function setAtlasDeck(deckId" in app
    assert "function applyAtlasDeck()" in app
    assert "data-atlas-deck" in app
    assert 'event.target.closest("#atlas-deck-dock [data-atlas-deck]")' in app
    assert 'event.target.closest("[data-atlas-deck]")' not in app
    assert 'params.set("deck", state.activeAtlasDeck)' in app
    assert "setAtlasDeck(\"history\"" in app
    assert "setAtlasDeck(\"command\"" in app
    assert "setAtlasDeck(\"library\"" in app

    assert 'id="atlas-deck-dock"' in index
    assert 'data-atlas-deck-section="control all"' in index
    assert 'data-atlas-deck-section="worlds all"' in index
    assert 'data-atlas-deck-section="command all"' in index
    assert 'data-atlas-deck-section="history all"' in index
    assert 'data-atlas-deck-section="library all"' in index

    for token in [
        ".atlas-deck-dock",
        ".atlas-deck-button",
        'body[data-atlas-deck="control"]',
        'body[data-atlas-deck="worlds"]',
        'body[data-atlas-deck="command"]',
        'body[data-atlas-deck="history"]',
        'body[data-atlas-deck="library"]',
        "deckButtonSweep",
        "deckSectionIn",
    ]:
        assert token in styles

    assert "Atlas Deck Dock" in readme
    assert "less scrolling" in readme


def test_atlas_teleport_rail_shortens_the_scroll_stack():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert 'atlasTeleportRail: document.querySelector("#atlas-teleport-rail")' in app
    assert "const ATLAS_TELEPORTS = [" in app
    assert "function renderAtlasTeleportRail()" in app
    assert "function activateAtlasTeleport(teleportId)" in app
    assert 'data-atlas-teleport="${escapeHtml(item.id)}"' in app
    assert 'event.target.closest("#atlas-teleport-rail [data-atlas-teleport]")' in app
    assert 'setAtlasDeck(item.deck, { scroll: false, stage: item.stage })' in app
    assert "document.querySelector(item.target)?.scrollIntoView" in app

    assert 'id="atlas-teleport-rail"' in index

    rail_start = styles.index(".atlas-teleport-rail")
    rail_end = styles.index(".hero-grid", rail_start)
    rail_slice = styles[rail_start:rail_end]
    assert "position: sticky;" in rail_slice
    assert "top: 82px;" in rail_slice
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in rail_slice
    assert "min-height: 42px;" in rail_slice
    assert ".atlas-teleport-pad" in rail_slice
    assert ".atlas-teleport-pad.active" in rail_slice
    assert "animation: atlasTeleportPulse 4.4s ease-in-out infinite;" in rail_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".atlas-teleport-rail" in mobile_slice
    assert "position: fixed;" in mobile_slice
    assert "bottom: 10px;" in mobile_slice
    assert "grid-auto-flow: column;" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice
    assert ".app-shell" in mobile_slice
    assert "padding-bottom: 92px;" in mobile_slice

    assert "@keyframes atlasTeleportPulse" in styles
    assert "Atlas Teleport Rail" in readme
    assert "20260619-atlas-teleport-rail" in index


def test_deck_stage_compression_bounds_active_deck_surfaces():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-deck-stage-compression" in index

    compression_start = styles.index('body[data-atlas-deck]:not([data-atlas-deck="all"]) [data-atlas-deck-section]')
    compression_end = styles.index(".brand-block", compression_start)
    compression_slice = styles[compression_start:compression_end]
    assert "max-height: min(640px, calc(100vh - 154px));" in compression_slice
    assert "overflow-y: auto;" in compression_slice
    assert "scrollbar-gutter: stable;" in compression_slice
    assert "scroll-snap-align: start;" in compression_slice
    assert "overscroll-behavior: contain;" in compression_slice
    assert 'body[data-atlas-deck="all"] [data-atlas-deck-section]' in compression_slice
    assert "max-height: none;" in compression_slice

    shell_start = styles.index(".app-shell")
    shell_slice = styles[shell_start : shell_start + 260]
    assert "scroll-snap-type: y proximity;" in shell_slice

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert 'body[data-atlas-deck]:not([data-atlas-deck="all"]) [data-atlas-deck-section]' in mobile_slice
    assert "max-height: min(520px, calc(100vh - 132px));" in mobile_slice

    assert "Deck Stage Compression" in readme


def test_deck_stage_compression_has_premium_stage_frame_motion():
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260619-deck-stage-frame-glow" in index

    frame_start = styles.index('body[data-atlas-deck]:not([data-atlas-deck="all"]) [data-atlas-deck-section]::before')
    frame_end = styles.index(".brand-block", frame_start)
    frame_slice = styles[frame_start:frame_end]
    assert 'body[data-atlas-deck]:not([data-atlas-deck="all"]) [data-atlas-deck-section]::before' in frame_slice
    assert 'body[data-atlas-deck]:not([data-atlas-deck="all"]) [data-atlas-deck-section]::after' in frame_slice
    assert "position: sticky;" in frame_slice
    assert "top: 0;" in frame_slice
    assert "height: 2px;" in frame_slice
    assert "animation: deckStageFrameScan 4.8s ease-in-out infinite;" in frame_slice
    assert "pointer-events: none;" in frame_slice
    assert 'body[data-atlas-deck="all"] [data-atlas-deck-section]::before' in frame_slice
    assert "content: none;" in frame_slice

    assert "@keyframes deckStageFrameScan" in styles
    assert "Deck Stage Frame Glow" in readme


def test_teleport_rail_focuses_one_stage_instead_of_whole_deck_stack():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "activeAtlasStage" in app
    assert "function defaultAtlasStageForDeck(deck)" in app
    assert "function validAtlasStage(stage)" in app
    assert "document.body.dataset.atlasStage = validAtlasStage(state.activeAtlasStage);" in app
    assert "params.set(\"stage\", state.activeAtlasStage);" in app
    assert "stage: \"assets\"" in app
    assert "setAtlasDeck(item.deck, { scroll: false, stage: item.stage })" in app
    assert "state.activeAtlasStage === item.stage" in app

    assert "20260619-atlas-stage-focus" in index
    assert 'data-atlas-stage="assets"' in index
    assert 'data-atlas-stage="worlds"' in index
    assert 'data-atlas-stage="feed"' in index
    assert 'data-atlas-stage="bots"' in index
    assert 'data-atlas-stage="cockpit map"' in index

    focus_start = styles.index('body[data-atlas-deck]:not([data-atlas-deck="all"])[data-atlas-stage="assets"]')
    focus_end = styles.index(".brand-block", focus_start)
    focus_slice = styles[focus_start:focus_end]
    assert 'body[data-atlas-deck]:not([data-atlas-deck="all"])[data-atlas-stage="assets"] [data-atlas-stage]:not([data-atlas-stage~="assets"])' in focus_slice
    assert 'body[data-atlas-deck]:not([data-atlas-deck="all"])[data-atlas-stage="worlds"] [data-atlas-stage]:not([data-atlas-stage~="worlds"])' in focus_slice
    assert 'body[data-atlas-deck]:not([data-atlas-deck="all"])[data-atlas-stage="feed"] [data-atlas-stage]:not([data-atlas-stage~="feed"])' in focus_slice
    assert 'body[data-atlas-deck]:not([data-atlas-deck="all"])[data-atlas-stage="bots"] [data-atlas-stage]:not([data-atlas-stage~="bots"])' in focus_slice
    assert 'body[data-atlas-deck="all"] [data-atlas-stage]' in focus_slice
    assert "display: revert;" in focus_slice

    assert "Atlas Stage Focus" in readme
