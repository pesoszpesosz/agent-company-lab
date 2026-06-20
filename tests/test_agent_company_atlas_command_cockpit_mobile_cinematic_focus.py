from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_cinematic_focus_removes_text_ghosts_from_playfield():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-cinematic-focus */"
    assert marker in styles
    focus_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    base = f"{scoped} .detail-content.detail-view-overview"

    assert "@media (max-width: 560px)" in focus_slice
    assert f"{base} .quest-depth-stack" in focus_slice
    assert "display: none !important;" in focus_slice
    assert f"{base} .quest-event-lens" in focus_slice
    assert "font-size: 0;" in focus_slice
    assert "width: 18px;" in focus_slice
    assert f"{base} .quest-insight-ribbon" in focus_slice
    assert "opacity: 0.18;" in focus_slice
    assert f"{base} .quest-route-capsule-node" in focus_slice
    assert "color: transparent;" in focus_slice
    assert f"{base} .quest-field-runner" in focus_slice
    assert "questMobileCinematicRunner" in focus_slice
    assert "Command Cockpit Mobile Cinematic Focus" in readme
    assert "20260620-command-cockpit-mobile-cinematic-focus" in index
