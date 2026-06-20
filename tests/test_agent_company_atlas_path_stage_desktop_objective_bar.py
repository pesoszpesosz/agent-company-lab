from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_desktop_objective_bar_removes_report_slab_from_clicked_path():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-desktop-objective-bar */"
    assert marker in styles
    objective_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    board = f'{scoped} .path-map-board.mission-stage[data-path-stage-depth-view="stage"]'

    assert "@media (min-width: 1121px)" in objective_slice
    assert f"{board} .path-mission-glance" in objective_slice
    assert "min-height: 60px;" in objective_slice
    assert "max-height: 72px;" in objective_slice
    assert f"{board} .path-glance-main" in objective_slice
    assert "grid-template-columns: 46px minmax(0, 1fr) 52px;" in objective_slice
    assert f"{board} .path-glance-main p" in objective_slice
    assert f"{board} .path-glance-cards" in objective_slice
    assert f"{board} .path-glance-actions" in objective_slice
    assert "display: none !important;" in objective_slice
    assert "Path Stage Desktop Objective Bar" in readme
    assert "20260620-path-stage-desktop-objective-bar" in index