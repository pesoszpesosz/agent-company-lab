from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_title_channel_reserves_nav_hud_space():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-title-channel */"
    assert marker in styles
    channel_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    board = f'{scoped} .path-map-board.mission-stage[data-path-stage-depth-view="stage"]'
    assert "@media (max-width: 560px)" in channel_slice
    assert f"{board} .path-mission-glance" in channel_slice
    assert "padding-right: 174px;" in channel_slice
    assert f"{board} .path-glance-main" in channel_slice
    assert "grid-template-columns: 34px minmax(0, 1fr);" in channel_slice
    assert f"{board} .path-glance-main h3" in channel_slice
    assert "max-width: 100%;" in channel_slice
    assert "white-space: nowrap;" in channel_slice
    assert "text-overflow: ellipsis;" in channel_slice
    assert f"{board} .path-glance-main .path-map-gauge" in channel_slice
    assert "display: none;" in channel_slice
    assert f"{board} .path-stage-nav-dock" in channel_slice
    assert "z-index: 8;" in channel_slice

    assert "Path Stage Mobile Title Channel" in readme
    assert "20260620-path-stage-mobile-title-channel" in index
