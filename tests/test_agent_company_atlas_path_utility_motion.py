from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_utility_dock_has_data_driven_motion_director():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathUtilityMotionMeta" in app
    assert "--utility-active-index" in app
    assert "--utility-count" in app
    assert "--utility-progress" in app
    assert "path-utility-motion" in app
    assert "path-utility-runner" in app
    assert "path-utility-beacons" in app
    assert "path-utility-beacon" in app
    assert "data-path-utility-motion" in app
    assert "data-path-utility-beacon" in app
    assert app.index("function pathUtilityMotionMeta") < app.index("function renderPathUtilityDock")

    for token in [
        ".path-utility-motion",
        ".path-utility-runner",
        ".path-utility-beacons",
        ".path-utility-beacon",
        ".path-utility-beacon.active",
        "pathUtilitySignalSweep",
        "pathUtilityRunnerPulse",
        "transform: translateX(var(--utility-progress))",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Utility Motion Director" in readme
    assert "20260618-path-utility-motion" in index
