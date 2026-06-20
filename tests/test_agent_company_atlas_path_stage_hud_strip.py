from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_hud_texture_is_integrated_as_system_asset():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    asset = ROOT / "web" / "assets" / "system" / "path-stage-hud-strip-20260618.png"

    assert asset.exists()
    assert asset.stat().st_size > 100_000

    assert "--path-stage-art:url('./assets/system/path-stage-hud-strip-20260618.png')" in app
    assert "system-path-stage-hud-strip" in app
    assert "Path Stage HUD Strip" in app
    assert "./assets/system/path-stage-hud-strip-20260618.png" in app

    stage_block = styles[styles.index(".path-stage-ribbon {") : styles.index(".path-stage-ribbon::before")]
    assert "var(--path-stage-art" in stage_block
    assert "background-size" in stage_block
    assert "background-position" in stage_block

    motion_block = styles[styles.index(".path-stage-motion {") : styles.index(".path-stage-motion-scan")]
    assert "var(--path-stage-art" in motion_block

    assert "Path Stage HUD Strip" in readme
    assert "20260618-path-stage-hud-strip" in index
