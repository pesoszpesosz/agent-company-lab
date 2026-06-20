from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_lane_genesis_foundry_contract():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/lane-genesis-foundry-20260618.png"

    assert 'laneGenesisFoundry: document.querySelector("#lane-genesis-foundry")' in app
    assert "function laneGenesisFoundryRecords()" in app
    assert "function laneGenesisFoundryStats(records)" in app
    assert "function renderLaneGenesisFoundry()" in app
    assert "function renderLaneGenesisCard(record)" in app
    assert "function renderLaneGenesisFutureSlots(records)" in app
    assert "renderLaneGenesisFoundry();" in app

    assert 'id="lane-genesis-foundry"' in index
    assert "Lane Genesis Foundry" in app
    assert "lane-genesis-foundry-20260618.png" in app
    assert "system-lane-genesis-foundry" in app

    for token in [
        "lane-genesis-foundry",
        "lane-genesis-visual",
        "lane-genesis-stats",
        "lane-genesis-grid",
        "lane-genesis-card",
        "lane-genesis-future",
        "lane-genesis-actions",
        'data-lane-genesis-action="forge"',
        'data-lane-genesis-action="games"',
        'data-lane-genesis-action="assets"',
        'data-lane-genesis-action="bots"',
        "data-lane-genesis-lane",
    ]:
        assert token in app

    for token in [
        ".lane-genesis-foundry-panel",
        ".lane-genesis-visual",
        ".lane-genesis-stats",
        ".lane-genesis-grid",
        ".lane-genesis-card",
        ".lane-genesis-future",
        ".lane-genesis-actions",
        "lane-genesis-foundry-20260618.png",
    ]:
        assert token in styles

    assert "Lane Genesis Foundry" in readme
    assert "lane-genesis-foundry-20260618.png" in readme
    assert asset.exists()
    assert asset.stat().st_size > 100_000
