from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_channel_dock_centralizes_local_bot_handoff():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function commandCockpitChannelDock(lane)" in app
    assert "function renderCommandCockpitChannelDock(lane)" in app
    assert "commandCockpitChannelDock(lane)" in app
    assert "${renderCommandCockpitChannelDock(lane)}" in app
    assert 'class="command-channel-dock"' in app
    assert 'class="command-channel-agent ${escapeHtml(model.tone)}"' in app
    assert 'data-stage-lane-command="${escapeHtml(lane.id)}"' in app
    assert 'data-detail-view="comms"' in app
    assert "Owner" in app
    assert "Queued" in app
    assert "Blocker" in app
    assert "Next Ask" in app
    assert "COM" in app

    marker = "/* 20260620-command-cockpit-channel-dock */"
    assert marker in styles
    dock_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    assert f"{scoped} .command-channel-dock" in dock_slice
    assert "grid-template-columns: minmax(184px, 0.82fr) repeat(3, minmax(0, 1fr)) auto;" in dock_slice
    assert "min-height: 58px;" in dock_slice
    assert "overflow: hidden;" in dock_slice
    assert f"{scoped} .command-channel-agent" in dock_slice
    assert "grid-template-columns: 34px minmax(0, 1fr);" in dock_slice
    assert f"{scoped} .command-channel-cell" in dock_slice
    assert f"{scoped} .command-channel-actions" in dock_slice
    assert "animation: commandChannelDockSweep 8.6s ease-in-out infinite;" in dock_slice
    assert "@media (max-width: 760px)" in dock_slice
    assert "grid-auto-flow: column;" in dock_slice
    assert "grid-auto-columns: minmax(132px, 168px);" in dock_slice
    assert "@keyframes commandChannelDockSweep" in dock_slice
    assert "prefers-reduced-motion: reduce" in dock_slice

    assert "20260620-command-cockpit-channel-dock" in index
    assert "Command Cockpit Channel Dock" in readme