from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_worlds_launch_surfaces_minigame_seed_cartridges():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-world-seed-cartridge-rail" in index
    assert "20260620-world-seed-cartridge-rail" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-world-seed-cartridge-rail" in index.split('<script src="./app.js?v=', 1)[1]
    assert "20260620-world-seed-cartridge-flex-rail" in index

    assert "function worldSeedCartridgeRecords(lanes, stats)" in app
    assert "function renderWorldSeedCartridgeRail(records)" in app
    assert "const seedCartridges = worldSeedCartridgeRecords(lanes, stats);" in app
    assert "${renderWorldSeedCartridgeRail(seedCartridges)}" in app
    assert 'class="world-seed-cartridge-rail"' in app
    assert 'class="world-seed-cartridge ${escapeHtml(record.tone)} ${record.lane?.id === state.selectedLaneId ? "active" : ""}"' in app
    assert 'data-worlds-launch-lane="${escapeHtml(record.lane.id)}"' in app
    assert 'data-worlds-launch-action="${escapeHtml(record.action)}"' in app
    assert "--seed-charge:${record.charge}%" in app

    marker = "/* 20260620-world-seed-cartridge-rail */"
    assert marker in styles
    seed_slice = styles[styles.index(marker):]
    assert ".world-seed-cartridge-rail" in seed_slice
    assert ".world-seed-cartridge-track" in seed_slice
    assert ".world-seed-cartridge" in seed_slice
    assert ".world-seed-cartridge.active" in seed_slice
    assert ".world-seed-cartridge.future" in seed_slice
    assert ".world-seed-cartridge-meter" in seed_slice
    assert "display: flex;" in seed_slice
    assert "flex-wrap: nowrap;" in seed_slice
    assert "flex: 0 0 clamp(128px, 42%, 148px);" in seed_slice
    assert "overflow-x: auto;" in seed_slice
    assert "worldSeedCartridgeSweep" in seed_slice
    assert "@media (max-width: 860px)" in seed_slice

    assert "World Seed Cartridge Rail" in readme
