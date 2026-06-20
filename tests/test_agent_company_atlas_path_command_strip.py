from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_command_strip_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function renderPathCommandStrip" in app
    assert "function pathCommandStripCells" in app
    assert "path-command-strip" in app
    assert "data-path-command-jump" in app
    assert "pathCommandJumpButton" in app
    assert 'route: ".path-route"' in app
    assert 'proof: ".path-proof-cache"' in app
    assert 'archive: ".path-chapter-archive"' in app
    assert app.index("function pathCoreDeckModules") < app.index("function renderPathCoreDeck")
    assert "content: () => renderPathCommandStrip(lane, trail, focusedNode, pathNotes)" in app
    assert "state.pathCoreDeckViewByLane" in app

    for token in [
        ".path-command-strip",
        ".path-command-cells",
        ".path-command-cell",
        ".path-command-actions",
        "pathCommandSweep",
        "scroll-snap-type: x proximity",
        ".path-command-strip::before",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "Path Command Strip" in readme
    assert "20260618-path-command-strip" in index


def test_path_command_strip_mobile_contract_stays_compact():
    styles = read("web/styles.css")

    for token in [
        ".path-command-strip-head h3",
        "-webkit-line-clamp: 1",
        "flex: 0 0 126px",
        "min-height: 50px",
        ".path-command-cell small",
        "display: none",
        "flex-wrap: nowrap",
        "flex: 0 0 58px",
        "width: 58px",
        "height: 30px",
        "min-height: 30px",
        "min-height: 36px",
        "min-height: 54px",
    ]:
        assert token in styles
