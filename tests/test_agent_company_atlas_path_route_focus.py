from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_route_focus_preserves_visible_cockpit_instead_of_yanking_to_top():
    app = read("web/app.js")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function focusPathBoardFromRoute(route = readRoute(), behavior = \"auto\")" in app

    focus_slice = app[app.index("function focusPathBoardFromRoute") : app.index("async function loadSnapshot")]
    assert 'document.querySelector(".path-map-board")?.scrollIntoView' in focus_slice
    assert 'block: "nearest"' in focus_slice
    assert 'block: "start"' not in focus_slice

    assert "Path Route Focus" in readme
    assert "20260618-path-route-focus" in index
