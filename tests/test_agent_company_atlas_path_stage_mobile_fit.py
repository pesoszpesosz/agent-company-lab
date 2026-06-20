from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_fit_compresses_route_into_one_board():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-fit */"
    assert marker in styles
    mobile_slice = styles[styles.index(marker) :]

    assert "@media (max-width: 560px)" in mobile_slice
    assert ".path-map-board.mission-stage[data-path-stage-depth-view=\"stage\"]" in mobile_slice
    assert "grid-template-rows: minmax(48px, auto) minmax(250px, 318px) 34px;" in mobile_slice
    assert "min-height: min(548px, calc(100vh - 168px));" in mobile_slice
    assert ".path-stage-ribbon" in mobile_slice
    assert "min-height: clamp(250px, 36vh, 318px);" in mobile_slice
    assert ".path-stage-node" in mobile_slice
    assert "min-height: 132px;" in mobile_slice
    assert "padding: 40px 7px 14px;" in mobile_slice

    assert "Path Stage Mobile Fit" in readme
    assert "20260620-path-stage-mobile-fit" in index.split('href="./styles.css?v=', 1)[1]
