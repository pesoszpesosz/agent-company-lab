from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_encounter_tether_connects_focused_node_to_board_lens():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "const visibleStageNodes = nodes.slice(0, 8);" in app
    assert "const pathStageFocusX" in app
    assert "--path-stage-focus-x:${pathStageFocusX}%" in app
    assert "class=\"path-stage-encounter-tether ${escapeHtml(focusedNode?.kind ?? \"future\")} ${escapeHtml(focusedNode?.status ?? \"future\")}\"" in app
    map_view_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert "${renderPathStageEncounterTether(focusedNode)}" in map_view_slice
    assert map_view_slice.index("${renderPathStageEncounterTether(focusedNode)}") < map_view_slice.index("${renderPathStageFocusLens(lane, focusedNode, pathProgress)}")

    marker = "/* 20260620-path-stage-encounter-tether */"
    assert marker in styles
    tether_slice = styles[styles.index(marker) :]

    assert ".path-stage-encounter-tether" in tether_slice
    assert ".path-stage-encounter-tether::before" in tether_slice
    assert ".path-stage-encounter-tether::after" in tether_slice
    assert ".path-stage-encounter-tether.gated" in tether_slice
    assert "var(--path-stage-focus-x" in tether_slice
    assert "pathStageEncounterTether" in tether_slice
    assert "pathStageEncounterAnchor" in tether_slice
    assert "pointer-events: none;" in tether_slice
    assert "@media (max-width: 560px)" in tether_slice
    assert "@media (prefers-reduced-motion: reduce)" in tether_slice

    assert "Path Stage Encounter Tether" in readme
    assert "20260620-path-stage-encounter-tether" in index
