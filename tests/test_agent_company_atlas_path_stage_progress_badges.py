from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_progress_badges_surface_gate_proof_and_unlock_state():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function pathStageNodeBadgeModel(node)" in app
    assert "function renderPathStageNodeBadges(node)" in app
    assert "path-stage-node-badges" in app
    assert "path-stage-node-badge" in app
    assert "renderPathStageNodeBadges(node)" in app
    assert "renderPathStageNodeBadges({ kind: \"future\", status: \"future\" })" in app

    marker = "/* 20260620-path-stage-progress-badges */"
    assert marker in styles
    badge_slice = styles[styles.index(marker) :]
    assert ".path-stage-node-badges" in badge_slice
    assert ".path-stage-node-badge" in badge_slice
    assert ".path-stage-node-badge.gate" in badge_slice
    assert ".path-stage-node-badge.unlock" in badge_slice
    assert ".path-stage-node-badge.future" in badge_slice
    assert "@keyframes pathStageBadgePulse" in badge_slice
    assert "@media (max-width: 560px)" in badge_slice
    assert "@media (prefers-reduced-motion: reduce)" in styles
    assert ".path-stage-node-badge" in styles[styles.index("@media (prefers-reduced-motion: reduce)") :]

    assert "Path Stage Progress Badges" in readme
    assert "20260620-path-stage-progress-badges" in index
