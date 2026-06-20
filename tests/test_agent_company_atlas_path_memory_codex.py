from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_memory_codex_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/path-memory-codex-20260618.png"

    assert "pathMemoryLensByLane" in app
    assert "function pathMemoryLensOptions(trail)" in app
    assert "function pathMemoryFilteredItems(lane, trail)" in app
    assert "function pathMemoryStats(lane, trail)" in app
    assert "function renderPathMemoryCodex(lane, trail)" in app
    assert "function renderPathMemoryCard(lane, item, index)" in app
    assert "function renderPathMemoryFutureSlots(lane, hidden)" in app
    assert "renderPathMemoryCodex(lane, trail)" in app

    for token in [
        "Path Memory Codex",
        "path-memory-codex-20260618.png",
        "system-path-memory-codex",
        'data-path-memory-action="',
        'data-path-memory-jump="path"',
        'data-path-memory-jump="comms"',
        'data-path-memory-jump="more"',
        "data-path-memory-event",
        "pathMemoryActionButton",
        "pathMemoryJumpButton",
        "pathMemoryEventButton",
    ]:
        assert token in app

    for token in [
        ".path-memory-codex",
        ".path-memory-visual",
        ".path-memory-stats",
        ".path-memory-lenses",
        ".path-memory-grid",
        ".path-memory-card",
        ".path-memory-future",
        ".path-memory-scan",
        "path-memory-codex-20260618.png",
    ]:
        assert token in styles

    assert "Path Memory Codex" in readme
    assert "path-memory-codex-20260618.png" in readme
    assert asset.exists()
    assert asset.stat().st_size > 100_000
