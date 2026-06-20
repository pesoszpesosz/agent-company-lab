from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_ribbon_surfaces_focused_level_lens():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderPathStageFocusLens(" in app
    assert "class=\"path-stage-focus-lens" in app
    assert "class=\"path-stage-focus-beam\"" in app
    assert "Focused path level" in app
    assert "renderPathStageFocusLens(lane, focusedNode, pathProgress)" in app

    ribbon_slice = app[app.index("function renderPathStageRibbon") : app.index("function pathCoreDeckModules")]
    assert "${renderPathStageFocusLens(lane, focusedNode, pathProgress)}" in ribbon_slice
    assert "--path-focus-progress:${pathProgress}%" in app

    for token in [
        ".path-stage-focus-lens",
        ".path-stage-focus-lens.gate",
        ".path-stage-focus-lens.unlock",
        ".path-stage-focus-beam",
        "pathStageFocusBeam",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Stage Focus Lens" in readme
    assert "20260618-path-stage-focus-lens" in index
