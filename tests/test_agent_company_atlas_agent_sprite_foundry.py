from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_agent_sprite_foundry_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/agent-sprite-foundry-20260618.png"
    constellation_asset = ROOT / "web/assets/system/agent-constellation-bay-20260619.png"

    assert "renderAgentSpriteFoundry(agents)" in app
    assert "function agentSpriteFoundryRecords" in app
    assert "function agentSpriteFoundryStats" in app
    assert "function agentConstellationBeacons(records)" in app
    assert "function renderAgentConstellationBeacon(record, index, position)" in app
    assert "function renderAgentSpriteFoundry" in app
    assert "function renderAgentSpriteCard" in app
    assert "function renderAgentSpriteFutureSlots" in app
    assert "${renderAgentSpriteFoundry(agents)}${renderOperatorIdentityBay(agents)}" in app
    assert "Agent Sprite Foundry" in app
    assert "agent-sprite-foundry-20260618.png" in app
    assert "agent-constellation-bay-20260619.png" in app
    assert "Agent Constellation Bay" in app
    assert "agent-sprite-foundry" in app
    assert "agent-sprite-visual" in app
    assert "agent-constellation-overlay" in app
    assert "agent-constellation-beacon" in app
    assert "agent-sprite-stats" in app
    assert "agent-sprite-grid" in app
    assert "agent-sprite-card" in app
    assert "agent-sprite-future" in app
    assert "agent-sprite-actions" in app
    assert 'data-agent-constellation-agent="${escapeHtml(agent.agent_id)}"' in app
    assert "--beacon-x:${position[0]}%;" in app
    assert "--agent-ready:${Math.max(8, readyScore)}%;" in app
    assert "system-agent-constellation-bay" in app
    assert 'data-agent-sprite-action="comms"' in app
    assert 'data-agent-sprite-action="assets"' in app
    assert 'data-agent-sprite-action="forge"' in app
    assert 'data-agent-sprite-lane' in app

    assert "agent-roster" in index
    assert "20260619-agent-constellation-bay" in index
    assert asset.exists()
    assert asset.stat().st_size > 100_000
    assert constellation_asset.exists()
    assert constellation_asset.stat().st_size > 100_000

    assert ".agent-sprite-foundry" in styles
    assert ".agent-sprite-visual" in styles
    assert ".agent-constellation-overlay" in styles
    assert ".agent-constellation-beacon" in styles
    assert ".agent-sprite-stats" in styles
    assert ".agent-sprite-grid" in styles
    assert ".agent-sprite-card" in styles
    assert ".agent-sprite-future" in styles
    assert ".agent-sprite-actions" in styles
    assert "@keyframes agentConstellationFloat" in styles
    assert "@keyframes agentConstellationSweep" in styles
    assert "animation: agentConstellationFloat 5.6s ease-in-out infinite;" in styles
    assert "animation: agentConstellationSweep 4.9s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in styles
    assert 'body[data-atlas-deck="command"][data-atlas-stage="bots"] .operator-roster-panel .agent-sprite-foundry' in styles
    assert "min-height: 360px;" in styles
    assert "max-height: 322px;" in styles
    assert "agent-constellation-bay-20260619.png" in styles

    mobile_start = styles.index("@media (max-width: 860px)")
    mobile_slice = styles[mobile_start:]
    assert ".agent-constellation-beacon {" in mobile_slice
    assert "grid-template-columns: 28px;" in mobile_slice
    assert ".agent-constellation-beacon span" in mobile_slice
    assert "display: none;" in mobile_slice
    assert "max-height: 180px;" in mobile_slice
    assert "min-height: 200px;" in mobile_slice
    assert "grid-template-columns: 40px minmax(0, 1fr);" in mobile_slice

    assert "Agent Sprite Foundry" in readme
    assert "agent-sprite-foundry-20260618.png" in readme
    assert "Agent Constellation Bay" in readme
