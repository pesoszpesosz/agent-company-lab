from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_desktop_cinematic_route_focus_demotes_duplicate_map_text():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-desktop-cinematic-route-focus */"
    assert marker in styles
    focus_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    base = f"{scoped} .detail-content.detail-view-overview"

    assert "@media (min-width: 761px)" in focus_slice
    assert f"{base} .quest-depth-layer" in focus_slice
    assert f"{base} .quest-node-echo" in focus_slice
    assert "font-size: 0;" in focus_slice
    assert "color: transparent;" in focus_slice
    assert f"{base} .quest-insight-ribbon" in focus_slice
    assert "opacity: 0.2;" in focus_slice
    assert f"{base} .quest-route-capsule-node" in focus_slice
    assert f"{base} .quest-selected-node-lens-depth" in focus_slice
    assert "display: none !important;" in focus_slice
    assert f"{base} .quest-mission-dossier" in focus_slice
    assert f"{base} .quest-path-depth-lens" in focus_slice
    assert f"{base} .quest-selected-node-lens-tray" in focus_slice
    assert "grid-template-columns: minmax(0, 1fr) 72px;" in focus_slice
    assert "Command Cockpit Desktop Cinematic Route Focus" in readme
    assert "20260620-command-cockpit-desktop-cinematic-route-focus" in index
