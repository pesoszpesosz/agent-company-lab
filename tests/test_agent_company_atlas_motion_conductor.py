from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "web" / "app.js"
CSS = ROOT / "web" / "styles.css"
INDEX = ROOT / "web" / "index.html"
README = ROOT / "web" / "README.md"


def test_atlas_motion_conductor_uses_existing_motion_signal_inside_ribbon():
    app = APP.read_text(encoding="utf-8")

    assert "function atlasMotionConductorModel(signal = motionSignal())" in app
    assert "const charges = [" in app
    assert 'id: "gate"' in app
    assert 'id: "proof"' in app
    assert 'id: "tests"' in app
    assert 'id: "unlock"' in app
    assert "signal.gateCharge" in app
    assert "signal.proofCharge" in app
    assert "signal.testCharge" in app
    assert "signal.unlockCharge" in app
    assert "function renderAtlasMotionConductor(model)" in app
    assert 'class="atlas-motion-conductor ${escapeHtml(model.mode)}"' in app
    assert 'data-atlas-motion-mode="${escapeHtml(model.mode)}"' in app
    assert 'data-atlas-motion-charge="${escapeHtml(charge.id)}"' in app
    assert "const conductor = atlasMotionConductorModel();" in app
    assert "${renderAtlasMotionConductor(conductor)}" in app

    ribbon_slice = app[app.index("function renderAtlasCommandRibbon()") : app.index("function activateAtlasCommandRibbon")]
    assert ribbon_slice.index("const conductor = atlasMotionConductorModel();") < ribbon_slice.index("el.atlasCommandRibbon.innerHTML")
    assert ribbon_slice.index("${renderAtlasMotionConductor(conductor)}") < ribbon_slice.index("${model.cells")


def test_atlas_motion_conductor_styles_are_premium_and_not_noisy():
    styles = CSS.read_text(encoding="utf-8")

    marker = "/* 20260620-atlas-motion-conductor */"
    assert marker in styles
    block = styles[styles.index(marker) :]
    assert ".atlas-motion-conductor" in block
    assert "grid-template-columns: 34px minmax(0, 1fr);" in block
    assert "min-height: 48px;" in block
    assert "animation: atlasMotionConductorSweep 10.8s ease-in-out infinite;" in block
    assert "@keyframes atlasMotionConductorSweep" in block
    assert ".atlas-motion-charge" in block
    assert "background: linear-gradient(90deg, var(--motion-a, var(--teal)), var(--motion-b, var(--amber))) 0 / var(--charge) 100% no-repeat" in block
    assert ".atlas-command-ribbon" in block
    assert "grid-template-columns: minmax(142px, 0.58fr) minmax(150px, 0.62fr) repeat(6, minmax(0, 1fr));" in block
    assert "@media (max-width: 760px)" in block
    assert "grid-auto-columns: minmax(132px, 166px);" in block
    assert ".atlas-motion-conductor::before," in block
    assert ".path-stage-signal" in block[block.rindex("@media (prefers-reduced-motion: reduce)") :]


def test_atlas_motion_conductor_documented_and_cache_busted():
    readme = README.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    assert "Atlas Motion Conductor" in readme
    assert "motion mode, lane focus, gate, proof, test, and unlock charge" in readme
    assert "20260620-atlas-motion-conductor" in index
    assert "20260620-atlas-command-ribbon-20260620-atlas-motion-conductor" in index