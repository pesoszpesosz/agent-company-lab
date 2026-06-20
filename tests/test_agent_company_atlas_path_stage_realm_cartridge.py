from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_realm_cartridge_exposes_lane_minigame_identity_without_scroll():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathStageRealmCartridgeModel(lane, pathProgress, gateCount)" in app
    assert "function renderPathStageRealmCartridge(lane, pathProgress, gateCount)" in app
    assert "path-stage-realm-cartridge" in app
    assert "path-stage-realm-thumb" in app
    assert "data-detail-view=\"game\"" in app
    assert "--path-realm-art:url" in app
    assert "renderPathStageRealmCartridge(lane, pathProgress, gateCount)" in app

    board_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert board_slice.index("renderPathMissionGlance") < board_slice.index("renderPathStageRealmCartridge")
    assert board_slice.index("renderPathStageRealmCartridge") < board_slice.index("renderPathStageEncounterTether")

    marker = "/* 20260620-path-stage-realm-cartridge */"
    assert marker in styles
    realm_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    cartridge = f"{scoped} .path-stage-realm-cartridge"

    assert cartridge in realm_slice
    assert f"{cartridge}::before" in realm_slice
    assert f"{cartridge} .path-stage-realm-thumb" in realm_slice
    assert "position: absolute;" in realm_slice
    assert "pointer-events: auto;" in realm_slice
    assert "background: var(--path-realm-art" in realm_slice
    assert "animation: pathStageRealmCartridgePulse" in realm_slice
    assert "@keyframes pathStageRealmCartridgePulse" in realm_slice
    assert "@media (max-width: 560px)" in realm_slice
    assert "display: none;" in realm_slice
    assert "@media (prefers-reduced-motion: reduce)" in realm_slice

    assert "Path Stage Realm Cartridge" in readme
    assert "20260620-path-stage-realm-cartridge" in index