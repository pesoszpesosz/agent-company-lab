from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mission_control_band_consolidates_first_screen_status():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function questMissionControlBandModel(lane, data, focusedCell, gateTitle, gateBody, crew)" in app
    assert "function renderQuestMissionControlBand(model)" in app
    assert "renderQuestMissionControlBand(missionControlBand)" in app
    assert 'class="quest-mission-control-band"' in app
    assert 'id: "latest"' in app
    assert 'id: "blocker"' in app
    assert 'id: "next"' in app
    assert 'id: "bot"' in app
    assert 'data-mission-control-cell="${escapeHtml(cell.id)}"' in app
    assert 'data-detail-view="${escapeHtml(cell.view)}"' in app

    marker = "/* 20260620-command-cockpit-mission-control-band */"
    assert marker in styles
    band_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    field = f'{scoped} .detail-content.detail-view-overview .quest-field[data-quest-motion-quality="premium"]'

    assert f"{field} .quest-mission-control-band" in band_slice
    assert "grid-template-columns: minmax(76px, 0.42fr) repeat(4, minmax(0, 1fr));" in band_slice
    assert "min-height: 62px;" in band_slice
    assert "animation: questMissionControlScan 6.8s ease-in-out infinite;" in band_slice
    assert f"{field} .quest-mission-control-cell" in band_slice
    assert "min-height: 46px;" in band_slice
    assert f"{field} .quest-board-identity-cartridge" in band_slice
    assert "opacity: 0.18;" in band_slice
    assert f"{field} .quest-mission-readout" in band_slice
    assert "top: 78px;" in band_slice
    assert "@media (max-width: 760px)" in band_slice
    assert "grid-template-columns: 64px repeat(4, 104px);" in band_slice
    assert "overflow-x: auto;" in band_slice
    assert "@media (max-width: 560px)" in band_slice
    assert "top: 8px;" in band_slice
    assert "min-height: 52px;" in band_slice
    assert "@keyframes questMissionControlScan" in band_slice
    assert "@media (prefers-reduced-motion: reduce)" in band_slice
    assert ".path-stage-signal" in band_slice[band_slice.rindex("@media (prefers-reduced-motion: reduce)") :]

    assert "Command Cockpit Mission Control Band" in readme
    assert "20260620-command-cockpit-mission-control-band" in index
    assert "20260620-command-cockpit-primary-readout-20260620-command-cockpit-mission-control-band" in index