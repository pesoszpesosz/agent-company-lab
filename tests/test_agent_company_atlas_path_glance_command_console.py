from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_glance_becomes_low_scroll_command_console():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-path-glance-command-console" in index
    assert "20260620-path-glance-command-console" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-path-glance-command-console" in index.split('<script src="./app.js?v=', 1)[1]

    glance_slice = app[app.index("function renderPathMissionGlance") : app.index("function pathCoreDeckView")]
    assert 'class="path-glance-command-console"' in glance_slice
    assert 'class="path-glance-cards"' in glance_slice
    assert 'class="path-glance-actions"' in glance_slice

    marker = "/* 20260620-path-glance-command-console */"
    assert marker in styles
    console_slice = styles[styles.index(marker):]
    assert ".path-map-board.mission-stage .path-glance-command-console" in console_slice
    assert ".path-map-board.mission-stage .path-glance-cards" in console_slice
    assert ".path-map-board.mission-stage .path-glance-actions" in console_slice
    assert "grid-template-columns: minmax(0, 1fr);" in console_slice
    assert "overflow-x: auto;" in console_slice
    assert "scroll-snap-type: x proximity;" in console_slice
    assert ".path-map-board.mission-stage .path-crew-presence" in console_slice
    assert "display: none;" in console_slice
    assert '.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-core-deck' in console_slice
    assert "align-self: start;" in console_slice
    assert "padding-bottom: 7px;" in console_slice
    assert '.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-core-panel' in console_slice
    assert ".path-map-board.mission-stage[data-path-stage-depth-view=\"stage\"] .path-core-motion-rail" in console_slice
    assert "Path Glance Command Console" in readme
