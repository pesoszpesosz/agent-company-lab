from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_board_clarity_removes_duplicate_text_slab():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-board-clarity */"
    assert marker in styles
    clarity_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    base = f"{scoped} .detail-content.detail-view-overview"

    assert "@media (max-width: 560px)" in clarity_slice
    assert f"{base} .quest-field[data-quest-motion-quality=\"premium\"] .quest-mission-readout" in clarity_slice
    assert "display: none !important;" in clarity_slice
    assert f"{base} .quest-board-signal-overlay" in clarity_slice
    assert "grid-template-columns: repeat(4, 8px);" in clarity_slice
    assert "max-width: 46px;" in clarity_slice
    assert "background: transparent;" in clarity_slice
    assert f"{base} .quest-board-signal-chip" in clarity_slice
    assert "width: 8px;" in clarity_slice
    assert "height: 8px;" in clarity_slice
    assert f"{base} .quest-board-signal-chip i" in clarity_slice
    assert "font-size: 0;" in clarity_slice
    assert f"{base} .quest-board-signal-chip strong" in clarity_slice
    assert f"{base} .quest-board-signal-chip em" in clarity_slice
    assert "Command Cockpit Mobile Board Clarity" in readme
    assert "20260620-command-cockpit-mobile-board-clarity" in index
