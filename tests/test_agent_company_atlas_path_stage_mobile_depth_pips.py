from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_depth_pips_turn_depth_tabs_into_game_controls():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-depth-pips */"
    assert marker in styles
    pip_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    dock = f'{scoped} .path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-dock'
    card = f'{dock} .path-stage-depth-card'
    assert "@media (max-width: 560px)" in pip_slice
    assert dock in pip_slice
    assert "min-height: 30px;" in pip_slice
    assert "max-height: 34px;" in pip_slice
    assert "border-radius: 999px;" in pip_slice
    assert f"{dock}::after" in pip_slice
    assert f"{dock} .path-stage-depth-cards" in pip_slice
    assert "grid-template-columns: repeat(3, minmax(0, 1fr));" in pip_slice
    assert card in pip_slice
    assert "grid-template-columns: 18px minmax(0, 1fr);" in pip_slice
    assert f"{card} span" in pip_slice
    assert "font-size: 0.46rem;" in pip_slice
    assert f"{card} strong" in pip_slice
    assert "order: -1;" in pip_slice
    assert "width: 18px;" in pip_slice
    assert f"{card} em" in pip_slice
    assert "clip: rect(0 0 0 0);" in pip_slice
    assert ".path-stage-depth-card.active strong" in pip_slice
    assert "@media (prefers-reduced-motion: reduce)" in pip_slice

    assert "Path Stage Mobile Depth Pips" in readme
    assert "20260620-path-stage-mobile-depth-pips" in index
