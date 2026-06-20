from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_route_first_hud_promotes_playfield_above_glance():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-route-first-hud */"
    assert marker in styles
    route_slice = styles[styles.index(marker) :]

    assert "@media (max-width: 560px)" in route_slice
    assert "grid-template-areas:" in route_slice
    assert '"route"' in route_slice
    assert '"scanner"' in route_slice
    assert ".path-mission-glance" in route_slice
    assert "position: absolute;" in route_slice
    assert "max-height: 54px;" in route_slice
    assert "top: -30px;" in route_slice
    assert "pointer-events: none;" in route_slice
    assert ".path-glance-command-console" in route_slice
    assert ".path-stage-ribbon" in route_slice
    assert "grid-row: 1;" in route_slice
    assert "min-height: clamp(322px, 39svh, 378px);" in route_slice
    assert "padding-top: 66px;" in route_slice
    assert ".path-stage-focus-lens" in route_slice
    assert "top: 88px;" in route_slice

    assert "Path Stage Mobile Route First HUD" in readme
    assert "20260620-path-stage-mobile-route-first-hud" in index
