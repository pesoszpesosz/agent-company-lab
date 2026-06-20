from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_worlds_reward_pickup_dock_avoids_world_selector_board():
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")

    marker = "/* 20260620-worlds-reward-pickup-dock */"
    assert marker in styles
    dock_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="worlds"][data-atlas-stage="worlds"]'
    assert f"{scoped} .unlock-toast" in dock_slice
    assert "top: 292px;" in dock_slice
    assert "bottom: auto;" in dock_slice
    assert "width: min(260px, calc(100vw - 28px));" in dock_slice
    assert "max-height: 58px;" in dock_slice
    assert f"{scoped} .unlock-toast-copy > p:not(.eyebrow)" in dock_slice
    assert f"{scoped} .unlock-toast-meta" in dock_slice
    assert f"{scoped} .unlock-toast-actions .trophy-open" in dock_slice
    assert "display: none;" in dock_slice[dock_slice.index(f"{scoped} .unlock-toast-copy > p:not(.eyebrow)") :]
    assert "@media (max-width: 560px)" in dock_slice
    assert "top: 224px;" in dock_slice
    assert "width: min(186px, calc(100vw - 28px));" in dock_slice
    assert "grid-template-columns: 32px minmax(0, 1fr);" in dock_slice
    assert "prefers-reduced-motion: reduce" in dock_slice
    score_slot = f"{scoped}:has(.unlock-toast:not([hidden])) .worlds-launch-score"
    assert score_slot in dock_slice
    assert "opacity: 0;" in dock_slice[dock_slice.index(score_slot) :]
    assert ".path-stage-signal" in dock_slice[dock_slice.rindex("@media (prefers-reduced-motion: reduce)") :]

    assert "20260620-worlds-reward-pickup-dock" in index
    assert "20260620-reward-pickup-dock-20260620-worlds-reward-pickup-dock" in index
    assert "Worlds Reward Pickup Dock" in readme