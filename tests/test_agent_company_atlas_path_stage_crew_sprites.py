from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_crew_sprites_put_bot_avatars_on_the_route_playfield():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderPathStageCrewSprites(lane, pathProgress)" in app
    assert "pathMissionCrewTokens(lane)" in app
    assert "agentRosterAvatar(record.agent)" in app
    assert "crewReadiness(record)" in app
    assert "crewMode(record)" in app
    assert "path-stage-crew-sprites" in app
    assert "path-stage-crew-sprite" in app

    ribbon_slice = app[app.index("function renderPathStageRibbon") : app.index("function pathCoreDeckModules")]
    assert "renderPathStageCrewSprites(lane, pathProgress)" in ribbon_slice

    marker = "/* 20260620-path-stage-crew-sprites */"
    assert marker in styles
    sprite_slice = styles[styles.index(marker) :]
    assert ".path-stage-crew-sprites" in sprite_slice
    assert ".path-stage-crew-sprite" in sprite_slice
    assert ".path-stage-crew-sprite .operator-avatar" in sprite_slice
    assert "@keyframes pathStageCrewSpriteDrift" in sprite_slice
    assert "@media (max-width: 560px)" in sprite_slice
    assert "pointer-events: none;" in sprite_slice

    assert "Path Stage Crew Sprites" in readme
    assert "20260620-path-stage-crew-sprites" in index
