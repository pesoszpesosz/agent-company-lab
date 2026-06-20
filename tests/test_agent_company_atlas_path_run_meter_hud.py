from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_run_meter_hud_texture_is_integrated_as_system_asset():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    asset = ROOT / "web" / "assets" / "system" / "path-run-meter-hud-20260618.png"

    assert asset.exists()
    assert asset.stat().st_size > 80_000

    assert "--path-run-art:url('./assets/system/path-run-meter-hud-20260618.png')" in app
    assert "system-path-run-meter-hud" in app
    assert "Path Run Meter HUD" in app
    assert "./assets/system/path-run-meter-hud-20260618.png" in app

    run_meter_block = styles[styles.index(".path-run-meter {") : styles.index(".path-run-track")]
    assert "var(--path-run-art" in run_meter_block
    assert "background-size" in run_meter_block
    assert "background-position" in run_meter_block

    assert "Path Run Meter HUD" in readme
    assert "20260618-path-run-meter-hud" in index
