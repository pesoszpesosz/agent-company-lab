from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_comms_command_room_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/comms-command-room-20260618.png"

    assert "function commsCommandRoomStats" in app
    assert "function renderCommsCommandRoom" in app
    assert "renderCommsCommandRoom(lane, ownerAgent, status, command)" in app
    assert asset.exists()
    assert asset.stat().st_size > 100_000
    assert "comms-command-room-20260618.png" in app
    assert "Comms Command Room" in app
    assert "comms-command-room" in app
    assert "comms-command-visual" in app
    assert "comms-command-stats" in app
    assert "comms-command-actions" in app
    assert "agentAvatarMarkup(ownerAgent" in app
    assert "state.stagedDispatches" in app
    assert "state.dispatchHistory" in app
    assert "data-stage-lane-command" in app
    assert "data-copy-command" in app
    assert 'data-detail-view="path"' in app

    assert ".comms-command-room" in styles
    assert ".comms-command-visual" in styles
    assert ".comms-command-stats" in styles
    assert ".comms-command-actions" in styles
    assert "comms-command-room-20260618.png" in styles

    assert "comms-command-room" in index
    assert "Comms Command Room" in readme
    assert "comms-command-room-20260618.png" in readme
