from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_run_pulse_makes_route_progress_feel_alive_without_extra_dom():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "--path-stage-progress:${pathProgress}%" in app
    assert "path-stage-motion-runner" in app

    marker = "/* 20260620-path-stage-run-pulse */"
    assert marker in styles
    pulse_slice = styles[styles.index(marker) :]

    assert ".path-stage-motion::after" in pulse_slice
    assert ".path-stage-motion-runner::after" in pulse_slice
    assert "left: clamp(26px, var(--path-stage-progress, 0%), calc(100% - 32px));" in pulse_slice
    assert "pathStageRunPulse" in pulse_slice
    assert "pathStageRunnerBeacon" in pulse_slice
    assert "pointer-events: none;" in pulse_slice
    assert "@media (prefers-reduced-motion: reduce)" in pulse_slice

    assert "Path Stage Run Pulse" in readme
    assert "20260620-path-stage-run-pulse" in index
