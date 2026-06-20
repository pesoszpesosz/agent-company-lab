from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_premium_route_motion_turns_board_into_live_game_layer():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-premium-route-motion */"
    assert marker in styles
    motion_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    field = f'{scoped} .detail-content.detail-view-overview .quest-field[data-quest-motion-quality="premium"]'

    assert f"{field} .quest-field-map-route" in motion_slice
    assert "animation: questPremiumRouteEnergy 5.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in motion_slice
    assert f"{field} .quest-field-map-route::before" in motion_slice
    assert "animation: questPremiumRouteCharge 4.4s linear infinite;" in motion_slice
    assert f"{field} .quest-field-runner" in motion_slice
    assert "animation: questPremiumRunnerDrift 5.8s cubic-bezier(0.42, 0, 0.18, 1) infinite;" in motion_slice
    assert f'{field} .quest-field-cell[data-quest-focused="true"]::after' in motion_slice
    assert "animation: questPremiumFocusSweep 3.8s ease-in-out infinite;" in motion_slice
    assert "@keyframes questPremiumRouteEnergy" in motion_slice
    assert "@keyframes questPremiumRouteCharge" in motion_slice
    assert "@keyframes questPremiumRunnerDrift" in motion_slice
    assert "@keyframes questPremiumFocusSweep" in motion_slice
    assert "@media (max-width: 560px)" in motion_slice
    assert "animation-duration: 7.2s;" in motion_slice
    assert "Command Cockpit Premium Route Motion" in readme
    assert "20260620-command-cockpit-premium-route-motion" in index
