from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_primary_readout_promotes_current_move_and_quiets_depth_lens():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-primary-readout */"
    assert marker in styles
    readout_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    field = f'{scoped} .detail-content.detail-view-overview .quest-field[data-quest-motion-quality="premium"]'

    assert f"{field} .quest-mission-readout" in readout_slice
    assert "grid-template-columns: minmax(84px, 0.56fr) minmax(0, 1.78fr) minmax(84px, 0.62fr);" in readout_slice
    assert "min-height: 58px;" in readout_slice
    assert f"{scoped} .detail-content.detail-view-overview .quest-mission-readout-core" in readout_slice
    assert "font-size: 0.82rem;" in readout_slice
    assert 'data-readout-cell="gate"' in readout_slice
    assert f"{scoped} .detail-content.detail-view-overview .quest-path-depth-lens" in readout_slice
    assert "opacity: 0.72;" in readout_slice
    assert "@media (max-width: 760px)" in readout_slice
    assert "grid-template-columns: 58px minmax(0, 1fr);" in readout_slice
    assert "grid-row: 1 / 3;" in readout_slice
    assert "-webkit-line-clamp: 2;" in readout_slice
    assert "Command Cockpit Primary Readout" in readme
    assert "20260620-command-cockpit-primary-readout" in index
