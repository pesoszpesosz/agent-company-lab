from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_mission_glance_has_compact_game_run_meter():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderPathMissionRunMeter(cards, pathProgress)" in app
    assert "renderPathMissionRunMeter(cards, pathProgress)" in app
    assert "class=\"path-run-meter\"" in app
    assert "class=\"path-run-step" in app
    assert "--path-run-progress:" in app
    assert "--path-run-step-index:" in app

    glance_slice = app[app.index("function renderPathMissionGlance") : app.index("function pathCoreDeckView")]
    assert "path-glance-copy" in glance_slice
    assert "renderPathMissionRunMeter(cards, pathProgress)" in glance_slice

    for token in [
        ".path-run-meter",
        ".path-run-track",
        ".path-run-step",
        ".path-run-step.gated",
        ".path-run-step.unlocked",
        "pathRunStepPulse",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Run Meter" in readme
    assert "20260618-path-run-meter" in index
