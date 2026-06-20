from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_bot_switchboard_groups_bot_state_without_more_scroll():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "function botCommandSwitchboardGroups(records)" in app
    assert "function renderBotCommandSwitchboard(records)" in app
    assert "renderBotCommandSwitchboard(records)" in app
    assert 'class="bot-command-switchboard"' in app
    assert 'class="bot-switchboard-group ${escapeHtml(group.id)}"' in app
    assert 'data-bot-switchboard-mode="${escapeHtml(group.id)}"' in app
    assert 'data-agent-lane-id="${escapeHtml(record.lane.id)}"' in app
    assert "Ready" in app
    assert "Gated" in app
    assert "Staged" in app
    assert "Watching" in app

    marker = "/* 20260620-command-bot-switchboard */"
    assert marker in styles
    switch_slice = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="bots"]'
    assert f"{scoped} .bot-command-switchboard" in switch_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in switch_slice
    assert "min-height: 118px;" in switch_slice
    assert "animation: botSwitchboardScan 7.2s ease-in-out infinite;" in switch_slice
    assert f"{scoped} .bot-switchboard-group" in switch_slice
    assert "min-height: 96px;" in switch_slice
    assert f"{scoped} .bot-switchboard-agent" in switch_slice
    assert "grid-template-columns: 30px minmax(0, 1fr) auto;" in switch_slice
    assert f"{scoped} .bot-switchboard-agent .operator-avatar" in switch_slice
    assert "width: 30px;" in switch_slice
    assert "@media (max-width: 860px)" in switch_slice
    assert "grid-auto-flow: column;" in switch_slice
    assert "grid-auto-columns: minmax(164px, 190px);" in switch_slice
    assert "@media (prefers-reduced-motion: reduce)" in switch_slice
    assert ".path-stage-signal" in switch_slice[switch_slice.rindex("@media (prefers-reduced-motion: reduce)") :]

    assert "Command Bot Switchboard" in readme
    assert "20260620-command-bot-switchboard" in index
    assert "20260620-command-bot-squadron-hud-20260620-command-bot-switchboard" in index