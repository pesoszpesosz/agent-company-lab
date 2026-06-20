from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_gate_encounter_turns_focused_blocker_into_boss_gate():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "class=\"path-stage-focus-lens ${escapeHtml(node.kind)} ${escapeHtml(node.status)}\"" in app
    assert "class=\"path-stage-node ${escapeHtml(node.kind)} ${escapeHtml(node.status)} ${active ? \"is-focused\" : \"\"}\"" in app
    map_view_slice = app[app.index("function renderPathMapView") : app.index("function pathUtilityDockView")]
    assert "${renderPathStageFocusLens(lane, focusedNode, pathProgress)}" in map_view_slice
    assert map_view_slice.index("${renderPathStageFocusLens(lane, focusedNode, pathProgress)}") < map_view_slice.index("${renderPathStageRibbon(lane, nodes, focusedNode, pathProgress)}")

    marker = "/* 20260620-path-stage-gate-encounter */"
    assert marker in styles
    encounter_slice = styles[styles.index(marker) :]

    assert ".path-stage-focus-lens.gate" in encounter_slice
    assert ".path-stage-focus-lens.gated" in encounter_slice
    assert "> .path-stage-focus-lens" in encounter_slice
    assert ".path-stage-ribbon > .path-stage-focus-lens" in encounter_slice
    assert ".path-stage-focus-lens.gated::before" in encounter_slice
    assert ".path-stage-focus-lens.gate::after" in encounter_slice
    assert ".path-stage-node.gated.is-focused" in encounter_slice
    assert ".path-stage-node.gate.is-focused" in encounter_slice
    assert "pathStageGateEncounter" in encounter_slice
    assert "pathStageGateLockLine" in encounter_slice
    assert "pointer-events: none;" in encounter_slice
    assert "@media (max-width: 560px)" in encounter_slice
    assert "@media (prefers-reduced-motion: reduce)" in encounter_slice

    assert "Path Stage Gate Encounter" in readme
    assert "20260620-path-stage-gate-encounter" in index
