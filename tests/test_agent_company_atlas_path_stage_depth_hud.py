from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_depth_hud_stops_covering_mobile_route_cards():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-depth-hud */"
    assert marker in styles
    hud_slice = styles[styles.index(marker) :]

    assert "@media (max-width: 560px)" in hud_slice
    assert ".path-stage-depth-dock" in hud_slice
    assert "position: relative;" in hud_slice
    assert "grid-row: 3;" in hud_slice
    assert "right: auto;" in hud_slice
    assert "bottom: auto;" in hud_slice
    assert "left: auto;" in hud_slice
    assert "min-height: 34px;" in hud_slice
    assert "transform: none;" in hud_slice

    assert ".path-stage-depth-card" in hud_slice
    assert "min-height: 28px;" in hud_slice
    assert ".path-stage-depth-card strong" in hud_slice
    assert "font-size: 0.7rem;" in hud_slice

    assert "Path Stage Depth HUD" in readme
    assert "20260620-path-stage-depth-hud" in index.split('href="./styles.css?v=', 1)[1]
