from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_kinetic_field_turns_canvas_motion_into_data_reactive_path_ribbons():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-path-stage-kinetic-field" in index

    signal_slice = app[app.index("function motionSignal") : app.index("function kineticFieldRibbons")]
    assert 'state.detailView === "path" ? "path"' in signal_slice
    assert "gateCharge" in signal_slice
    assert "proofCharge" in signal_slice
    assert "testCharge" in signal_slice

    assert "function kineticFieldRibbons(signal)" in app
    ribbon_slice = app[app.index("function kineticFieldRibbons") : app.index("function applyMotionTheme")]
    assert '{ id: "gate", charge: signal.gateCharge' in ribbon_slice
    assert '{ id: "proof", charge: signal.proofCharge' in ribbon_slice
    assert '{ id: "tests", charge: signal.testCharge' in ribbon_slice
    assert '{ id: "unlock", charge: signal.unlockCharge' in ribbon_slice
    assert 'signal.mode === "path" ? 8 : 4' in ribbon_slice

    particle_slice = app[app.index("function runParticles") :]
    assert "const ribbons = kineticFieldRibbons(signal);" in particle_slice
    assert 'if (signal.mode === "path" || signal.mode === "playback")' in particle_slice
    assert "ctx.quadraticCurveTo(controlX, controlY, endX, endY);" in particle_slice
    assert "ctx.fillRect(-packetSize / 2, -packetSize / 2, packetSize, packetSize);" in particle_slice

    marker = "/* 20260620-path-stage-kinetic-field */"
    assert marker in styles
    field_slice = styles[styles.index(marker) :]
    assert 'body[data-motion-mode="path"] #particle-field' in field_slice
    assert 'body[data-motion-mode="path"] {' in field_slice
    assert "--motion-test-charge" in field_slice

    assert "Path Stage Kinetic Field" in readme
