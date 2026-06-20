from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_playfield_rail_stops_route_nodes_from_stretching():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-playfield-rail */"
    assert marker in styles
    playfield_slice = styles[styles.index(marker) :]

    assert ".path-stage-ribbon" in playfield_slice
    assert "align-items: center;" in playfield_slice
    assert "grid-auto-columns: minmax(132px, 0.86fr);" in playfield_slice
    assert "overflow-x: auto;" in playfield_slice
    assert ".path-stage-node" in playfield_slice
    assert "height: clamp(116px, 58%, 152px);" in playfield_slice
    assert "min-height: 116px;" in playfield_slice
    assert "align-self: center;" in playfield_slice
    assert ".path-stage-node:nth-of-type(2n)" in playfield_slice
    assert "translateY(18px)" in playfield_slice
    assert ".path-stage-focus-lens" in playfield_slice
    assert "top: 12px;" in playfield_slice
    assert "bottom: auto;" in playfield_slice
    assert "@media (max-width: 560px)" in playfield_slice
    assert "height: clamp(104px, 44%, 126px);" in playfield_slice

    assert "Path Stage Playfield Rail" in readme
    assert "20260620-path-stage-playfield-rail" in index.split('href="./styles.css?v=', 1)[1]
