from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_arcade_shell_starts_board_earlier():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-arcade-shell */"
    assert marker in styles
    shell_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'

    assert "@media (max-width: 560px)" in shell_slice
    assert "--cockpit-shell-height: calc(100dvh - 96px);" in shell_slice
    assert f"{scoped} .topbar" in shell_slice
    assert "height: 28px;" in shell_slice
    assert f"{scoped} .atlas-deck-dock" in shell_slice
    assert "height: 21px;" in shell_slice
    assert f"{scoped} .atlas-deck-button span" in shell_slice
    assert f"{scoped} .atlas-deck-button em" in shell_slice
    assert "font-size: 0.48rem;" in shell_slice
    assert f"{scoped} .lane-list-panel" in shell_slice
    assert "height: 29px !important;" in shell_slice
    assert f"{scoped} .lane-list" in shell_slice
    assert "overflow-x: auto !important;" in shell_slice
    assert f'{scoped} .lane-list[data-lane-selector-mode="gate"]' in shell_slice
    assert f"{scoped} .lane-button," in shell_slice
    assert "flex: 0 0 46px !important;" in shell_slice
    assert "width: 46px !important;" in shell_slice
    assert "max-width: 46px !important;" in shell_slice
    assert "min-height: 24px !important;" in shell_slice
    assert "max-height: 24px !important;" in shell_slice
    assert f"{scoped} .lane-world-signal strong" in shell_slice
    assert f"{scoped} .lane-expansion-slots" in shell_slice
    assert "display: none !important;" in shell_slice
    assert f"{scoped} .detail-content.detail-view-overview" in shell_slice
    assert "height: clamp(440px, calc(100dvh - 188px), 670px) !important;" in shell_slice
    assert "Command Cockpit Mobile Arcade Shell" in readme
    assert "20260620-command-cockpit-mobile-arcade-shell" in index
