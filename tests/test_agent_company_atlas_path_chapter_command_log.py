from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_command_log_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/path-chapter-command-relay-20260618.png"

    assert "function pathChapterCommandLogRecords" in app
    assert "function pathChapterCommandRelayStats" in app
    assert "function renderPathChapterCommandLog" in app
    assert asset.exists()
    assert asset.stat().st_size > 100_000
    assert "path-chapter-command-relay-20260618.png" in app
    assert "Path Chapter Command Relay" in app
    assert "path-chapter-command-log" in app
    assert "path-chapter-command-visual" in app
    assert "path-chapter-command-signal" in app
    assert "path-chapter-command-entry" in app
    assert "path-chapter-command-actions" in app
    assert "renderPathChapterCommandLog(lane, chapter)" in app
    assert "state.dispatchHistory" in app
    assert "state.stagedDispatches" in app
    assert '${stagedCount ? "OK" : "Q"}' in app
    assert "data-stage-lane-command" in app
    assert 'data-detail-view="comms"' in app
    assert "renderDetail();" in app

    assert ".path-chapter-command-log" in styles
    assert ".path-chapter-command-visual" in styles
    assert ".path-chapter-command-signal" in styles
    assert ".path-chapter-command-entry" in styles
    assert ".path-chapter-command-actions" in styles
    assert "path-chapter-command-relay-20260618.png" in styles

    assert "path-chapter-command-log" in index
    assert "path-chapter-command-relay" in index
    assert "Chapter Command Log" in readme
    assert "Path Chapter Command Relay" in readme
    assert "path-chapter-command-relay-20260618.png" in readme
