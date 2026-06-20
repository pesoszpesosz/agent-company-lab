from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_gate_stack_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/path-chapter-gate-heatfield-20260618.png"

    assert "function pathChapterGateStackItems" in app
    assert "function pathChapterGateHeatfieldItems" in app
    assert "function renderPathChapterGateHeatfield" in app
    assert "function renderPathChapterGateStack" in app
    assert "path-chapter-gate-stack" in app
    assert "path-chapter-gate-heatfield" in app
    assert "path-chapter-gate-ping" in app
    assert "path-chapter-gate-sweep" in app
    assert "path-chapter-gate-heatfield-20260618.png" in app
    assert "path-chapter-gate-card" in app
    assert "path-chapter-gate-actions" in app
    assert "renderPathChapterGateHeatfield(lane, chapter, items, peakPressure)" in app
    assert "renderPathChapterGateStack(lane, chapter)" in app
    assert "gateRadarItems(lane)" in app
    assert "gateRadarNoteForItem(lane, item)" in app
    assert "data-stage-lane-command" in app
    assert 'data-detail-view="comms"' in app
    assert "system-path-chapter-gate-heatfield" in app

    assert ".path-chapter-gate-stack" in styles
    assert ".path-chapter-gate-heatfield" in styles
    assert ".path-chapter-gate-ping" in styles
    assert ".path-chapter-gate-sweep" in styles
    assert "@keyframes gateHeatfieldSweep" in styles
    assert ".path-chapter-gate-card" in styles
    assert ".path-chapter-gate-actions" in styles

    assert "path-chapter-gate-heatfield" in index
    assert "Chapter Gate Stack" in readme
    assert "Chapter Gate Heatfield" in readme
    assert "path-chapter-gate-heatfield-20260618.png" in readme
    assert asset.exists()
    assert asset.stat().st_size > 500_000
