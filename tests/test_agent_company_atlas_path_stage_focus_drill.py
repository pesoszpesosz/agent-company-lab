from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_focus_drill_surfaces_related_events_in_focused_lens():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderPathStageFocusLens(lane, focusedNode, pathProgress)" in app
    assert "const events = pathStageNodeEchoEvents(lane, node);" in app
    assert "path-stage-focus-drill" in app
    assert "pathEventGlyphType(item)" in app
    assert "renderPathStageFocusLens(lane, focusedNode, pathProgress)" in app

    marker = "/* 20260620-path-stage-focus-drill */"
    assert marker in styles
    drill_slice = styles[styles.index(marker) :]

    assert ".path-stage-focus-drill" in drill_slice
    assert "--path-focus-drill-tone" in drill_slice
    assert ".path-stage-focus-drill b.gate" in drill_slice
    assert ".path-stage-focus-drill b.proof" in drill_slice
    assert ".path-stage-focus-drill b.task" in drill_slice
    assert "@keyframes pathStageFocusDrillPulse" in drill_slice
    assert "@media (max-width: 560px)" in drill_slice
    assert "@media (prefers-reduced-motion: reduce)" in drill_slice

    assert "Path Stage Focus Drill" in readme
    assert "20260620-path-stage-focus-drill" in index
