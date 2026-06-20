from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_playfield_texture_is_generated_and_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")
    asset = ROOT / "web" / "assets" / "system" / "path-stage-playfield-rail-20260620.png"

    assert asset.exists()
    assert asset.stat().st_size > 1_000_000

    assert "--path-playfield-art:url('./assets/system/path-stage-playfield-rail-20260620.png')" in app
    assert "system-path-stage-playfield-rail" in app
    assert "Path Stage Playfield Rail" in app
    assert "./assets/system/path-stage-playfield-rail-20260620.png" in app

    marker = "/* 20260620-path-stage-playfield-texture */"
    assert marker in styles
    texture_slice = styles[styles.index(marker) :]
    assert "var(--path-playfield-art, none) center / cover no-repeat" in texture_slice
    assert "background-blend-mode: normal, screen, screen, normal, normal;" in texture_slice
    assert ".path-stage-ribbon::after" in texture_slice
    assert "mix-blend-mode: screen;" in texture_slice
    assert ".path-stage-node" in texture_slice
    assert "backdrop-filter: blur(8px) saturate(1.16);" in texture_slice
    assert "text-shadow: 0 1px 10px rgba(0, 0, 0, 0.82);" in texture_slice

    assert "Path Stage Playfield Texture" in readme
    assert "path-stage-playfield-rail-20260620.png" in readme
    assert "20260620-path-stage-playfield-texture" in index
