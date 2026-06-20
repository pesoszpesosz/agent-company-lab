from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_worlds_launch_surface_contract_is_wired():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/lane-expansion-portal-deck-20260619.png"

    assert 'worldsLaunch: document.querySelector("#worlds-launch")' in app
    assert "function worldsLaunchStats()" in app
    assert "function worldsLaunchLanes()" in app
    assert "function worldsExpansionPortalSlots(lanes, stats)" in app
    assert "function renderWorldsExpansionPortals(lanes, stats)" in app
    assert "function renderWorldsLaunch()" in app
    assert "function renderWorldsLaunchRoute(lanes)" in app
    assert "function renderWorldsLaunchLane(lane, index)" in app
    assert "renderWorldsLaunch();" in app
    assert "data-worlds-launch-action" in app
    assert "data-worlds-launch-lane" in app
    assert "worlds-expansion-deck" in app
    assert "worlds-expansion-portal" in app
    assert "lane-expansion-portal-deck-20260619.png" in app
    assert "system-lane-expansion-portal-deck" in app
    assert 'event.target.closest("[data-worlds-launch-action]")' in app
    assert 'event.target.closest("[data-worlds-launch-lane]")' in app
    assert 'selectLane(worldsLaunchLane.dataset.worldsLaunchLane, "path")' in app
    assert 'setAtlasDeck("library", { scroll: false })' in app

    assert 'id="worlds-launch"' in index
    assert 'aria-label="Worlds launch surface"' in index
    assert 'data-atlas-deck-section="worlds all"' in index
    assert "worlds-launch" in index
    assert "20260619-lane-expansion-portal-deck" in index
    assert "20260620-worlds-launch-low-scroll-console" in index

    for token in [
        ".worlds-launch-panel",
        ".worlds-launch-shell",
        ".worlds-launch-actions",
        ".worlds-launch-lane-stage",
        ".worlds-launch-route-map",
        ".worlds-launch-route-runner",
        ".worlds-launch-route-node",
        ".worlds-launch-lanes",
        ".worlds-launch-action",
        ".worlds-launch-lane",
        ".worlds-expansion-deck",
        ".worlds-expansion-track",
        ".worlds-expansion-portal",
        ".worlds-expansion-ring",
        ".worlds-expansion-track::-webkit-scrollbar",
        "worldsExpansionSweep",
        "worldsExpansionRing",
        "worldsLaunchRouteRunner",
        "worldsLaunchActiveNode",
        "prefers-reduced-motion",
        "scroll-snap-type",
        "flex-wrap: nowrap;",
        "flex: 0 0 clamp(104px, 30%, 128px);",
        "--launch-progress",
        "--launch-node-position",
        "--portal-charge",
    ]:
        assert token in styles

    assert "Worlds Launch surface" in readme
    assert "compact level-select dock" in readme
    assert "Lane Expansion Portal Deck" in readme
    assert "future minigame sockets" in readme
    assert "Worlds Launch Low-Scroll Console" in readme
    assert "priority lane buttons" in readme
    assert "animated route-map layer" in readme
    assert asset.exists()
    assert asset.stat().st_size > 100_000
