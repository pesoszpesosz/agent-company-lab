from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_core_motion_rail_tracks_active_core_module():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathCoreMotionMeta(modules, activeModule)" in app
    assert "--path-core-index:" in app
    assert "--path-core-progress:" in app
    assert "class=\"path-core-motion-rail\"" in app
    assert "class=\"path-core-motion-runner\"" in app
    assert "class=\"path-core-motion-sweep\"" in app
    assert "class=\"path-core-beacon" in app
    assert "data-path-core-beacon" in app

    core_slice = app[app.index("function renderPathCoreDeck") : app.index("function renderPathMapView")]
    assert "pathCoreMotionMeta(modules, activeModule)" in core_slice
    assert "motion.beacons" in core_slice
    assert "module.id === activeModule.id ? \"active\"" in core_slice

    for token in [
        ".path-core-motion-rail",
        ".path-core-motion-track",
        ".path-core-motion-runner",
        ".path-core-motion-sweep",
        ".path-core-beacon",
        "pathCoreSignalSweep",
        "pathCoreRunnerDrift",
        "transform: translateX",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Core Motion Rail" in readme
    assert "20260618-path-core-motion" in index
