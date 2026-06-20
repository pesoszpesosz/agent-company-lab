from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_mission_glance_surfaces_compact_crew_presence():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathMissionCrewTokens(lane)" in app
    assert "function renderPathMissionCrewPresence(lane)" in app
    assert "pathMissionCrewTokens(lane)" in app
    assert "renderPathMissionCrewPresence(lane)" in app
    assert "class=\"path-crew-presence\"" in app
    assert "class=\"path-crew-token" in app
    assert "agentRosterAvatar(record.agent)" in app
    assert "crewReadiness(record)" in app

    glance_slice = app[app.index("function renderPathMissionGlance") : app.index("function pathCoreDeckView")]
    assert "renderPathMissionCrewPresence(lane)" in glance_slice
    assert "renderPathMissionRunMeter(cards, pathProgress)" in glance_slice

    for token in [
        ".path-crew-presence",
        ".path-crew-token",
        ".path-crew-token.gated",
        ".path-crew-token.ready",
        ".path-crew-token.staged",
        "pathCrewTokenPulse",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Crew Presence" in readme
    assert "20260618-path-crew-presence" in index
