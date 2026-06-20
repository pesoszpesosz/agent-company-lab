from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_unlock_chain_models_level_quest_gate_proof_reward():
    app = read("web/app.js")

    assert "function cockpitUnlockChainModel(lane)" in app
    assert "const checkpoints = lane.quest?.checkpoints ?? [];" in app
    assert "const completedCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === \"complete\").length;" in app
    assert "const trail = chronicleTrail(lane);" in app
    assert "const outcomeCount = lane.counts?.outcomes ?? 0;" in app
    assert "const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);" in app
    assert "const stages = [" in app
    assert 'id: "level"' in app
    assert 'id: "quest"' in app
    assert 'id: "gate"' in app
    assert 'id: "proof"' in app
    assert 'id: "reward"' in app
    assert "function renderCockpitUnlockChain(model)" in app
    assert 'class="cockpit-unlock-chain"' in app
    assert 'data-cockpit-unlock-tone="${escapeHtml(model.tone)}"' in app
    assert 'data-cockpit-unlock-stage="${escapeHtml(stage.id)}"' in app
    assert 'data-detail-view="${escapeHtml(stage.view)}"' in app


def test_command_cockpit_unlock_chain_mounts_before_route_minimap():
    app = read("web/app.js")
    render_start = app.index("function renderDetail()")
    render_end = app.index("function renderDetailBody", render_start)
    render_slice = app[render_start:render_end]

    assert "const cockpitUnlockChain = cockpitUnlockChainModel(lane);" in render_slice
    assert render_slice.index("const cockpitUnlockChain = cockpitUnlockChainModel(lane);") < render_slice.index("el.detailPanel.innerHTML")
    assert "${renderCockpitUnlockChain(cockpitUnlockChain)}" in render_slice
    assert render_slice.index("${renderCockpitCrewHandoffRail(cockpitCrewHandoffRail)}") < render_slice.index("${renderCockpitUnlockChain(cockpitUnlockChain)}")
    assert render_slice.index("${renderCockpitUnlockChain(cockpitUnlockChain)}") < render_slice.index("${renderCommandCockpitRouteMinimap(lane)}")


def test_command_cockpit_unlock_chain_is_compact_animated_and_documented():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-unlock-chain */"
    assert marker in styles
    block = styles[styles.index(marker) :]
    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"]'

    assert f"{scoped} .cockpit-unlock-chain" in block
    assert "grid-template-columns: repeat(5, minmax(0, 1fr));" in block
    assert "min-height: 46px;" in block
    assert "overflow: hidden;" in block
    assert ".cockpit-unlock-chain::before" in block
    assert "animation: cockpitUnlockChainSweep 10.2s ease-in-out infinite;" in block
    assert "@keyframes cockpitUnlockChainSweep" in block
    assert ".cockpit-unlock-stage" in block
    assert ".cockpit-unlock-stage::after" in block
    assert "@media (max-width: 760px)" in block
    assert "grid-auto-columns: minmax(86px, 112px);" in block
    assert "overflow-x: auto;" in block
    assert "@media (prefers-reduced-motion: reduce)" in block
    assert ".cockpit-unlock-chain::before," in block
    assert ".path-stage-signal" in block
    assert "Command Cockpit Unlock Chain" in readme
    assert "Level, Quest, Gate, Proof, and Reward" in readme
    assert "20260620-command-cockpit-unlock-chain" in index