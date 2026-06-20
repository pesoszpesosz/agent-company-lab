from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLESHEET = ROOT / "web" / "styles.css"


def test_stylesheet_is_not_empty_after_recovery():
    assert STYLESHEET.exists()
    assert STYLESHEET.stat().st_size > 100_000


def test_stylesheet_keeps_recovered_visual_contract_layers():
    styles = STYLESHEET.read_text(encoding="utf-8")

    assert ":root {" in styles
    assert "20260620-recovery-contract-layer" in styles
    assert "20260620-command-cockpit-board-first-shelf" in styles
    assert "20260620-command-cockpit-hud-stack" in styles
    assert "20260620-command-cockpit-runway-pulse" in styles


def test_reduced_motion_keeps_path_stage_signal_guard():
    styles = STYLESHEET.read_text(encoding="utf-8")

    reduced_motion_start = styles.rindex("@media (prefers-reduced-motion: reduce)")
    reduced_motion_slice = styles[reduced_motion_start:]

    assert ".path-stage-signal" in reduced_motion_slice
    assert "animation: none;" in reduced_motion_slice
