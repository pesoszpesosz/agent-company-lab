from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_comms_command_inbox_board_keeps_lane_messages_scannable():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")

    assert "function commsCommandInboxItems(lane, ownerAgent, command)" in app
    assert "function renderCommsCommandInbox(lane, ownerAgent, command)" in app
    assert "${renderCommsCommandInbox(lane, ownerAgent, command)}" in app
    assert 'class="comms-command-inbox"' in app
    assert 'class="comms-inbox-cell ${escapeHtml(item.tone)}"' in app
    assert 'data-comms-inbox-cell="${escapeHtml(item.id)}"' in app
    assert "Queued" in app
    assert "Local Log" in app
    assert "Blocker" in app
    assert "Next Ask" in app
    assert "state.stagedDispatches.filter((draft) => draft.laneId === lane.id)" in app
    assert "state.dispatchHistory.filter((item) => item.laneName === lane.name)" in app

    marker = "/* 20260620-comms-command-inbox-board */"
    assert marker in styles
    inbox_slice = styles[styles.index(marker) :]
    assert ".comms-command-inbox" in inbox_slice
    assert "grid-template-columns: repeat(4, minmax(0, 1fr));" in inbox_slice
    assert "min-height: 72px;" in inbox_slice
    assert ".comms-inbox-cell" in inbox_slice
    assert "animation: commsInboxScan 7.8s ease-in-out infinite;" in inbox_slice
    assert "@keyframes commsInboxScan" in inbox_slice
    assert "@media (max-width: 760px)" in inbox_slice
    mobile_slice = inbox_slice[inbox_slice.index("@media (max-width: 760px)") :]
    assert "grid-auto-flow: column;" in mobile_slice
    assert "grid-auto-columns: minmax(132px, 154px);" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice
    assert "@media (prefers-reduced-motion: reduce)" in inbox_slice

    assert "20260620-comms-command-inbox-board" in index
    assert "Comms Command Inbox Board" in readme