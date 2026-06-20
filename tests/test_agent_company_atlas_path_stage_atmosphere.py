from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_atmosphere_texture_powers_the_cockpit_board():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    asset = ROOT / "web" / "assets" / "system" / "path-stage-atmosphere-20260618.png"

    assert asset.exists()
    assert asset.stat().st_size > 100_000

    assert "--path-stage-atmosphere:url('./assets/system/path-stage-atmosphere-20260618.png')" in app
    assert "system-path-stage-atmosphere" in app
    assert "Path Stage Atmosphere" in app
    assert "./assets/system/path-stage-atmosphere-20260618.png" in app

    stage_block = styles[styles.index(".path-map-board.mission-stage {") : styles.index(".path-map-board.mission-stage::after")]
    assert "var(--path-stage-atmosphere" in stage_block
    assert "background-size" in stage_block
    assert "background-position" in stage_block
    assert "background-blend-mode" in stage_block

    assert "Path Stage Atmosphere" in readme
    assert "20260618-path-stage-atmosphere" in index
