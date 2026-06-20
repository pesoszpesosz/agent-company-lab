from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_route_spine_contract_is_wired():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "path-route-spine" in app
    assert "path-route-runner" in app
    assert "--path-route-count" in app
    assert "--path-route-active" in app
    assert "--path-node-charge" in app
    assert "focusPathBoardFromRoute(route)" in app
    assert 'document.querySelector(".path-map-board")?.scrollIntoView' in app
    assert "function renderPathRouteRail(lane, nodes, focusedNode)" in app
    assert "content: () => renderPathRouteRail(lane, nodes, focusedNode)" in app
    assert app.index("function renderPathRouteRail") < app.index("function renderPathCoreDeck")

    assert "20260618-path-route-spine" in index

    for token in [
        ".path-route-spine",
        ".path-route-runner",
        ".path-node::before",
        ".path-node.is-focused::before",
        "grid-auto-flow: column",
        "scroll-snap-type: x proximity",
        "grid-auto-columns: minmax(210px, 84vw)",
        "pathRouteRunner",
        "pathRouteNodePulse",
        "prefers-reduced-motion",
    ]:
        assert token in styles

    assert "route spine" in readme
