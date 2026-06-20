from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_live_ops_pulse_contract():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/live-ops-pulse-20260618.png"

    assert 'liveOpsPulse: document.querySelector("#live-ops-pulse")' in app
    assert "function liveOpsPulseRecords()" in app
    assert "function liveOpsPulseStats(records)" in app
    assert "function renderLiveOpsPulse()" in app
    assert "function renderLiveOpsPulseCard(record)" in app
    assert "function renderLiveOpsPulseFutureSlots(records)" in app
    assert "renderLiveOpsPulse();" in app

    assert 'id="live-ops-pulse"' in index
    assert "Live Ops Pulse" in app
    assert "live-ops-pulse-20260618.png" in app
    assert "system-live-ops-pulse" in app

    for token in [
        "live-ops-pulse",
        "live-ops-visual",
        "live-ops-stats",
        "live-ops-grid",
        "live-ops-card",
        "live-ops-future",
        "live-ops-actions",
        'data-live-ops-action="latest"',
        'data-live-ops-action="gates"',
        'data-live-ops-action="comms"',
        'data-live-ops-action="timeline"',
        "data-live-ops-lane",
    ]:
        assert token in app

    for token in [
        ".live-ops-pulse-panel",
        ".live-ops-visual",
        ".live-ops-stats",
        ".live-ops-grid",
        ".live-ops-card",
        ".live-ops-future",
        ".live-ops-actions",
        "live-ops-pulse-20260618.png",
    ]:
        assert token in styles

    assert "Live Ops Pulse" in readme
    assert "live-ops-pulse-20260618.png" in readme
    assert asset.exists()
    assert asset.stat().st_size > 100_000
