from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_objective_bar_cuts_report_text_from_board():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-objective-bar */"
    assert marker in styles
    objective_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    base = f"{scoped} .detail-content.detail-view-overview"

    assert "@media (max-width: 560px)" in objective_slice
    assert f"{base} .quest-cockpit[data-quest-motion-quality=\"premium\"]" in objective_slice
    assert "grid-template-rows: 30px minmax(0, 1fr) !important;" in objective_slice
    assert f"{base} .quest-mission-director" in objective_slice
    assert "max-height: 30px;" in objective_slice
    assert "grid-template-columns: minmax(0, 1fr) auto;" in objective_slice
    assert f"{base} .quest-director-current > p:not(.eyebrow)" in objective_slice
    assert "display: none !important;" in objective_slice
    assert f"{base} .quest-director-chips" in objective_slice
    assert "display: none !important;" in objective_slice
    assert f"{base} .quest-director-progress" in objective_slice
    assert "height: 3px;" in objective_slice
    assert f"{base} .quest-selected-node-lens-tray" in objective_slice
    assert "grid-template-columns: minmax(0, 1fr) 58px;" in objective_slice
    assert "min-height: 54px;" in objective_slice
    assert f"{base} .quest-selected-node-lens-copy em" in objective_slice
    assert "Command Cockpit Mobile Objective Bar" in readme
    assert "20260620-command-cockpit-mobile-objective-bar" in index
