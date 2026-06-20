from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_signal_weather_adds_meaningful_cockpit_motion():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathStageWeatherSignals(lane, trail, nodes, pathNotes)" in app
    assert "function renderPathStageSignalWeather(lane, trail, nodes, pathNotes)" in app
    assert "pathStageWeatherSignals(lane, trail, nodes, pathNotes)" in app
    assert "${renderPathStageSignalWeather(lane, trail, nodes, pathNotes)}" in app
    assert 'class="path-stage-weather"' in app
    assert 'class="path-stage-signal' in app

    assert ".path-stage-weather" in styles
    assert ".path-stage-signal" in styles
    assert ".path-stage-signal.gate" in styles
    assert ".path-stage-signal.proof" in styles
    assert ".path-stage-signal.work" in styles
    assert ".path-stage-signal.note" in styles
    assert "@keyframes pathStageSignalDrift" in styles
    assert "prefers-reduced-motion: reduce" in styles
    assert ".path-stage-signal" in styles[styles.rindex("@media (prefers-reduced-motion: reduce)") :]

    assert "Path Stage Signal Weather" in readme
    assert "20260618-path-stage-signal-weather" in index
