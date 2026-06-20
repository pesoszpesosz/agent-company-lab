from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_mission_scan_contract_is_wired():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "function pathMissionScanStages(lane, trail, nodes, focusedNode)" in app
    assert "function renderPathMissionScan(lane, trail, nodes, focusedNode, mapStats, pathProgress)" in app
    assert "renderPathMissionScan(lane, trail, nodes, focusedNode, mapStats, pathProgress)" in app
    assert "path-mission-scan" in app
    assert "path-mission-stage" in app
    assert "path-mission-runner" in app
    assert "pathEventGlyphType(item)" in app

    assert "20260618-path-mission-scan" in index

    for token in [
        ".path-mission-scan",
        ".path-mission-scan-core",
        ".path-mission-stats",
        ".path-mission-stage",
        ".path-mission-runner",
        ".path-mission-progress",
        "pathMissionSweep",
        "pathMissionRunner",
        "scroll-snap-type",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Mission Scan" in readme
    assert "compact animated Mission Scan" in readme
