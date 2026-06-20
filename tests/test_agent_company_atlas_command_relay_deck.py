from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_relay_deck_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/command-relay-deck-20260618.png"

    assert "commandRelayDeck: document.querySelector(\"#command-relay-deck\")" in app
    assert "function commandRelayDeckRecords" in app
    assert "function commandRelayDeckStats" in app
    assert "function renderCommandRelayDeck" in app
    assert "function renderCommandRelayCard" in app
    assert "function renderCommandRelayFutureSlots" in app
    assert "renderCommandRelayDeck()" in app
    assert "Command Relay Deck" in app
    assert "command-relay-deck-20260618.png" in app
    assert "command-relay-deck" in app
    assert "command-relay-visual" in app
    assert "command-relay-stats" in app
    assert "command-relay-grid" in app
    assert "command-relay-card" in app
    assert "command-relay-future" in app
    assert "command-relay-actions" in app
    assert 'data-command-relay-action="queue"' in app
    assert 'data-command-relay-action="comms"' in app
    assert 'data-command-relay-action="matrix"' in app
    assert "data-command-relay-lane" in app

    assert '<section class="command-relay-deck-panel" id="command-relay-deck"' in index
    assert "command-relay-deck" in index
    assert asset.exists()
    assert asset.stat().st_size > 100_000

    assert ".command-relay-deck-panel" in styles
    assert ".command-relay-visual" in styles
    assert ".command-relay-stats" in styles
    assert ".command-relay-grid" in styles
    assert ".command-relay-card" in styles
    assert ".command-relay-future" in styles
    assert ".command-relay-actions" in styles
    assert "command-relay-deck-20260618.png" in styles

    assert "Command Relay Deck" in readme
    assert "command-relay-deck-20260618.png" in readme
