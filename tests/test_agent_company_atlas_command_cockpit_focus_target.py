from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_focus_target_makes_selected_node_playable():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-focus-target */"
    assert marker in styles
    focus_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    board = f'{scoped} .detail-content.detail-view-overview .quest-field[data-quest-board-focus-mode="spotlight"]'
    focused = f'{board} .quest-field-cell[data-quest-focused="true"]'
    unfocused = f'{board} .quest-field-cell:not([data-quest-focused="true"])'
    tray = f"{scoped} .detail-content.detail-view-overview .quest-selected-node-lens-tray"

    assert "--quest-focus-target-glow" in focus_slice
    assert unfocused in focus_slice
    assert "opacity: 0.11;" in focus_slice
    assert "filter: saturate(0.32) blur(0.18px);" in focus_slice
    assert "transform: translateY(0) scale(0.68);" in focus_slice
    assert focused in focus_slice
    assert "z-index: 36;" in focus_slice
    assert "height: 86px;" in focus_slice
    assert "min-width: 92px;" in focus_slice
    assert "animation: questFocusTargetLock 4.8s" in focus_slice
    assert ".quest-mission-dossier ~ .quest-selected-node-lens-tray" in focus_slice
    assert "opacity: 1 !important;" in focus_slice
    assert "pointer-events: auto !important;" in focus_slice
    assert tray in focus_slice
    assert "bottom: 96px;" in focus_slice
    assert "bottom: 118px;" in focus_slice
    assert "opacity: 0.62;" in focus_slice
    assert "bottom: 202px;" in focus_slice
    assert "opacity: 0.42;" in focus_slice
    assert "@media (max-width: 760px)" in focus_slice
    assert "@media (prefers-reduced-motion: reduce)" in focus_slice
    assert "Command Cockpit Focus Target" in readme
    assert "20260620-command-cockpit-focus-target" in index
