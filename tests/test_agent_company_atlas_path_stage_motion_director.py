from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_ribbon_has_premium_motion_director():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    stage_slice = app[app.index("function renderPathStageRibbon") : app.index("function pathCoreDeckModules")]
    assert "path-stage-motion" in stage_slice
    assert "path-stage-motion-scan" in stage_slice
    assert "path-stage-motion-runner" in stage_slice
    assert "path-stage-node-spark" in stage_slice
    assert "data-stage-kind" in stage_slice
    assert "data-stage-status" in stage_slice
    assert "--path-stage-progress:" in stage_slice
    assert "--path-stage-active:" in stage_slice

    for token in [
        ".path-stage-motion",
        ".path-stage-motion-scan",
        ".path-stage-motion-runner",
        ".path-stage-node-spark",
        ".path-stage-node.gated .path-stage-node-spark",
        ".path-stage-node.unlocked .path-stage-node-spark",
        ".path-stage-node.is-focused .path-stage-node-spark",
        "pathStageScanDrift",
        "pathStageRunnerTrace",
        "pathStageSparkWake",
        "pathStageUnlockBloom",
    ]:
        assert token in styles

    motion_block = styles[styles.index(".path-stage-motion {") : styles.index(".path-stage-motion-scan")]
    assert "pointer-events: none;" in motion_block
    assert "overflow: hidden;" in motion_block

    reduced_motion = styles[styles.index("@media (prefers-reduced-motion: reduce)") :]
    assert ".path-stage-motion-scan" in reduced_motion
    assert ".path-stage-motion-runner" in reduced_motion
    assert ".path-stage-node-spark" in reduced_motion

    assert "Path Stage Motion Director" in readme
    assert "20260618-path-stage-motion-director" in index
