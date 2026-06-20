from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_selected_node_bot_handoff_adds_comms_chip_to_node_cartridge():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-selected-node-bot-handoff */"
    assert "botLensAvatar:" in app
    assert "quest-selected-node-lens-bot" in app
    assert "data-quest-lens-bot" in app
    assert 'data-detail-view="comms"' in app
    assert "Open ${escapeHtml(model.botCallsign)} Comms" in app

    assert marker in styles
    handoff_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    base = f"{scoped} .detail-content.detail-view-overview"
    assert f"{base} .quest-selected-node-lens-bot" in handoff_slice
    assert "grid-template-columns: 24px minmax(0, 1fr) 24px;" in handoff_slice
    assert "questSelectedNodeBotPing" in handoff_slice
    assert "@media (min-width: 761px)" in handoff_slice
    assert "grid-template-columns: minmax(0, 1fr) 126px 72px;" in handoff_slice
    assert "@media (max-width: 560px)" in handoff_slice
    assert "display: none !important;" in handoff_slice
    assert "Command Cockpit Selected Node Bot Handoff" in readme
    assert "20260620-command-cockpit-selected-node-bot-handoff" in index
